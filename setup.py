# from setuptools import find_packages
from setuptools import setup

setup(
    name="streakimage",
    version="2.3.1",
    description="Python Class for streak camera files.",
    author="Nico Hofeditz",
    author_email="nicohfdtz@gmail.com",
    url="https//github.com/nicohfdtz/streakimage",
    packages=["streakimage"],
    package_data={"streakimage": ["correction_data/*", "streakimage.ini"]},
)