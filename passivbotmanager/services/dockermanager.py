import docker

from passivbotmanager.services.logger import logger
from passivbotmanager.settings import docker_image_tag

client = docker.from_env()


def is_image_created():
    try:
        client.images.get(docker_image_tag)
        logger.info("Image found, avoiding creating an image again")
        return True
    except docker.errors.ImageNotFound:
        logger.warning("Image not found")
        return False
    except docker.errros.APIError as e:
        logger.error(f"Docker API error{e}")


def create_passivbot_image():
    logger.info("Building Passivbot image...")
    client.images.build(path="passivbot/", tag=docker_image_tag, nocache=True)
    logger.info("Passivbot image created sucessfully")


def run_bot_container(env: dict, name: str):
    bot_container = client.containers.run(
        docker_image_tag, environment=env, detach=True, name=name
    )
    return bot_container.id


def get_container_name(id: str):
    container = client.containers.get(id)
    name = container.name
    return name
