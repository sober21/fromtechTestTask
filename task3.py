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

payment_unit_timing = {'no_input_timeout': 4500,
                        'recognition_timeout': 90000,
                        'speech_complete_timeout': 1150,
                        'asr_complete_timeout': 1150,
                        'interruption_no_input_timeout': 800}

tv_unit_timing = {'no_input_timeout': 4500,
                        'recognition_timeout': 90000,
                        'speech_complete_timeout': 1150,
                        'asr_complete_timeout': 1150,
                        'interruption_no_input_timeout': 800}

internet_unit_timing = {'no_input_timeout': 4500,
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

#################################### Hello_Unit
hello_unit_entity_list =[
        "payment_problem",
        "internet_problem",
        "tv_problem",
        "repeat",
        "operator",
        "robot"
        ]

hello_unit_entity_interruption_list =[
        "payment_problem",
        "internet_problem",
        "tv_problem",
        "repeat",
        "operator",
        "robot"
        ]

#################################### Payment_Unit
payment_unit_entity_list = [
    "pay_site",
    "offices",
    "repeat",
    "promise_pay",
    "operator",
    "confirm"
    ]

payment_unit_entity_interruption_list = [
    "pay_site",
    "offices",
    "repeat",
    "promise_pay",
    "operator"
    ]

#################################### Tv_Unit
tv_unit_entity_list = [
    "repeat",
    "robot",
    "confirm",
    "operator"
    ]

tv_unit_entity_interruption_list = [
    "repeat",
    "robot",
    "operator"
    ]

#################################### Internet_Unit
internet_unit_entity_list = [
    "robot",
    "repeat",
    "operator",
    "confirm"
    ]

internet_unit_entity_interruption_list = [
    "robot",
    "repeat",
    "operator",
    ]

#################################### Internet_Green_Unit
internet_green_unit_entity_list = [
    "robot",
    "repeat",
    "operator",
    "confirm"
    ]

internet_green_unit_entity_interruption_list = [
    "robot",
    "repeat",
    "operator",
    ]

#################################### More_Question_Unit
more_question_unit_entity_list = [
        "payment_problem",
        "internet_problem",
        "tv_problem",
        "confirm",
        "operator",
        "robot"
        "no_question"
    ]

more_question_unit_entity_interruption_list = [
        "payment_problem",
        "internet_problem",
        "tv_problem",
        "operator",
        "robot"
    ]


def main():
    """Первая функция, создающая звонок"""
    nn.call('+7' + nn.dialog['msisdn'], entry_point='main_online_container', #Функция, с которой начать звонок когда возьмут трубку
            on_success_call='after_call_succes', #Функция обработки успешного звонка после завершения
            on_failed_call='after_call_fail', #Функция обработки неуспешного звонка после завершения
            )


def main_online_container():
    """Функция - обёртка, обрабатывающая возникающие исключения, входная точка при начале звонка"""
    try:
        now = datetime.datetime.now() + datetime.timedelta(hours=3)
        nn.env('start_time_str', str(now)) # В env start_time_str записываем текущее время по МСК (чтобы запомнить время начала звонка)
        main_online()
    except InvalidCallStateError: #Обработка исключения InvalidCallStateError, возникающее при завершении звонка
        nn.log("Звонок завершен, пропускается выполнение функций")
    finally: # Первичная обработка после завершения звонка
        nn.env('duration', nv.get_call_duration()) #Запоминаем длительность звонка
        nn.env('call_transcript', nv.get_call_transcription(return_format=nv.TRANSCRIPTION_FORMAT_TXT)) #Записываем транскрипцию


def main_online():
    """Функция, где инициализируются переменные, включается фоновый шум и тп"""
    nn.log('Новый звонок, начало логики main_online')
    nv.background('office') #Включение фонового шума
    return hello_unit()


@check_call_state(nv) #Декоратор, проверяющий перед вызвовом функции - сбросили звонок или нет. Если звонок сбросили - вызовет исключение InvalidCallStateError
def hello_unit(*prompts):
    nn.log('unit', 'hello_unit')
    """Функция распознавания речи и озвучивания переданных фраз."""
    nv.set_default('listen', hello_unit_timing)
    with nv.listen(( #Запуск распознавания
            hello_unit_entity_interruption_list, #Список сущностей для перебивания
            None, None, 'AND'), #Дополнительные параметры перебивания (константа)
            entities=hello_unit_entity_list #Список сущностей для распознавания
           ) as r:
        for prompt in prompts: #Цикл, в котором озвучиваем переданные промпты
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
        nv.hangup()

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('hello_null_counter', '+') <= 1:
            return hello_unit('hello_null_prompt')
        return goodbye_null_prompt()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return hello_unit('hello_default_prompt')

    if r.has_entity('payment_problem'):
        if r.entity('payment_problem') == "true":
            nn.log('condition', 'payment_problem=true')
            return payment_unit('payment_main_prompt')

    if r.has_entity('tv_problem'):
        if r.entity('tv_problem') == "true":
            nn.log('condition', 'tv_problem=true')
            return tv_unit('tv_main_prompt')

    if r.has_entity('internet_problem'):
        if r.entity('internet_problem') == "true":
            nn.log('condition', 'internet_problem=true')
            return internet_unit('internet_main_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == "true":
            nn.log('condition', 'repeat=true')
            return hello_unit('hello_repeat_prompt')

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return hello_unit('hello_robot_prompt')

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()


#  //--//--//--//--//--//--//
# Payment_Unit

@check_call_state(nv)
def payment_unit(*prompts):
    nn.log('unit', 'can_callback_unit')
    """Функция распознавания речи и озвучивания переданных фраз."""
    nv.set_default('listen', payment_unit_timing)
    with nv.listen((
            payment_unit_entity_interruption_list,
            None, None, 'AND'),
            drop_ni_utterance=True,
            entities=payment_unit_entity_list
    ) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
                nv.say(prompt)
    return payment_logic(r)

def payment_logic(r):
    nn.log("payment_logic")
    if nn.counter('payment_logic', '+') >= 100:
        nn.log('Recursive usage')
        nv.hangup()

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('payment_null_counter', '+') <= 1:
            return payment_unit('payment_null_prompt')
        return goodbye_null_prompt()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return payment_unit('payment_default_prompt')

    if r.has_entity('pay_site'):
        if r.entity('pay_site') == 'true':
            nn.log('condition', 'pay_site=true')
            return payment_unit('payment_site_prompt')

    if r.has_entity('offices'):
        if r.entity('offices') == 'true':
            nn.log('condition', 'offices=true')
            return payment_unit('payment_offices_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == 'true':
            nn.log('condition', 'repeat=true')
            return payment_unit('payment_repeat_prompt')

    if r.has_entity('promise_pay'):
        if r.entity('promise_pay') == 'true':
            nn.log('condition', 'promise_pay=true')
            return payment_unit('payment_promise_pay_prompt')

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()

    if r.has_entity('confirm'):
        if r.entity('confirm') == "true":
            nn.log('condition', 'confirm=true')
            return more_question_main_prompt('more_question_main_prompt')
        elif r.entity('confirm') == 'false':
            nn.log('condition', 'confirm=false')
            return goodbye_main_prompt()


#  //--//--//--//--//--//--//
# Tv_Unit
@check_call_state(nv)
def tv_unit(*prompts):
    nn.log('unit', 'tv_unit')
    nv.set_default('listen', tv_unit_timing)
    with nv.listen((tv_unit_entity_interruption_list, None, None, 'AND'),
                   entities=tv_unit_entity_list) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
            nv.say(prompt)
    return tv_logic(r)


def tv_logic(r):
    nn.log("tv_logic")
    if nn.counter('tv_logic', '+') >= 100:
        nn.log('Recursive usage')
        nv.hangup()

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('tv_null_counter', '+') <= 1:
            return payment_unit('tv_null_prompt')
        return goodbye_null_prompt()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return payment_unit('tv_default_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == 'true':
            nn.log('condition', 'repeat=true')
            return payment_unit('tv_repeat_prompt')

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return hello_unit('tv_robot_prompt')

        if r.has_entity('confirm'):
            if r.entity('confirm') == "true":
                nn.log('condition', 'confirm=true')
                return more_question_main_prompt('more_question_main_prompt')
            elif r.entity('confirm') == 'false':
                nn.log('condition', 'confirm=false')
                return goodbye_main_prompt()

#  //--//--//--//--//--//--//
# Internet_Unit

def internet_unit(*prompts):
    nn.log('unit', 'internet_unit')
    nv.set_default('listen', internet_unit_timing)
    with nv.listen((internet_unit_entity_interruption_list, None, None, 'AND'),
                   entities=internet_unit_entity_list) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
            nv.say(prompt)
    return internet_logic(r)


def internet_logic(r):
    nn.log("internet_logic")
    if nn.counter('internet_logic', '+') >= 100:
        nn.log('Recursive usage')
        nv.hangup()

    if not r:
        nn.log("condition", "NULL")
        if nn.counter('internet_null_counter', '+') <= 1:
            return payment_unit('internet_null_prompt')
        return goodbye_null_prompt()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return payment_unit('internet_default_prompt')

    if r.has_entity('repeat'):
        if r.entity('repeat') == 'true':
            nn.log('condition', 'repeat=true')
            return payment_unit('internet_repeat_prompt')

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return hello_unit('internet_robot_prompt')

        if r.has_entity('confirm'):
            if r.entity('confirm') == "true":
                nn.log('condition', 'confirm=true')
                return goodbye_operator_prompt()
            elif r.entity('confirm') == 'false':
                nn.log('condition', 'confirm=false')
                return internet_green_unit('internet_green_main_prompt')

#  //--//--//--//--//--//--//
# Internet_Green_Unit

def internet_green_unit(*prompts):
    nn.log('unit', 'internet_unit')
    nv.set_default('listen', internet_green_unit_timing)
    with nv.listen((internet_unit_entity_interruption_list, None, None, 'AND'),
                   entities=internet_unit_entity_list) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
            nv.say(prompt)
    return internet_logic(r)
#  //--//--//--//--//--//--//

# Goodbye_Unit

def goodbye_main_prompt():
    nn.log('unit', 'goodbye_main')
    nv.say('goodbye_main_prompt')
    nn.env('set_output', 'Вопрос решён')
    nv.hangup()

def goodbye_null_prompt():
    nn.log('unit', 'goodbye_null')
    nv.say('goodbye_null_prompt')
    nn.env('set_output', 'Тишина')
    nv.hangup()

def goodbye_operator_prompt():
    nn.log('unit', 'goodbye_operator')
    nv.say('goodbye_operator_prompt')
    nn.env('set_output', 'Перевод на оператора')
    nv.method('Соединение с оператором')

def goodbye_operator_demand_prompt():
    nn.log('unit', 'goodbye_operator_demand')
    nv.say('goodbye_operator_demand_prompt')
    nn.env('set_output', 'Требует оператора')
    nv.method('Соединение с оператором')

def goodbye_internet_green_prompt():
    nn.log('unit', 'goodbye_internet_green')
    nv.say('goodbye_internet_green_prompt')
    nn.env('set_output', 'Возможно перезвонит')
    nv.hangup()
