
def xor_func(block, vec_init, key):
    block_xor_vec_init = bytes(a ^ b for (a, b) in zip(block, vec_init))
    block_xor_vec_init_xor_key = bytes(a ^ b for (a, b) in zip(block_xor_vec_init, key))
    return block_xor_vec_init_xor_key


class OFB_mode:
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
            encrypted_block = xor_func(vec_init, self.key, block)
            ciphertext += encrypted_block
            vec_init = bytes(a ^ b for (a, b) in zip(self.key, vec_init))
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b''
        vec_init = self.initialization_vector
        while ciphertext:
            block = ciphertext[0:16]
            ciphertext = ciphertext[16:]
            decrypted_block = xor_func(vec_init, self.key, block)
            plaintext += decrypted_block
            vec_init = bytes(a ^ b for (a, b) in zip(self.key, vec_init))
        return plaintext
