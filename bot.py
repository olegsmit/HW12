from collections import UserDict
from datetime import datetime


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if value.isalpha():
            Field.value.fset(self, value)
        else:
            raise ValueError


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if value.replace("+", "").replace("(", "").replace(")", "").replace("-", "").isdigit():
            Field.value.fset(self, value)
        else:
            raise ValueError


class Birthday(Field):
    def __int__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        try:
            datetime.strptime(value, "%Y/%m/%d")
            Field.value.fset(self, value)
        except:
            Field.value.fset(self, "")


class Record:
    def __init__(self, name: Name, phones: list[Phone] = None, birthday: Birthday = None):
        self.name = name
        self.phone = phones
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
        if self.birthday:
            current_date = datetime.now().date()
            year_cur = current_date.year
            number_day = datetime.strptime(self.birthday.value, "%Y/%m/%d").replace(
                year=year_cur).date() - current_date
            if number_day.days < 0:
                number_day = datetime.strptime(self.birthday.value, "%Y/%m/%d").replace(
                    year=year_cur + 1).date() - current_date
            return f"{number_day.days} to {self.name.value}'s birthday"
        else:
            return "Can't calculate"

    def __repr__(self):
        return f"Name: {self.name.value}, Phone: {[ph.value for ph in self.phone]}, Birthday: {self.birthday.value}"


class AddressBook(UserDict):
    N = 2

    def add_user(self, record: Record):
        self.data[record.name.value] = record

    def show_phone(self, name: Name):
        return [n.value for n in self.data[name].phone]

    def show_all_records(contacts, *args):
        if not contacts:
            return 'Address book is empty'
        result = 'List of all users:\n'
        print_list = contacts.iterator()
        for item in print_list:
            result += f'{item}'
        return result

    def iterator(self):
        index, print_block = 1, '-' * 50 + '\n'
        for record in self.data.values():
            print_block += str(record) + '\n'
            if index < self.N:
                index += 1
            else:
                yield print_block
                index, print_block = 1, '-' * 50 + '\n'
        yield print_block


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


# @input_error
def add(*arg):
    try:
        name = Name(arg[0])
    except ValueError:
        return "Please enter a name"
    phone_list = []
    for ph in arg:
        try:
            phone_list.append(Phone(ph))
        except ValueError:
            continue
    try:
        birthday = Birthday(arg[-1])
    except ValueError:
        birthday = Birthday(None)

    rec = Record(name, phone_list, birthday)
    if rec.name.value not in phone_book:
        phone_book.add_user(rec)
    else:
        return f"A contact with the name '{name.value}' already exists. To change his number, use the command 'change {name.value} phone'."
    return f"Contact '{name.value}' added successfully."


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
    return phone_book.show_all_records(args[0])


@input_error
def d_to_b(*args):
    return phone_book[args[0]].days_to_birthday()


COMMANDS = {quit: ["good bye", "close", "exit"],
            hello: ["hello"],
            add_phone: ["add phone"],
            del_phone: ["del phone"],
            add: ["add"],
            change_phone: ["change"],
            show_all: ["show all"],
            show_phone: ["phone"],
            d_to_b: ["birthday"]
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
