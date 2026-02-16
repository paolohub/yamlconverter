"""
Setup configuration for YAML Excel Converter
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="yamlexcelconverter",
    version="1.0.0",
    author="Paolo Cardamone",
    author_email="",
    description="Convert YAML ↔ Excel with GPG encryption support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/yamlconverter",  # Update with actual URL
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "openpyxl>=3.1.0",
        "tkinterdnd2>=0.3.0",
        "python-gnupg>=0.5.0",
    ],
    entry_points={
        "console_scripts": [
            "yamlconverter=yamlconverter.gui.main:main",
        ],
        "gui_scripts": [
            "yamlconverter-gui=yamlconverter.gui.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "yamlconverter": ["../translations/*.json"],
    },
)
