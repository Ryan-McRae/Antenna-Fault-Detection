# PostgreSQL Cheatsheet (Ubuntu + DBeaver)

Notes from setting up a local PostgreSQL server, connecting with DBeaver, and loading CSV files.

## Contents

1. [Core concepts](#1-core-concepts)
2. [Managing the server with systemctl](#2-managing-the-server-with-systemctl)
3. [Clusters](#3-clusters)
4. [Roles and authentication](#4-roles-and-authentication)
5. [Databases](#5-databases)
6. [psql commands](#6-psql-commands)
7. [Loading CSV files](#7-loading-csv-files)
8. [Running SQL scripts](#8-running-sql-scripts)
9. [Backup and restore](#9-backup-and-restore)
10. [Connecting with DBeaver](#10-connecting-with-dbeaver)
11. [Common errors](#11-common-errors)

---

## 1. Core concepts

```
cluster → databases → schemas → tables → rows
```

| Term | Meaning |
|---|---|
| **Server** | The PostgreSQL program running in the background, listening on a port (default `5432`). |
| **Client** | Anything that connects and sends SQL: `psql`, DBeaver, a Python script. |
| **Cluster** | One server instance and everything it manages (see [section 3](#3-clusters)). |
| **Database** | A named container for related tables. You connect to one at a time. |
| **Schema** | A folder inside a database. The default is `public`. |
| **Role** | A user or group account inside PostgreSQL. |

Installing the `postgresql` package creates a cluster, starts the server, and creates the `postgres` superuser role. Your data lives in the server's data directory.

---

## 2. Managing the server with systemctl

### What is systemctl?

Most modern Linux distributions (including Ubuntu) use **systemd** to start, stop, and supervise background programs. These programs are called **services** (or *units*). `systemctl` is the command-line tool for controlling systemd.

PostgreSQL is a service, so you manage it like any other: you ask systemd to start it, stop it, restart it, or report on it. Systemd also starts it automatically at boot if it is *enabled*.

### Common commands

```bash
sudo systemctl status postgresql      # is it running? shows recent log lines
sudo systemctl start postgresql       # start the server
sudo systemctl stop postgresql        # stop the server
sudo systemctl restart postgresql     # stop then start (needed after some config changes)
sudo systemctl reload postgresql      # reload config without dropping connections
sudo systemctl enable postgresql      # start automatically at boot
sudo systemctl disable postgresql     # do not start at boot
```

Press `q` to leave the `status` output.

### Reading the status output

- `active (exited)` is normal for the `postgresql` umbrella service on Ubuntu. It is a wrapper that launches the real per-cluster services.
- To see whether the actual server is up, use `pg_lsclusters` and look for `online`.

### Viewing logs

```bash
journalctl -u postgresql              # service logs via systemd
sudo tail -f /var/log/postgresql/postgresql-*-main.log   # the PostgreSQL log file itself
```

---

## 3. Clusters

### What is a database cluster?

A **database cluster** is *one PostgreSQL server instance together with all the data it manages*. It is not a group of machines working together, which is what "cluster" means in most other contexts.

A cluster consists of:

- one **data directory** on disk holding all its files
- one **running server process** managing that directory
- one **port** it listens on
- a set of **databases** (at least `postgres`, `template0`, `template1`)
- a set of **roles**, shared across all databases in the cluster

Two consequences are worth remembering:

- **Roles belong to the cluster, not to a database.** A role you create can be granted access to any database in that cluster.
- **Databases are separate from each other.** You cannot query across two databases in one statement, even within the same cluster.

### Multiple clusters

Ubuntu names the default cluster `main` and tags it with the PostgreSQL version (for example `16 main`). You can run several clusters side by side, each with its own data directory and port (`5432`, `5433`, and so on). This is how people run two PostgreSQL versions on one machine, for example when testing an upgrade.

```bash
pg_lsclusters                          # list clusters
sudo pg_createcluster 16 test          # create a new cluster (version 16, named "test")
sudo pg_ctlcluster 16 test start       # start a specific cluster
sudo pg_dropcluster 16 test            # delete a cluster (destroys its data)
```

### Listing clusters

```bash
pg_lsclusters
```

Output columns:

```
Ver Cluster Port Status Owner    Data directory              Log file
```

Version, cluster name, port, status (`online` / `down`), owner (Linux user), data directory, and log file.

### Finding the data directory

```sql
SHOW data_directory;
```

Typically `/var/lib/postgresql/<version>/main`. Look but do not edit these files by hand, and do not copy them while the server is running. Use `pg_dump` for backups instead.

---

## 4. Roles and authentication

### The default superuser

The installer creates a role named `postgres`, tied to the Linux user of the same name. Reach it with:

```bash
sudo -u postgres psql
```

Avoid working as a superuser day to day. Create a role matching your own Linux username instead.

### Create your own role

```bash
sudo -u postgres createuser --superuser "$USER"
```

`$USER` is a built-in shell variable holding your Linux username, so type it literally. Superuser is fine on a local learning machine but not on a real server.

For a safer, non-superuser role:

```bash
sudo -u postgres createuser --createdb "$USER"
```

### List roles

```sql
\du
```

or from the shell:

```bash
sudo -u postgres psql -c "\du"
```

### Set a role's password

Run this inside `psql`. It sets the password for the **role you are currently connected as**, not for a database:

```sql
\password
```

To set it for another role:

```sql
\password role_name
```

### Two ways to connect

| | Socket (local) | Network (TCP) |
|---|---|---|
| Command | `psql db_name` | `psql -h localhost -p 5432 -U role_name -d db_name` |
| Authentication | **Peer**: your Linux username must match the role name | **Password** |
| Password needed | No | Yes |
| Used by | Terminal shortcuts | DBeaver, Python scripts, any app |

Peer authentication is why `psql db_name` works without a password when your role matches your Linux user.

---

## 5. Databases

```bash
createdb db_name                 # create a database
dropdb db_name                   # delete a database (permanent)
psql -l                          # list all databases in the cluster
```

Note: `psql -l` lists **every database in the cluster**, whichever role you connect as. The `-U` flag changes who you connect as, not which databases are shown:

```bash
psql -U role_name -l             # list databases, connected as role_name
```

To see which databases a role *owns*, use `\l` and read the Owner column.

### Design guidance

- One database per **project**, not per season or per time period. Store the season as a column.
- Tables in the same database are usually related (linked by foreign keys), but PostgreSQL does not require it.
- `template1` is the blueprint copied by `CREATE DATABASE`. `template0` is a pristine backup of it. Leave both alone.

---

## 6. psql commands

Connect to a database:

```bash
psql db_name
```

Backslash commands run inside `psql`. They are client shortcuts and do not end with a semicolon. SQL statements do end with `;`.

| Command | Action |
|---|---|
| `\l` | List databases |
| `\c db_name` | Connect to a different database |
| `\dt` | List tables in the current schema |
| `\dt *.*` | List tables in all schemas |
| `\d table_name` | Describe a table (columns, types, keys, constraints) |
| `\d+ table_name` | Describe with extra detail |
| `\dn` | List schemas |
| `\du` | List roles |
| `\conninfo` | Show how you are connected |
| `\x` | Toggle expanded display (useful for wide rows) |
| `\timing` | Show how long each query takes |
| `\i file.sql` | Run a SQL file from within psql |
| `\copy ...` | Import or export a file (see section 7) |
| `\password` | Set your role's password |
| `\?` | Help for backslash commands |
| `\h CREATE TABLE` | Help for an SQL command |
| `\q` | Quit |

### Prompt meanings

- `fpl=#` ready for a command (`#` means superuser).
- `fpl=>` ready for a command (regular role).
- `fpl-#` psql thinks a statement is unfinished. Type `;` or press `Ctrl+C` to reset.

---

## 7. Loading CSV files

### Recommended workflow

1. Create the target table.
2. Load the raw CSV into a **staging table** where every column is `TEXT`, so nothing fails on import.
3. Check the data, for example that names match your reference tables.
4. Copy from staging into the real table with `INSERT ... SELECT`, converting types and swapping names for IDs.
5. Run sanity checks, then `TRUNCATE` the staging table.

### The `\copy` command

```
\copy table_name (col1, col2) FROM '/full/path/to/file.csv' WITH (FORMAT csv, HEADER true)
```

- List the columns in the same order as the CSV fields. You can leave out the column list only if the CSV matches the table exactly.
- Leave out columns the database fills itself, such as an identity `id`.
- `HEADER true` skips the first line. Use `false` if the file has no header.
- Use a full path. `~` is not expanded inside the quotes.

### `\copy` versus `COPY`

- `\copy` is a psql command. The **client** reads the file and sends it to the server, so it works with files in your home folder.
- `COPY` runs on the **server**, which reads the file as the `postgres` Linux user. That usually fails on files in your home directory because of permissions.

### Import in DBeaver

Right-click the table, choose **Import Data**, select CSV, then check that columns are mapped correctly and nothing is mapped to an auto-generated `id`.

### Handy table features

```sql
id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY   -- auto-numbered ID
name TEXT NOT NULL UNIQUE                              -- required and no duplicates
team_id INTEGER REFERENCES teams (id)                  -- foreign key
CHECK (gameweek BETWEEN 1 AND 38)                      -- custom rule
PRIMARY KEY (season, gameweek, team_id)                -- composite key
```

### Useful maintenance statements

```sql
TRUNCATE table_name;                           -- remove all rows, keep the table
TRUNCATE table_name RESTART IDENTITY;          -- also reset the ID counter
DROP TABLE table_name;                         -- delete the table entirely
```

### Check queries: empty result means healthy

```sql
-- names in staging with no match in the reference table
SELECT s.squad
FROM staging_standings s
LEFT JOIN teams t ON t.name = s.squad
WHERE t.id IS NULL;

-- points should equal 3*won + drawn
SELECT * FROM standings WHERE points <> 3 * won + drawn;
```

---

## 8. Running SQL scripts

Write SQL in any editor (Sublime, DBeaver, Notepad) and save it as `script.sql`. An editor only holds the text. A client runs it.

```bash
psql -d db_name -f script.sql
```

In DBeaver, press `Ctrl+Enter` to run the current statement, or `Alt+X` to run the whole script. Saved scripts live in `~/.local/share/DBeaverData/workspace6/General/Scripts/`.

Save any statements you repeat (for example a weekly `INSERT ... SELECT`) as a script.

---

## 9. Backup and restore

```bash
pg_dump db_name > backup.sql                 # export one database as SQL
pg_dump -Fc db_name > backup.dump            # compressed custom format
psql -d new_db -f backup.sql                 # restore from a SQL dump
pg_restore -d new_db backup.dump             # restore from a custom-format dump
pg_dumpall > everything.sql                  # whole cluster, including roles
```

Restore into an empty database (`createdb new_db` first). Keep your original CSV files too, since they let you rebuild from scratch.

---

## 10. Connecting with DBeaver

| Field | Value |
|---|---|
| Host | `localhost` |
| Port | `5432` |
| Database | your database name |
| Username | your role name |
| Password | the one set with `\password` |

DBeaver is just a client. It stores only connection settings, scripts, and drivers (under `~/.local/share/DBeaverData`). Your data stays in the server's data directory.

Test the connection first from a terminal. If this works, DBeaver will work:

```bash
psql -h localhost -p 5432 -U "$USER" -d db_name
```

---

## 11. Common errors

| Error | Likely cause and fix |
|---|---|
| `role "x" does not exist` | The role has not been created, or its name does not match your Linux username. Create it, or use `-U`. |
| `database "x" does not exist` | Create it with `createdb`, or check the spelling with `psql -l`. |
| `Peer authentication failed` | Connecting over the socket as a different Linux user than the role. Use `sudo -u postgres psql`, or connect with `-h localhost`. |
| `Connection refused` | The server is not running. Check `pg_lsclusters` and `sudo systemctl start postgresql`. |
| `password authentication failed` | Wrong password. Reset it with `\password`. |
| `duplicate key value violates unique constraint` | You are inserting a row that already exists, or the CSV has duplicates. |
| `null value in column ... violates not-null constraint` | A blank cell, or columns mapped in the wrong order. |
| `cannot insert a non-DEFAULT value into column "id"` | Your import includes an `ALWAYS` identity column. Leave `id` out. |
| `permission denied` on `COPY` | The server cannot read your file. Use `\copy` instead. |
| `insert or update violates foreign key constraint` | A value points to a row that does not exist in the referenced table. Add that row first. |