from setuptools import setup

__VERSION__ = "0.0.2"

setup(
    version=__VERSION__,
    name="joseph_hello_world",
    description="Minimal Hello world plugin for Joseph",
    author="Niek Keijzer",
    author_email="info@niekkeijzer.com",
    url="https://github.com/NiekKeijzer/HelloWorld",
    download_url="https://github.com/NiekKeijzer/HelloWorld/archive/"
                 "{}.tar.gz".format(__VERSION__),
    entry_points={
        'joseph.plugins': [
            'hello_world = src.hello'
        ]
    }
)
