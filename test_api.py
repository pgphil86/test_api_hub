import os
import requests
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')
REPO_NAME = os.getenv('REPO_NAME')

logging.debug(f'GITHUB_TOKEN: {GITHUB_TOKEN}')
logging.debug(f'GITHUB_USERNAME: {GITHUB_USERNAME}')
logging.debug(f'REPO_NAME: {REPO_NAME}')

if not all([GITHUB_TOKEN, GITHUB_USERNAME, REPO_NAME]):
    logging.error('Не все переменные установлены.')
    raise ValueError('Не все переменные установлены.')


def create_repo():
    """
    Функция для создания тестового репозитория.
    Если необходимо изменить приватность репозитория,
    то надо изменить пункт private(True=приватный).
    """
    url = "https://api.github.com/user/repos"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'name': REPO_NAME,
        'private': False
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        logging.info(f'{REPO_NAME} создан успешно.')
    else:
        logging.error('Ошибка создания репозитория: '
                      f'{response.status_code} - {response.text}')


def check_repo():
    """
    Функция для проверки тестового репозитория.
    """
    url = f'https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        logging.info(f'{REPO_NAME} существует.')
    elif response.status_code == 404:
        logging.warning(f'{REPO_NAME} отсутствует.')
    else:
        logging.error('Ошибка проверки: '
                      f'{response.status_code} - {response.text}')


def delete_repo():
    """
    Функция для удаления тестового репозитория.
    """
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}"
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        logging.info(f'{REPO_NAME} удалён.')
    else:
        logging.error('Ошибка при удалении: '
                      f'{response.status_code} - {response.text}')


create_repo()
check_repo()
delete_repo()
