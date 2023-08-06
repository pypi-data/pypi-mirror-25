from learncrypy import *


class Symmetric:
    def caesar(self, message, key=0, decrypt=False):
        assert str(key).isdigit, "Key must be a non-negative integer"

        mapping = {}
        alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        message = message.upper()
        key = int(key)

        for i in range(26):
            alphabet = alphabets[i]

            if not decrypt:
                index = (i + key) % 26
            else:
                index = (i - key) % 26
            mapping[alphabet] = alphabets[index]

        return "".join(list(map((lambda x: mapping[x] if x in mapping.keys() else x), message)))

    def caesar_break(self, message):
        for key in range(26):
            print("For K=", key, " decrypted text is ->", self.caesar(message, key=key, decrypt=True))

    def monoalphabetic(self, message, key="ABCDEFGHIJKLMNOPQRSTUVWXYZ", decrypt=False):
        assert (
            len(key) == 26 and len(set(key)) == 26 and str(key).isalpha()), "Key must be a string with all 26 alphabets"
        message = message.upper()
        key = key.upper()
        alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if not decrypt:
            mapping = dict(zip(alphabets, key))
        else:
            mapping = dict(zip(key, alphabets))

        return "".join(list(map((lambda x: mapping[x] if x in mapping.keys() else x), message)))
