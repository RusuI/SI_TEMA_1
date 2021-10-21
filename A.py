import socket
import Info
from ECB import *
from OFB import *
from Crypto.Cipher import AES

print(" EBC -> 1\n OFB -> 2")
print("Selecteaza modul preferat: ")
input = input()
if input == '1':
    mode_operation = 'ECB'
    print(mode_operation)
else:
    mode_operation = 'OFB'
    print(mode_operation)

key = b''
enc_key = b''


def aes_decrypt(ciphertext, key):
    aes = AES.new(key, AES.MODE_ECB)
    decrypted = aes.decrypt(ciphertext)
    return decrypted


def encryp_msg(msg):
    if mode_operation == 'ECB':
        ecb = ECB_mode(Info.initialization_vector, key)
        enc_msg = ecb.encrypt(msg)
    elif mode_operation == 'OFB':
        ofb = OFB_mode(Info.initialization_vector, key)
        enc_msg = ofb.encrypt(msg)
    return enc_msg


def conn_KM(KM_port):
    global key, enc_key
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as kms:
        kms.connect((Info.port, KM_port))

        kms.sendall(bytes(mode_operation, "utf-8"))
        kms.sendall(enc_key)
        enc_key = kms.recv(16)
        print(f'Cheia  de la Key Manager: {enc_key}')
        key = aes_decrypt(enc_key, Info.K1)
        print(f'Cheia decriptata: {key}')


def conn_B(B_port):
    global key, enc_key
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((Info.port, B_port))

        s.sendall(bytes(mode_operation, "utf-8"))
        s.sendall(enc_key)
        data = s.recv(5)
        print(f'Semnalul: {data.decode("utf-8")}')

        try:

            with open("file.txt", "rb") as f:
                file = f.read()
                size = len(file)
                s.sendall(bytes(str(size), 'utf8'))
                enc_msg = encryp_msg(file)
                s.sendall(enc_msg)

        except FileNotFoundError:
            print("Did not find the requested file")


if __name__ == "__main__":
    conn_KM(Info.portul_a_km)
    conn_B(Info.portul_a_b)
