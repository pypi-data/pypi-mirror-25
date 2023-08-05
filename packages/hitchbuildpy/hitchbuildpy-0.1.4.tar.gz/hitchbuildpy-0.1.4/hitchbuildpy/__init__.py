from commandlib import CommandPath, Command
from path import Path
import hitchbuild


class PythonBuild(hitchbuild.HitchBuild):
    def __init__(self, version):
        super(PythonBuild, self).__init__()
        self._version = version
    
    @property
    def basepath(self):
        return self.path.share.joinpath("python{0}".format(self._version))
    
    @property
    def bin(self):
        return CommandPath(self.basepath.joinpath("bin"))
    
    def trigger(self):
        return self.monitor.non_existent(self.basepath)

    def build(self):
        if self.basepath.exists():
            self.basepath.rmtree(ignore_errors=True)
        self.basepath.mkdir()
        
        Command(
            Path(__file__).dirname().abspath().joinpath("bin", "python-build")
        )(self._version, self.basepath).run()

        self.bin.easy_install("--upgrade", "setuptools").run()
        self.bin.easy_install("--upgrade", "pip").run()
        self.bin.pip("install", "virtualenv", "--upgrade").without_env("PIP_REQUIRE_VIRTUALENV").run()
        self.verify()
    
    def verify(self):
        assert self._version in self.bin.python("--version").output()


@hitchbuild.needs(base_python=PythonBuild)
class VirtualenvBuild(hitchbuild.HitchBuild):
    def __init__(self, base_python):
        super(VirtualenvBuild, self).__init__()
        self._requirements = {"base_python": base_python}

    @property
    def bin(self):
        return CommandPath(self.basepath.joinpath("bin"))

    @property
    def basepath(self):
        return self.path.build.joinpath(self.name)

    def trigger(self):
        return self.monitor.non_existent(self.basepath)

    def build(self):
        if self.basepath.exists():
            self.basepath.rmtree(ignore_errors=True)
        self.basepath.mkdir()
        self._requirements['base_python'].bin.virtualenv(self.basepath).run()
        self.verify()
    
    def verify(self):
        assert self._requirements['base_python']._version in self.bin.python(
            "-c", "import sys ; sys.stdout.write(sys.version)"
        ).output()
        
        

__version__ = "0.1.4"
