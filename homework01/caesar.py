import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""

    for i in plaintext:
        if 65 <= ord(i) <= 122:
            if i.isupper():
                if ord(i) >= 87:
                    ciphertext += chr(65 + (ord(i) + shift) % 91)
                else:
                    ciphertext += chr(ord(i) + shift)
            else:
                if ord(i) >= 119:
                    ciphertext += chr(97 + (ord(i) + shift) % 123)
                else:
                    ciphertext += chr(ord(i) + shift)
        else:
            ciphertext += i

    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""

    for i in ciphertext:
        if 65 <= ord(i) <= 122:
            if i.isupper():
                if ord(i) <= 68:
                    plaintext += chr(90 - (2 - (ord(i) % 65)))
                else:
                    plaintext += chr(ord(i) - shift)
            else:
                if ord(i) <= 99:
                    plaintext += chr(122 - (2 - (ord(i) % 97)))
                else:
                    plaintext += chr(ord(i) - shift)
        else:
            plaintext += i

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0

    for shift in range(26):
        plaintext = decrypt_caesar(ciphertext, shift)
        if plaintext in dictionary:
            best_shift = shift
            break
    return best_shift
