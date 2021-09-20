FROM hub.debio.network/miniconda_ipyrad:1.0.1

WORKDIR /ipyrad
COPY . /ipyrad

RUN python3 pca.py