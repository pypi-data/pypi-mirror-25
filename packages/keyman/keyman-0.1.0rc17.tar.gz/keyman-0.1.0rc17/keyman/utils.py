from __future__ import unicode_literals

import sys
import getpass
import datetime
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

from keyman.config import KEY, IV

PY3 = sys.version_info[0] == 3  # sys.version_info > (3,)


def input_func(msg, is_passwd=False, required=False, is_secret=False):
    input_value = None
    if is_passwd:
        is_secret = True

    while True:
        if not is_passwd:
            # Shim for raw_input in python3
            if PY3:
                input_value = input(msg)
            else:
                # For python 2, raw_input will return a str rather than an
                # unicode, so str -> unicode decoding is needed.
                input_value = raw_input(msg).decode(sys.stdin.encoding)

        else:
            while True:
                password = getpass.getpass(msg)
                if not PY3:  # str -> unicode for python 2
                    password = password.decode(sys.stdin.encoding)

                confirm = getpass.getpass("Confirm your password: ")
                if not PY3:  # str -> unicode for python 2
                    confirm = confirm.decode(sys.stdin.encoding)

                if password == confirm:
                    break
                else:
                    print("Password and confirm don't match!")

            input_value = password

        if required and input_value == "":
            print("Input value cannot be empty!")
        else:
            if is_secret:
                input_value = repr(CBCCipher(KEY, IV).encrypt(input_value))
            return input_value


def edit_func(msg, is_passwd=False, is_secret=False):
    # Ask whether the user want to edit the term:
    choice = input_func(msg, is_passwd=False, is_secret=False)

    while True:
        if choice in ('n', ""):  # no editing
            return None
        elif choice == "y":  # editing
            new_value = input_func(
                "New password: " if is_passwd else "New value: ",
                is_passwd=is_passwd, is_secret=is_secret
            )
            return new_value
        else:
            print("Invalid choice character.")
            choice = input_func(msg, is_passwd=False, is_secret=False)


def python_2_unicode_compatible(klass):
    """
    A decorator that defines __unicode__ and __str__ methods under Python 2.
    Under Python 3 it does nothing.

    To support Python 2 and 3 with a single code base, define a __str__ method
    returning (unicode) text and apply this decorator to the class.

    Copied from six.py. Copyright (c) 2010-2015 Benjamin Peterson

    """
    if sys.version_info[0] == 2:
        if '__str__' not in klass.__dict__:
            raise ValueError("@python_2_unicode_compatible cannot be applied "
                             "to %s because it doesn't define __str__()." %
                             klass.__name__)
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
    return klass


class CBCCipher:
    def __init__(self, key, iv, encoding="utf"):
        """
        Initialize the Crypter.

        :param key: byte string
            The secret key to use in the symmetric cipher. It must be 16 (AES-
            128), 24 (AES-192), or 32 (AES-256) bytes long.

        :param iv: byte string
            The initialization vector to use for encryption or decryption.

            For all modes except MODE_OPENPGP, MODE_ECB and MODE_CTR, it must be
            AES.block_size (=16) bytes long. See the doc for Crypto.Cipher.AES
            in https://www.dlitz.net/software/pycrypto/api/current/ for more
            details.

            It is optional and when not present it will be given a default value
            of all zeroes.

        """
        self.key = key
        self.mode = AES.MODE_CBC
        self.iv = iv
        self.encoding = encoding

        # Since we cannot reuse a BlockAlgo cipher object for encrypting or
        # decrypting other data with the same key, we can't add a cipher as a
        # feature of this class.
        # self.cipher = AES.new(self.key, self.mode, self.iv)

    def encrypt(self, plaintext):
        """
        Encrypt the given data.

        :param plaintext: str (unicode in python 2)

        :return: bytes (also str in python 2)
            Encrypted data.

        """
        cipher = AES.new(self.key, self.mode, self.iv)
        return b2a_hex(cipher.encrypt(self._text_padding(
            plaintext.encode(self.encoding)
        )))

    def decrypt(self, ciphertext):
        """
        Decrypt the cipher data.

        :param ciphertext: bytes (also str in python 2)

        :return: str (unicode in python 2)
            Original data.

        """
        cipher = AES.new(self.key, self.mode, self.iv)
        plaintext = cipher.decrypt(a2b_hex(ciphertext))
        return self._text_unpadding(plaintext).decode(self.encoding)

    def _text_padding(self, plaintext):
        """
        Perform padding for plaintext.

        For MODE_ECB, MODE_CBC, and MODE_OFB, plaintext length (in bytes) must
        be a multiple of AES.block_size. See the API of Crypto.Cipher.blockalgo.
        BlockAlgo.encrypt() in the doc
        https://www.dlitz.net/software/pycrypto/api/current/ for more details.

        :param plaintext: byte string
            The piece of data to encrypt.

        :return: byte string
            The padded text.

        """
        remainder = len(plaintext) % AES.block_size

        if remainder != 0:
            plaintext += b"\0" * (AES.block_size - remainder)

        return plaintext

    def _text_unpadding(self, plaintext):
        return plaintext.rstrip(b"\0")


time_format = "%Y-%m-%d %H:%M:%S"
dt2str = lambda dt: dt.strftime(time_format)
str2dt = lambda tstr: datetime.datetime.strptime(tstr, time_format)
