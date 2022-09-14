
import string
import secrets


valid_email = "27raco@gmail.com"
valid_password = '12345'

num = 256
string_of_256 = str(''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num)))

num_1 = 1000
string_of_1000 = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num_1))

some_numbers = 8764
