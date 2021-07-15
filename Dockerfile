FROM ghcr.io/commonknowledge/do-app-baseimage-django-node:9fedf9b96654087efd8e0e978514f24b573d5f2b
RUN pip install pipenv

# Install the project requirements and build.
COPY --chown=app:app .bin/install.sh requirements.txt package.json yarn.lock .
RUN SKIP_MIGRATE=1 bash install.sh

# Copy the rest of the sources over
COPY --chown=app:app . .
ENV DJANGO_SETTINGS_MODULE=stopwatch.settings.production \
    NODE_ENV=production

RUN bash .bin/build.sh
