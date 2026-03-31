ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache \
    python3 \
    py3-pip \
    bash

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN python3 -m venv /opt/venv
RUN /opt/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

COPY app.py /app/app.py
COPY run.sh /run.sh
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
