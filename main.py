from time import sleep
import requests
from environs import Env
import logging

if __name__ == '__main__':
    env = Env()
    env.read_env()
    logging.basicConfig(level=logging.INFO)

    dvmn_lp_url = 'https://dvmn.org/api/long_polling/'

    dvmn_token = env('DVMN_TOKEN')
    headers = {'Authorization': f'Token {dvmn_token}'}
    params = {}

    while True:
        try:
            if params:
                response = requests.get(dvmn_lp_url, headers=headers, params=params)
            else:
                response = requests.get(dvmn_lp_url, headers=headers)
            response.raise_for_status()
            logging.info(response.url)

            poll_answer = response.json()
            if poll_answer['status'] == 'timeout':
                params['timestamp'] = poll_answer['timestamp_to_request']
                logging.info(poll_answer)
            elif poll_answer['status'] == 'found':
                params['timestamp'] = poll_answer['last_attempt_timestamp']
                logging.info(poll_answer)
            continue

        except requests.exceptions.ReadTimeout:
            logging.info('Ответ не получен, повторный запрос.')
            continue

        except requests.ConnectionError:
            logging.info('Ошибка соединения, повторная попытка через 60 секунд.')
            sleep(60)
            continue


