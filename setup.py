from setuptools import find_packages, setup

requires = []

with open("requirements.txt") as f:
    requires.extend(f.read().splitlines())
    requires = requires[: len(requires) - 2]

# with open("bttmbot/requirements_liveonly.txt") as f:
#     requires_bttmbot = f.read().splitlines()
#     requires.extend(requires_bttmbot)

setup(
    name="bttmbot-manager",
    version="0.2",
    description="BTTMBot Manager Library",
    author="BTM",
    license="",
    url="https://github.com/botthemoon/bttmbot-manager",
    packages=find_packages(),
    install_requires=requires,
)
