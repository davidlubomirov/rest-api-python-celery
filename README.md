# Contact API

[Link to task](https://docs.google.com/document/d/16lL6Zg_PPIUULz_ZvWuK1JyqnXCCpVLU7s1Ky_hF12Y)

## Notes

- code documentation won't be generated
- implementation and testing using `python 3.8`
- all tests can be executed using [run_all_tests](./api/run_all_tests) script
- project remarks can be found at [TODO.md](./TODO.md)
- API layout was defined in [api-layout.raml](./api-layout.raml), but still not updated with the latest changes introduced in TASK 2 and TASK 3
- there are missing unit and integration tests left intentionally
- the celery worker was tested with Redis brocker running on `localhost` from docker container

## External tools

- [Leasot](https://github.com/pgilad/leasot)

## Using Leasot

Project `TODO` and `FIXME` remarks were exported in [TODO.md](./TODO.md)

To install the tool - `npm install --global leasot`

To export all remarks execute the following command from the root of this project directory - `leasot -x --reporter markdown '**/*.py' > TODO.md` or run [export_remarks](./export_remarks)

## Running all services

### Requirements

The following environment variables are required:

| Name              |  Type  |                  Description                   |         Example          |
| ----------------- | :----: | :--------------------------------------------: | :----------------------: |
| REDIS_BROCKER_URL | string |   URL to RedisDB. User for the Celery worker   | "redis://localhost:6379" |
| SQLITE_FILE_NAME  | string |          sqlite file name to be used           |       "db.sqlite"        |
| JWT_SECRET        | string |         used for creation of API token         |   "secretPassword123"    |
| API_AUTH_USER     | string | username to use for validation in `/api/login` |      "testUsername"      |
| API_AUTH_PASSWORD | string | password to use for validation in `/api/login` |      "testPassword"      |

**While implementing and testing the application, all environment variables were defined in `.env` file under `<project_root>/api` folder.**

### Start API and async worker

To run the API and the async worker three terminals are needed:

1. from the first terminal start the API service - `cd api && source .env && python run.app`
2. from the seconds terminal start the Celery worker - `cd api && source .env && celery worker -A celery_worker.celery --loglevel=info`
3. from the third terminal start Celery beat (scheduler) - `cd api && source .env && celery beat -A celery_worker.celery --loglevel=info`

## Example of .env configuration

```
export REDIS_BROCKER_URL="redis://localhost:6379"
export SQLITE_FILE_NAME="db.sqlite"
export JWT_SECRET="Sav!?9123L"
export API_AUTH_USERNAME="test"
export API_AUTH_PASSWORD="test"
```
