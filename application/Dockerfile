FROM python:3.8.3

ENV FLASK_APP=app.py



RUN mkdir -p /opt/app
RUN python -m pip install flask flask_sqlalchemy psycopg2 loguru names
WORKDIR /opt/app
ADD . ./

CMD ["flask", "run", "--host=0.0.0.0"]