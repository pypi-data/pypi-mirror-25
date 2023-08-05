from setuptools import setup, find_packages


setup(
    name='XYXY',
    version='0.0.1a2',
    description='Datasets manager for Python',
    url='https://github.com/xyxy-io/xyxy',
    author='Artiem Krinitsyn',
    author_email='artiemq@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',

        'Intended Audience :: Science/Research',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3',
    keywords='dataset research',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['pymongo']
    )
