from setuptools import setup


__VERSION__ = "1.0.1"

setup(
    name="pyaap",
    version=__VERSION__,
    description="Yet Another Argument Parser",
    url="https://github.com/kaniblu/pyaap",
    author="Kang Min Yoo",
    author_email="k@nib.lu",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    keywords="argparse argument options",
    packages=["yaap"],
    install_requires=["configargparse"]
)