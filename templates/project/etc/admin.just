
run:
    just manage runserver

redb:
    just rm-db
    just migrate
    just seed

rm-db:
    rm -f ./db.sqlite3
    

remigrate:
    rm -rf api/migrations/
    just rm-db
    just makemigrations api
    just seed

seed:
    just manage seed

check:
    just manage check

migrate *args:
    just manage migrate {{args}}

makemigrations *args:
    just manage makemigrations {{args}}
    just migrate

manage *args:
    python ./manage.py {{args}}


fetch:
  curl https://raw.githubusercontent.com/Kirei-Systems/django-tropeiro/refs/heads/main/templates/project/etc/admin.just > etc/admin.just
