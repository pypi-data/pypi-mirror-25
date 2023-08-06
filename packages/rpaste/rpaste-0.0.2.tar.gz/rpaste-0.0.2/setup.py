from distutils.core import setup

version = '0.0.2'
setup(
    name='rpaste',
    packages=['rpaste'],
    version=version,
    description='Code Snippets Uploader',
    author='Anup Pokhrel',
    author_email='virtualanup@gmail.com',
    url='https://github.com/rpaste/rpaste',
    download_url='https://github.com/rpaste/rpaste/archive/{}.tar.gz'.format(
        version),
    keywords=['rpaste', 'paste', 'bin'],
    classifiers=[],
    entry_points={
        "console_scripts": [
            "rpaste=rpaste:main",
        ]
    },
    install_requires=[
    ],
)
