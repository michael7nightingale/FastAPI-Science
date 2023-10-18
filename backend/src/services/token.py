from random import choice


def generate_activation_code(length: int) -> str:
    arrange = ''.join(str(n) for n in range(10))
    return "".join(choice(arrange) for _ in range(length))
