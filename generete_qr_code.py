import qrcode
import random
import string

def create_password():
    characters = string.digits+string.ascii_letters+string.ascii_lowercase+string.punctuation
    password = ''.join(random.choices(characters,k=15))
    return password

def qrcode_create(data):
    qr = qrcode.make(data)
    qr.save('admin.png')

password = create_password()
qrcode_create(password)

