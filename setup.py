import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="PyHackTheBox",
    version="0.2.0",
    author="clubby789@github.com",
    author_email="clubby789@gmail.com",
    description="A wrapper for the Hack The Box API.",
    long_description=long_description,
    url="https://github.com/clubby789/htb-api",
    project_urls={
        "Documentation": "https://pyhackthebox.readthedocs.io/en/latest/"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["hackthebox"],
    python_requires='>=3.8',
    install_requires=[
        "requests==2.25.1",
        "python-dateutil==2.8.1"
    ],
    long_description_content_type='text/markdown'
)
