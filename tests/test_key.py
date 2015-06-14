import unittest
from io import BytesIO

from keyserver.key import PublicKey, PrivateKey

# {{{
pub = """-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mI0EVX2+IQEEAL3TABO0HqcHFD3uGnp9FQeuorE3vL7GGGvSkS9BhOG9r8Hu4Bq5
txu4uVxH4Gcx/ksVNCP8nChYvbs7qBdxZPpDzKEzIeFKsGU3oVwbmIoXMiZC1WHx
p2y/dwUKWG5bUlmbU4dBEBjpbBF0IhoNkWzfWG/w+YF/IC8FWrjO4uc7ABEBAAG0
GlRlc3RpbmcgPHRlc3RAZXhhbXBsZS5uZXQ+iL4EEwECACgFAlV9viECGwMFCV38
DwAGCwkIBwMCBhUIAgkKCwQWAgMBAh4BAheAAAoJEAyCAiR3+vU3uwUD/03RRGzE
jsZf+keS2epefTORgBUgPJ1bXpN3wv5zaBCUUDtAzjLzwIyVIe5irEJWBkIRgtHE
MXS40N8cOwNmAyJ95UsrlCFI5FJ5So82N0EgZo2VGaF1fYhHMLcAXc8xaiERJ/A9
r8M7UNeZOa+j08vEWhwhbNZEI+rD91ddKimpuI0EVX2+IQEEAKtrH9S6Vyba0bS1
PQyicwtMnw50bcroY5vbK8JtAknDmzrd/xpLTToUu31u/z4zWu6kql3H/IJk7+rq
zjkTzZDn4uoqn4O7652v57yWm79tkTunPUNvChCu5OeGCp5qYIwhcUnqK0tPqGRJ
MuWE+KlhdJuxEv2if3AeONphmiuJABEBAAGIpQQYAQIADwUCVX2+IQIbDAUJXfwP
AAAKCRAMggIkd/r1N6OJA/967pbal7t793+NecoESlBQupndkZf1NBvOxxl3hBVF
85E5zp+wlTn2E/jnEqu7kSt+t+A9sgz1d/81Crsylov2Jgl7GkOblnAJ20zsIEPU
wDce+G3sUq66QUwPV3lxSxMu6Y+zkOIdboxaLs/SiACQI1gxwUo4sPX3+XYC53P3
6A==
=nCE/
-----END PGP PUBLIC KEY BLOCK-----"""

