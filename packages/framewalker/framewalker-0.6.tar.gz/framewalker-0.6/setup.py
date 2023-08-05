from setuptools import setup

setup(
    name='framewalker',
    version='0.6',
    url='https://github.com/stefanbie/FrameWalker',
    install_requires=[
        'peewee',
        'PyMySQL',
    ],
    py_modules=['Timings','IFrame', 'JavaScript','DB']
    )
