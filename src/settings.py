from environs import Env

env = Env()
env.read_env()

# Telegram

# Logging
log_level = env.str('LOG_LEVEL', 'DEBUG').upper()

# MongoDB
mongo_host = env.str('MONGO_HOST', 'localhost')
mongo_port = env.int('MONGO_PORT', 27017)
mongo_database = env.str('MONGO_DB', 'localhost')
mongo_user = env.str('MONGO_USER', '')
mongo_password = env.str('MONGO_PASSWORD', '')

mongo_uri = env.str("MONGO_URI", "mongodb+srv://<username>:<password>@<host>/test?retryWrites=true&w=majority")
mongo_db = env.str('MONGO_DB', 'bots')

docker_image_tag = env.str("DOCKER_IMAGE_TAG", "passivbot-btm:4")
