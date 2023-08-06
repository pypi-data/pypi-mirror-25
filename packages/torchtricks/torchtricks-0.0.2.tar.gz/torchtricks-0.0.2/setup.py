from setuptools import setup
# to deploy
# python setup.py sdist bdist_wheel upload
setup(
    name='torchtricks',
    version='0.0.2',
    description='PyTorch trainers, datasets, criterion, and utility functions',
    url='https://github.com/A-Jacobson/TorchTricks',
    download_url='https://github.com/A-Jacobson/TorchTricks/archive/0.0.1.tar.gz',
    license='MIT',
    python_requires='>=3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6'
    ],
    packages=['torchtricks'],
    # install_required=['pytorch>=version']
)
