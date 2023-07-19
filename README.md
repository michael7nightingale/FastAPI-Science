# FastAPI Science.

I found my old project and decided to make it more interesting. So the fact is I restructured the project to change its architecture.
Some new features are coming. The web-app is both fullstack and API.

## Stack
- `Python`;
- `FastAPI`;
- `fastapi_authtools` (my authentication library);
- `Pydantic`;
- `SQLAlchemy`;
- `Asyncpg`;
- `numpy` / `pandas` / `sympy` / `matplotlib` for calculations;
- `Docker`;
- `HTML` / `CSS` / `js` for fullstack;


## Requirements
I use `Python 3.11` as the project language.
The environment variables seem to be nice, but you can change it with ones you need
(.dev.env for developing, .docker.env for running application in Docker).  


## Running application
You can run it using `Docker`. Run this command in the project root directory.

The server is default running at `localhost:8000`.

```commandline
docker-compose up -d --build
```
