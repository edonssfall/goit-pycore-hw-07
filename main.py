import sys

from colorama import Fore, init

from bot import Bot


def main():
    """
    chatbot entry point: request-response loop; also catches errors outside handlers (empty input, exit, EOF)
    """
    print("Welcome to the assistant bot!")
    bot = Bot()
    while True:
        try:
            user_input = input("Enter a command: ")
            print(bot(user_input))
        except EOFError:
            print('\nGood bye!')
            sys.exit()
        except Exception as e:
            print(Fore.RED + f'Error: {e}')


if __name__ == '__main__':
    init(autoreset=True)
    main()
