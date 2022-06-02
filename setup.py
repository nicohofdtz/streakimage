# from setuptools import find_packages
from setuptools import setup
from pathlib import Path

streak_data = [
    str(path.relative_to("streakimage"))
    for path in Path("streakimage/correction_data").rglob("*.npy")
]
streak_data.append("streakimage.ini")

setup(
    name="streakimage",
    version="2.3.6",
    description="Python Class for streak camera files.",
    author="Nico Hofeditz",
    author_email="nicohfdtz@gmail.com",
    url="https//github.com/nicohfdtz/streakimage",
    packages=["streakimage"],
    package_data={"streakimage": streak_data},
)
