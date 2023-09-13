# PostgreSQL scripts for mina

To set up for PostgreSQL, change user to `postgres` and do

```sh
python3 postgres_setup.py
```

This sets up the `postgres` user's

- `~/.bashrc`
  - sets up postgres env vars and aliases
- `~/.bash_profile`
  - automatically sources `~/.bashrc`
- `~/.mina`
  - `mina_archive_run.sh`
  - `postgres_start.sh`
