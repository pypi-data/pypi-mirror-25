import base64
import hashlib
import random
import nacl.signing


def gen_code_verifier(length=128):
    """
    Generate a high entropy code verifier, used for PKCE

    args:
        length (int): length of the code

    returns:
        str:
    """
    choices = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~'
    r = random.SystemRandom()
    return "".join(r.choice(choices) for _ in range(length))


def gen_code_challenge(code_verifier):
    """
    Transform the PKCE code verifier in a code challenge

    args:
        code_verifier (str): a string generated with `gen_code_verifier()`
    """
    return base64.urlsafe_b64encode(hashlib.sha256(code_verifier).digest()).rstrip('=')


def make_verifier(key):
    """
    Create a NaCL verifier

    args:
        key (str): A verification key

    returns:
        nacl.signing.VerifyKey: a nacl verifykey object
    """
    return nacl.signing.VerifyKey(key, encoder=nacl.encoding.Base64Encoder)
