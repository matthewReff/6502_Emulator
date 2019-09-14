def prompt_for_input():
    try:
        temp = input("> ")
    except EOFError:
        return False, None
    except KeyboardInterrupt:
        return False, None

    if temp.upper() == "EXIT":
        return False, None

    return True, temp


def main():
    succeeded, input_string = prompt_for_input()
    while succeeded:
        print(input_string)
        print(ord(input_string[0]))
        succeeded, input_string = prompt_for_input()


if __name__ == "__main__":
    main()

