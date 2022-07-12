FROM joyzoursky/python-chromedriver

WORKDIR /tmp
COPY requirements.txt  /tmp/requirements.txt
COPY config.ini /joyreactor

RUN pip install --no-cache-dir -q -Ur requirements.txt

WORKDIR /joyreactor

RUN git clone https://github.com/Krops/JoyreactorParser.git .
RUN python bot.py
