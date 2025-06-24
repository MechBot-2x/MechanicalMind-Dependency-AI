from setuptools import setup, find_packages

setup(
    name="mechanicalmind_ai",
    version="4.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "django=4.2.22",
        "drf-yasg==1.21.7",
    ],
)
