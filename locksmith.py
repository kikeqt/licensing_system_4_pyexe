__version__ = "$Version: 0.1.3"

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


class Locksmith(object):
    """Build and protect public key cryptography keys"""
    _private_key = None
    _public_key = None


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
    
    
    def set_private_key(self, private_key: bytes):
        """Use when your private key is already protected"""
        self._private_key = private_key
    
    
    def set_and_protect_private_key(self, key_4_private_key: str, private_key: bytes):
        # We protect the private key
        data = private_key
        length = 16 - (len(data) % 16)
        data += bytes([length])*length

        key_file = SHA256.new()
        key_file.update(key_4_private_key.encode())
        nonce = key_file.digest()[:15]
        
        cipher = AES.new(key_file.digest(), AES.MODE_OCB, nonce=nonce)
        self._private_key = cipher.encrypt(data)
        
    
    def set_public_key(self, public_key: bytes):
        self._public_key = public_key


    private_key = property(get_private_key, set_private_key)
    public_key = property(get_public_key, set_public_key)


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

    key_2_private_key = '01234567'
    private_key_file_name = 'locksmith_private.pem'
    public_key_file_name = 'locksmith_public.pem'

    # BEGIN Cleaning for example
    if exists(private_key_file_name):
        remove(private_key_file_name)
        print(f'Deleted {private_key_file_name}')

    if exists(public_key_file_name):
        remove(public_key_file_name)
        print(f'Deleted {public_key_file_name}')
    # END Cleaning for example


    locksmith = Locksmith()    

    
    # BEGIN We generate, store and retrieve the keys
    print('\n\nWe generate, store and retrieve the keys')
    locksmith.build_keys(key_2_private_key)

    locksmith.save_private_key(private_key_file_name)
    locksmith.save_public_key(public_key_file_name)

    locksmith.load_private_key(private_key_file_name)
    locksmith.load_public_key(public_key_file_name)

    print('\nWe verify the keys')
    print(locksmith.decrypt_private_key(key_2_private_key))
    print(locksmith.get_public_key)
    # END We generate, store and retrieve the keys
    
    
    # BEGIN We provide the keys and protect the private key at run time
    print('\n\nWe provide the keys and protect the private key at run time')
    locksmith.set_and_protect_private_key(key_2_private_key, b'-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAoyvdbtW5v3dqziewtm6eKAPLvI62OHSmAKYtiOxSMXEBt5Wi\nzvUb6yzKLVoHpm2AA2L5RzXQ6pEHpGSfdgr1+925pSxlIO2/OLIfF86vEJCKWSGX\nYkz292cRX1f8JSv6XzoT71v0GQFJ5Y37W7oNM8jLvzMTYywN0hy2YmA+Mj9iag8w\nkg0PIKb3ZdfrAZ1bSxXCTnC5ap+gi9LweIaD2ekHJK2oX88KA+Ne54g8ygPz6EQv\noUcuwd1p4act/bhjd92xBcDQMY+rITDvIb6RvSGrap0rxQBDMFCDHpAQMWYaJjvP\n9WynJs3snXEmXrdmyumB1b4duXsMG2kbm/v5TQIDAQABAoIBABbuafjy198o3u14\nhfzpeFgaynXmH4U5HYA/Wmxg+98faNSeVqpbp5AKNCKiAau5vVEchnhjv4fLmIWZ\nr5BVE4NRQo8MOW0ihGppG/YKUa+UBKFol2AU/WtBBJ+/23t03gOmg5kytNATzokQ\nhlf6gnL53+pvuOSJ0yppZxdVu7/vT4QCrzP11ssl6XytMPtR1hfRihekFK20CWcs\n9AY8lxtms7XU6jPm2ZvH47QwzpeEqcF0QdyhTjfniXFtZ0IEuxOqEmz7sY6wjrg3\nI2xpMO2Ot8uuS+IPCl4WMyzfEePA27baYOSTezVmkCX/LKvCY5XhZke7yeJVk1ZM\nRqP6JYkCgYEAxzU4524Mi6SuVqyrfLA+VYrUyy3eB6I+i6DFNedgCIKjlKiQyZnv\nY9hbdLccbbd7lpv8mnPYn0Ar9Bwwq9NEJHqoYIrVxSwCTaB0KQZ0+aKvOHzuzUYg\nuLiGMalIFqDK55ycQF0jF8rZXy3NJFmlFjwRLymTvcbkX/dHAdVe5AkCgYEA0bCW\n2e9u7ftLgI4SgCl58chob9fnomk8zJbhTn6Jzhga8DxnI0dz+HQv+nmQTY8W4+R/\nzbAlzdoocPiBh/FEFNc42xJwnkpZUIBGmVrmfsETIvi9tAvKJcwjwW+MbU8ESqoy\nU4KRpxJcMvmnwW0AtfYDkxrYAfR60SPUzd4F5CUCgYEAn3DDuMfmFqaaOxk8sDHH\n0mOp6W0utmFvOgZVkc08mdMl5kf8ir9AUWPL32DnyhD/RA5ZYa2zBdMw2tLtSblw\nYtohhhPZAVU2CreQAX3/hgZlxAqKf5XPfsmB7qGU5zeO703z6bgh7FsZHArmlF+D\nuIYfIuZeL5jPFNgv5xHGPzECgYEAtyFWXbcyVj0lz3xExBF1Iqg4LZWOAtWN98+9\nrePtTkTXIgBewvzgV5iBXmtUj6fsAdPJmkXAfmuM7jzaQ3N+VgUw7oLIQDYGkru0\n7LHqo8DTibNbWicBwMjsYT+ekMh1ow/JLA3YTuVGCG7pB5C/EittK8hB5lMx//0f\nGTxSQNECgYB+qz4JFzKxoNcVyBCkttCjces1V6pXrn/H+x1XvFsPSveXUC33OEO9\n61AHYZ4fqk/oJ8YtUBFCLm2dDlPadD8CRPpSM5TSdpNYE66KLV+g/tgBU32fsQ6S\nfma199BO5PDvtyOwkEErLNeJy7ydP4aMF56u1MMnkauBbsYvBXGnBg==\n-----END RSA PRIVATE KEY-----')
    
    locksmith.set_public_key(b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoyvdbtW5v3dqziewtm6e\nKAPLvI62OHSmAKYtiOxSMXEBt5WizvUb6yzKLVoHpm2AA2L5RzXQ6pEHpGSfdgr1\n+925pSxlIO2/OLIfF86vEJCKWSGXYkz292cRX1f8JSv6XzoT71v0GQFJ5Y37W7oN\nM8jLvzMTYywN0hy2YmA+Mj9iag8wkg0PIKb3ZdfrAZ1bSxXCTnC5ap+gi9LweIaD\n2ekHJK2oX88KA+Ne54g8ygPz6EQvoUcuwd1p4act/bhjd92xBcDQMY+rITDvIb6R\nvSGrap0rxQBDMFCDHpAQMWYaJjvP9WynJs3snXEmXrdmyumB1b4duXsMG2kbm/v5\nTQIDAQAB\n-----END PUBLIC KEY-----')
    
    print('\nWe verify the keys')
    print(locksmith.decrypt_private_key(key_2_private_key))
    print(locksmith.get_public_key)
    # END We provide the keys and protect the private key at run time
    
    
    # We recover the protected private key at run time
    print('\n\nWe recover the protected private key at run time')
    protected_private_key = locksmith.get_private_key
    print(protected_private_key)
    
    
    # BEGIN We provide the private key at run time
    print('\n\nWe provide the keys and protect the public key at run time')
    locksmith.set_private_key(b'\x90\xc0vOk\xf1&@\xc0\xa3\xceVQ\x1e\xde\xa9ITv\xc9\xe3\xd7l\x00t\x89\xc1\x82Bw\x14\x96\x00,\xfc\xf8\xd4\xe4\xd9Q\xa4\ryb\xf7(L\xf8\xd6/\xfd\xf5\xba|\xb9J\xe1\x03gt\x077\x08\xac\'\xad\x8e\xa9\x7fA1\x9b\x10\xb4\xc5\xf1y\x89\xb6m\xd6 \x10\xd4\xaa\xa8\x00\xa6\x18U\xa7e\'x\xc5\xb3\xc2\xacsn\x0f] H\xb9\xdf\x07P\xa7\xf3\x1a\xfe\xd7Q\xf2\xea[+\xc5<\xc8\x94\xe1;\xa3VP\x08\xa5\x89\xfe\xef\'\x05\xbd\xdf\xb9\x867]\xb1\xe3\x7f\xefx\xb6\'\xa1z1-\xfe@\x9b\x9d[\xeb\xdcJ\x8f\x81\xe3]\x01Z\x1e0\xff\xb2jF\xcc\xcf\xad\xd5\xd5\x08\x16t\xf0>4\xf8\x89\xaeg\x9e\x87\xa5#\x8d\\\xf7p\x1a\x06\x80>\xbf5\xd1\xe4\xf0\xb7H\xeaA\x06\x8b\xd2\xce)\xd5\x11\x05\xd1*N-\x96\x11\xd1\x07m\xe9\xf4\xb3;F\xe1\x0b\x1d\xb0\xfe+\xce"\x8a\x81\x07\xfe\x99\xb6\xd1\\\xd9i\xa6\x04\x80\xf3\xc6HQ\xf9\x87\xf0\xa1\xa1\xd8\x16\x1b=\x0c\xfa\xf8O,\xb6\x8c\x83%\xf5u\xe3*\xfe\xce\x07U\xe8\x87=7B=\x0b\xda\xb1\x9eP\x93\xf5\\<y\xef\x95D\x84O\xbf\xfd=\xfd;\xd8\x12\x83\xfe\x16w8\xcd\xa9\x1bD\xa5Oz\xa9\xbe|\x7f\xa0\xf6U\xc7M\xdat.\x93g\xafSy\xd1\x91\x0f\x05eLb\xf7\xbe\xedN\x1eH\x16\xe0m\xa9(\x9eI\x19\x05\x8f\x12\xee\xaa\x01\xc1\x98\x12F)\x7f\x08\x8dE\xe4\x10\xc2\x0f\xc9\xdc\xfa\x82\x03\xc8}\xeb}\x0b%\xbb\r\xf9\x94\xc7\xf2\xf0m|\xb5\xd9H}\x91\x18\xdf\x1c\xb7\x1bZ\x91\x9c\xe3\x19\xa9d\x1buY\xb6\xfd\xa0/\x80\x1cg\xe5\xda\xf6v\xdc\x80\xf5\xdc\x19\xab\x1fh\xf0\x80\x84\xde\xc4I\xbdf<j\xc6?\xeb5\x11\xbbQ-B\x0c?\xde\x92vS s\xc0\n]i\xbd\xa4\x97\xa5\x0f\x12\x9e\xdb&c4\x06\x04E\\0\x93\x8e#\xe9\xed|\xbf\x89\xfc\xbb\x82 \x90\x1b\x1eW\xfc\xeb\xe1\x80K\xd9w\xa5F&W\x1f\x84\xf5\x81\x83\\R\xc6\x1a\x157M\xed\x07\x95\xfd3\x00p\xf4\xa1\x8e~\x18dM\xd7reyg\xbb\xbf\xbf\xe2\x8a4y\xf6E\xad%\x89;\x9b\xb0\x84<\xd8q\x96r\xd6\xc7\x01ug\x17U\x9f7\xadS\xbc2q+%\xc0X\xc2\'g\xcaq\xde$\xe6\xfc{8\'\x1c\xa7\x03\xe7\x08\x0c\x14$\xbcL\xc1\xe0\xe5\xcft\xd1\x1f\xca\xc3\x0e\xfeLm\x9a\xc3\xe3=_Q\xb0\xba#*\x00\xf9\x04\xbf3\xbe]qi\x83\xb3\xfc\xdevE\xf6b\xa6\xa9P\xc1VQd\xa0\x8cbV4\xd6\xea\xf8\xdf~Y\xad\x9f\xc70\xdb\xd7\rC\x0f<|h\tt\x18\x15`\xa3z\xfa~ S\x94\xdb\x99\xf4%\xa0\xb3\xe9\x9f\xf8\xb9\'/\xe5A\x1d\xfaF\x91c\xda?p=\xb3\xa2\xd6\xc7\xe4 \x0f\xdc\xd7\xf5\'\xd7\x88c4=\xc2\xdb\xaf*h\x16\x82\x0b\xd3i9\x9cY\xd4p\xd7\xbamL1c.(\xc82q\xde\x9a]\xc3w\x06\xe7\xc0Y8k\xc0\x95\x87KS/\t\xbfwG\xb5\xd0\xcc\xda\xbe\n\x04)\x07\x9b\xc5\x89\xe7;>I\x08\x82\x12\xd6\xfe\x1a\xe2\xad\xe6\xde\xc3\xaa\x92\x07\x16\xdf\x1bB\xad\to\xd1\xda\x83@\xe5\xacl\xa4\xdd\x8d\xf7\xa6>\xacu/D\xa2\xd2\x8fB\xeaH\xd5=\xd8{H<#,\x88\x97\xbc\xe3\xd2\xa2\x1a\xdf\xe5\xd3\xf5\xd2\x0c\xd5#\'b\x80\xc9\xf9\xaf\xa7x\x07{\x1b-P\xd7\xdc\xb2\xd0\xaeh"\xfb\x8e\x0f\xc1\xa08\xff\xcdh7\xbeI\x89~x[4\xfb\xa2a~\x0f\xb6\x92\xd7y\x98\xe4@,\xde\x1a\x12W\x16\xab\xeb%H\x92\xe0\xdb\n\x19G\x81\xd0b\x07\x89\x9d\xb4\xab+\x98z\xe2\xb8\x00K\x7f\xadQ\x10\x7f\x8c\xf4=LMUu\xd0\xe0\xca\xfc~\xe4\x1f\x8c\xc8\xfe\x8d\xcf\x00p\x07\xd2u\x8c\xc6\xbb>\x9b\xe4Dz%Ug\x87\xcf\xdca=\x93Fw,5b#\xbe\x84\x18\'\'\x08\xe8\xab+xSj\xeb]V\xc4^\x0cz\xac\xf7c/\x9f$\xe6a\xa3\x8d\x14\xdbzl"??\xf2h\x0b\xbe\x8e\xa9\xc3#\xb0\xedI4\xf2DH\xaf-\x02[7\xdb\x0b\xdb\xde>\xbbR\xd5\xb9\xa8\n\x9c0\x82\xb3\x14\xfc\x9e\xc8\xb6^?L.\xd9\x1d\x99>\xcdz\xf4Zq\xfb5\xa9\xbc\x03\xe30\xbc\xe2s/\xb0:\xc3\xb6\x8c\xc5\xc1&\xb0\xbb\x04++\x1f\x10Dp\x88\xe6(\x0e\x07\\\xf6Q\xd4\xb7\x99\x117\xd6G\x84[\xf7\xe7t{j\xf7\x85\xd7\xcd0\xef\xd3\x88\xafT\xc7a\x08\xc4FW\x86It\xe9$\x12\x03\x8d\xff\xfcH\xa8\x05\x97\xe7#\xf3\x95+\xf4\xe8v\x82\xfb\x95Y\x7f]\xf5\x1d\xa2;c0\xd7m\xf9D \xb0\x0f\x9bt\xad\xf8\xe0\xfd?t\xe9\xf7\xb6aN\xff\xe9\xd9\xd1H\r\x8d\xfa\xf5\xbeV\x00\x12\xceX\x1b\x84\xf5G>\xb6O\xfb\x88\x9d\xa7\x14"\xcfl\xec\x81\x12\xaf\x13\x95\xcbo\xdc\xb8\x94\x8dm\xe8-\xb2\x8b\xfa\xfb:\xe2\x975\xfe\xe8\x9dyjUES\xf3\x84?\x91L\xf1z\xa1Q\xd9\x07\xa7\x02-W\xac\x06\xa4\x04\x10\x8b\x96\x8fi\x97\xf3\xe4\\\xb9Ig+y\x94"H?\xfd7\x89\x03\xb3\xc4\x93\xfc\x98\xf2\x03\x10\xff5{\xf3]>\xa4(\xc9+8}\xd9\xe7\x1c\x95\xf5\x01\x0b\xde\x96\xb6s\xc1\x17\rJF\xe9O\xd5\x8f\xceR\xf0\xeft\rk\xcb\x92\xde\xcf\xf4$Y\xf3\x88\xda\x18\xa1\xc5D\x1e\t7\x99\x9b>\xa7\xe6\xae\xb1\xf7\xd5&\x92\xdfm\x9arip\t^\xefw\x8fn\xe3\xac\xb6_\x7f\x0f}\xe5\x04\xec|\xfe\xc3T\x1da\x1b\x85\xf23\xb7\x19}\xbb[\xac\x04\xdcN|\x17y\n\xa8\xc5E]\x18\xa8nF~\x89Xax~\xb5#\xa3\x83o\xa4\nC\xc2\x9a`^\x9c\xd5\xeak\x80\x91\x04\xa0\x83\x9a\xf9*\xbe\x995\x958`{\xd1\xb2\xd5,\xb4\r\xc4\x06P[\xe0&\x86\xa521\xc4b\x1b\xffD\x1b\xcb\xf8\x1dD\xd7\x0b\xb8\xd1\xc8\x83\x8e\xf2\xf3\x10\x1f\x84\xb3\x1b?m\xf6\xac )\xaa\xc2P\xf5\x96OV\xeb{a\x9d\xc1\x87~\x7f\x16\xbd\xb1\xa94\x96\x99I<4\xa6\xbd\x90Z\x07\xe0\x90^\xe1}\xd6}\xca\xc7\xf3\xca\x08jq\x90\xc1\xb3\x9c\xbdN\xc7\xee\xcc\xedsr\xabw1-\xab\xfa&RSr\xfbT\xba\xf1yS\x01\xc6\xca\x8d\xb3\x7f\x9f\xb44\xa4.{.\xda\xc9\xe5\x01l\x11ZD{\xfe\x1e\xb2\xbd\xa9\xdalhq\xd9\xb8\xb1\x93I\r\x1e\xfb\xa9G\x9bSgq=\x95\xf9\xd3(\xe0\xa1\xbb\xf2\xae\x1c\x06\xf3\x88\x9f\x8e0\x0b=\x8e\x18\xdf\xad\x9ff0\x96\x8b\xa0\xd8\xe2e*\xb4`\x7f\x7f\xb9\x9dh\xc7Ad\xd5\xa4\xca\x82\x074\x0cQ\x06\xb7*F\xbc')
    
    print('And we verify the private key')
    print(locksmith.decrypt_private_key(key_2_private_key))
    # END We provide the private key at run time