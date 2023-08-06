from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='pycent',
    version="1.0",
    description='Calculate the percentage of a value, or the reverse',
    long_description=readme(),
    author='LordFlashmeow',
    author_email='lordflashmeow@gmail.com',
    url='http://github.com/LordFlashmeow/pycent',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Mathematics',
        ],
    keywords='percent percentage math',
    packages=['pycent'],
    zip_safe=True,
)