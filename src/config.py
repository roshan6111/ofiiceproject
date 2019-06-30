# default config
class BaseConfig(object):
    DEBUG = False
    AUTH_KEY = 'paymatez2p'
    DATABASE_URL = 'mongodb://admin:codespider@localhost:27017/'
    # REMOTE_FILE_PATH = 'http://52.221.212.204:3000/uploads/BankStatements/'
    REMOTE_FILE_PATH = 'http://localhost:6000/static/serverFiles/'
    LOCAL_FILE_PATH = 'DownloadFiles/'
    LOCAL_FILE_PATH_TESTING = '../DownloadFiles/'