priv = """-----BEGIN PGP PRIVATE KEY BLOCK-----
Version: GnuPG v1

lQHXBFV9viEBBAC90wATtB6nBxQ97hp6fRUHrqKxN7y+xhhr0pEvQYThva/B7uAa
ubcbuLlcR+BnMf5LFTQj/JwoWL27O6gXcWT6Q8yhMyHhSrBlN6FcG5iKFzImQtVh
8adsv3cFClhuW1JZm1OHQRAY6WwRdCIaDZFs31hv8PmBfyAvBVq4zuLnOwARAQAB
AAP/Uxyr93SRSTN9xuHWIRRcHVl2rV5Im0TT033GCKlIu6gYaLKk177Br/cQ3Zkw
5S4L96bohesoGjhEllJ39g+1lGWDOQWmauqdyCpg6TWDnmmfsy/l7dHHYUXvFh5U
9oLib8GUkusEAZ5UToiJIL8VYlknEaW7m3YaxWHK6jcmsbUCAMJnSNjaMl3DFGmF
88zk6HKCmiHcBDyIIxkf0LhkbX4S+MCxULAAOiEJ4BSh8/z78TyXm2EhpUqQqV9q
ufiGQK0CAPn4R1O0kgqm5AXhK850pVI/2dtrpRwEcloEkoPJzkV5apZamquatgM8
QU7x9o43X9ccNztU08yfTMt/xV0vfIcB+IzZ2Hyj93iHEd6C/lGDAVaqHCThcUyV
0ZdbSGamZV2q7ZFpF61VIdb0YpkHjZOMvEmZ0EUDIHenl5omp+xtSaKNtBpUZXN0
aW5nIDx0ZXN0QGV4YW1wbGUubmV0Poi+BBMBAgAoBQJVfb4hAhsDBQld/A8ABgsJ
CAcDAgYVCAIJCgsEFgIDAQIeAQIXgAAKCRAMggIkd/r1N7sFA/9N0URsxI7GX/pH
ktnqXn0zkYAVIDydW16Td8L+c2gQlFA7QM4y88CMlSHuYqxCVgZCEYLRxDF0uNDf
HDsDZgMifeVLK5QhSORSeUqPNjdBIGaNlRmhdX2IRzC3AF3PMWohESfwPa/DO1DX
mTmvo9PLxFocIWzWRCPqw/dXXSopqZ0B2ARVfb4hAQQAq2sf1LpXJtrRtLU9DKJz
C0yfDnRtyuhjm9srwm0CScObOt3/GktNOhS7fW7/PjNa7qSqXcf8gmTv6urOORPN
kOfi6iqfg7vrna/nvJabv22RO6c9Q28KEK7k54YKnmpgjCFxSeorS0+oZEky5YT4
qWF0m7ES/aJ/cB442mGaK4kAEQEAAQAD/ArSqiv/vJCZoJjvbSnW4zrzklf9djsp
SLS79fuCGh1h1Mi24IGeqdhrcQUJP44D/GSfOpnOOSgFyyIYGNTWERSlIwFz0UXx
BhVnJQGGmQx29oZHa08ma0kD5LUmuCrsW0rrzz7MpU+4SQ8kD2K81ZgyVdQfCavC
OfHJmUhD2cabAgDO8OTPNI2jedXpeJAD0f1OMuNdIcbnUtA02dMTSjet/XYKTCCL
+kodJLrZBbjhV20a9aXzmtrkUlTPeuVK3+IfAgDUDmRrCS7vFYTXH6m8i2QvdHVE
kzURkoQ+AdFI24BD6pyjD1ipnLRsXUb6Xhqck7HZi2sx2ISqdWi2VfxxX01XAf0d
qXD/FOY2cSNbwJdK+2h+RForH7uQQzhm+2kwPQlRhL/7EE2hZy1F4u7fA1OD4snt
r1p5r/P1Y2Bab0H7S8N+oLKIpQQYAQIADwUCVX2+IQIbDAUJXfwPAAAKCRAMggIk
d/r1N6OJA/967pbal7t793+NecoESlBQupndkZf1NBvOxxl3hBVF85E5zp+wlTn2
E/jnEqu7kSt+t+A9sgz1d/81Crsylov2Jgl7GkOblnAJ20zsIEPUwDce+G3sUq66
QUwPV3lxSxMu6Y+zkOIdboxaLs/SiACQI1gxwUo4sPX3+XYC53P36A==
=rcc3
-----END PGP PRIVATE KEY BLOCK-----"""
# }}}


class KeyTestCase(unittest.TestCase):

    def test_encrypt_decrypt(self):
        key = PublicKey(pub)
        data = key.encrypt("test data")
        self.assertNotEqual(0, len(data))
        private = PrivateKey(priv)
        decrypted_data = private.decrypt(data)
        self.assertEqual(b"test data", decrypted_data)

    def test_export(self):
        key = PublicKey(pub)
        fp = BytesIO()
        key.export(fp)
        fp.seek(0)
        data = fp.read()
        self.assertFalse(len(data) == 0)
        self.assertFalse(data.startswith(b"----"))

    def test_properties(self):
        key = PublicKey(pub)
        self.assertEqual(2065, key.expire.year)
        self.assertEqual("Testing", key.name)
        self.assertEqual("test@example.net", key.email)
        self.assertEqual("<PublicKey: Testing <test@example.net>>: "
                         "A1FB2F8540F8E694BF48D8AC0C82022477FAF537", repr(key))
