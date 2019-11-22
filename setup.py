from setuptools import find_packages, setup

setup(
    name="slideception",
    description="Framework for interactive slide decks in the terminal",
    author="Colin Chan",
    author_email="colinchan@lumeh.org",
    license="MIT",
    url="https://github.com/kalgynirae/slideception",
    version="0.1",
    py_modules=["slideception",],
    python_requires=">=3.8",
    install_requires=["boxing", "ipython", "mistletoe", "Pygments",],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
    ],
)
