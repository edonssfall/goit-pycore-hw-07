from .core import Name, Phone, Birthday


class Record:
    """
    contact: a Name, a list of Phone objects and an optional Birthday
    """

    def __init__(self, name: str):
        self.name: Name = Name(name)
        self.phones: list[Phone] = list()
        self.birthday = None

    def __str__(self):
        res = f'Contact name: {self.name.value}'
        if self.phones:
            res += f', phones: {self.get_phones()}'
        return res

    def add_phone(self, phone: str) -> None:
        """
        add a phone to the contact
        :param phone: phone number: str (validated by Phone); raises ValueError if the contact already has it
        """
        if phone in self.phones:
            raise ValueError(f'Phone {phone} is already in contact {self.name}')
        self.phones.append(Phone(phone))

    def get_phones(self) -> str:
        """
        phones of the contact for output
        :return: phones joined with '; ', or a message if the contact has no phones: str
        """
        if self.phones:
            return '; '.join(p.value for p in self.phones)
        return f'No phones by contact {self.name}'

    def find_index(self, phone: str) -> int:
        """
        find the index of a phone in the phones list
        :param phone: phone number: str
        :return: index: int; raises ValueError if the phone is not in the record
        """
        try:
            return self.phones.index(phone)
        except ValueError:
            raise ValueError(f'Phone {phone} is not in record.')

    def edit_phone(self, old: str, new: str) -> str | None:
        """
        replace the old phone with a new one at the same position;
        if the new phone is already in the contact, its other copy is removed (no duplicates)
        :param old: phone number to replace: str
        :param new: new phone number: str (validated by Phone)
        :return: new phone; raises ValueError if the old phone is not found or the new one is invalid
        """
        to_remove = None
        if new in self.phones:
            to_remove = self.find_index(new)

        index = self.find_index(old)
        if index is not None:
            self.phones[index] = Phone(new)
            if not to_remove is None and index != to_remove:
                self.phones.pop(to_remove)
            return new

    def find_phone(self, phone: str) -> Phone:
        """
        find a phone in the contact
        :param phone: phone number: str
        :return: Phone object; raises ValueError if not found
        """
        return self.phones[self.find_index(phone)]

    def remove_phone(self, phone: str) -> Phone:
        """
        remove a phone from the contact
        :param phone: phone number: str
        :return: removed Phone object; raises ValueError if not found
        """
        return self.phones.pop(self.find_index(phone))

    def add_birthday(self, birthday: str):
        """
        set the birthday of the contact (only one, a new value replaces the old one)
        :param birthday: date in format DD.MM.YYYY: str (validated by Birthday)
        """
        self.birthday = Birthday(birthday)
