import os.path
import subprocess

from distutils.core import setup
from distutils.extension import Extension
from distutils.command.build_ext import build_ext
from Cython.Build import cythonize

class prepare_tinydtls(build_ext):
    def run(self):
        def run_command(args):
            print("Running:", " ".join(args))
            subprocess.check_call(args, cwd=os.path.join(os.path.dirname(__file__), "./DTLSSocket/tinydtls"))
        commands = [
            ["git", "submodule", "update", "--init"],
            ["autoconf"],
            ["autoheader"],
            ["./configure", "--without-ecc"],
            ]
        for command in commands:
            run_command(command)
        build_ext.run(self)

cy_build = cythonize([
      Extension("DTLSSocket.dtls",
                ["DTLSSocket/dtls.pyx", "DTLSSocket/tinydtls/dtls.c", "DTLSSocket/tinydtls/crypto.c",
                 "DTLSSocket/tinydtls/ccm.c", "DTLSSocket/tinydtls/hmac.c", "DTLSSocket/tinydtls/netq.c",
                 "DTLSSocket/tinydtls/peer.c", "DTLSSocket/tinydtls/dtls_time.c",
                 "DTLSSocket/tinydtls/session.c", "DTLSSocket/tinydtls/dtls_debug.c",
                 "DTLSSocket/tinydtls/aes/rijndael.c", "DTLSSocket/tinydtls/sha2/sha2.c"],
                include_dirs=['DTLSSocket/tinydtls'],
                define_macros=[('DTLSv12', '1'),
                               ('WITH_SHA256', '1'),
                               ('DTLS_CHECK_CONTENTTYPE', '1'),
                               ('_GNU_SOURCE', '1')],
                undef_macros = [ "NDEBUG" ],
                )])

setup(
    name="DTLSSocket",
    version='0.1.0',
    description = "DTLSSocket is a cython wrapper for tinydtls with a Socket like interface",
    author      = "Jannis Konrad",
    author_email= "Jannis.Konrad@h-brs.de",
    url         = "https://git.fslab.de/jkonra2m/tinydtls-cython",
    py_modules  = [ "DTLSSocket.DTLSSocket"],
    cmdclass    = {"build_ext": prepare_tinydtls},
    ext_modules = cy_build,
    )
