FROM python:3.11.0-slim-buster

# App directory
WORKDIR /var/www/my-game-list

RUN apt-get update \
    && apt-get -y install --no-install-recommends curl vim \
    && pip install -U pip

COPY settings.py gunicorn.conf.py entrypoint.sh *.whl ./

# Install Django app
RUN pip install -U *.whl \
    && cd `pip show my-game-list | grep Location | awk '{print $2}'` \
    && pip install -r requirements/requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
