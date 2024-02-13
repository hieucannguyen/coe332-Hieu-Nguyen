FROM ubuntu:20.04

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip

RUN pip3 install pytest==8.0.0

COPY ml_data_analysis.py /code/ml_data_analysis.py

RUN chmod +rx /code/ml_data_analysis.py

ENV PATH="/code:$PATH"
