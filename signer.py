__version__ = "$Version: 1.0.0"

from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from os.path import exists

from license_verifier import License_Verifier
from locksmith import Locksmith


class Signer(License_Verifier):
    _cipher = None
    _locksmith = None 
    
    def __init__(self, key_to_the_file, external_object=None):
        # We pass the object for communication with graphic interface
        self._external_object = external_object
        
        super()._config()

        self._locksmith = Locksmith()
        
        # BEGIN Illustrative example, but you should enter the public and private
        # variables directly in the self._public_key and self._private_key
        if exists(self._public_key_file):
            self._load_key_files()
        
        else:
            self.__generate_keys(key_to_the_file)
        # END Illustrative example
        
        # I recommend this way
        # self._locksmith.set_public_key = b'-----BEGIN RSA PRIVATE KEY-----\n...'
        # self._private_key = Here you should enter the contents of the crypt private key'
        
        self.__make_license_file(key_to_the_file)
    
    def __generate_keys(self, key_to_the_file):
        if not exists(self._public_key_file):
            self._add_2_status("Generating keys")

            self._locksmith.build_keys(key_to_the_file)
            
            self._locksmith.save_private_key(self._private_key_file)
            self._locksmith.save_public_key(self._public_key_file)
            
            self._add_2_status("\tSuccessfully")
    
    def _load_key_files(self):
        super()._load_key_files()
        
        self._add_2_status("Loading private key")
        
        self._locksmith.load_private_key(self._private_key_file)
            
        self._add_2_status("\tSuccessfully")
    
    def __make_license_file(self, key_to_the_file):
        if not exists(self._license_file):
            self._add_2_status("Building license file")
            private_key = self._locksmith.decrypt_private_key(key_to_the_file)
            
            try:
                rsa_key = RSA.importKey(private_key)
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
                        "\tFatal error: License cannot be validated")
            except:
                self._add_2_status("\tWrong key")
        else:
            self._add_2_status("Error: The license file already exists")
    

if __name__ == '__main__':
    # BEGIN Debug. This section is for debugging only
    from os import system
    system('cls')
    system('erase *.pem')
    system('erase *.lic')
    # END Debug
    
    # You should enter this value in some other way, but this is just for example
    password = 'Replace this key'
    
    license_maker = Signer(password)
