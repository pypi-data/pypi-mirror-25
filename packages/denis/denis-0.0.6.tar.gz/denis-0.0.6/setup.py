from setuptools import setup, find_packages


description = (
    'A thin set of abstractions to perform geometrical operations on '
    'top of the latitude/longitude coordinate system'
)


setup(
    name='denis',
    version='0.0.6',
    description=description,
    url='https://github.com/mozaiques/denis',
    author='Bastien Gandouet',
    author_email='bastien@mozaiqu.es',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=['numpy'],
)
