from time import sleep
import requests
from environs import Env
import logging
import telegram

def get_response(url, headers, params):
    if params:
        response = requests.get(url, headers=headers, params=params)
    else:
        response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response


def send_message(poll_answer, chat_id):
    if poll_answer['status'] == 'found' and poll_answer['new_attempts'][0]['is_negative']:
        message_text = f'''
Преподаватель проверил Вашу работу {poll_answer['new_attempts'][0]['lesson_title']}.
К сожалению, в работе нашлись ошибки.
Ссылка на урок: {poll_answer['new_attempts'][0]['lesson_url']}'''

    elif poll_answer['status'] == 'found':
        message_text = f'''
Преподаватель проверил Вашу работу {poll_answer['new_attempts'][0]['lesson_title']}.
Работа принята!
Ссылка на урок: {poll_answer['new_attempts'][0]['lesson_url']}'''

    bot.send_message(
        text=message_text,
        chat_id=chat_id,
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    logging.basicConfig(level=logging.INFO)

    tg_token = env('TG_TOKEN')
    chat_id = env('CHAT_ID')
    bot = telegram.Bot(token=tg_token)

    dvmn_lp_url = 'https://dvmn.org/api/long_polling/'
    dvmn_token = env('DVMN_TOKEN')
    headers = {'Authorization': f'Token {dvmn_token}'}
    params = {}

    while True:
        try:
            response = get_response(dvmn_lp_url, headers, params)
            poll_answer = response.json()

            if poll_answer['status'] == 'timeout':
                params['timestamp'] = poll_answer['timestamp_to_request']
            elif poll_answer['status'] == 'found':
                params['timestamp'] = poll_answer['last_attempt_timestamp']
                send_message(poll_answer, chat_id)

        except requests.exceptions.ReadTimeout:
            logging.info('Истекло время ожидания, повторный запрос...')
            continue

        except requests.ConnectionError:
            logging.info('Ошибка соединения, повторная попытка через 60 секунд.')
            sleep(60)
            continue
