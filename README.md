# Telegram Session Keeper CLI

A CLI tool that lets you log into a Telegram account and store the session so that a verification code can be retrieved later for logging into the same account on another device.

# How to use

## Create Telegram credentials

- Login at [my.telegram.org](https://my.telegram.org)
- Create an app at [my.telegram.org/apps](https://my.telegram.org/apps)
- Copy "App api_id" and "App api_hash"

## Environment variables

| Variable    | Required | Type   | Default     | Description                          |
|-------------|----------|--------|-------------|--------------------------------------|
| `api_id`    | yes      | int    | —           | Telegram App API ID                  |
| `api_hash`  | yes      | str    | —           | Telegram App API hash                |
| `db_path`   | no       | str    | `db.csv`    | Path to the session database file    |
| `log_level` | no       | str    | `WARNING`   | Python logging level                 |

`api_id` and `api_hash` have no default and must always be supplied.

## Run

### In Docker

Pull and run the published image `deusalex/telegram-session-keeper-cli`.
All examples below mount `$(pwd)/data` on the host to `/app/src/data` inside the container and set `db_path=data/db.csv` so the session database is persisted on the host.

#### create — log in and save (or display) a session

> **Important:** you must pass `-it` so Docker forwards stdin. Without it the container hangs waiting for the Telegram verification code that is sent to your device.

```shell
docker run -it --rm \
  -e api_id=<App api_id> \
  -e api_hash=<App api_hash> \
  -e db_path=data/db.csv \
  -v $(pwd)/data:/app/src/data \
  deusalex/telegram-session-keeper-cli \
  cli create -p <phone> -a save
```

Use `-a display` instead of `-a save` to print the raw session string instead of writing it to the database:

```shell
docker run -it --rm \
  -e api_id=<App api_id> \
  -e api_hash=<App api_hash> \
  -e db_path=data/db.csv \
  -v $(pwd)/data:/app/src/data \
  deusalex/telegram-session-keeper-cli \
  cli create -p <phone> -a display
```

#### list — show all saved phone numbers

```shell
docker run --rm \
  -e api_id=<App api_id> \
  -e api_hash=<App api_hash> \
  -e db_path=data/db.csv \
  -v $(pwd)/data:/app/src/data \
  deusalex/telegram-session-keeper-cli \
  cli list
```

#### code — wait for and return a Telegram login code

Use `-t` to control how many seconds to wait for the code (default: 60):

```shell
docker run --rm \
  -e api_id=<App api_id> \
  -e api_hash=<App api_hash> \
  -e db_path=data/db.csv \
  -v $(pwd)/data:/app/src/data \
  deusalex/telegram-session-keeper-cli \
  cli code -p <phone> -t 120
```

#### remove — delete a saved session

```shell
docker run --rm \
  -e api_id=<App api_id> \
  -e api_hash=<App api_hash> \
  -e db_path=data/db.csv \
  -v $(pwd)/data:/app/src/data \
  deusalex/telegram-session-keeper-cli \
  cli remove -p <phone>
```

#### Docker entrypoint extras

The image entrypoint also accepts `shell` and `sleep` as the first argument:

- `shell` — opens an interactive shell inside the container
- `sleep` — keeps the container alive indefinitely (useful for debugging)

### In console

- Clone: `git clone https://github.com/alex-deus/telegram-session-keeper.git`
- Set environment variables:

```shell
export api_id=<App api_id>   # required
export api_hash=<App api_hash>  # required
export db_path=db.csv           # default
```

- Execute: `./telegram_session_keeper/cli.py <command> [args]`
- Keep the file referenced by `db_path` (`db.csv` by default)

## Commands

### create

Logs into the account and either saves the session to the database file or displays the raw session string.

**Options:**

- `-p, --phone` (required): Phone number as digits.
- `-a, --action` (choices: `save`, `display`; default: `save`)

### list

Displays a list of saved phone numbers and their creation timestamps from the database file.

### code

Waits for and returns a Telegram verification code using the session stored in the database file.

**Options:**

- `-p, --phone` (required): Phone number as digits.
- `-t, --timeout` (default: `60`): Seconds to wait for the Telegram login code.

### remove

Removes a session from the database file.

**Options:**

- `-p, --phone` (required): Phone number as digits.
