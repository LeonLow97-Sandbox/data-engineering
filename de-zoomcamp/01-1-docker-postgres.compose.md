# Docker for Data Engineering: Postgres, Docker Compose, and Real-World Workflows

## Docker

- Docker containers are isolated from the host machine.

```sh
docker run -it ubuntu   # Run an interactive Ubuntu container
    apt update          # Update package lists
    apt install python3 # Install Python 3
    python3 -V

docker run -it python:3.13.11
docker run -it python:3.13.11-slim  # Slim version without extra packages
docker run -it --entrypoint=bash python:3.13.11-slim    # Override entrypoint to bash

docker ps -a                # List all containers
docker rm `docker ps -aq`   # Remove all containers

# Docker Volumes
docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.11-slim # Mount host machine 'test' directory to '/app/test' in container

# Dockerfile
docker build -t test:python .
docker run -it --entrypoint=bash --rm test:pandas
docker run -it --rm test:pandas 12
```

## Python Virtual Environments

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install pandas pyarrow
deactivate # Exit virtual environment

# Using uv to init virtual environment
brew install uv
uv init --python 3.13.11
uv add pandas pyarrow
```

## PostgreSQL

```sh
# Create a Docker volume for Postgres data

# -v ny_taxi_postgres_data:/var/lib/postgresql --> Internal volume to persist data
# -p 5432:5432 --> Map host port 5432 to container port 5432
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18

brew install libpq
brew link --force libpq
uv add --dev pgcli  # dependencies needed for development, not needed in production
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

# Jupyter notebook
uv add jupyter
uv run jupyter notebook

# SQL Alchemy (for pandas to interact with database)
uv add sqlalchemy psycopg2-binary

# Convert Jupyter notebook to Python script
uv run jupyter nbconvert --to=script notebook.ipynb
mv notebook.py ingest_data.py
uv run python ingest_data.py

# Using click command for interactive CLI arguments
# Running on Localhost to run pipeline that ingests data into Postgres
uv run python ingest_data.py --help
uv run python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table=yellow_taxi_trips_2021_1

# Run dockerfile to build the ingest_data image
# Running the same command inside the container
docker build -t taxi_ingest:v001 .
docker run -it --rm \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=host.docker.internal \
  --port=5432 \
  --db=ny_taxi \
  --table=yellow_taxi_trips_2021_1

# To access from one container (ingest_data) to another container (Postgres), create a user-defined bridge network
# Either use host.docker.internal (for Mac and Windows) or create a user-defined bridge network
docker network create pg-network
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network pg-network \
  --name pg-database-network \
  postgres:18
docker build -t taxi_ingest:v001 .
docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pg-database-network \
  --port=5432 \
  --db=ny_taxi \
  --table=yellow_taxi_trips_2021_1

# In another terminal, run pgAdmin on the same network
# Visit http://localhost:8085
  # Email: admin@admin.com
  # Password: root
  # Add New Server:
    # General: Name: pg-database-network
    # Connection:
      # Host name/address: pg-database-network
      # Port: 5432
      # Maintenance database: ny_taxi
      # Username: root
      # Password: root
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

## Docker Compose

- Up until now, the docker commands are run individually.
- Docker Compose allows you to define and run multi-container Docker applications.
- "Networks" is not needed because Docker Compose creates a default network for the services to communicate.

```sh
docker-compose up

# At this point, both Postgres and pgAdmin are running.
# In another terminal, run the ingest_data container to ingest data into Postgres
docker network ls
# NETWORK ID     NAME               DRIVER    SCOPE
# 2f259bab93aa   bridge             bridge    local
# 0487a8e930a3   kind               bridge    local
# 880511edd75d   pg-network         bridge    local
# e2878c3ab3a6   pipeline_default   bridge    local

# pipeline_default is the network created by Docker Compose because we did not specify a network name in docker-compose.yml
docker build -t taxi_ingest:v001 .
docker run -it --rm \
  --network=pipeline_default \
  taxi_ingest:v001 \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table=yellow_taxi_trips_2021_1
```
