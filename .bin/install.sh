set -e

python -m pipenv install
yarn

if [ "$SKIP_MIGRATE" != "1" ]; then
  python -m pipenv run python manage.py migrate
  python -m pipenv run python manage.py preseed_transfer_table auth wagtailcore wagtailimages.image wagtaildocs search stopwatch stopwatch
  python -m pipenv run python manage.py createsuperuser
  touch stopwatch/settings/local.py
fi
