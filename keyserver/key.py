from datetime import datetime
import gpgme
from io import BytesIO


class PublicKey:

    def __init__(self, fp):
        if isinstance(fp, str):
            fp = BytesIO(bytes(fp, "ascii"))
        elif isinstance(fp, bytes):
            fp = BytesIO(fp)
        self.ctx = gpgme.Context()
        self.ctx.armor = False
        self._import = self.ctx.import_(fp)
        self.fpr = self._import.imports[0][0]
        self._key = self.ctx.get_key(self.fpr)

    def __repr__(self):
        return "<PublicKey: %s <%s>>: %s" % (self.name, self.email, self.fpr)

    def encrypt(self, data):
        data = BytesIO(bytes(data, "ascii"))
        ciphertext = BytesIO()
        self.ctx.encrypt([self._key], gpgme.ENCRYPT_ALWAYS_TRUST,
                         data, ciphertext)
        ciphertext.seek(0)
        return ciphertext.read()

    def export(self, fp):
        self.ctx.export(self.fpr, fp)

    @property
    def key(self):
        fp = BytesIO()
        self.export(fp)
        fp.seek(0)
        return fp.read()

    @property
    def expire(self):
        expire = 0
        for sk in self._key.subkeys:
            if sk.expires > expire:
                expire = sk.expires
        if expire:
            return datetime.fromtimestamp(expire)

    @property
    def ids(self):
        return [sk.keyid for sk in self._key.subkeys]

    @property
    def name(self):
        return self._key.uids[0].name

    @property
    def email(self):
        return self._key.uids[0].email


class PrivateKey:

    def __init__(self, data):
        self.ctx = gpgme.Context()
        self.ctx.armor = False
        self._import = self.ctx.import_(BytesIO(bytes(data, "ascii")))

    def decrypt(self, data):
        plaintext = BytesIO()
        ciphertext = BytesIO(data)
        self.ctx.decrypt(ciphertext, plaintext)
        plaintext.seek(0)
        return plaintext.read()
