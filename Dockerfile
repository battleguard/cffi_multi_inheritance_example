FROM centos:7

RUN yum install -y http://repo.okay.com.mx/centos/7/x86_64/release/okay-release-1-1.noarch.rpm \
    && yum makecache
RUN yum install -y gcc-c++ make cmake3 wget which  openssl-devel bzip2-devel libffi-devel zlib-devel

WORKDIR /usr/src
RUN PYVER=3.8.9 \
    && wget https://www.python.org/ftp/python/${PYVER}/Python-${PYVER}.tgz \
    && tar xzf Python-${PYVER}.tgz \
    && cd Python-${PYVER} \
    && ./configure --enable-optimizations --with-ensurepip=install \
    && make altinstall -j $(nproc) \
    && ln -s $(which python3.8) /usr/local/bin/python3 \
    && ln -s $(which python3.8) /usr/local/bin/python

WORKDIR /workspace/cffi_multi_inheritance_example
RUN rm -rdf /usr/src/Python-*

COPY units_cpp/ units_cpp/
COPY units_py/ units_py/ 

RUN cmake3 -S units_cpp/ -B build
RUN cmake3 --build build/ --target install

WORKDIR /workspace/cffi_multi_inheritance_example/units_py

RUN python -m pip install -r requirements.txt
ENV PYTHONPATH=/workspace/cffi_multi_inheritance_example/units_py