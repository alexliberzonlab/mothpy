import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mothpy",
    version="0.0.1",
    author="Noam Benelli and Alex Liberzon",
    author_email="alex.liberzon@gmail.com",
    description="MothPy allows simulation moth-like navigators in dynamic 2D odour concentration fields spread in turbulent flows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexliberzonlab/mothpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)