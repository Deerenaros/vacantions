FROM python:3.8.3

ENV FLASK_APP=app.py


ADD requirements.txt ./

RUN apt-get update && apt-get install -y libldap2-dev libsasl2-dev libssl-dev
RUN python -m pip install -r requirements.txt

RUN mkdir -p /opt/
WORKDIR /opt/
ADD . ./

CMD uwsgi --master \
  --workers 2 \
  --threads 20 \
  --protocol http \
  --socket 0.0.0.0:5000 \
  --module app:app