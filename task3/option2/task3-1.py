import datetime
from config1.units_timing1 import *
from config1.entities1 import *

"""Библиотеки Фромтек"""
from task3 import lib_fromtech

nn = lib_fromtech.FromtechNetLibrary()
nlu = lib_fromtech.FromtechNluLibrary()
nv = lib_fromtech.FromtechVoiceLibrary()
InvalidCallStateError = lib_fromtech.InvalidCallStateError
check_call_state = lib_fromtech.check_call_state


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


@check_call_state(nv)  # Декоратор, проверяющий перед вызвовом функции - сбросили звонок или нет.
# Если звонок сбросили - вызовет исключение InvalidCallStateError
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
    return logic(r, hello_unit)


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
    return logic(r, payment_unit)


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
    return logic(r, tv_unit)


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
    return logic(r, internet_unit)


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
    return logic(r, internet_green_unit)


#  //--//--//--//--//--//--//
# More_Question_Unit

def more_question_unit(*prompts):
    nn.log('unit', 'internet_unit')
    nv.set_default('listen', more_question_unit_timing)
    with nv.listen((internet_unit_entity_interruption_list, None, None, 'AND'),
                   entities=internet_unit_entity_list) as r:
        for prompt in prompts:
            if isinstance(prompt, tuple):
                if 'synthesize' in prompt[0]:
                    nv.synthesize(prompt[1])
                else:
                    nv.say(prompt[0], prompt[1])
            nv.say(prompt)
    return logic(r, more_question_unit)


# -//-//-//-//-//-//-//-//-//-//-/-//-//-
# Logic
def logic(r, func):
    pattern = f'{func.__name__[:-5]}'  # название функции без последних 5 символов(_unit), чтобы записивать в логи и счётчики
    nn.log(f'{pattern}_logic')
    if nn.counter(f'{pattern}logic', '+') >= 100:
        nn.log('Recursive usage')
        nv.hangup()

    if not r:
        nn.log("condition", "NULL")
        if nn.counter(f'{pattern}_null_counter', '+') <= 1 and func.__name__ != 'tv_unit': # tv_unit сбрасывает сразу. Так написано в Task_script
            return func(f'{pattern}_null_prompt')
        return goodbye_null_prompt()

    if not r.has_entities():
        nn.log('condition', 'DEFAULT')
        return func(f'{pattern}_default_prompt')

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

    if r.has_entity('operator'):
        if r.entity('operator') == "true":
            nn.log('condition', 'operator=true')
            return goodbye_operator_demand_prompt()

    if r.has_entity('robot'):
        if r.entity('robot') == "true":
            nn.log('condition', 'robot=true')
            return func(f'{pattern}_robot_prompt')

    if r.has_entity('confirm'):
        if r.entity('confirm') == "true":
            nn.log('condition', 'confirm=true')
            return confirm_true(func.__name__)
        if r.entity('confirm') == "false":
            nn.log('condition', 'confirm=true')
            return confirm_false(func.__name__)

    if r.has_entity('no_question'):
        if r.entity('no_question') == "true":
            nn.log('condition', 'confirm=true')
            return goodbye_main_prompt()


def confirm_true(func_name: str):
    if func_name in ('payment_unit', 'tv_unit', 'internet_green_unit'):
        return more_question_unit('more_question_main_prompt')
    if func_name == 'internet_unit':
        return goodbye_operator_prompt()
    if func_name == 'more_question_unit':
        return more_question_unit('more_question_confirm_prompt')


def confirm_false(func_name: str):
    if func_name in ('payment_unit', 'tv_unit'):
        return goodbye_main_prompt()
    if func_name == 'internet_unit':
        return internet_green_unit('internet_green_main_prompt')
    if func_name == 'internet_green_unit':
        return goodbye_internet_green_prompt()


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


if __name__ == '__main__':
    main()
