from datetime import datetime

from colorama import Fore

from database import AddressBook, Record
from utils import input_error


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """
    command `add [name] [phone]`: create a new contact or add a phone to an existing one
    :param args: [name] or [name, phone]: list[str]; phone is optional
    :param book: AddressBook
    :return: answer to print; wrong number of args or an invalid phone (ValueError) are handled by input_error
    """
    name, phone = None, None
    match len(args):
        case 0:
            raise ValueError('Need minimum 1 argument.\nUsage: add <name> <phone<optional>>')
        case 1:
            name = args[0]
        case 2:
            name, phone = args
        case _:
            raise ValueError('Need maximum 2 arguments.\nUsage: add <name> <phone<optional>>')

    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args: list, book: AddressBook) -> str | None:
    """
    command `change [name] [old phone] [new phone]`: replace a phone of an existing contact
    :param args: [name, old_phone, new_phone, ...]: list[str]
    :param book: AddressBook
    :return: answer to print; a missing contact (KeyError), a missing old phone or an invalid new one (ValueError)
        are handled by input_error
    """
    try:
        name, old_phone, new_phone, *_ = args
    except ValueError:
        raise ValueError('Need 3 arguments.\nUsage: change <name> <old_phone> <new_phone>')
    if record := book.find(name):
        record.edit_phone(old_phone, new_phone)
        return 'Contact updated.'
    raise KeyError


@input_error
def show_phone(args: list, book: AddressBook) -> str:
    """
    command `phone [name]`: show all phones of a contact
    :param args: [name, ...]: list[str]
    :param book: AddressBook
    :return: phones joined with '; ' (or a message if there are none);
        raises KeyError if the contact is not found (handled by input_error)
    """
    try:
        name, *_ = args
    except ValueError:
        raise ValueError('Need 1 argument.\nUsage: phone <name>')
    if rec := book.find(name):
        return rec.get_phones()
    raise KeyError


@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    """
    command `add-birthday [name] [DD.MM.YYYY]`: set the birthday of a contact
    :param args: [name, birthday, ...]: list[str]
    :param book: AddressBook
    :return: answer to print; a missing contact (KeyError) and an invalid date (ValueError) are handled by input_error
    """
    try:
        name, birthday, *_ = args
    except ValueError:
        raise ValueError('Need 2 arguments.\nUsage: add-birthday <name> <DD.MM.YYYY>')
    if record := book.find(name):
        record.add_birthday(birthday)
        return "Birthday added."
    raise KeyError


@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    """
    command `show-birthday [name]`: show the birthday of a contact
    :param args: [name, ...]: list[str]
    :param book: AddressBook
    :return: birthday (DD.MM.YYYY); a missing contact (KeyError) or a contact without a birthday (ValueError)
        are handled by input_error
    """
    try:
        name, *_ = args
    except ValueError:
        raise ValueError('Need 1 argument.\nUsage: show-birthday <name>')

    if rec := book.find(name):
        if rec.birthday:
            return str(rec.birthday)
        raise ValueError('Birthday not found.')
    raise KeyError


@input_error
def birthdays(_, book: AddressBook):
    """
    command `birthdays`: show contacts to congratulate during the next week
    :param _: command args (not used)
    :param book: AddressBook
    :return: one line '<name>: <congratulation date>' per contact, or a message if there are none
    """
    if bdays := book.get_upcoming_birthdays(today=datetime.today().date()):
        return '\n'.join([f'{rec["name"]}: {rec["congratulation_date"]}' for rec in bdays])
    return f'No birthdays found for a week.'


@input_error
def show_all(_, book: AddressBook) -> str:
    """
    command `all`: show all contacts of the address book, if there are any
    :param _: command args (not used)
    :param book: AddressBook
    :return: answer to print
    """
    if book:
        return ''.join(
            f"{Fore.BLUE if i % 2 == 0 else Fore.YELLOW}{record}\n"
            for i, record in enumerate(book.values())
        ).rstrip()
    return 'Nothing to show, because DB is empty.'


@input_error
def hello(*_):
    """
    command `hello`: greet the user
    :return: greeting
    """
    return 'How can I help you?'


@input_error
def end(*_):
    """
    commands `close` / `exit`: stop the bot; raises EOFError, main prints "Good bye!" and exits
    """
    raise EOFError


def parse_input(user_input: str) -> tuple[str, list]:
    """
    split user input into a command (lowercase) and its args
    :param user_input: user input
    :return: (command: str, *args); raises Exception for empty input (handled in main)
    """
    if not user_input.strip():
        raise Exception('Please enter a command.')
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


ACTIONS = {
    'hello': hello,
    'add': add_contact,
    'change': change_contact,
    'phone': show_phone,
    'all': show_all,
    'add-birthday': add_birthday,
    'show-birthday': show_birthday,
    'birthdays': birthdays,
    'close': end,
    'exit': end
}
