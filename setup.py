from distutils.core import setup

setup(
    name="streakimage",
    version="1.1",
    description="Python Class for ITEX-Files",
    author="nicohfdtz",
    url="https://github.com/nicohofdtz/streakimage",
    packages=["streakimage"],
    package_data={"streakimage": ["correction_data/*"]},
    py_modules=["streakimage/streak_image"],
)
