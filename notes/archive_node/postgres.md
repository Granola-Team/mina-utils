# Postgres

## Running an archive node (after initial setup)

After completing the intial setup, to get an archive node running

- `postgres` user starts the PostgreSQL server `postgres -p 5432 -D /usr/local/var/postgres`
- `postgres` user does `mina_archive_run`
- then `mina_archive_daemon`


## Install from source

Follow [instructions](https://www.postgresql.org/docs/current/installation.html) to install from source

### Install dependencies

Before building PostgreSQL from source, you need to install some dependencies

```sh
sudo apt-get install build-essential libreadline-dev zlib1g-dev flex bison libxml2-dev libxslt-dev libssl-dev
```

### Download source

Download the [source code](https://www.postgresql.org/ftp/source/) from the PostgreSQL website. Once you have the file, extract it

```sh
tar xvfz postgresql-VERSION.tar.gz
```

### Configure and build

Once the source code is extracted, you can configure and build it with the following commands

```sh
cd postgresql-VERSION
./configure
make
```

### Install

Once the build is complete, you can install PostgreSQL with the following command

```sh
sudo make install
```

#### Add `postgres` user

Add user and set password

```sh
adduser postgres
sudo passwd postgres
```

#### Switch to `postgres` user and add env vars

```sh
su - postgres
nano ~/.bashrc
```

Add the following to `~/.bashrc`

```sh
LD_LIBRARY_PATH=/usr/local/pgsql/lib
export LD_LIBRARY_PATH

PATH=/usr/local/pgsql/bin:$PATH
export PATH

MANPATH=/usr/local/pgsql/share/man:$MANPATH
export MANPATH
```

Save and refresh

```sh
source ~/.bashrc
```

(if env vars are not set, then you must use fully qualified commands `/usr/local/pgsql/bin/COMMAND`)

### Initialize db and start Postgres server

Once PostgreSQL is installed, initialize the database

```sh
initdb -D /usr/local/var/postgres
```

You can now start the PostgreSQL server

```sh
postgres -p 5432 -D /usr/local/var/postgres
```

(make sure no other postgres instances are running, see [postgres](./../helpful_commands.md#postgresql), otherwise you will most likely get postmaster errors)

Only on the first time setting up the archive node, you need to create the `archive` db

```sh
createdb -h localhost -p 5432 -e archive
psql -h localhost -p 5432 -d archive \
  -f <(curl -Ls https://raw.githubusercontent.com/MinaProtocol/mina/master/src/app/archive/create_schema.sql)
```

Start the archive process on port `3086` with the `postgres` user

```sh
mina-archive run \
  --postgre-uri postgres://localhost:5432/archive \
  --server-port 3086
```

Alternatively, `postgres` can run [`mina_archive_run`](../../scripts/mina_archive_run.sh)

Finally, open another terminal and start the daemon, connecting it to the archive process on port `3086`

```sh
mina daemon \
  --peer-list-url https://storage.googleapis.com/mina-seed-lists/mainnet_seeds.txt \
  --archive-address 3086
```

Alternatively, you can run [`mina_archive_daemon`](../../scripts/mina_archive_daemon.sh)

You can also connect to an archive process on another machine by specifying a hostname in `--archive-address`, e.g. `localhost:3086`

### Config

`postgresql.conf` is located in `/etc/postgresql/VERSION/main/`
