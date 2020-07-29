__version__ = "$Version: 0.0.1"

from base64 import b64encode
from base64 import b64decode
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from datetime import datetime
from os.path import exists
import tkinter as tk

from id_hardware import Id_Hardware


class License_Verifier(object):
    
    _key_file = None
    _license_file = ""
    _nonce = None
    _private_key = None
    _private_key_file = "private.pem"
    _public_key = None
    _public_key_file = "public.pem"
    _status = ""
    _external_object = None
    
    def __init__(self, external_object=None):
        # We pass the object for communication with graphic interface
        self._external_object = external_object
        
        self._config()
        
        # Illustrative example, but you should enter the public key directly in
        # the variable self._public_key
        self._load_key_files()
        # I recommend this way
        # self._public_key = b'Here you should enter the contents of the public key'
    
    def _config(self):
        self._id_hardware = Id_Hardware()
        self._license_file = f'{self._id_hardware.get_hostname.decode()}.lic'
    
    def _add_2_status(self, message):
        # Module for communication with graphic interface
        type_interface = str(type(self._external_object))
        
        time_stamp = datetime.now().strftime("%y/%m/%d %H:%M:%S.%f")[:-4]
        
        if type_interface == "<class 'NoneType'>":
            print(f"{time_stamp}  {message}")
            
        elif type_interface == "<class 'tkinter.Listbox'>":
            self._external_object.insert(tk.END, f"{time_stamp}  {message}")

        elif type_interface == "<class 'tkinter.Text'>":
            self._external_object.insert(tk.END, f"{time_stamp}  {message}\n")
        
        else:
            print(f'Fatal error: How to use this object {type(self._external_object)}')
            exit()
	
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
    license = License_Verifier()
    
    if license.check_license():
        print('Licencia valida')
        
    else:
        print('Licencia no válida')
