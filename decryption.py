from Crypto.Cipher import DES, AES
import zipfile
import time

def readCiphertextfromFile(filename):
    with open(filename, "rb") as file:
        return file.read()

def pad_key(key,algo):
    if algo == "DES":
        if len(key) < 8:
            key += b'\x00' * (8 - len(key))
        return key
    else:
        if len(key) < 16:
            key += b'\x00' * (16 - len(key))
        return key


def decrypt_text(encryptedText, key, algorithm):
    key = pad_key(key,algorithm)
    if algorithm == 'DES':
        cipher = DES.new(key[:8], DES.MODE_ECB)
    elif algorithm == 'AES':
        cipher = AES.new(key[:16], AES.MODE_ECB)
    decryptedText = cipher.decrypt(encryptedText)
    return decryptedText


def decrypt_zip_file(zip_file_path,key,algo):
    key = pad_key(key.encode(),algo)
    if algo == 'DES':
        cipher = DES.new(key[:8], DES.MODE_ECB)
    elif algo == 'AES':
        cipher = AES.new(key[:16], AES.MODE_ECB)
    with zipfile.ZipFile(zip_file_path, "r") as zip_file:
        for file_name in zip_file.namelist():
            encrypted_file_data = zip_file.read(file_name)
            file_data = cipher.decrypt(encrypted_file_data)
            with zipfile.ZipFile("plaintext.zip", "a") as new_zip_file:
                new_zip_file.writestr(file_name, file_data)
        new_zip_file.close()






algo = input("Press 1 for DES\nPress 2 for AES\n");
key = input("Enter Encryption Key: ");
file_type = int(input("Press 1 for TextFile\nPress 2 for ExeFile\nPress 3 for ZipFile\n"))
algo = "DES" if algo == "1" else "AES"

if file_type == 1:
    ciphertext_filename = "ciphertext.txt"
elif file_type == 2:
    ciphertext_filename = "ciphertext.exe"
elif file_type == 3:
    ciphertext_filename = "ciphertext.zip"
    decrypt_zip_file(ciphertext_filename, key,algo)
    exit(0)

cipherText = readCiphertextfromFile(ciphertext_filename)
start_time = time.time()
plainText = decrypt_text(cipherText, key.encode(), algo)
end_time = time.time()

print("Time taken: ",end_time-start_time)

if file_type == 1:
    with open("plaintext.txt", "wb") as file:
        file.write(plainText)

elif file_type == 2:
    with open("plaintext.exe", "wb") as file:
        file.write(plainText)



