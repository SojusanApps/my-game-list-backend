FROM python:3.12.1-slim-bullseye

# Create a new non-root user
RUN adduser --system --no-cache-home nonroot

# To locally connect your container image to a repository:
LABEL org.opencontainers.image.source https://github.com/Sojusan/my-game-list

# App directory
WORKDIR /var/www/my-game-list

RUN apt-get update \
    && apt-get -y install --no-install-recommends curl=7.64.0-4+deb10u6 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pip==23.1.2

COPY settings.py gunicorn.conf.py entrypoint.sh *.whl ./

# Install Django app
RUN pip install --no-cache-dir -U ./*.whl
WORKDIR /usr/local/lib/python3.12/site-packages
RUN  pip install --no-cache-dir -r requirements/requirements.txt

WORKDIR /var/www/my-game-list

# Run application as non-root user
USER nonroot

ENTRYPOINT ["./entrypoint.sh"]
