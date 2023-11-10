import setuptools   

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DPMaterial",
    version="0.0.1",
    author="BalaBala",
    author_email=" ",
    description="Batterry Automation Workflow",
    # long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/MumuMaster2021/DPMaterial.git",
    packages=setuptools.find_packages(),
    install_requires=[
        "pydflow>=1.7.83",
        "dpdispatcher",
        "matplotlib",
    ],

    entry_points={
        "console_scripts": [
            "battery = DPMaterial.__main__:main",
        ],
    },
)