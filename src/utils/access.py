import hashlib
from functools import wraps

from flask import request

import src.database.SQL_requests as sql
from src.connections import DB
from src.constants import *
from src.utils.utils import *


def hash_sha256(auth_string: str) -> str:
    hash = hashlib.sha256(auth_string.encode()).hexdigest()
    return hash

def get_logined_userid():
    token = request.cookies.get('session_token')
    if not token:
        return ''
    session = DB.execute(sql.selectUserIdBySessionToken, [token])
    if len(session) == 0:
        return ''
    return session['userid']


def get_logined_user():
    token = request.cookies.get('session_token')
    if not token:
        return None
    result = DB.execute(sql.selectUserDataBySessionToken, [token])
    if len(result) == 0:
        return None
    return result


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        userData = get_logined_user()
        if not userData:
            return jsonResponse("Не авторизован", HTTP_INVALID_AUTH_DATA)
        if not userData['isconfirmedbyadmin']:
            return jsonResponse("Не подтвержден", HTTP_NO_PERMISSIONS)
        return f(*args, userData, **kwargs)

    return wrapper


def __login_and_property_required(propertyName, denyMessage):
    userData = get_logined_user()
    if not userData:
        return userData, jsonResponse("Не авторизован", HTTP_INVALID_AUTH_DATA)
    if not userData['isconfirmedbyadmin']:
        return jsonResponse("Не подтвержден", HTTP_NO_PERMISSIONS)
    if not userData[propertyName]:
        return userData, jsonResponse(denyMessage, HTTP_NO_PERMISSIONS)
    return userData, None


def login_and_email_confirmation_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('isconfirmedemail', "E-Mail не подтверждён")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_edit_achievements_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('caneditachievements', "Нет прав на изменение достижений")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_assign_achievements_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('canassignachievements', "Нет прав на назначение достижений")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_confirm_new_users_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('canconfirmnewusers', "Нет прав на подтверждение новых пользователей")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_edit_events_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('caneditevents', "Нет прав на изменение событий")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_edit_users_titles_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('canedituserstitles', "Нет прав на изменение титулов пользователей")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_edit_participations_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('caneditparticipations', "Нет прав на изменение участий пользователей в событиях")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_edit_docs_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('caneditdocs', "Нет прав на изменение документов")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_edit_places_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('caneditplaces', "Нет прав на изменение возможных мест проведения")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_edit_positions_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('caneditpositions', "Нет прав на изменение возможных занятий")
        return res or f(*args, userData, **kwargs)
    return wrapper
def login_and_can_execute_sql_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        (userData, res) = __login_and_property_required('canexecutesql', "Нет прав на выполнение произвольных SQL-запросов")
        return res or f(*args, userData, **kwargs)
    return wrapper

def login_required_return_id(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        userData = get_logined_user()
        if not userData:
            return jsonResponse("Не авторизован", HTTP_INVALID_AUTH_DATA)
        if not userData['isconfirmedbyadmin']:
            return jsonResponse("Не подтвержден", HTTP_NO_PERMISSIONS)
        return f(*args, userData['id'], **kwargs)

    return wrapper


def login_or_none(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        userData = get_logined_user()
        if not userData:
            userData = None
        return f(*args, userData, **kwargs)

    return wrapper


def login_or_none_return_id(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        userId = get_logined_userid()
        if not userId:
            userId = None
        return f(*args, userId, **kwargs)

    return wrapper
