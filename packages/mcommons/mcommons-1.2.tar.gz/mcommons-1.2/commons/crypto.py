
import base64


class AESCipher:

    def pad(self, s):
        BS = 16
        return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        from Crypto.Cipher import AES
        from Crypto import Random
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new( self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        from Crypto.Cipher import AES
        from Crypto import Random
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self.unpad(cipher.decrypt(enc[16:]))