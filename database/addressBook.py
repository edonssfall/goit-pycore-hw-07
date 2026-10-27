from collections import UserDict
from datetime import datetime, timedelta

from .core import Name
from .record import Record


class AddressBook(UserDict):
    """
    address book: records stored in self.data by contact name
    """
    data: dict[Name, Record]

    def add_record(self, rec: Record) -> None:
        """
        add a record to the address book (overwrites a record with the same name)
        :param rec: Record
        """
        self.data[rec.name] = rec

    def find(self, name: str) -> Record | None:
        """
        find a record by name
        :param name: contact name: str
        :return: Record, or None if not found
        """
        if rec := self.data.get(name):
            return rec
        return None

    def delete(self, name: str):
        """
        delete a record by name
        :param name: contact name: str
        :return: deleted Record, or None if not found
        """
        if record := self.find(name):
            self.data.pop(record.name)
            return record
        return None

    def get_upcoming_birthdays(self, today=datetime.today().date(), days: int = 7) -> list[
        dict[str, str]]:
        """
        contacts with a birthday in the next `days` days; weekend ones move to Monday,
        on Monday the past weekend ones are congratulated too. Contacts without a birthday are skipped.
        :param today: date to count from (default is evaluated once, at import)
        :param days: window length, today included
        :return: [{"name": <Name>, "congratulation_date": <DD.MM.YYYY>}, ...]
        """
        res = list()

        for user in self.data.values():
            if user.birthday:
                for year in (today.year - 1, today.year, today.year + 1):
                    birthday_year = user.birthday.replace_year(year)

                    in_window = birthday_year >= today and 0 <= (birthday_year - today).days < days

                    past_weekend = today.weekday() == 0 and -2 <= (birthday_year - today).days < 0

                    if in_window or past_weekend:
                        bday = birthday_year + timedelta(
                            days=7 - birthday_year.weekday()) if birthday_year.weekday() >= 5 else birthday_year
                        res.append({
                            'name': user.name,
                            'congratulation_date': datetime.strftime(bday, user.birthday.FORMAT),
                        })
        return res
