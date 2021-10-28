from setuptools import find_packages, setup

with open("requirements.txt") as f:
    requires = f.read().splitlines()
    requires = requires[: len(requires) - 2]

with open("passivbot/requirements_liveonly.txt") as f:
    requires_passivbot = f.read().splitlines()
    requires.extend(requires_passivbot)

setup(
    name="passivbot_manager",
    version="0.1.3",
    description="Passivbot Manager Library",
    author="BTM",
    url="https://github.com/botthemoon/passivbot-manager",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    zip_safe=True,
)
