import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-dataio",
    version="0.0.1",
    author="Fazel Momeni",
    author_email="fzl8747@example.com",
    description="A Django utility for importing and exporting model data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FZl47/django-dataio",
    packages=setuptools.find_packages(),
    install_requires=[
        "openpyxl>=3.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    include_package_data=True,
)