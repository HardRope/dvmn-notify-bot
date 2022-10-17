import logging
from time import sleep
from textwrap import dedent

import telegram
import requests
from environs import Env

if __name__ == '__main__':
    env = Env()
    env.read_env()
    logging.basicConfig(level=logging.INFO)

    tg_token = env('TG_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')
    bot = telegram.Bot(token=tg_token)

    dvmn_lp_url = 'https://dvmn.org/api/long_polling/'
    dvmn_token = env('DVMN_TOKEN')
    headers = {'Authorization': f'Token {dvmn_token}'}
    params = {}

    while True:
        try:
            response = requests.get(dvmn_lp_url, headers=headers, params=params)
            response.raise_for_status()

            review_check_result = response.json()

            if review_check_result['status'] == 'timeout':
                params['timestamp'] = review_check_result['timestamp_to_request']
            elif review_check_result['status'] == 'found':
                params['timestamp'] = review_check_result['last_attempt_timestamp']

                if review_check_result['new_attempts'][0]['is_negative']:
                    message_text = f'''
                    Преподаватель проверил Вашу работу {review_check_result['new_attempts'][0]['lesson_title']}.
                    К сожалению, в работе нашлись ошибки.
                    Ссылка на урок: {review_check_result['new_attempts'][0]['lesson_url']}'''

                else:
                    message_text = f'''
                    Преподаватель проверил Вашу работу {review_check_result['new_attempts'][0]['lesson_title']}.
                    Работа принята!
                    Ссылка на урок: {review_check_result['new_attempts'][0]['lesson_url']}'''

                bot.send_message(
                    text=dedent(message_text),
                    chat_id=tg_chat_id,
                )

        except requests.exceptions.ReadTimeout:
            logging.info('Истекло время ожидания, повторный запрос...')
            continue

        except requests.ConnectionError:
            logging.info('Ошибка соединения, повторная попытка через 60 секунд.')
            sleep(60)
            continue
