from functools import wraps

from colorama import Fore


def input_error(func):
    """
    decorator for command handlers: turn input errors into a message for the user, so the bot keeps running.
    ValueError and IndexError (wrong number of args) show their own text, KeyError means the contact was not found.
    :param func: command handler
    :return: wrapped function that returns the handler result or an error message
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return Fore.RED + str(e)
        except KeyError:
            return Fore.RED + "Give me existing name."

    return inner


def validate_args(args_count: list[int], usage: str):
    """
    decorator factory for Bot command methods (self, args): check the number of command args
    :param args_count: allowed numbers of args, e.g. [1, 2]
    :param usage: message for a wrong number of args
    :return: decorator; the wrapped method raises IndexError(usage), handled by input_error
    """

    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            _, check_args = args
            if len(check_args) not in args_count:
                raise IndexError(usage)

            return func(*args, **kwargs)

        return wrap

    return decorator
