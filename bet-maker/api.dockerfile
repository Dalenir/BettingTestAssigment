FROM python:3.11 as core

ENV PYTHONUNBUFFERED=1

LABEL version = '0.5'

WORKDIR /bet-maker
COPY . ./

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


FROM core as test_extended

RUN apt-get update
RUN apt-get -y install software-properties-common

RUN apt install -y default-jre
RUN curl -o /tmp/allure-2.24.0.tgz -OLs https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.24.0/allure-commandline-2.24.0.tgz
RUN tar -zxvf /tmp/allure-2.24.0.tgz -C /opt/
RUN ln -s /opt/allure-2.24.0/bin/allure /usr/bin/allure

RUN apt-get autoclean -y & apt-get autoremove -y

COPY ./tests/test_reqs.txt /tmp/
RUN pip3 install -r /tmp/test_reqs.txt