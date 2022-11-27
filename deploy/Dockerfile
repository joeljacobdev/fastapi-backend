FROM python:3.10.5-slim-bullseye
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]