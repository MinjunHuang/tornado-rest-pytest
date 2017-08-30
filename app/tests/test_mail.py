from app.handlers.mail import MailHandler
from app.application import Application
from app.tests.fixtures import test_server
import json
import pytest
import requests

def test_post(test_server):
    payload = {'email_id_one':1, 'email_id_two':2}
    response = requests.post(test_server('/mail'), data=json.dumps(payload))
    assert response.code == 200


def test_post_no_emails(test_server):
    payload = {'email_id_one':1233, 'email_id_two':2343}
    response = requests.post(test_server('/mail'), data=json.dumps(payload))
    assert response.code == 401


def test_post_wrong_json(test_server):
    payload = 'this is not a json'
    response = requests.post(test_server('/mail'), data=json.dumps(payload))
    assert response.code == 401


def test_noise_remove_clean_string():
    body = "My name is fabian"
    clean_body = MailHandler.noise_remove(body)
    assert clean_body == body    

def test_noise_remove_dirty_string():
    body = "My name is fabian and i like to code a lot then im a nerd"
    clean_body = MailHandler.noise_remove(body)
    assert clean_body == "My name is fabian i like to code lot im nerd"    


def test_compare_mail_body_equal_words():
    body_one = "a b c d e f g h i j"
    body_two = "a b c d e f g h i j"
    result = MailHandler.compare_mail_body(body_one, body_two)
    assert result == True

def test_compare_mail_body_diff_words():
    body_one = "a b c d e f g h i j"
    body_two = "a b c d e a b c d e"
    result = MailHandler.compare_mail_body(body_one, body_two)
    assert result == False

def test_compare_mail_same_subjects():
    subj_one = "a b c"
    subj_two = "a b c"
    result = MailHandler.compare_mail_subject(subj_one, subj_two)
    assert result == True

def test_compare_mail_diff_subjects():
    subj_one = "a b c"
    subj_two = "a b x"
    result = MailHandler.compare_mail_subject(subj_one, subj_two)
    assert result == False
