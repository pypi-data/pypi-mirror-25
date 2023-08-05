from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='labelord',
    version='0.0',
    keywords='github labels projects management',
    description='Simple toolkit for manipulating the GitHub labels of multiple repositories.',
    long_description=long_description,
    author='Marek Suchánek',
    author_email='suchama4@fit.cvut.cz',
    license='MIT',
    url='https://github.com/MarekSuchanek/labelord_priv',
    zip_safe=False,
    py_modules=['labelord'],
    entry_points={
        'console_scripts': [
            'labelord = labelord:cli',
        ]
    },
    install_requires=[
        'click',
        'requests',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet',
    ],
)
