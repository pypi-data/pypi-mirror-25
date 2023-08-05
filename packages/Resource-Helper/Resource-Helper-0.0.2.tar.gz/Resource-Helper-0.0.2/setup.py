from setuptools import setup, find_packages

setup(
    name='Resource-Helper',
    version='0.0.2',
    description='A project that manage resource data',
    author='jmg7173',
    author_email='jmg7173@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    url='https://gitlab.com/heumtax/resource_helper/',
    packages={'resource_helper': 'resource_helper'},
    install_requires=['requests'],
    python_requires='>=3.5',
    license='MIT',
)