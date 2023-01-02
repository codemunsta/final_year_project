import random
import string


def generate_password(length):
    letters = string.ascii_uppercase
    result_caps = ''.join(random.choice(letters) for i in range(3))
    letters = string.punctuation
    result_special = ''.join(random.choice(letters))
    letters = string.ascii_letters + string.digits
    result_lower = ''.join(random.choice(letters) for i in range(length - 3))
    result = result_caps + result_special + result_lower
    return result

