from setuptools import find_packages, setup

requires = []

with open("requirements.txt") as f:
    requires.extend(f.read().splitlines())
    requires = requires[: len(requires) - 2]

with open("bttmbot/requirements_liveonly.txt") as f:
    requires_passivbot = f.read().splitlines()
    requires.extend(requires_passivbot)

setup(
    name="passivbot-manager",
    version="0.1.5",
    description="Passivbot Manager Library",
    author="BTM",
    license="",
    url="https://github.com/botthemoon/passivbot-manager",
    packages=find_packages(),
    install_requires=requires,
)
