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



## Setup fleet
- update the env variables
FLEET_ENROLL=0
FLEET_SERVER_ENABLE=0
- start all server through docker compose up
- docker exec -it deploy-elasticsearch-1 bash
- ./bin/elasticsearch-setup-passwords interactive
- restart docker compose
- login to kibana with elastic user http://0.0.0.0:9600/login=
- add fleet server
copy the fleet-server-service-token and fleet-server-policy
- restart docker compose up with env
FLEET_SERVER_SERVICE_TOKEN
FLEET_SERVER_POLICY_ID
- add policy for ES (System policy)
- copy and add set FLEET_ENROLLMENT_TOKEN and FLEET_ENROLL=1
- restart es - docker-compose restart elasticsearch
- ./agent/elastic-agent install --url=${FLEET_URL} --enrollment-token=${FLEET_ENROLLMENT_TOKEN} -n -i
- TODO - figure out why the status is unhealthy
- TODO - figure out how to avoid calling elastic agent manually