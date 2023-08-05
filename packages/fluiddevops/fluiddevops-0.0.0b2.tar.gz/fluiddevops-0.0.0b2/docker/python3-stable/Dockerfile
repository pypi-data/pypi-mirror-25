FROM python:3.6
MAINTAINER Ashwin Vishnu Mohanan <avmo@kth.se>

RUN pip install numpy matplotlib -U
RUN pip install scipy -U
RUN pip install psutil -U

RUN apt-get update
RUN apt-get install -y libfftw3-dev
RUN pip install pyfftw -U

RUN apt-get install -y libhdf5-openmpi-dev
RUN apt-get install -y openmpi-bin
RUN pip install mpi4py -U
RUN pip install h5py -U
