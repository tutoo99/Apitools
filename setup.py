from setuptools import setup, find_namespace_packages

setup(
    name="pyside6-enterprise-framework",
    version="0.1.0",
    packages=find_namespace_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PySide6>=6.0.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="PySide6 企业级桌面应用框架",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pyside6-enterprise-framework",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
) 