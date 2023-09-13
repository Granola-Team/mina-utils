##### for mina archive node #####

# PostgreSQL

LD_LIBRARY_PATH=/usr/local/pgsql/lib
export LD_LIBRARY_PATH

PATH=/usr/local/pgsql/bin:$PATH
export PATH

MANPATH=/usr/local/pgsql/share/man:$MANPATH
export MANPATH

# aliases

alias mina-archive-run="sh ~/.mina/mina_archive_run.sh"
alias mina-postgres-start-server="sh ~/.mina/postgres_start.sh"
