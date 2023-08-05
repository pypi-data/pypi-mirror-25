from setuptools import setup, Extension
from distutils.command.build_ext import build_ext


class build_ext(build_ext):

    def build_extension(self, ext):
        self._ctypes = isinstance(ext, CTypes)
        return super().build_extension(ext)

    def get_export_symbols(self, ext):
        if self._ctypes:
            return ext.export_symbols
        return super().get_export_symbols(ext)

    def get_ext_filename(self, ext_name):
        if self._ctypes:
            return ext_name + '.so'
        return super().get_ext_filename(ext_name)


class CTypes(Extension):
    pass


cgaddag = CTypes("cgaddag", sources=["src/cgaddag.c", "src/gdg.c"])

setup(name="GADDAG",
      version="0.1.2",
      description="Python wrapper of a C GADDAG implementation",
      author="Jordan Bass",
      author_email="jordan.bass@mykolab.com",
      url="https://github.com/jorbas/GADDAG",
      download_url="https://github.com/jorbas/GADDAG/archive/0.1.2.tar.gz",
      keywords=["gaddag", "trie"],
      package_dir={"": "src"},
      py_modules=["gaddag"],
      ext_modules=[cgaddag],
      cmdclass={"build_ext": build_ext},
      classifiers=[])
