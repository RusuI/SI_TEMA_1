import socket
import Info
from ECB import *
from OFB import *
from Crypto.Cipher import AES

key, enc_key = b'', b''

def AES_decrypt(ciphertext, key):
    aes = AES.new(key, AES.MODE_ECB)
    decrypted = aes.decrypt(ciphertext)
    return decrypted

def decr_msg(mode, message):
    if mode == 'ECB':
        ecb = ECB_mode(Info.initialization_vector, key)
        dec_msg = ecb.decrypt(message)
    else:
        ofb = OFB_mode(Info.initialization_vector, key)
        dec_msg = ofb.decrypt(message)
    return dec_msg


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((Info.port, Info.portul_a_b))
    s.listen()
    conn, _ = s.accept()
    with conn:
        mode = conn.recv(3)
        print(f'Modul de operare: {mode.decode("utf-8")}')

        enc_key = conn.recv(16)
        print(f'Cheia de la A: {enc_key}')
        key = AES_decrypt(enc_key, Info.K1)
        print(f'Cheia decriptata: {key}')

        conn.sendall(bytes("Start", "utf-8"))

        size = conn.recv(4)
        dec_msg = decr_msg(mode.decode('utf-8'), conn.recv(int(str(size, 'utf8'))))

        print(f'Mesajul A: {dec_msg.decode("ISO-8859-1")}')