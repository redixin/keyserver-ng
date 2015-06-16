import unittest
import shutil
import socket
import tempfile
import configparser
import subprocess
import os.path
import time
import urllib
from urllib import request


def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def wait_for_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        e = s.connect_ex(("localhost", port))
        if e:
            time.sleep(0.1)
        else:
            s.close()
            return


class DBFileTestCase(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.tmp_path = tempfile.mkdtemp("keyserver_ng_tests")
        print(self.tmp_path)
        port = get_free_port()
        self.url = "http://localhost:%s/" % port
        logfile = os.path.join(self.tmp_path, "server.log")
        config = configparser.ConfigParser()
        cfg_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                "..", "..", "etc", "config.ini")
        config.read(cfg_file)
        config["database"]["module"] = "keyserver.db"
        config["database"]["path"] = os.path.join(self.tmp_path, "db")
        config["mailer"]["module"] = "keyserver.fake_mailer"
        config["logging"]["file"] = logfile
        config["keyserver"]["listen_addr"] = "localhost"
        config["keyserver"]["listen_port"] = str(port)
        new_cfg_path = os.path.join(self.tmp_path, "config.ini")
        with open(new_cfg_path, "w") as conf:
            config.write(conf)
        self.server_out = open(os.path.join(self.tmp_path, "out.log"), "w+")
        self.server_err = open(os.path.join(self.tmp_path, "err.log"), "w+")
        self.server = subprocess.Popen(["keyserver-ng", new_cfg_path],
                                       stdout=self.server_out,
                                       stderr=self.server_err)
        wait_for_port(port)

    @classmethod
    def tearDown(self):
        self.server.terminate()
        self.server_out.seek(0)
        self.server_err.seek(0)
        print(self.server_out.read())
        print(self.server_err.read())
        shutil.rmtree(self.tmp_path)

    def test_upload_400(self):
        data = urllib.parse.urlencode({"lol": "ok"}).encode("ascii")
        with self.assertRaises(urllib.error.HTTPError) as e:
            request.urlopen(self.url + "pks/add", data)
        self.assertEqual(e.exception.code, 400)
