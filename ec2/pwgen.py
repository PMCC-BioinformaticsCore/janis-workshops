def gen_password(min_length=12):

    if len(lines) < 10:
        raise Exception(
            "Couldn't generate a password, you should fill in a list of possible words within this script"
        )

    from random import randint

    seen = set()

    def generate_word():
        idx = None
        while idx is None or idx in seen:
            idx = randint(0, len(lines))
        seen.add(idx)
        return lines[idx]

    password = "-".join(generate_word() for _ in range(3))
    while len(password) < min_length:
        password += "-" + generate_word()

    return password


lines = []

if __name__ == "__main__":
    print(gen_password())
