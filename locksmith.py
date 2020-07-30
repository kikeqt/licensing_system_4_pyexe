__version__ = "$Version: 0.0.1"

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


class Locksmith(object):
    """Build and protect public key cryptography keys"""
    _private_key = None
    _public_key = None


    def __init__(self):
        pass


    def build_keys(self, key_4_private_key: str):
        key = RSA.generate(2048)
        self._private_key = key.export_key()
        self._public_key = key.publickey().export_key()

        # We protect the private key
        data = self._private_key
        length = 16 - (len(data) % 16)
        data += bytes([length])*length

        key_file = SHA256.new()
        key_file.update(key_4_private_key.encode())
        nonce = key_file.digest()[:15]
        
        cipher = AES.new(key_file.digest(), AES.MODE_OCB, nonce=nonce)
        self._private_key = cipher.encrypt(data)
    
    
    @property
    def get_public_key(self):
        return self._public_key

    
    @property
    def get_private_key(self):
        return self._private_key


    def decrypt_private_key(self, key_4_private_key: str):
        key = SHA256.new()
        key.update(key_4_private_key.encode())
        nonce = key.digest()[:15]

        cipher = AES.new(key.digest(), AES.MODE_OCB, nonce=nonce)

        data = cipher.decrypt(self._private_key)
        return data[: -data[-1]]


    def load_private_key(self, private_key_file_name: str="private.pem"):
        with open(private_key_file_name, "rb") as file:
            self._private_key = file.read()

    
    def load_public_key(self, public_key_file_name: str="public.pem"):
        with open(public_key_file_name, "rb") as file:
            public_key = file.read()
            self._public_key = public_key.decode()


    def save_private_key(self, private_key_file_name: str="private.pem"):
        with open(private_key_file_name, "wb") as file_out:
            file_out.write(self._private_key)


    def save_public_key(self, public_key_file_name: str="public.pem"):
        with open(public_key_file_name, "wb") as file_out:
            file_out.write(self._public_key)



if __name__ == "__main__":
    from os import remove
    from os.path import exists

    key = '01234567'
    private_key_file_name = 'locksmith_private.pem'
    public_key_file_name = 'locksmith_public.pem'

    if exists(private_key_file_name):
        remove(private_key_file_name)

    if exists(public_key_file_name):
        remove(public_key_file_name)

    locksmith = Locksmith()
    locksmith.build_keys(key)

    locksmith.save_private_key(private_key_file_name)
    locksmith.save_public_key(public_key_file_name)

    locksmith.load_private_key(private_key_file_name)
    locksmith.load_public_key(public_key_file_name)

    print(locksmith.decrypt_private_key(key))