try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

if sys.version_info.major != 3:
    print("""
This package doesn't support Python 2.
You may want to try 'pip3 install python-locker'"""
    )

setup(
    name="python-locker",
    description="A place to keep your valuables.",
    long_description=open("README.rst").read(),
    author="coal0",
    author_email="githubcoal@protonmail.com",
    url="https://github.com/Coal0/Locker",
    download_url="https://github.com/Coal0/Locker/releases/tag/v1.0.0",
    version="1.0.2",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords=[
        "locker",
        "secure",
        "encrypt",
        "storage"
    ],
    packages=["locker"],
    install_requires=["cryptography"],
    python_requires=">=3"
)
