# ToDo: вынести в константы ключи JSON-настроек, да и все остаьные строки
# ToDo: Прикрутить технологию описания типов параметров (Декораторы)

from playsound3 import playsound
import os
import datetime
import random
import subprocess
import json
from sound import Sound

SETTINGS_FILE = os.sep.join([os.getcwd(),'settings.json'])


def play_sample(file_name, inc_volume = ''):
    """
    воспроизводим звуковой файл
    :param file_name: абсолютное имя файла
    :param inc_volume: надо ли перед проигрыванием усилить громкость
    :return:
    """
    prev_volume = Sound.current_volume()  # записать текущую громкость
    if not prev_volume:
        prev_volume = 20
    #ToDo: подумать о inc_volume == min
    if inc_volume == 'max':
        #ToDo: увеличить громкость на время проигрывания файла
        print('Увеличиваем громкость')
        Sound.volume_max()

    playsound(file_name)
    print(file_name)
    if inc_volume:
        print('Возвращаем громкость')
        Sound.volume_set(prev_volume)

def run_app(app_name, params = ''):
    # запускаем программу
    params = params.split(' ')
    subprocess.Popen([app_name, *params], shell = False)

def run_py_script(py_file_name):
    # Запускаем py-скрипт
    subprocess.Popen(py_file_name)

def last_day_of_month(date_obj):
    # Находим первый день следующего месяца
    if date_obj.month == 12:
        next_month = datetime.datetime(date_obj.year + 1, 1, 1)
    else:
        next_month = datetime.datetime(date_obj.year, date_obj.month + 1, 1)
    # Вычитаем один день
    return next_month - datetime.timedelta(days=1)

def check_period(period_settings):
    """
    Проверяем условия активации
    Если не указан день - весь месяц,
    Если указан месяц или год - текущие
    Если не задан finish, сделать только в день start
    :param period_settings: dict :
				"start": {
					"month": 4,
					"day": 1
				},
				"finish": {
					"month": 4,
					"day": 2
				}
    :return:
    """
    today = datetime.date.today()
    res = False
    #ToDo: Сделать проверку наличия ключей
    if 'start' in period_settings:
        start_year = period_settings['start'].get('year', today.year)
        start_month = period_settings['start'].get('month', today.month)
        start_day = period_settings['start'].get('day', 1)

        if 'finish' in period_settings:
            finish_year = period_settings['finish'].get('year', today.year)
            finish_month = period_settings['finish'].get('month', today.month)
            finish_day = period_settings['finish'].get('day', last_day_of_month(today))
        else:
            finish_year = start_year
            finish_month = start_month
            if 'day' in period_settings['start']:
                #Только указанный день
                finish_day = start_day
            else:
                #Весь месяц
                finish_day = last_day_of_month(today)
        start_date = datetime.date(start_year, start_month, start_day)
        finish_date = datetime.date(finish_year, finish_month, finish_day)
        res = (start_date <= today) and (finish_date >= today)
    else:
        res = False
    return res

def get_absolute_file_name(folder, file_name):
    return os.sep.join([os.getcwd(), *folder, file_name])

def launch_action(folder, actions_settings):
    """
    Выбор и запуск акции
    :param folder: Папка с артифактами по акции
    :param actions_settings: list:
     [
     	{
		    "type": "sound",
			"weight": 10,
			"options": [
                {
                    "file_name": "1.mp3",
                    "volume": "max"
                },
                {
                    "file_name": "2.mp3",
                    "volume": "max"
                }
            ]
		},
		{
			"type": "apps",
			"weight": 1,
			"options": [
                {
                    "file_name": "sheeps.exe",
                    "description": "Запуск windows-овечки"
                }
           ]
		},
		{
            "type": "py_scripts",
            "weight": 2,
            "options": [
                "change_win_palette.py"
            ]
        }
    ]
    :return:
    """
    #ToDo: сделать акции на классах и вызывать общий метод
    weight_list = list(map(lambda x: x["weight"], actions_settings))
    action = random.choices(actions_settings, weights = weight_list)[0]

    print(f'action = {action["type"]}')
    if action["type"] == 'sound':
        file_name = get_absolute_file_name([folder, action], choiced_setting['file_name'])
        play_sample(file_name, choiced_setting.get('volume', ''))
    elif action["type"] == 'apps':
        file_name = get_absolute_file_name([folder, action], choiced_setting['file_name'], )
        run_app(file_name, params = choiced_setting.get('params', ''))
    elif action["type"] == 'py_scripts':
        file_name = get_absolute_file_name([folder, action], choiced_setting['file_name'])
        run_py_script(file_name)

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        jsn_file = open(SETTINGS_FILE, encoding='utf-8')
        try:
            settings = json.loads(jsn_file.read())
            return settings
        except:
            # ToDo: переделать в исключение
            print(f'Кривой JSON-файл с настройками {SETTINGS_FILE}')
        # ToDo: обработать бы валидность
    else:
        # ToDo: переделать в исключение
        print(f'Не найден файл настроек: {SETTINGS_FILE}')


def event_dispatcher():
        settings = load_settings()
        if settings:
            for s in settings['events']:
                if 'activation' in s:
                    if check_period(s['activation']):
                        launch_action(s['folder'], s['actions'])

if __name__ == '__main__':
    event_dispatcher()