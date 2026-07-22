#!/usr/bin/env sh
if ! which uv >/dev/null; then
  echo 'This script needs `uv` to work:' 'https://docs.astral.sh/uv/'
  exit 1
fi

proj=$1
tropeiro=$(dirname $(realpath $0))
set -eux pipefail
if [ -z $proj ]; then
  echo 'Project name: '
  read proj
fi
mkdir $proj
cd $proj
uv init --bare
uv add $tropeiro
source .venv/bin/activate

django-admin startproject $proj . --template $tropeiro/templates/project
python manage.py makemigrations
python manage.py migrate

echo 'Project created!'
echo ''
echo 'To deal with venv, we recommend setting up `direnv` and creating the following `.envrc` file:'
echo '```'
echo 'export VIRTUAL_ENV=.venv'
echo 'layout python3'
echo '```'
