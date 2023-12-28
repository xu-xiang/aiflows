# Install

## Docker Compose

### nocodb

```bash
# for MySQL
cd nocodb-compose/mysql
```

You can access nocodb by opening http://localhost:8080 in your web browser.

We provide different docker-compose.yml files
under [this directory](https://github.com/nocodb/nocodb/tree/master/docker-compose). Here are some examples.

[nocodb](https://github.com/nocodb/nocodb)

### n8n

#### Starts n8n with PostgreSQL as database

To start n8n with PostgreSQL simply start docker-compose by executing the following
command in the current folder.

**IMPORTANT:** But before you do that change the default users and passwords in the [`.env`](.env) file!

```bash
cd n8n-compose/withPostgres
docker-compose up -d
```

You can access n8n by opening http://localhost:5678 in your web browser.

#### Configuration

The default name of the database, user and password for PostgreSQL can be changed in the [`.env`](.env) file in the
current directory.

[n8n](https://github.com/n8n-io/n8n)

### one-api

```bash
cd one-api/withSQLite
docker-compose up -d

```
You can access one-api by opening http://localhost:3000 in your web browser.


## Docker

### nocodb

```bash
# for SQLite
docker run -d --name nocodb \
-v "$(pwd)"/nocodb:/usr/app/data/ \
-p 8080:8080 \
nocodb/nocodb:latest

# for MySQL
docker run -d --name nocodb-mysql \
-v "$(pwd)"/nocodb:/usr/app/data/ \
-p 8080:8080 \
-e NC_DB="mysql2://host.docker.internal:3306?u=root&p=password&d=d1" \
-e NC_AUTH_JWT_SECRET="569a1821-0a93-45e8-87ab-eb857f20a010" \
nocodb/nocodb:latest

# for PostgreSQL
docker run -d --name nocodb-postgres \
-v "$(pwd)"/nocodb:/usr/app/data/ \
-p 8080:8080 \
-e NC_DB="pg://host.docker.internal:5432?u=root&p=password&d=d1" \
-e NC_AUTH_JWT_SECRET="569a1821-0a93-45e8-87ab-eb857f20a010" \
nocodb/nocodb:latest

# for MSSQL
docker run -d --name nocodb-mssql \
-v "$(pwd)"/nocodb:/usr/app/data/ \
-p 8080:8080 \
-e NC_DB="mssql://host.docker.internal:1433?u=root&p=password&d=d1" \
-e NC_AUTH_JWT_SECRET="569a1821-0a93-45e8-87ab-eb857f20a010" \
nocodb/nocodb:latest
```

### n8n

```bash
docker volume create n8n_data

docker run -it --rm \
 --name n8n \
 -p 5678:5678 \
 -e DB_TYPE=postgresdb \
 -e DB_POSTGRESDB_DATABASE=<POSTGRES_DATABASE> \
 -e DB_POSTGRESDB_HOST=<POSTGRES_HOST> \
 -e DB_POSTGRESDB_PORT=<POSTGRES_PORT> \
 -e DB_POSTGRESDB_USER=<POSTGRES_USER> \
 -e DB_POSTGRESDB_SCHEMA=<POSTGRES_SCHEMA> \
 -e DB_POSTGRESDB_PASSWORD=<POSTGRES_PASSWORD> \
 -v n8n_data:/home/node/.n8n \
 docker.n8n.io/n8nio/n8n
```

### one-api

```bash
# SQLite 
docker run --name one-api -d --restart always -p 3000:3000 -e TZ=Asia/Shanghai -v /home/ubuntu/data/one-api:/data justsong/one-api
# MySQL Add `-e SQL_DSN="root:123456@tcp(localhost:3306)/oneapi"`
docker run --name one-api -d --restart always -p 3000:3000 -e SQL_DSN="root:123456@tcp(localhost:3306)/oneapi" -e TZ=Asia/Shanghai -v /home/ubuntu/data/one-api:/data justsong/one-api
```