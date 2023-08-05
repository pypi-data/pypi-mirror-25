from distutils.core import setup

version = '0.0.2'

setup(
    name='freeipmi',
    packages=['freeipmi'],
    version=version,
    description='Python library for FreeIPMI',
    author='Matteo Cerutti',
    author_email='matteo.cerutti@hotmail.co.uk',
    url='https://github.com/m4ce/freeipmi-python',
    download_url='https://github.com/m4ce/freeipmi-python/tarball/%s' % (
        version,),
    keywords=['freeipmi', 'ipmi'],
    classifiers=[]
)
