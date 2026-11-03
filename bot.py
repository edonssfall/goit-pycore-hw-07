from colorama import Fore

from database import AddressBook, Record
from utils import input_error, validate_args


class Bot:
    """
    assistant bot: keeps the AddressBook and runs commands on it
    """

    def __init__(self):
        self.book: AddressBook = AddressBook()
        self.actions = {
            'hello': self.hello,
            'add': self.add_contact,
            'change': self.change_contact,
            'phone': self.show_phone,
            'all': self.show_all,
            'add-birthday': self.add_birthday,
            'show-birthday': self.show_birthday,
            'birthdays': self.birthdays,
            'close': self.end,
            'exit': self.end
        }

    def __call__(self, *args, **kwargs):
        """
        run one user command: parse the input and call the matching handler
        :return: answer to print, or 'Invalid command.' for an unknown command
        """
        cmd, *args = self.parse_input(*args, **kwargs)

        if handler := self.actions.get(cmd):
            return handler(args)

        else:
            return Fore.RED + 'Invalid command.'

    @input_error
    @validate_args(args_count=[1, 2], usage='Usage: add <name> <phone<optional>>')
    def add_contact(self, args: list) -> str:
        """
        command `add [name] [phone]`: create a new contact or add a phone to an existing one
        :param args: [name] or [name, phone]: list[str]; phone is optional
        :return: answer to print; wrong number of args or an invalid phone (ValueError) are handled by input_error
        """
        if len(args) == 2:
            name, phone = args
        else:
            name, phone = args[0], None

        record = self.book.find(name)
        message = "Contact updated."
        if record is None:
            record = Record(name)
            self.book.add_record(record)
            message = "Contact added."
        if phone:
            record.add_phone(phone)
        return message

    @input_error
    @validate_args(args_count=[3], usage='Usage: change <name> <old_phone> <new_phone>')
    def change_contact(self, args: list) -> str | None:
        """
        command `change [name] [old phone] [new phone]`: replace a phone of an existing contact
        :param args: [name, old_phone, new_phone, ...]: list[str]
        :return: answer to print; a missing contact (KeyError), a missing old phone or an invalid new one (ValueError)
            are handled by input_error
        """
        name, old_phone, new_phone = args
        if record := self.book.find(name):
            record.edit_phone(old_phone, new_phone)
            return 'Contact updated.'
        raise KeyError

    @input_error
    @validate_args(args_count=[1], usage='Usage: phone <name>')
    def show_phone(self, args: list) -> str:
        """
        command `phone [name]`: show all phones of a contact
        :param args: [name, ...]: list[str]
        :return: phones joined with '; ' (or a message if there are none);
            raises KeyError if the contact is not found (handled by input_error)
        """
        if rec := self.book.find(args[0]):
            return rec.get_phones()
        raise KeyError

    @input_error
    @validate_args(args_count=[2], usage='Usage: add-birthday <name> <DD.MM.YYYY>')
    def add_birthday(self, args: list) -> str:
        """
        command `add-birthday [name] [DD.MM.YYYY]`: set the birthday of a contact
        :param args: [name, birthday, ...]: list[str]
        :return: answer to print; a missing contact (KeyError) and an invalid date (ValueError) are handled by input_error
        """
        name, birthday = args
        if record := self.book.find(name):
            record.add_birthday(birthday)
            return "Birthday added."
        raise KeyError

    @input_error
    @validate_args(args_count=[1], usage='Usage: show-birthday <name>')
    def show_birthday(self, args: list) -> str:
        """
        command `show-birthday [name]`: show the birthday of a contact
        :param args: [name, ...]: list[str]
        :return: birthday (DD.MM.YYYY); a missing contact (KeyError) or a contact without a birthday (ValueError)
            are handled by input_error
        """
        if rec := self.book.find(args[0]):
            if rec.birthday:
                return str(rec.birthday)
            raise ValueError('Birthday not found.')
        raise KeyError

    @input_error
    def birthdays(self, *_):
        """
        command `birthdays`: show contacts to congratulate during the next week
        :param _: command args (not used)
        :return: one line '<name>: <congratulation date>' per contact, or a message if there are none
        """
        if bdays := self.book.get_upcoming_birthdays():
            return '\n'.join([f'{rec["name"]}: {rec["congratulation_date"]}' for rec in bdays])
        return f'No birthdays found for a week.'

    @input_error
    def show_all(self, *_) -> str:
        """
        command `all`: show all contacts of the address book, if there are any
        :param _: command args (not used)
        :return: answer to print
        """
        if self.book:
            return ''.join(
                f"{Fore.BLUE if i % 2 == 0 else Fore.YELLOW}{record}\n"
                for i, record in enumerate(self.book.values())
            ).rstrip()
        return 'Nothing to show, because DB is empty.'

    @staticmethod
    @input_error
    def hello(*_):
        """
        command `hello`: greet the user
        :return: greeting
        """
        return 'How can I help you?'

    @staticmethod
    @input_error
    def end(*_):
        """
        commands `close` / `exit`: stop the bot; raises EOFError, main prints "Good bye!" and exits
        """
        raise EOFError

    @staticmethod
    def parse_input(user_input: str) -> tuple[str, ...]:
        """
        split user input into a command (lowercase) and its args
        :param user_input: user input
        :return: (command: str, *args); raises IndexError for empty input (handled in main)
        """
        if not user_input.strip():
            raise IndexError('Please enter a command.')
        cmd, *args = user_input.split()
        cmd = cmd.strip().lower()
        return cmd, *args
