from Crypto.Cipher import DES3

key = b'Sixteen byte key'
cipher = DES3.new(key, DES3.MODE_ECB)
plaintext = b'sona si latine loqueris '
msg = cipher.encrypt(plaintext)

print(msg)