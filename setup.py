import setuptools

with open("README.md", "r") as filehandler:
    long_description = filehandler.read()

setuptools.setup(
    name="covid19-dashboard-pkg-cajo22",
    version="1.0.0",
    author="cajo22",
    description="A dashboard to show COVID-19 statistics and related news articles.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cajo22/covid19-dashboard",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)