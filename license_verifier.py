from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from os.path import exists
from id_hardware import Id_Hardware


class License_Verifier(object):
    _cipher = None
    _key_file = None
    _license_file = ""
    _nonce = None
    _private_key = None
    _private_key_file = "private.pem"
    _public_key = None
    _public_key_file = "public.pem"
    _status = ""
    
    def __init__(self, key_to_the_file):
        print('Constructor de license_verifier')
        self._config(key_to_the_file)
        
        self._cipher = AES.new(self._key_file.digest(), 
                               AES.MODE_OCB, nonce=self._nonce)
        self._load_key_files()
        
    def _config(self, key_to_the_file):
        self._id_hardware = Id_Hardware()
        self._license_file = f'{self._id_hardware.get_hostname.decode()}.lic'

        # Preparing keys
        self._key_file = SHA256.new()
        self._key_file.update(key_to_the_file)
        self._nonce = self._key_file.digest()[:15]
    
    def _add_2_status(self, message):
        # Module for communication with graphic interface
        print(message)
        self._status += message
        
    def _load_key_files(self):
        self._add_2_status("Loading public key")

        with open(self._public_key_file, "rb") as file:
            public_key = file.read()
            self._public_key = public_key.decode()

        self._add_2_status("\tSuccessfully")

    def check_license(self):
        if exists(self._license_file):
            self._add_2_status("Checking license")
            license = None

            with open(self._license_file, "r") as file:
                license = file.read()
            
            license = license.encode()
            
            data = self._id_hardware.__str__().encode()

            rsa_key = RSA.importKey(self._public_key)
            signer = PKCS1_v1_5.new(rsa_key)
            digest = SHA256.new(b64encode(data))

            if signer.verify(digest, b64decode(license)):
                self._add_2_status("\tValid license")
                return  True
            
            else:
                self._add_2_status("\tInvalid license")
                return False

        else:
            self._add_2_status("You do not have a valid license")
            return False


if __name__ == '__main__':
    password = b'Replace this key'
    license = License_Verifier(password)
    
    if license.check_license():
        print('Licencia valida')
        
    else:
        print('Licencia no válida')
