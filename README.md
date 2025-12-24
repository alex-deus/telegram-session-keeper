# Telegram Session Keeper CLI

## Commands

### create
- **Options:**
    - `-a, --action` (choices: save, display; default: save)
    - `-p, --phone` (required): Phone number as digits.

### show-list
Displays a list of saved phone numbers and their creation timestamps.

### get-code
- **Options:**
    - `-p, --phone` (required): Phone number as digits.
    - `-t, --timeout` (default: 60): Timeout in seconds to wait for a Telegram login code.

### remove
- **Options:**
    - `-p, --phone` (required): Phone number as digits.
      Removes the session associated with the phone number.
