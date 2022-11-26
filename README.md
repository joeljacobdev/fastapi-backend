# FASTAPI BACKEND

Make sure python version is 3.10.5. If not install it using `pyenv`

Install the required packages using 
```commandline
pipenv shell
pipenv install
```

Create your `app/config/local.py` file from `app/config/local.template`.
Create your `deploy/.env` file from `deploy/.env.template`.
Make sure to do the required updates in these files.

Run the required dependencies through `docker-compose -f deploy/docker-compose.yml up`