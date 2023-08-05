"""Console script to print and save system information. (:mod:`fluiddevops.info`)
=================================================================================

"""
from __future__ import print_function
from importlib import import_module as _import
import os
import shlex
import inspect
from collections import OrderedDict
import platform
import argparse
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess

from fluiddyn.util.paramcontainer import ParamContainer


COL_WIDTH = 32


def _get_hg_repo(path_dir):
    if path_dir == '':
        return ''

    pwd = os.getcwd()
    os.chdir(path_dir)
    cmd = shlex.split('hg paths')
    output = subprocess.check_output(cmd)
    os.chdir(pwd)
    try:
        output = output.splitlines()[0]
    except:
        pass

    if output == '':
        return 'not an hg repo'
    elif output.startswith('default'):
        return output.split(' ')[2]
    else:
        return output


def make_dict_about(pkg):
    about_pkg = OrderedDict([
        ('installed', None),
        ('version', ''),
        ('local_path', ''),
        ('remote_path', ''),
    ])
    try:
        pkg = _import(pkg)
    except ImportError:
        about_pkg['installed'] = False
        return about_pkg
    else:
        about_pkg['installed'] = True
        about_pkg['version'] = pkg.__version__
        init_file = inspect.getfile(pkg)
        if 'site-packages' in init_file or 'dist-packages' in init_file:
            about_pkg['local_path'] = os.path.dirname(init_file)
            about_pkg['remote_path'] = ''
        else:
            about_pkg['local_path'] = os.path.dirname(os.path.dirname(init_file))
            about_pkg['remote_path'] = _get_hg_repo(about_pkg['local_path'])
        return about_pkg


def get_info(pkgs=None):
    if pkgs is None:
        pkgs = OrderedDict.fromkeys(
            ['fluiddyn', 'fluidsim', 'fluidlab', 'fluidimage', 'fluidfft',
             'fluidcoriolis', 'fluiddevops', 'fluidkth']
        )
    for pkg in pkgs:
        dict_pkg = make_dict_about(pkg)
        pkgs[pkg] = dict_pkg

    return pkgs


def get_info_third_party():
    pkgs = OrderedDict.fromkeys(
        ['numpy', 'cython', 'mpi4py', 'pythran', 'pyfftw', 'matplotlib',
         'scipy', 'skimage']
    )
    return get_info(pkgs)


def get_info_software():
    uname = platform.uname()
    info_sw = dict(zip(
        ['system', 'hostname', 'kernel'], uname))
    try:
        info_sw['distro'] = ' '.join(platform.linux_distribution())
    except:
        pass

    info_sw['CC'] = platform.python_compiler()
    info_sw['MPI'] = subprocess.check_output(shlex.split(
        'mpirun --version')).splitlines()[0]
    return info_sw


def get_info_hardware():
    try:
        from cpuinfo import cpuinfo

        info_hw = cpuinfo.get_cpu_info()
        info_hw = dict((k, v) for k, v in info_hw.items() if k in [
            'arch', 'brand', 'count', 'hz_actual', 'hz_advertised',
            'l2_cache_size'])

    except ImportError:
        import psutil

        hz = psutil.cpu_freq()
        info_hw = {
            'arch': platform.machine(),
            'brand': platform.processor(),
            'count': psutil.cpu_count(),
            'hz_actual': '{:.2f} Ghz'.format(hz.current / 1000),
            'hz_advertised': '{:.2f} Ghz'.format(hz.max / 1000),
        }
    return info_hw


def print_sys_info():
    pkgs = get_info()

    pkgs_keys = list(pkgs)
    title = ['Package']
    title.extend([col.replace('_', ' ').title() for col in pkgs[pkgs_keys[0]]])
    title2 = ['=' * len(col) for col in title]

    def print_item(item):
        print(item.ljust(COL_WIDTH), end='')

    for col in title:
        print_item(col)

    print()
    for col in title2:
        print_item(col)

    print()

    def print_pkg(about_pkg):
        for v in about_pkg.values():
            v = str(v)
            if len(v) > COL_WIDTH:
                v = v[:10] + '...' + v[10 + 4 - COL_WIDTH:]
            print_item(str(v))

        print()

    for pkg_name, about_pkg in pkgs.items():
        print(pkg_name.ljust(COL_WIDTH), end='')
        print_pkg(about_pkg)

    pkgs_third_party = get_info_third_party()
    for pkg_name, about_pkg in pkgs_third_party.items():
        print(pkg_name.ljust(COL_WIDTH), end='')
        print_pkg(about_pkg)


def save_sys_info(filename='sys_info.xml'):
    sys_info = ParamContainer('sys_info')
    info_sw = get_info_software()
    info_hw = get_info_hardware()
    pkgs = get_info()
    pkgs_third_party = get_info_third_party()

    sys_info._set_child('software', info_sw)
    sys_info._set_child('hardware', info_hw)
    sys_info._set_child('python')
    for pkg in pkgs:
        sys_info.python._set_child(pkg, pkgs[pkg])

    for pkg in pkgs_third_party:
        sys_info.python._set_child(pkg, pkgs_third_party[pkg])

    sys_info._save_as_xml(filename, find_new_name=True)


def main():
    parser = argparse.ArgumentParser(
        prog='fluidinfo',
        description='print and save system information')
    parser.set_defaults(func=print_sys_info)
    parser.add_argument(
        '-s', '--save', help='saves system information to an xml file',
        action='store_true')

    args = parser.parse_args()
    if args.save:
        save_sys_info()
    else:
        print_sys_info()


if __name__ == '__main__':
    main()
