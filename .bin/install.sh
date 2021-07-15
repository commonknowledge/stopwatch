set -e

pipenv install
yarn

if [ "$SKIP_MIGRATE" != "1" ]; then
  pipenv run python manage.py migrate
  pipenv run python manage.py preseed_transfer_table auth wagtailcore wagtailimages.image wagtaildocs search home stopwatch
  pipenv run python manage.py createsuperuser
  touch stopwatch/settings/local.py
fi
