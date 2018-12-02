FROM python:alpine
MAINTAINER John Peel "john@dgby.org"
WORKDIR /app

RUN apk add --no-cache build-base musl-dev libnsl libaio \
 && pip install --upgrade pip setuptools \
 && ln /usr/lib/libnsl.so.2 /usr/lib/libnsl.so.1

ENV INSTANTCLIENT instantclient_11_2
ENV ORACLE_BASE /usr/lib/${INSTANTCLIENT}
ENV LD_LIBRARY_PATH /usr/lib/${INSTANTCLIENT}
ENV TNS_ADMIN /usr/lib/${INSTANTCLIENT}
ENV ORACLE_HOME /usr/lib/${INSTANTCLIENT}

ADD https://dgby.org/~john/.oracle/instantclient-basiclite-linux.x64-11.2.0.4.0.zip /
RUN unzip /instantclient-*.zip \
 && rm /instantclient-*.zip \
 && mv ${INSTANTCLIENT} /usr/lib/

COPY requirements.txt /app
RUN python -m venv /app/venv \
 && /app/venv/bin/pip install -r requirements.txt \
 && /app/venv/bin/pip install gunicorn \
 && chmod +x /app/boot.sh
COPY . /app

ENV FLASK_APP app.py
RUN adduser -D appuser \
 && chown -R appuser:appuser /app
USER appuser

ENTRYPOINT ["/app/boot.sh"]
