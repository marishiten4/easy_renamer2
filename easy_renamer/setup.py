from setuptools import setup

setup(
    name="EasyRenamer",
    version="0.1",
    packages=["src", "src.ui", "src.core", "src.utils"],
    install_requires=["PyQt5", "Pillow", "exifread"],
    entry_points={
        "console_scripts": [
            "easy_renamer=src.main:main"
        ]
    }
)
