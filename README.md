# goit-pycore-hw-07

Assistant bot with an address book: contacts, phones and birthdays.

## Setup

The bot needs `colorama`.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

From the repo root:

```bash
python main.py
```

## Commands

| Command                                 | Description                                                                         |
|-----------------------------------------|-------------------------------------------------------------------------------------|
| `hello`                                 | Greeting                                                                            |
| `add <name> [phone]`                    | Add a new contact, or add a phone to an existing one (phone is optional, 10 digits) |
| `change <name> <old_phone> <new_phone>` | Replace a phone of a contact                                                        |
| `phone <name>`                          | Show the phones of a contact                                                        |
| `all`                                   | Show all contacts                                                                   |
| `add-birthday <name> <DD.MM.YYYY>`      | Set the birthday of a contact                                                       |
| `show-birthday <name>`                  | Show the birthday of a contact                                                      |
| `birthdays`                             | Show who to congratulate during the next week (weekend birthdays move to Monday)    |
| `close` / `exit`                        | Exit the bot                                                                        |

## Structure

- `main.py` — entry point, request-response loop
- `bot.py` — command handlers and the `ACTIONS` table
- `database/` — `Field`, `Name`, `Phone`, `Birthday`, `Record`, `AddressBook`
- `utils/` — `input_error` decorator
