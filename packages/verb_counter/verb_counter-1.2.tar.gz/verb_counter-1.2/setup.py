from setuptools import setup, find_packages
from os.path import join, dirname
import verb_counter

setup(
    name='verb_counter',
    version=verb_counter.__version__,
    packages=find_packages(),
    author='Vladimir Aleshin',
    author_email='rancvova@gmail.com',
    url='https://github.com/Ranc58/verbs_counter',
    license='MIT License',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    entry_points={
        'console_scripts':
            ['verbs = verb_counter.verb_counter:output_to_cli']
    },
    install_requires=[
        'nltk==3.2.4'
    ],
    test_suite='tests',
)
