# Telegram Session Keeper CLI
The library allows logging into a Telegram account and storing the session so that it can later be used to obtain a verification code for logging into the same account on another device.

# How to use
## Create Telegram credentials
  - Login at [my.telegram.org](https://my.telegram.org)
  - Create an app at [my.telegram.org/apps](https://my.telegram.org/apps)
  - Copy "App api_id" & "App api_hash"

## Run
### In console
- clone: `git clone https://github.com/alex-deus/telegram-session-keeper.git`
- set envs:
```shell
export api_id=<App api_id>  # required
export api_hash=<App api_hash>  # required
export db_path=db.csv  # default
```
- execute: `./telegram_session_keeper/cli.py <command> [args]`
- keep file `db.csv` (from env `db_path`)

### In a docker
- execute:
```shell
docker run \
  -e api_id=<App api_id> \
  -e api_hash=<App api_hash> \
  -e db_path=data/db.csv \
  -v $(pwd)/data:/app/src/data \
  deusalex/telegram-session-keeper-cli \
  cli <command> [arg]
```
- keep file `data/db.csv`

## Commands
### create
- **Description**: The command allows logging into the account and saves the session to the **db.csv** file.
- **Options:**
  - `-a, --action` (choices: save, display; default: save)
  - `-p, --phone` (required): Phone number as digits.

### list
Displays a list of saved phone numbers and their creation timestamps from the **db.csv** file.

### code
- **Description**: Allows retrieving a verification code using the session stored in the **db.csv** file.
- **Options:**
  - `-p, --phone` (required): Phone number as digits.
  - `-t, --timeout` (default: 60): Timeout in seconds to wait for a Telegram login code.

### remove
- **Description**: Removes the session from the **db.csv** file.
- **Options:**
  - `-p, --phone` (required): Phone number as digits.
