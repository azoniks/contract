FROM python:3.10

RUN apt-get update

RUN pip install --upgrade pip

RUN mkdir /contracts

WORKDIR /contracts

COPY ./requirements.txt ./contracts/

RUN pip install -r ./contracts/requirements.txt

COPY . /contracts

RUN chmod +x entrypoint.sh

ENTRYPOINT ["bash", "/contracts/entrypoint.sh"]