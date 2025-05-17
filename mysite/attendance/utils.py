import random
import string

def generate_access_key(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
