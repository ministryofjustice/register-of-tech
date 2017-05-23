FROM alpine:3.5

RUN apk add --update \
    postgresql-dev \
    build-base \
    uwsgi-python \
    bash \
    linux-headers \
    pcre-dev

RUN apk add --no-cache --update python3 python3-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    /usr/bin/pip3 install --upgrade pip setuptools uwsgi && \
    rm -r /root/.cache

ADD . /app
WORKDIR /app
RUN mkdir -p /app/static

RUN /usr/bin/pip3 install -r requirements.txt
RUN /usr/bin/python3 manage.py collectstatic --noinput

CMD bash /app/docker/run.sh ${PORT:-8000}
