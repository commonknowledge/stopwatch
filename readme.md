# Stopwatch

Turning a spotlight on stop and search.

Staging: https://stopwatch.commonknowledge.dev/

## Stack

- Django (fullstack django app, no js frontend)
- Bootstrap (css an' stuff)
- Wagtail (CMS, administration, editor workflows and storage)
- Webpack (asset pipeline)
- PostgreSQL (Database & search index)
- Digital Ocean App Platform (Compute, database hosting, object storage & CDN)

## Dev quickstart

### Easy mode: VSCode Dev Container

- Make sure you have Docker, VSCode, and the Remote Development extension installed.
- Once installed run the command "Clone Repository in Container Volume" in VSCode selecting this repository. This methodology makes for a slightly faster site.
- Wait for the dev container to build.
- Check your terminal and respond to any setup prompts it asks for
- Search for `stopwatch/settings/local.py` on LastPass and paste its contents into the corresponding local file
- Use VSCodes' 'run' command (usually aliased to F5) to run the app.
  - Make sure you use the 'App' configuration, which will start both the Djagno app and the frontend Webpack build pipeline.
  - You may need to go to View > Run to look at this configuration.
- Go to [localhost:8000/admin](localhost:8000/admin)
- Use the 'import' option on the left to seed the archive with content from the staging site.
- OR run the setup script to populate some demo pages
  ```
  python manage.py setup_pages --scratch True --ensure-site True --ensure-pages True
  ```

If you're having issues getting started this way, see [Troubleshooting](#troubleshooting-setup) for some ideas.

### Hard mode: Using Dockerfiles

Figure it out for yourself based on the .devcontainer dockerfile and write it up here ;)

## Technical documentation

### Build process

This repository has a development dockerfile (.devcontainer/Dockerfile) and a production one (./Dockerfile).

They both run .bin in ./.bin to configure their environments and install dependencies:

- Base container configuration, which is run infrequently (installing apt packages, etc) should be configured in prepare.sh.
- Frequently-run .bin (installing pip packages, etc) should go in install.sh. The difference between these is that changing prepare.sh triggers a full rebuild of the development container, whereas install.sh is only run after the container is built.
- build.sh is the last thing run on deploy to production

## Troubleshooting setup

This is based on the experience of @freemvmt trying to set up the project on [Easy mode](#easy-mode-vscode-dev-container) for the first time in March 2026.

1. The `Clone Repository in Container Volume` function, which pulls `main` from the remote and tries to build it in a local Docker container, didn't work for me, whereas `Open Folder in Container` (i.e. using my local copy of the repo) did.

2. Once inside the container, `install.sh` was failing due to multiple copies of `virtualenv` being available. I fixed this by changing all references of `pipenv` to `python -m pipenv`, to ensure that we use the version associated with the python installation (merged in via #[86](https://github.com/commonknowledge/stopwatch/pull/86)).

3. The 'import' option in Wagtail admin dashboard only appeared after populating the `stopwatch/settings/local.py` file. Even then, the import function proved error prone, so we instead used a psql dump from staging to produce a relevant dev environment (i.e. I ran something like `PGPASSWORD=postgres psql -h db -U postgres -d postgres < /workspace/stopwatch_staging.psql`).

4. The dev site was not initially styled, despite the webpack server that runs as part of the 'App' config in `launch.json` - I ran `yarn webpack` manually to fix that.
