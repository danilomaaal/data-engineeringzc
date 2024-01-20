## Configs

Intall terraform:

``` sh
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list

apt update && sudo apt install terraform

```
Docker images

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
```