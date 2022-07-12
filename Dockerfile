FROM joyzoursky/python-chromedriver

WORKDIR /tmp
COPY requirements.txt  /tmp/requirements.txt

RUN pip install --no-cache-dir -q -Ur requirements.txt

WORKDIR /joyreactor

RUN git clone https://github.com/Krops/JoyreactorParser.git .
COPY config.ini /joyreactor/config.ini
RUN python bot.py
