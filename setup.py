import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="htb-api-clubby789",
    version="0.0.1",
    author="clubby789@github.com",
    author_email="clubby789@gmaol.com",
    description="A wrapper for the HTB API.",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)