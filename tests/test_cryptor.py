import Spartacus
from Spartacus import Utils

try:
    v_cryptor = Spartacus.Utils.Cryptor("password")

    v_plain = 'This text is secret and must be hidden!'
    print('Plain: {0}'.format(v_plain))

    v_hashed = v_cryptor.Hash(v_plain)
    print('Hashed: {0}'.format(v_hashed))

    v_encrypted = v_cryptor.Encrypt(v_plain)
    print('Encrypted: {0}'.format(v_encrypted))

    v_decrypted = v_cryptor.Decrypt(v_encrypted)
    print('Decrypted: {0}'.format(v_decrypted))

    v_str_to_decrypt = 'T8br3Tsc0lLOlTX/rIekM6aTX4qm1Didbc4fi1a7+39ju+kXCSmv'
    v_decrypted = v_cryptor.Decrypt(v_str_to_decrypt)
    print('Decrypted from existing string: {0}'.format(v_decrypted))
except Spartacus.Utils.Exception as exc:
    print(str(exc))
except Exception as exc:
    print(str(exc))
