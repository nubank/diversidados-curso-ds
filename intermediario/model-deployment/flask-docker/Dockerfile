# INSTRUCOES NO FINAL DESTE ARQUIVO

# FROM python:3.8.6-alpine3.12
# RUN apk add --no-cache python3-dev libffi-dev gcc musl-dev make
# https://stackoverflow.com/a/61264535/7649076
# https://github.com/gevent/gevent/issues/1567
# https://stackoverflow.com/questions/30624829/no-such-file-or-directory-limits-h-when-installing-pillow-on-alpine-linux
# --> desisti porque a instalacao dos requirements demora muito

FROM python:3.8.6-slim-buster
# Python images: https://hub.docker.com/_/python

COPY requirements.txt /app/
RUN python3 -m pip install --no-cache-dir -r /app/requirements.txt

COPY model.pkl scores.csv models_realtime_batch.py /app/
WORKDIR /app

# RUN mkdir /app/logs && \
#   touch /app/logs/model-app.log

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["models_realtime_batch.py"]

# INSTRUCOES:

# docker build -t my-flask-app .

# docker run -e FLASK_APP=models_realtime_batch.py my-flask-app -m flask routes

# docker run -e FLASK_APP=models_realtime_batch.py -e FLASK_ENV=development -p 5000:5000 my-flask-app
# docker run -e FLASK_APP=models_realtime_batch.py -e FLASK_ENV=development -p 5000:5000 my-flask-app -m flask run --host 0.0.0.0

# docker logs $(docker ps --filter ancestor=my-flask-app -q) --follow

# docker run -it --entrypoint='' my-flask-app /bin/sh
