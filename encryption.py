from Crypto.Cipher import DES,AES
from Crypto.Util.Padding import pad, unpad
import zipfile
import time


def pad_key(key,algo):
    if algo == "DES":
        if len(key) < 8:
            key += b'\x00' * (8 - len(key))
        return key
    if len(key) < 16:
        key += b'\x00' * (16 - len(key))
    return key

def pad_input_data(input_data):
    padding_length = 8 - (len(input_data) % 8)
    padding = b'\x00' * padding_length
    padded_input_data = input_data + padding
    return padded_input_data


def encryption_algo(text,key,algo):
    key = pad_key(key,algo)
    if algo == "DES":
        cipher = DES.new(key[:8],DES.MODE_ECB)
    elif algo == "AES":
        cipher = AES.new(key[:16],AES.MODE_ECB)

    text_with_pad = pad(text,cipher.block_size)
    cipherText = cipher.encrypt(text_with_pad)
    return cipherText


def encrpytion_algo_zip_file(file_name,key,algo):
    key = pad_key(key.encode(),algo)
    if algo == "DES":
        cipher = DES.new(key[:8],DES.MODE_ECB)
    elif algo == "AES":
        cipher = AES.new(key[:16],AES.MODE_ECB)
    # text_with_pad = pad(text,cipher.block_size)
    # cipherText = cipher.encrypt(text_with_pad)
    # return cipherText
    with zipfile.ZipFile(file_name, "r") as zip_file:
        for filename in zip_file.namelist():
            print(filename)
            file_data = zip_file.read(filename)
            file_data = pad(file_data,cipher.block_size)
            encrypted_file_data = cipher.encrypt(file_data)
            with zipfile.ZipFile("ciphertext.zip", "a") as new_zip_file:
                new_zip_file.writestr(filename, encrypted_file_data)
        new_zip_file.close()

def read_file(filename):
    with open(filename, "rb") as file:
        return file.read()

menu = int(input("Enter Choice\n1. Enter Text \n2. Read from file \n"))

if menu == 1:
    text = input("Enter Text: ")
elif menu == 2:
    file_menu = int(input('Enter Choice\n1. 1MBTEXTFILE.txt\n2. 10MBTEXTFILE.txt\n3. 100MBTEXTFILE.txt\n4. EXEFILE.exe\n5. ZIPFILE.zip\n'))
    if file_menu == 1:
        file_name = "1MBTEXTFILE.txt"
    elif file_menu == 2:
        file_name = "10MBTEXTFILE.txt"
    elif file_menu == 3:
        file_name = "100MBTEXTFILE.txt"
    elif file_menu == 4:
        file_name = "EXEFILE.exe"
    elif file_menu == 5:
        file_name = "ZIPFILE.zip"
    else:
        print("Wrong Choice Entered")
        exit(0)
    text = read_file(file_name)
else:
    print("Wrong Choice Entered")
    exit(0)

algo = input("Press 1 for DES\nPress 2 for AES\n")
key = input("Enter Encryption Key: ")
algo = "DES" if algo == "1" else "AES"

if file_menu == 5:
    print('in zip file')
    start_time = time.time()
    encrpytion_algo_zip_file(file_name,key,algo)
    end_time = time.time()
    print("Time taken: ",end_time-start_time)
    print("encrpytion of zip file done")
    exit(0)

if menu == 1:
    encryptedText = encryption_algo(text.encode(),key.encode(),algo)
else:
    start_time = time.time()
    encryptedText = encryption_algo(text,key.encode(),algo)
    end_time = time.time()

    print("Time taken: ",end_time-start_time)
if file_menu == 4:
    with open("ciphertext.exe", "wb") as file:
        file.write(encryptedText)
else:
    with open("ciphertext.txt", "wb") as file:
        file.write(encryptedText)
