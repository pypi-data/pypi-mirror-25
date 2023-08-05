import os
import glob
from setuptools import setup, find_packages
import shutil

from setuptools.command.develop import develop
from setuptools.command.install import install

def _post_install():
    print("Installing styles...")
    import matplotlib as mpl

    # ~ # ref  ->  matplotlib/style/core
    BASE_LIBRARY_PATH = os.path.join(mpl.get_data_path(), 'stylelib')
    STYLE_PATH = os.path.join(os.getcwd(),'lifeqstyles', 'mplstyles')
    STYLE_EXTENSION = 'mplstyle'
    style_files = glob.glob(os.path.join(STYLE_PATH, "*.%s" % (STYLE_EXTENSION)))

    print(BASE_LIBRARY_PATH)
    print(STYLE_PATH)
    print(os.path.join(STYLE_PATH, "*.%s" % (STYLE_EXTENSION)))
    print(style_files)

    for _path_file in style_files:
        _, fname = os.path.split(_path_file)
        dest = os.path.join(BASE_LIBRARY_PATH, fname)
        shutil.copy(_path_file, dest)
        print("%s style installed" % (fname))


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        develop.run(self)
        self.execute(_post_install, [],
                     msg="Running post install task")

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        self.execute(_post_install, [],
                     msg="Running post install task")

from lifeqstyles._version import __version__

setup(
    name='lifeqstyles',
    version=__version__,
    description="Standard Matplotlib LifeQ and HealthQ plot styles.",
    long_description=open("README.md").read(),
    classifiers=[
        "Programming Language :: Python"
    ],
    keywords='python lifeq heatlthq matplotlib styles stylesheet',
    author='Salomon',
    author_email='salomon@healthqtech.com',
    url='https://bitbucket.org/HealthQ/lifeqstyles',
    license='proprietary',
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    namespace_packages=[],
    zip_safe=False,
    install_requires=[
        'setuptools', 'matplotlib'
    ],
    dependency_links=[
    ],
    extras_require={
        'develop': ['nose', 'matplotlib']
    },
    cmdclass={
        'install': PostInstallCommand,
        'develop': PostDevelopCommand
    },
)

