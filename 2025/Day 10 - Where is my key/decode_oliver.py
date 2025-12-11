from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

# Mot de passe trouvé dans le binaire
password = "grinch_eggnog2025"

# Lecture du fichier chiffré
with open("oliver_list.enc", "rb") as f:
    data = f.read()

# Vérification du header OpenSSL
if not data.startswith(b"Salted__"):
    raise SystemExit("Erreur : pas d'en-tête 'Salted__' dans le fichier.")

# Extraction du sel et du ciphertext
salt = data[8:16]
ciphertext = data[16:]

def decrypt(nbr_iterations):
    # Dérivation clé + IV (32 + 16 octets)
    key_iv = PBKDF2(
        password,
        salt,
        dkLen=48,
        count=nbr_iterations,
        hmac_hash_module=SHA256
    )
    key, iv = key_iv[:32], key_iv[32:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = cipher.decrypt(ciphertext)

    # Suppression du padding PKCS#7
    pad_len = pt[-1]
    if pad_len == 0 or pad_len > 16:
        return None
    if pt[-pad_len:] != bytes([pad_len]) * pad_len:
        return None

    return pt[:-pad_len]

# Nombre d'itérations trouvé dans le binaire : 0x186A0 = 100000
iterations = 100000

plaintext = decrypt(iterations)

if plaintext is None:
    print("Erreur : padding invalide, déchiffrement incorrect.")
else:
    print(plaintext.decode(errors="ignore"))
