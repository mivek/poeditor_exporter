import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="poeditorexporter",
    version="1.0.0",
    author="Jean-Kevin KPADEY",
    author_email="jeankevin@gmail.com",
    description="CLI package to export poeditor translations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests'
    ],
    license='MIT',
    py_modules=['poeditorexporter'],
    url="https://github.com/mivek/poeditor_exporter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='poeditor exporter',
    python_requires='>=3.6',
)
