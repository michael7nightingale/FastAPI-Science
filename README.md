# FastAPI Science.

[![Build Status](https://github.com/michael7nightingale/FastAPI-Science/actions/workflows/fastapi-app.yml/badge.svg)](https://github.com/michael7nightingale/FastAPI-Science/actions/workflows/fastapi-app.yml/)
[![Build Status](https://github.com/michael7nightingale/FastAPI-Science/actions/workflows/codeql.yml/badge.svg)](https://github.com/michael7nightingale/FastAPI-Science/actions/workflows/codeql.yml/)
[![Build Status](https://github.com/michael7nightingale/FastAPI-Science/actions/workflows/docker-image.yml/badge.svg)](https://github.com/michael7nightingale/FastAPI-Science/actions/workflows/docker-image.yml/)

I found my old project and decided to make it more interesting. So the fact is I restructured the project to change its architecture.
Some new features are coming. The web-app is both fullstack and API.

*NOTE*: .git root is project root;

## Stack
- `Python 3.11`;
- `FastAPI`;
- `PostgreSQL`;
- `fastapi_authtools` (my authentication library);
- `Pydantic 2.0`;
- `SQLAlchemy`;
- `Asyncpg` async engine for production and development, `aiosqlite` for testing;
- `numpy` / `pandas` / `sympy` / `matplotlib` for calculations;
- `Docker`;
- `HTML` / `CSS` / `js` for fullstack;
- `pytest` in async mode for testing;
- `flake8` linter;

## Requirements
I use `Python 3.11` as the project language.
The environment variables seem to be nice, but you can change it with ones you need
(.dev.env for developing, .docker.env for running application in Docker, .test.env for testing).  

You can install application requirements with:
```commandline
pip install -r requirements.txt
```

## Tests and linters
First install development requirements with:
```commandline
pip install -r dev-requirements.txt
```

To run flake8 linter:
```commandline
flake8
```

To run tests:
```commandline
pytest
```

or write this for more information:
```commandline
pytest -s -vv
```


## Running application
You can run it using `Docker`. Run this command in the project root directory.

The server is default running at `localhost:8000`.

```commandline
docker-compose up -d --build
```

For local running using `uvicorn` run:
```commandline
uvicorn app.main:create_app --reload --port 8000
```
