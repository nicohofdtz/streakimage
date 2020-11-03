from distutils.core import setup

setup(
    name="StreakImage",
    version="1.0",
    description="Python Class for ITEX-Files",
    author="nicohfdtz",
    url="https://github.com/nicohofdtz/streakimage",
    packages=["streakimage"],
    package_data={"streakimage": ["correction_data/*"]},
)
