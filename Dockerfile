FROM python:3.9

# 動作しない version [110.0.5481.30]: As of 2023/02/26
#ENV CHROMEDRIVER_VERSION=104.0.5112.29
ENV CHROMEDRIVER_VERSION=110.0.5481.30
ENV CHROMEDRIVER_ZIP_PATH=/tmp/chromedriver.zip
# google chrome 日本語化
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP.UTF-8
# set display port to avoid crash
ENV DISPLAY=:99

# Install google chrome
# https://www.digitalocean.com/community/tutorials/install-chrome-on-linux-mint
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get update && apt-get install -y \
  fonts-ipafont-gothic \
  google-chrome-stable \
  sudo \
  unzip \
  vim

# root 権限意外でも扱えるようにする
WORKDIR /opt

# Install chromedriver
ADD https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip $CHROMEDRIVER_ZIP_PATH
RUN unzip $CHROMEDRIVER_ZIP_PATH chromedriver -d /usr/bin/

COPY ./requirements.txt ./
RUN pip3 install --upgrade pip && \
  pip3 install -r requirements.txt

COPY . .

# creat user
ARG UID=1000
RUN useradd -m -u ${UID} docker
USER ${UID}

WORKDIR /work
CMD ["/bin/bash"]
