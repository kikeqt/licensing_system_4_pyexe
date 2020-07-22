from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from os.path import exists
from id_hardware import Id_Hardware

from license_verifier import License_Verifier


class Signer(License_Verifier):
    def __generate_keys(self):
        if not exists(self._public_key_file):
            self._add_2_status("Generating keys")
            # Randomly generated key
            key = RSA.generate(2048)
            private_key = key.export_key()
            public_key = key.publickey().export_key()
            
            with open(self._public_key_file, "wb") as file_out:
                file_out.write(public_key)
            
            # We protect the private key
            data = private_key
            length = 16 - (len(data) % 16)
            data += bytes([length])*length
            
            ciphertext = self._cipher.encrypt(data)

            with open(self._private_key_file, "wb") as file_out:
                file_out.write(ciphertext)
                
            self._add_2_status("\tSuccessfully")
    
    def _load_key_files(self):
        super()._load_key_files()
        
        self._add_2_status("Loading private key")
        
        with open(self._private_key_file, "rb") as file:
            ciphertext = file.read()
            data = self._cipher.decrypt(ciphertext)
            data = data[: -data[-1]]
            private_key = data
            self._private_key = private_key.decode()
            
        self._add_2_status("\tSuccessfully")
    
    def __make_license_file(self):
        if not exists(self._license_file):
            self._add_2_status("Building license file")
            rsa_key = RSA.importKey(self._private_key)
            signer = PKCS1_v1_5.new(rsa_key)
            
            data = self._id_hardware.__str__().encode()
            digest = SHA256.new(b64encode(data))
            
            signature = b64encode(signer.sign(digest))
            
            with open(self._license_file, "w") as file_out:
                file_out.write(signature.decode())
        
            if self.check_license():
                self._add_2_status("\tSuccessfully")
            
            else:
                self._add_2_status(
                    "\tFatal error: License cannot be validatedy")
    
    def __init__(self, key_to_the_file):
        print('Constructor de signer')
        self._config(key_to_the_file)
        
        self._cipher = AES.new(self._key_file.digest(),
                               AES.MODE_OCB, nonce=self._nonce)
        self.__generate_keys()
        
        self._cipher = AES.new(self._key_file.digest(),
                               AES.MODE_OCB, nonce=self._nonce)
        self._load_key_files()
        
        self.__make_license_file()
    

if __name__ == '__main__':
    from os import system
    system('erase *.pem')
    system('erase *.lic')
    password = b'Replace this key'
    license = Signer(password)
