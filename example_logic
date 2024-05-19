import datetime

if __name__ == '__main__':
    """Библиотеки Фромтек"""
    from task3 import lib_fromtech

    nn = lib_fromtech.FromtechNetLibrary()
    nlu = lib_fromtech.FromtechNluLibrary()
    nv = lib_fromtech.FromtechVoiceLibrary()
    InvalidCallStateError = lib_fromtech.InvalidCallStateError
    check_call_state = lib_fromtech.check_call_state

"""Тайминги для спикера по юнитам"""

hello_unit_timing = {'no_input_timeout': 2700,
                     'recognition_timeout': 6000,
                     'speech_complete_timeout': 700,
                     'asr_complete_timeout': 700,
                     'interruption_no_input_timeout': 50}

work_type_unit_timing = {'no_input_timeout': 4500,
                         'recognition_timeout': 90000,
                         'speech_complete_timeout': 1150,
                         'asr_complete_timeout': 1150,
                         'interruption_no_input_timeout': 800}

can_callback_unit_timing = {'no_input_timeout': 4000,
                            'recognition_timeout': 100000,
                            'speech_complete_timeout': 1300,
                            'asr_complete_timeout': 1300,
                            'start_timeout': 1000,
                            'interruption_no_input_timeout': 2000}

"""Паттерны распознавания"""
####################################Hello_Unit
hello_unit_entity_list = [
    "voicemail",
    "who_is_it",
    "what_do",
    "not_sure",
    "not_boss",
    "repeat",
    "dont_disturb",
    "confirm",
    "robot"
]

hello_unit_entity_interruption_list = [
    "voicemail",
    "who_is_it",
    "what_do",
    "not_sure",
    "not_boss",
    "repeat",
    "dont_disturb",
    "robot"
]

##################################Work_Type_Unit
work_type_unit_entity_list = [
    "facade",
    "roof",
    "not_sure",
    "both",
    "repeat",
    "robot"
]

work_type_unit_entity_interruption_list = [
    "facade",
    "roof",
    "not_sure",
    "both",
    "repeat",
    "robot"
]

##################################Work_Type_Unit
can_callback_unit_entity_list = [
    "repeat",
    "callback",
    "confirm",
    "robot"
]

can_callback_unit_entity_interruption_list = [
    "repeat",
    "callback",
    "confirm",
    "robot"
]


def main():
    """Первая функция, создающая звонок"""
    nn.call('+7' + nn.dialog['msisdn'], entry_point='main_online_container',
            # Функция, с которой начать звонок когда возьмут трубку
            on_success_call='after_call_succes',  # Функция обработки успешного звонка после завершения
            on_failed_call='after_call_fail',  # Функция обработки неуспешного звонка после завершения
            )


def main_online_container():
    """Функция - обёртка, обрабатывающая возникающие исключения, входная точка при начале звонка"""
    try:
        now = datetime.datetime.now() + datetime.timedelta(hours=3)
        nn.env('start_time_str',
               str(now))  # В env start_time_str записываем текущее время по МСК (чтобы запомнить время начала звонка)
        main_online()
    except InvalidCallStateError:  # Обработка исключения InvalidCallStateError, возникающее при завершении звонка
        nn.log("Звонок завершен, пропускается выполнение функций")
    finally:  # Первичная обработка после завершения звонка
        nn.env('duration', nv.get_call_duration())  # Запоминаем длительность звонка
        nn.env('call_transcript',
               nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT))  # Записываем транскрипцию


def main_online():
    """Функция, где инициализируются переменные, включается фоновый шум и тп"""
    nn.log('Новый звонок, начало логики main_online')
    nv.background('office')  # Включение фонового шума
    return hello_unit()


#  HELLO_UNIT

@check_call_state(
    nv)  # Декоратор, проверяющий перед вызвовом функции - сбросили звонок или нет. Если звонок сбросили - вызовет исключение InvalidCallStateError
def hello_unit(*prompts):
    nn.log('unit', 'hello_unit')
    """Функция распознавания речи и озвучивания переданных фраз."""
    nv.set_default('listen', hello_unit_timing)
    with nv.listen((  # Запуск распознавания
            hello_unit_entity_interruption_list,  # Список сущностей для перебивания
            None, None, 'AND'),  # Дополнительные параметры перебивания (константа)
            entities=hello_unit_entity_list  # Список сущностей для распознавания
    ) as r:
        for prompt in prompts:  # Цикл, в котором озвучиваем переданные промпты
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return hello_logic(r)


