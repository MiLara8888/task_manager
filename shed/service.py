#!/usr/bin/env python
# -- coding: utf-8 --
"""
функции вынесенные для удобства
"""
import pymorphy2
from datetime import timedelta, datetime, timezone
from django.utils.timezone import get_current_timezone


morph = pymorphy2.MorphAnalyzer()


def time_zon(dt):
    """преобразует время в данную в сеттинге таймзону"""
    if (dt is not None) and type(dt)==datetime:
        tz = get_current_timezone()
        return dt + tz.utcoffset(dt)


def get_current_time() -> datetime:
    """для получения текущей даты со смещением , эту дату можно сравнивать с джанговской"""
    delta = timedelta(hours=3, minutes=0)
    return datetime.now(timezone.utc) + delta


def word_form(str_obj: str, num: int)->str:
    word_inp = morph.parse(str_obj)[0]
    res_word = word_inp.make_agree_with_number(num).word
    return res_word


def time_check(date: timedelta):
    """Преобразование времени в нормальный вид"""
    days = abs(date.days)    #вычисление дней
    s = date.seconds
    hour = s//3600    #часов
    s = s-(hour * 3600)
    minutes = s//60
    if days==0 and hour==0:
        return f"{minutes} {word_form('минута',minutes)}"
    elif days!=0 and hour==0:
        return f"{days} {word_form('день', days)} {minutes} {word_form('минута',minutes)}"
    elif days==0:
        return f"{hour} {word_form('час', hour)} {minutes} {word_form('минута',minutes)}"
    elif days!=0 :
        return f"{days} {word_form('день', days)} {hour} {word_form('час', hour)} {minutes} {word_form('минуты',minutes)}"