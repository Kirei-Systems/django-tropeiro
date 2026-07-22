
run:
    just manage runserver

run-all:
    tmux 

redb:
    rm ./db.sqlite3
    just migrate
    just seed

seed:
    just manage seed

check:
    just manage check

migrate *args:
    just manage migrate {{args}}

makemigrations *args:
    just manage makemigrations {{args}}

manage *args:
    python ./manage.py {{args}}


fetch:
  curl https://raw.githubusercontent.com/Kirei-Systems/django-tropeiro/refs/heads/main/templates/project/etc/admin.just > etc/admin.just
