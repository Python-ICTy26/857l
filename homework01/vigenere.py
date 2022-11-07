def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    key_length = len(keyword)
    key_int = [ord(i) for i in keyword]
    plaintext_int = [ord(i) for i in plaintext]

    for i in range(len(plaintext_int)):
        if plaintext_int[i] == 32:
            plaintext += " "
            continue
        elif plaintext[i].isupper():
            value = (plaintext_int[i] + key_int[i % key_length]) % 26
            ciphertext += chr(value + 65)
        else:
            value = (plaintext_int[i] + key_int[i % key_length] - 64) % 26
            ciphertext += chr(value + 97)

    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_length = len(keyword)
    key_int = [ord(i) for i in keyword]
    ciphertext_int = [ord(i) for i in ciphertext]

    for i in range(len(ciphertext_int)):
        if ciphertext_int[i] == 32:
            plaintext += " "
            continue
        elif chr(ciphertext_int[i]).isupper():
            value = (ciphertext_int[i] - key_int[i % key_length]) % 26
            plaintext += chr(value + 65)
        else:
            value = (ciphertext_int[i] - key_int[i % key_length]) % 26
            plaintext += chr(value + 97)

    return plaintext
