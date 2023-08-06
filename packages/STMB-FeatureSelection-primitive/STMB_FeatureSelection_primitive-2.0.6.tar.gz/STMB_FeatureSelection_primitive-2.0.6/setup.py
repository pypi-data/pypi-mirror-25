# Copyright 2015-2017 The MathWorks, Inc.

# from distutils.core import setup
from setuptools import setup, find_packages
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
        name="STMB_FeatureSelection_primitive",
        version="2.0.6",
        description='A module to call MATLAB from Python',
        author='MathWorks',
        url='http://www.mathworks.com/',
        platforms=['Linux', 'Windows', 'MacOS'],
        packages=[
            'STMB_FeatureSelection_primitive'
        ],
        package_data={'STMB_FeatureSelection_primitive': ['*.ctf']},
        # Executes the custom code above in order to delete the build area.
        cmdclass={'install': InstallRuntime}
    )


