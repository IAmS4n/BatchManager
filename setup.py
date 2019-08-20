import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BatchManager",
    version="0.0.1",
    author="Ehsan Montahaei",
    author_email="ehsan.montahaei@gmail.com",
    description="A general purpose batch manager.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ehsan-MAE/BatchManager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
