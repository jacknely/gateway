install:
	docker-compose build

run:
	docker-compose up --force-recreate service

test:
	docker-compose run service sh -c ' \
	    flake8 --docstring-convention google service && \
	    mypy --ignore-missing-imports service && \
	    APPLICATION_STAGE=test py.test -vv --failed-first \
		--durations=10 service/tests'

pytest:
	docker-compose run --no-deps service sh -c ' \
	    APPLICATION_STAGE=test --failed-first $(test)'

analyse:
	docker-compose run service sh -c 'pylint --ignore tests --exit-zero service'
