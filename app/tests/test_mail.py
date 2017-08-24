from app.handlers.mail import MailHandler
import pytest

@pytest.mark.parametrize("body, expected_output",
                         [
                            ("My name is fabian","My name is fabian"),
                            ("My name is fabian and i like to code a lot",\
                                "My name is fabian i like to code lot"),
                            ("and and then then","")
                         ]
                        )
def test_noise_remove(body, expected_output):
    clean_body = MailHandler.noise_remove(body)
    assert clean_body == expected_output

@pytest.mark.parametrize("bd_one, bd_two, expected_output",
                         [
                            ("aa bb cc dd aa bb cc dd aa bb",\
                             "aa bb cc dd aa bb cc dd aa bb", True),
                            ("aa bb cc dd aa bb cc dd aa bb",\
                             "aa bb cc dd aa bb cc dd aa bb cc dd", True),
                            ("aa bb cc dd aa bb cc dd aa bb",\
                             "aa bb cc dd aa bb cc dd aa cc", False),
                            ("aa bb cc dd aa",\
                             "aa bb cc dd aa bb cc dd aa cc", False),
                         ]
                        )
def test_compare_mail_body(bd_one, bd_two, expected_output):
    result = MailHandler.compare_mail_body(bd_one, bd_two)
    assert result == expected_output

@pytest.mark.parametrize("sbj_one, sbj_two, expected_output",
                         [
                            ("aa bb cc", "aa bb cc", True),
                            ("aa bb cc", "aa bb cc dd aa", True),
                            ("aa bb cc", "aa aa aa", False),
                            ("aa bb cc", "", False),
                         ]
                        )
def test_compare_mail_subject(sbj_one, sbj_two, expected_output):
    result = MailHandler.compare_mail_subject(sbj_one, sbj_two)
    assert result == expected_output
