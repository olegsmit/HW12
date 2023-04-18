from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value: str) -> None:
        self.value = value


class Name(Field):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone) -> None:
        super().__init__(phone)


class Birthday(Field):
    def __int__(self, birthday) -> None:
        super().__int__(birthday)

class Record:
    def __init__(self, name: Name, phone: list, birthday: Birthday = None):
        self.name = name
        self.phone = phone
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phone.append(phone)

    def del_phone(self, phone: Phone):
        for ph in self.phone:
            if phone.value == ph.value:
                self.phone.remove(ph)

    def edit_phone(self, old_phone: Phone, new_phone: Phone):
        self.del_phone(old_phone)
        self.add_phone(new_phone)

    def days_to_birthday(self):
        pass

    def __repr__(self):
        return f"{self.name.value}: {[ph.value for ph in self.phone]}"


class AddressBook(UserDict):
    def add_user(self, record: Record):
        self.data[record.name.value] = record

    def show_phone(self, name: Name):
        return [n.value for n in self.data[name].phone]

    def iterator(self):
        pass


phone_book = AddressBook()



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
    if args[0] not in phone_book:
        name = Name(args[0])
        phones = []
        for ph in args[1:]:
            phones.append(Phone(ph))
        rec = Record(name, phones)
        phone_book.add_user(rec)
    else:
        return f"A contact with the name '{args[0]}' already exists. To change his number, use the command 'change {args[0]} phone'."
    return f"Contact '{args[0]}':'{args[1]}' added successfully."


@input_error
def show_phone(*args):
    return phone_book.show_phone(args[0])

@input_error
def add_phone(*args):
    phone_book[args[0]].add_phone(Phone(args[1]))
    return f"For user {args[0]} add phone {args[1]}"

@input_error
def del_phone(*args):
    phone_book[args[0]].del_phone(Phone(args[1]))
    return f"For user {args[0]} del phone {args[1]}"


@input_error
def change_phone(*args):
    phone_book[args[0]].edit_phone(Phone(args[1]), Phone(args[2]))
    return f"Contact '{args[0]}' changed phone '{args[2]}' successfully."


def show_all(*args):
    lst = ["{:^10}: {:>10}".format(k, str(v)) for k, v in phone_book.items()]
    return "{:^10}: {:^10}".format("Name", "Phones") + "\n" + "\n".join(lst)


COMMANDS = {quit: ["good bye", "close", "exit"],
            hello: ["hello"],
            add_phone: ["add phone"],
            del_phone: ["del phone"],
            add: ["add"],
            change_phone: ["change"],
            show_all: ["show all"],
            show_phone: ["phone"]
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