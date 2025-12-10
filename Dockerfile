FROM python:3.12.3

# install packages (openjdk, curl, tar)
RUN apt-get update && \
 apt-get install -y openjdk-17-jre curl tar && \
 curl -o allure-2.29.0.tgz -Ls https://repo.maven.apache.org/maven2/io/qameta/allure/allure-commandline/2.29.0/allure-commandline-2.29.0.tgz && \
 tar -zxvf allure-2.29.0.tgz -C /opt/ && \
 ln -s /opt/allure-2.29.0/bin/allure /usr/bin/allure && \
 rm allure-2.29.0.tgz

WORKDIR /test_project
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install --with-deps firefox
