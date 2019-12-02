from pathlib import Path
from setuptools import setup

readme = Path("README.md").read_text()

setup(
    name="slideception",
    version="0.1.0",
    author="Colin Chan",
    author_email="colinchan@lumeh.org",
    description="Framework for interactive slide decks in the terminal",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/kalgynirae/slideception",
    py_modules=["slideception",],
    python_requires=">=3.8",
    install_requires=["boxing", "ipython", "mistletoe", "Pygments",],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Multimedia :: Graphics :: Presentation",
        "Topic :: Terminals",
    ],
)