@check_call_state(nv)
def hello_logic(r):
    """Функция обработки сказанной фразы"""
    nn.log("hello_logic")
    if nn.counter('hello_logic', '+') >= 100:
        nn.log('Recursive usage')
        return

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('hello_null_counter', '+') <= 1:
            return hello_unit('hello_null_prompt')
        return hangup_hull_prompt()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return hello_unit('hello_default_prompt')

    if r.has_entity('real_human'):
        if r.entity('real_human') == "true":
            nn.log('condition', 'real_human=true')
            return hello_unit('hello_main_prompt')

    if r.has_entity('voicemail'):
        if r.entity('voicemail') == "true":
            nn.log('condition', 'voicemail=true')
            return hangup_voicemail()

    if r.has_entity('who_is_it'):
        if r.entity('who_is_it') == "true":
            nn.log('condition', 'who_is_it=true')
            return hello_unit('hello_who_are_we_prompt')

    if r.has_entity('what_do'):
        if r.entity('what_do') == "true":
            nn.log('condition', 'what_do=true')
            return hello_unit('hello_what_do_prompt')

    if r.has_entity('not_sure'):
        if r.entity('not_sure') == "true":
            nn.log('condition', 'not_sure=true')
            return can_callback_unit('can_callback_main_prompt')

    if r.has_entity('not_boss'):
        if r.entity('not_boss') == "true":
            nn.log('condition', 'not_boss=true')
            return can_callback_unit('can_callback_main_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == "true":
            nn.log('condition', 'repeat=true')
            return hello_unit('hello_repeat_prompt')

    if r.has_entity('dont_disturb'):
        if r.entity('dont_disturb') == "true":
            nn.log('condition', 'dont_disturb=true')
            return hangup_dont_disturb_prompt()

    if r.has_entity('confirm'):
        if r.entity('confirm') == "true":
            nn.log('condition', 'confirm=true')
            return work_type_unit('work_type_main_prompt')
        if r.entity('confirm') == "false":
            nn.log('condition', 'confirm=true')
            return hangup_goodbye_prompt()

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return hello_unit('hello_robot_prompt')


# //--//--//--//--//--//--//


# WORK_TYPE_UNIT

@check_call_state(nv)
def work_type_unit(*prompts):
    nn.log('unit', 'work_type_unit')
    """Функция распознавания речи и озвучивания переданных фраз."""
    nv.set_default('listen', work_type_unit_timing)
    with nv.listen((
            work_type_unit_entity_interruption_list,
            None, None, 'AND'),
            drop_ni_utterance=True,
            entities=work_type_unit_entity_list
    ) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return work_type_logic(r)


@check_call_state(nv)
def work_type_logic(r):
    nn.log("work_type_logic")
    if nn.counter('work_type_logic', '+') >= 100:
        nn.log('Recursive usage')
        return

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('work_type_null_counter', '+') <= 1:
            return work_type_unit('work_type_null_prompt')
        return hangup_hull_prompt()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return work_type_unit('work_type_default_prompt')

    if r.has_entity('facade'):
        if r.entity('facade') == "true":
            nn.log('condition', 'facade=true')
            return hangup_callback_prompt()

    if r.has_entity('roof'):
        if r.entity('roof') == "true":
            nn.log('condition', 'roof=true')
            return hangup_callback_prompt()

    if r.has_entity('both'):
        if r.entity('both') == "true":
            nn.log('condition', 'both=true')
            return hangup_callback_prompt()

    if r.has_entity('not_sure'):
        if r.entity('not_sure') == "true":
            nn.log('condition', 'not_sure=true')
            return can_callback_unit('can_callback_main_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == "true":
            nn.log('condition', 'repeat=true')
            return work_type_unit('work_type_repeat_prompt')

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return work_type_unit('work_type_robot_prompt')


# //--//--//--//--//--//--//

# CAN_CALLBACK_UNIT

@check_call_state(nv)
def can_callback_unit(*prompts):
    nn.log('unit', 'can_callback_unit')
    """Функция распознавания речи и озвучивания переданных фраз."""
    nv.set_default('listen', can_callback_unit_timing)
    with nv.listen((
            can_callback_unit_entity_interruption_list,
            None, None, 'AND'),
            drop_ni_utterance=True,
            entities=can_callback_unit_entity_list
    ) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return can_callback_logic(r)


@check_call_state(nv)
def can_callback_logic(r):
    nn.log("can_callback_logic")
    if nn.counter('can_callback_logic',
                  '+') >= 100:  # счётчик заходов в логику на случай рекурсии для избежания ситуации с циклированием робота, например, другим роботом
        nn.log('Recursive usage')
        return

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('can_callback_null_counter', '+') <= 1:
            return can_callback_unit('can_callback_null_prompt')
        return hangup_hull_prompt()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return can_callback_unit('can_callback_default_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == "true":
            nn.log('condition', 'repeat=true')
            return can_callback_unit('can_callback_repeat_prompt')

    if r.has_entity('confirm'):
        if r.entity('confirm') == "true":
            nn.log('condition', 'confirm=true')
            return hangup_callback_prompt()
        if r.entity('confirm') == "false":
            nn.log('condition', 'confirm=true')
            return hangup_not_callback_prompt()

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return can_callback_unit('can_callback_robot_prompt')


# //--//--//--//--//--//--//

# HANGUP_UNIT

def hangup_dont_disturb_prompt():
    nn.log('unit', 'hangup_dont_disturb')
    nv.say('hangup_dont_disturb_prompt')
    nn.env("set_output", "Не беспокоить")
    nv.hangup()
    return


def hangup_callback_prompt():
    nn.log('unit', 'hangup_callback')
    nv.say('hangup_callback_prompt')
    nn.env("set_output", "Надо перезвонить")
    nv.hangup()
    return


def hangup_goodbye_prompt():
    nn.log('unit', 'hangup_goodbye')
    nv.say('hangup_goodbye_prompt')
    nn.env("set_output", "Надо перезвонить")
    nv.hangup()
    return


def hangup_hull_prompt():
    nn.log('unit', 'hangup_hull')
    nv.say('hangup_hull_prompt')
    nn.env("set_output", "Тишина")
    nv.hangup()
    return


def hangup_not_callback_prompt():
    nn.log('unit', 'hangup_not_callback')
    nv.say('hangup_not_callback_prompt')
    nn.env("set_output", "Не перезванивать")
    nv.hangup()
    return


def hangup_voicemail():
    nn.log('unit', 'hangup_voicemail')
    nn.env("set_output", "Автоответчик")
    nv.hangup()
    return


# //--//--//--//--//--//--//

def after_call_succes():
    """Функция, отрабатывающая после завершения звонка, где взяли трубку"""
    pass


def after_call_fail():
    """Функция, отрабатывающая после завершения звонка, где не взяли трубку"""
    pass
