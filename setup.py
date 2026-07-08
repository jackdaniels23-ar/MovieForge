from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="movieforge",
    version="1.0.0",
    author="jackdaniels23-ar",
    author_email="your-email@example.com",
    description="MovieForge - Forge your movie collection, watch anywhere",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jackdaniels23-ar/MovieForge",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "flask>=2.0.0",
        "flask-cors>=3.0.0",
        "werkzeug>=2.0.0",
        "gunicorn>=20.0.0",
        "requests>=2.31.0",
        "rich>=13.7.0",
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "movieforge=cli:main",
        ],
    },
)
