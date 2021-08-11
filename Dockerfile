FROM python:3.9
ENV PYTHONUNBUFFERED=1

RUN apt-get install -yqq unzip

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
# Updating apt to see and install Google Chrome
RUN apt-get -y update
# Magic happens
RUN apt-get install -y google-chrome-stable

RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/93.0.4577.15/chromedriver_linux64.zip

RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

ENV DISPLAY=:99

RUN chmod +x /usr/local/bin/chromedriver

WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
RUN pip install webdriver-manager
RUN pip install random_user_agent