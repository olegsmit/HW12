phone_book = {}


def input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "Please enter the command in the format 'command name phone'."
        except ValueError as v_error:
            return v_error
        except KeyError as k_error:
            return k_error

    return wrapper


def quit(*args):
    return "Good bye!"


def hello(*args):
    return "How can I help you?"


@input_error
def add(*args):
    name = args[0]
    phone = args[1]
    if name not in phone_book:
        phone_book[name] = phone
    else:
        return f"A contact with the name '{name}' already exists. To change his number, use the command 'change {name} phone'."
    return f"Contact '{name}':'{phone}' added successfully."


@input_error
def phone(*args):
    name = args[0]
    if name in phone_book:
        return f"Contact '{name}' has the number '{phone_book[name]}'."
    else:
        return f"Contact '{name}' it not found."


@input_error
def change_phone(*args):
    name = args[0]
    phone = args[1]
    if name in phone_book:
        phone_book[name] = phone
    else:
        return f"Contact '{name}' not found. Please add the contact '{name}' first using the command 'add {name} phone'."
    return f"Contact '{name}':'{phone}' changed successfully."


def show_all(*args):
    lst = ["{:^10}: {:>10}".format(k, v) for k, v in phone_book.items()]
    return "{:^10}: {:^10}".format("Name", "Phone")+"\n"+"\n".join(lst)


COMMANDS = {quit: ["good bye", "close", "exit"],
            hello: ["hello"],
            add: ["add"],
            phone: ["phone"],
            change_phone: ["change"],
            show_all: ["show all"]
            }


def parse_command(user_input: str):
    for k, v in COMMANDS.items():
        for i in v:
            if user_input.lower().startswith(i.lower()):
                return k, tuple(user_input[len(i):].title().strip().split(" "))


def main():
    while True:
        user_input = input(">>>")
        if user_input == ".":
            break
        try:
            result, data = parse_command(user_input)
            print(result(*data))
            if result is quit:
                break
        except TypeError:
            print("Command not found.")


if __name__ == "__main__":
    main()
