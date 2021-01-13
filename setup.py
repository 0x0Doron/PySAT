from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pysat',
    version='1.0.0',
    author='Aritz Romo',
    description='User Friendly IT Service Analysis Tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Windows :: Linux :: OSX',
    ],
    python_requires='>=3.6',
)
