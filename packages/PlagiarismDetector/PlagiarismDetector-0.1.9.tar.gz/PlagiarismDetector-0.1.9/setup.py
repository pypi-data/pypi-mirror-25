from setuptools import setup


setup(
    name='PlagiarismDetector',
    version='0.1.9',
    author='Ayush Singh',
    author_email='singhay@ccs.neu.edu',
    packages=['plagiarismdetector', 'tests'],
    url='http://pypi.python.org/pypi/PlagiarismDetector/',
    license='MIT',
    package_data={
            '': ['LICENSE.txt', 'README.rst']
        },
    entry_points={
           'console_scripts': [
               'plagiarismdetector = plagiarismdetector:main',
           ],
        },
    description='Calculates percentage of N-Tuples from file1 found in another file2',
    long_description=open('README.rst').read()
)