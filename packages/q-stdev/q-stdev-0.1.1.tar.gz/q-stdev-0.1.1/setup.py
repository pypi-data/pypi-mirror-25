from setuptools import setup, find_packages


setup(
    name='q-stdev',
    version='0.1.1',
    url='https://github.com/coddingtonbear/q-stdev',
    description=(
        'Adds a new `stdev` aggregate to Q (textasdata).'
    ),
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[],
    packages=find_packages(),
    entry_points={
        'q_aggregates': {
            'stdev = q_stdev:StDev'
        }
    }
)
