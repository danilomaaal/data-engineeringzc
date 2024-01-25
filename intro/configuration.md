## Configs

Intall terraform:

``` sh
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

apt update && sudo apt install terraform

```
Docker image:

```sh
docker network create pg-network

docker volume create --name postgres_volume_local -d local

docker run -it -e POSTGRES_USER="root" \
	-e POSTGRES_PASSWORD="root" \
	-e POSTGRES_DB="ny_taxy" \
	-v postgres_volume_local:/var/lib/postgresql/data \
	-p 5432:5432 \
	--network=pg-network \
	--name pg-database postgres:13

docker container start pg-database
```

PGAdmin:

```sh
docker run -it -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
	-e PGADMIN_DEFAULT_PASSWORD="root" \
	-p 8080:80 \
	--network=pg-network \
	--name pgadmin \
	 dpage/pgadmin4 
```

Ingesting script:

``` sh
python scripts/ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --database=ny_taxy \
    --table-name=yellow_taxy_trips \
    --url=$URL
```


Access pgcli:
```sh
pgcli -h localhost -p 5432 -u root -d ny_taxy
```

Confirm record count:
```sql
SELECT COUNT(1)
FROM yellow_taxy_trips

```

Build and run dockerized scrpt:
```sh
docker build -t taxy_ingets:v1 .

docker run -it \
    --network=pg-network \
    taxy_ingets:v1 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --database=ny_taxy \
    --table-name=yellow_taxy_trips \
    --url=$URL
```

Run docker compose

```sh
docker compose up -d

docker compose down
```