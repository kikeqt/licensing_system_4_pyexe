__version__ = "$Version: 0.1.0"

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
        self._private_key = private_key
        
    
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

    key = '01234567'
    private_key_file_name = 'locksmith_private.pem'
    public_key_file_name = 'locksmith_public.pem'

    if exists(private_key_file_name):
        remove(private_key_file_name)
        print(f'Deleted {private_key_file_name}')

    if exists(public_key_file_name):
        remove(public_key_file_name)
        print(f'Deleted {public_key_file_name}')

    locksmith = Locksmith()
    locksmith.build_keys(key)

    locksmith.save_private_key(private_key_file_name)
    locksmith.save_public_key(public_key_file_name)

    locksmith.load_private_key(private_key_file_name)
    locksmith.load_public_key(public_key_file_name)

    print(locksmith.decrypt_private_key(key))
    print(locksmith.get_public_key)
    
    locksmith.set_private_key(b'-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAoyvdbtW5v3dqziewtm6eKAPLvI62OHSmAKYtiOxSMXEBt5Wi\nzvUb6yzKLVoHpm2AA2L5RzXQ6pEHpGSfdgr1+925pSxlIO2/OLIfF86vEJCKWSGX\nYkz292cRX1f8JSv6XzoT71v0GQFJ5Y37W7oNM8jLvzMTYywN0hy2YmA+Mj9iag8w\nkg0PIKb3ZdfrAZ1bSxXCTnC5ap+gi9LweIaD2ekHJK2oX88KA+Ne54g8ygPz6EQv\noUcuwd1p4act/bhjd92xBcDQMY+rITDvIb6RvSGrap0rxQBDMFCDHpAQMWYaJjvP\n9WynJs3snXEmXrdmyumB1b4duXsMG2kbm/v5TQIDAQABAoIBABbuafjy198o3u14\nhfzpeFgaynXmH4U5HYA/Wmxg+98faNSeVqpbp5AKNCKiAau5vVEchnhjv4fLmIWZ\nr5BVE4NRQo8MOW0ihGppG/YKUa+UBKFol2AU/WtBBJ+/23t03gOmg5kytNATzokQ\nhlf6gnL53+pvuOSJ0yppZxdVu7/vT4QCrzP11ssl6XytMPtR1hfRihekFK20CWcs\n9AY8lxtms7XU6jPm2ZvH47QwzpeEqcF0QdyhTjfniXFtZ0IEuxOqEmz7sY6wjrg3\nI2xpMO2Ot8uuS+IPCl4WMyzfEePA27baYOSTezVmkCX/LKvCY5XhZke7yeJVk1ZM\nRqP6JYkCgYEAxzU4524Mi6SuVqyrfLA+VYrUyy3eB6I+i6DFNedgCIKjlKiQyZnv\nY9hbdLccbbd7lpv8mnPYn0Ar9Bwwq9NEJHqoYIrVxSwCTaB0KQZ0+aKvOHzuzUYg\nuLiGMalIFqDK55ycQF0jF8rZXy3NJFmlFjwRLymTvcbkX/dHAdVe5AkCgYEA0bCW\n2e9u7ftLgI4SgCl58chob9fnomk8zJbhTn6Jzhga8DxnI0dz+HQv+nmQTY8W4+R/\nzbAlzdoocPiBh/FEFNc42xJwnkpZUIBGmVrmfsETIvi9tAvKJcwjwW+MbU8ESqoy\nU4KRpxJcMvmnwW0AtfYDkxrYAfR60SPUzd4F5CUCgYEAn3DDuMfmFqaaOxk8sDHH\n0mOp6W0utmFvOgZVkc08mdMl5kf8ir9AUWPL32DnyhD/RA5ZYa2zBdMw2tLtSblw\nYtohhhPZAVU2CreQAX3/hgZlxAqKf5XPfsmB7qGU5zeO703z6bgh7FsZHArmlF+D\nuIYfIuZeL5jPFNgv5xHGPzECgYEAtyFWXbcyVj0lz3xExBF1Iqg4LZWOAtWN98+9\nrePtTkTXIgBewvzgV5iBXmtUj6fsAdPJmkXAfmuM7jzaQ3N+VgUw7oLIQDYGkru0\n7LHqo8DTibNbWicBwMjsYT+ekMh1ow/JLA3YTuVGCG7pB5C/EittK8hB5lMx//0f\nGTxSQNECgYB+qz4JFzKxoNcVyBCkttCjces1V6pXrn/H+x1XvFsPSveXUC33OEO9\n61AHYZ4fqk/oJ8YtUBFCLm2dDlPadD8CRPpSM5TSdpNYE66KLV+g/tgBU32fsQ6S\nfma199BO5PDvtyOwkEErLNeJy7ydP4aMF56u1MMnkauBbsYvBXGnBg==\n-----END RSA PRIVATE KEY-----')
    locksmith.set_public_key(b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoyvdbtW5v3dqziewtm6e\nKAPLvI62OHSmAKYtiOxSMXEBt5WizvUb6yzKLVoHpm2AA2L5RzXQ6pEHpGSfdgr1\n+925pSxlIO2/OLIfF86vEJCKWSGXYkz292cRX1f8JSv6XzoT71v0GQFJ5Y37W7oN\nM8jLvzMTYywN0hy2YmA+Mj9iag8wkg0PIKb3ZdfrAZ1bSxXCTnC5ap+gi9LweIaD\n2ekHJK2oX88KA+Ne54g8ygPz6EQvoUcuwd1p4act/bhjd92xBcDQMY+rITDvIb6R\nvSGrap0rxQBDMFCDHpAQMWYaJjvP9WynJs3snXEmXrdmyumB1b4duXsMG2kbm/v5\nTQIDAQAB\n-----END PUBLIC KEY-----')
    
    print()
    print(locksmith.decrypt_private_key(key))
    print(locksmith.get_public_key)