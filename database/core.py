import re

from datetime import datetime


class Field:
    """
    base class for record fields; value must not be empty
    """

    def __init__(self, value):
        if not value:
            raise ValueError('Value must be provided.')
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, value: object, /) -> bool:
        """
        compare by value, so a field equals its plain string (e.g. Name('John') == 'John')
        """
        return self.value == value

    def __hash__(self) -> int:
        return hash(self.value)


class Name(Field):
    """
    contact name (required)
    """
    pass


class Phone(Field):
    """
    phone number: exactly 10 digits
    """
    FORMAT = r'^\d{10}'

    def __init__(self, value):
        """
        validate the phone: exactly 10 digits, otherwise raise ValueError
        """
        if not re.fullmatch(self.FORMAT, value):
            raise ValueError('Phone must be correct: 10 numbers.')
        super().__init__(value)

    def __str__(self) -> str:
        return str(self.value)


class Birthday(Field):
    """
    birthday: parsed from 'DD.MM.YYYY' and stored as a date
    """
    FORMAT = '%d.%m.%Y'

    def __init__(self, value):
        """
        validate the date format and convert the string to a date, otherwise raise ValueError
        :param value: birthday in format DD.MM.YYYY: str
        """
        try:
            value = datetime.strptime(value, self.FORMAT).date()
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self) -> str:
        """
        show the birthday in the same format the user enters it: DD.MM.YYYY
        """
        return datetime.strftime(self.value, self.FORMAT)
