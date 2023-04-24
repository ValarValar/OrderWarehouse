THIS_FILE := $(lastword $(MAKEFILE_LIST))
.PHONY: help migrate_and_run createsuperuser
help:
	make -pRrq  -f $(THIS_FILE) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'
migrate_and_run_store:
	python store/manage.py makemigrations
	python store/manage.py migrate
	python store/manage.py loaddata store/fixtures/store.json
	python store/manage.py createsuperuser --noinput
	python store/manage.py runserver 0.0.0.0:8000
migrate_and_run_warehouse:
	python store/manage.py makemigrations
	python store/manage.py migrate
	python store/manage.py loaddata store/fixtures/warehouse.json
	python store/manage.py createsuperuser --noinput
	python store/manage.py runserver 0.0.0.0:8001