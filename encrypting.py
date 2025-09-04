import random, string
chars = " "+ string.ascii_letters + string.digits + string.punctuation
chars=list(chars)
keys=chars.copy()
random.shuffle(keys)
# print(f"chars: {chars}")
# print(f"keys: {keys}")
mode=input("\nWhat mode do you want, encrypt or decrypt?: ")
if mode=="encrypt":
    plain_text=input("Enter a message to encrypt: ")
    cipher_text =""

    for letter in plain_text:
        index=chars.index(letter)
        cipher_text+=keys[index]

    print(f"\nOriginal text: {plain_text}")
    print(f"Cipher text: {cipher_text}")
elif mode=="decrypt":
    plain_text=input("Enter a message to decrypt: ")
    cipher_text =""

    for letter in plain_text:
        index=keys.index(letter)
        cipher_text+=chars[index]

    print(f"\nEncrypted text: {plain_text}")
    print(f"Original text: {cipher_text}")