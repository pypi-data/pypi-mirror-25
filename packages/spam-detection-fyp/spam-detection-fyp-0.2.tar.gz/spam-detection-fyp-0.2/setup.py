from setuptools import setup

setup(

    name='spam-detection-fyp',    # This is the name of your PyPI-package.
    version='0.2',
    description='This pacage includes some random files which was created for Spam detection in reviews.',
    author='Raheel Riaz',
    author_email='raheelriaz@elitHUB.com',
    url='https://www.python.org/sigs/distutils-sig/',
    package_dir={'': 'utils'},
    scripts=['DBInterfaceGUI.py']                  # The name of your scipt, and also the command you'll be using for calling i
 )