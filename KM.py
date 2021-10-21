import os
import socket
from Info import *
from Crypto.Cipher import AES

def aes_encrypt(message, key):
    aes = AES.new(key, AES.MODE_ECB)
    encrypted = aes.encrypt(message)
    return encrypted

K = os.urandom(16)  #generarea random a cheii
print("Cheia asociata modului de operare: %d",K)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((port, portul_a_km))
    s.listen()
    conn, _ = s.accept()
    with conn:
        data = conn.recv(3)
        print(f'Modul de operare: {data.decode("utf-8")}')
        conn.sendall(bytes(aes_encrypt(K, K1)))
