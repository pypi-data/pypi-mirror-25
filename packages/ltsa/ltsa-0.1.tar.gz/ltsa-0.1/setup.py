from setuptools import setup

setup(
    name='ltsa',
    version='0.1',
    description='Package for local tangent space alignment manifold learning.',
    author= "Charles Gadd",
    author_email= "cwlgadd@gmail.com",
    packages=['ltsa', 'ltsa.utils', 'ltsa.testing', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.txt').read(),
    zip_safe=False,
)
