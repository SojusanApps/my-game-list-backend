FROM python:3.12.1-slim-bullseye

# Application log path from env
ARG MGL_LOG_DIR_PATH

# Create a new non-root user
RUN adduser --system --no-create-home nonroot

# To locally connect your container image to a repository:
LABEL org.opencontainers.image.source https://github.com/SojusanApps/my-game-list-backend

# App directory
WORKDIR /var/www/my-game-list

RUN apt-get update \
    && apt-get -y install --no-install-recommends curl=7.74.0-1.3+deb11u13 \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir pip==24.3.1

COPY settings.py gunicorn.conf.py entrypoint.sh *.whl ./

# Install Django app
RUN pip install --no-cache-dir -U ./*.whl
WORKDIR /usr/local/lib/python3.12/site-packages
RUN  pip install --no-cache-dir -r requirements/requirements.txt

WORKDIR /var/www/my-game-list

# Create the needed directories and set a non-root user as the owner to omit the permission error
RUN mkdir -p ${MGL_LOG_DIR_PATH} && chown -R nonroot: ${MGL_LOG_DIR_PATH}
RUN mkdir -p /opt/my_game_list/static && chown -R nonroot: /opt/my_game_list/static

# Run application as non-root user
USER nonroot

ENTRYPOINT ["./entrypoint.sh"]
