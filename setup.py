import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="forecastpy",
    version="1.0.2",
    author="Cosimo Matteini",
    author_email="dev.matteini@gmail.com",
    description="A python package to interact with the OpenWeatherAPI in a simple and fast way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devmatteini/forecastpy",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keywords="weather forecast openweathermap"
)
