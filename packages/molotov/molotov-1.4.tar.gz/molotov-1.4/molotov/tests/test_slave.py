import os
from molotov import __version__
from molotov.slave import main
from molotov.tests.support import TestLoop, dedicatedloop, set_args


_REPO = 'https://github.com/loads/molotov'


class TestSlave(TestLoop):
    @dedicatedloop
    def test_main(self):
        with set_args('moloslave', _REPO, 'test') as out:
            main()

        if os.environ.get("TRAVIS") is not None:
            return
        output = out[0].read()
        self.assertTrue('Preparing 1 worker...' in output, output)
        self.assertTrue('OK' in output, output)

    @dedicatedloop
    def test_fail(self):
        with set_args('moloslave', _REPO, 'fail'):
            self.assertRaises(Exception, main)

    @dedicatedloop
    def test_version(self):
        with set_args('moloslave', '--version') as out:
            try:
                main()
            except SystemExit:
                pass
        version = out[0].read().strip()
        self.assertTrue(version, __version__)
