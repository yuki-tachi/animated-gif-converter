FROM python

# Docker CLIのインストール
RUN apt update
RUN apt-get -y install \
    ca-certificates \
    gnupg \
    lsb-release
RUN mkdir -m 0755 -p /etc/apt/keyrings
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
RUN apt update
RUN apt -y install docker-ce-cli docker-compose-plugin

WORKDIR /usr/src/app
COPY requirements.txt ./

ENV FLASK_APP=./flaskr/main

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]