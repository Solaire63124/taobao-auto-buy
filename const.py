import os

PROJ_PATH = os.getcwd()
TAOBAO_URL = 'https://www.taobao.com/'
COOKIE_SAVE_PATH = f'{PROJ_PATH}/data'
COOKIE_FILE = f'{COOKIE_SAVE_PATH}/cookies.json'
LOGIN_RETRYS = 20
LOGIN_TIMEOUT = 500