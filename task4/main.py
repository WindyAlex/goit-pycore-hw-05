def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the argument for the command"
    return inner


def parse_input(user_input: str):
    cmd, *args = user_input.split()
    if not cmd:
        return "", []
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    if len(args) < 2:
        raise ValueError("Please use input standart: add [name] [phone]")
    name, phone = args[0], args[1]

    if not name.isalpha():
        raise ValueError("Name contains not only letters")

    if phone.startswith("+"):
        phone = phone[1:]
    if not phone.isdigit():
        raise ValueError("Phone number contains not only digits")
    phone = "+" + phone

    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) < 2:
        raise ValueError("Please use input standart: change [name] [phone]")
    name, phone = args[0], args[1]
    if name not in contacts:
        return KeyError(name)

    if phone.startswith("+"):
        phone = phone[1:]
    if not phone.isdigit():
        raise ValueError("Phone number contains not only digits")
    phone = "+" + phone

    contacts[name] = phone
    return "Contact updated."


@input_error
def show_phone(args, contacts):
    name = args[0]
    if name not in contacts:
        return KeyError(name)
    return contacts[name]


@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts yet."
    lines = [f"{name}: {phone}" for name, phone in contacts.items()]
    return "\n".join(lines)


def main():
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


main()
