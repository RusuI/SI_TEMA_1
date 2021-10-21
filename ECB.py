
from Crypto.Cipher import AES


class ECB_mode:
   def __init__(self, vec_init, key):
      self.initialization_vector = vec_init
      self.key = key

   def encrypt(self, plaintext):
          ciphertext = b''
          vec_init = self.initialization_vector
          while plaintext:
              block = plaintext[0:16]
              block = block + b'\0' * (16 - len(block))
              plaintext = plaintext[16:]

              aes = AES.new(self.key,AES.MODE_ECB)
              ciphertext += aes.encrypt(block)
          return ciphertext

   def decrypt(self, ciphertext):
          plaintext = b''
          vec_init = self.initialization_vector
          while ciphertext:
              block = ciphertext[0:16]
              block = block + b'\0' * (16 - len(block))
              ciphertext = ciphertext[16:]
              aes = AES.new(self.key,AES.MODE_ECB)
              plaintext += aes.decrypt(block)
          return plaintext
