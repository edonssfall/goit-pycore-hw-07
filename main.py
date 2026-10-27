import sys

from colorama import Fore, init

from database import AddressBook
from bot import ACTIONS, parse_input


def main():
    """
    chatbot entry point: request-response loop; also catches errors outside handlers (empty input, exit, EOF)
    """
    print("Welcome to the assistant bot!")
    book = AddressBook()
    while True:
        try:
            user_input = input("Enter a command: ")
            cmd, *args = parse_input(user_input)

            if handler := ACTIONS.get(cmd):
                print(handler(args, book))

            else:
                print(Fore.RED + 'Invalid command.')
        except EOFError:
            print('\nGood bye!')
            sys.exit()
        except Exception as e:
            print(Fore.RED + f'Error: {e}')


if __name__ == '__main__':
    init(autoreset=True)
    main()
