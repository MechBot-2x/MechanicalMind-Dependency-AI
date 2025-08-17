from setuptools import setup, find_packages

setup(
    name="mechanicalmind",
    version="3.0.1",
    description="MechanicalMind Dependency AI",
    author="MechBot-2x",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.25.1",
        "pyyaml>=6.0",
        "sqlalchemy>=1.4.0",
        "click>=8.0.0",
        "django>=4.2.16",
    ],
)
