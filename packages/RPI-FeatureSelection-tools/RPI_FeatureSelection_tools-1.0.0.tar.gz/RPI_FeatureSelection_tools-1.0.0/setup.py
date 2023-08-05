# Copyright 2015-2016 The MathWorks, Inc.

# from distutils.core import setup
from setuptools import setup
from distutils.command.clean import clean
from distutils.command.install import install

class InstallRuntime(install):
    # Calls the default run command, then deletes the build area 
    # (equivalent to "setup clean --all").
    def run(self):
        install.run(self)
        c = clean(self.distribution)
        c.all = True
        c.finalize_options()
        c.run()

if __name__ == '__main__':

    setup(
        name="RPI_FeatureSelection_tools",
        version="1.0.0",
        description='RPI Feature Selection toolbox, the initial version with 4 primitives including the baseline methods',
        author='Keyi Liu',
	    author_email='liuk7@rpi.edu',
        url='https://www.ecse.rpi.edu/~cvrl/liuk',
        platforms=['Linux', 'Windows', 'MacOS'],
        packages=[
            'RPI_FeatureSelection_tools'
        ],
        package_data={'RPI_FeatureSelection_tools': ['*.ctf']},
        # Executes the custom code above in order to delete the build area.
        cmdclass={'install': InstallRuntime}
    )

