import random
import string

def api_gen():
    api_key = ""
    for i in range(32):
        api_key += random.choice(string.ascii_letters + string.digits)
    return api_key

print(api_gen())
