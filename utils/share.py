from colorama import Fore


def input_error(func):
    """
    decorator for command handlers: turn input errors into a message for the user, so the bot keeps running.
    ValueError shows its own text, KeyError means the contact was not found.
    :param func: command handler
    :return: wrapped function that returns the handler result or an error message
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return Fore.RED + str(e)
        except KeyError:
            return Fore.RED + "Give me existing name."
        except IndexError:
            return Fore.RED + "Give me <command> <name> <phone-optional> please."

    return inner
