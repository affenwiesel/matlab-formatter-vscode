from distutils.core import setup
from json import load

with open("package.json", "r") as fp:
    pkg_json = load(fp)

    setup(
        name=pkg_json["name"],
        version=pkg_json["version"],
        description=pkg_json["description"],
        author=pkg_json["publisher"],
        url=pkg_json["repository"]["url"],
        packages=[
            "matlab_formatter",
        ],
        entry_points={
            "console_scripts": [
                "matlab-formatter=matlab_formatter:main",
            ],
        },
    )
