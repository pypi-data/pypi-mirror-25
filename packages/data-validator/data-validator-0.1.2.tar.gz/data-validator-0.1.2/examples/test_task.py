import re

from data_validator import Validator
from data_validator.validators.base import BaseValidator

sentence = "test   .TyGrr.  sdf,m,.m."


class ValidatorEmptyWords(BaseValidator):
    def __init__(self, expected, handler=None):
        """

        :param expected: Expected number of empty words in list
        :type expected: int
        :param handler: Function to change value if value is unexpected
        """
        super().__init__(expected, handler)

    def validate(self, value):
        """

        :type value: list
        :return:
        """

        return True if len(list(filter(lambda x: x == '', value))) > (self.expected or 0) else False


class ValidatorPunctuationCount(BaseValidator):
    def __init__(self, expected, handler=None):
        super().__init__(expected, handler)

    def validate(self, value):
        """

        :type value: str
        :return:
        """
        p = re.findall(r'[^\w\s]', value)
        if not p:
            return
        for i, s in enumerate(value):
            if s in p and i > 0 and value[i - 1] in p:
                return True


class ValidatorUpperCaseStrangeLogic(BaseValidator):
    def __init__(self, expected=None, handler=None):
        super().__init__(expected, handler)

    def validate(self, value):
        """

        :type value: str
        :return:
        """
        return True if len(value) > 1 and '.' == value[0] and not value[1:].istitle() else False


def analize(text):
    raw_words = sentence.split(text)
    errors = []
    rules = [ValidatorEmptyWords(0)]
    res, unexpected = Validator.validate_value(raw_words, rules)
    if not res:
        errors.extend(unexpected)
        rules = [ValidatorPunctuationCount(1), ValidatorUpperCaseStrangeLogic()]
    for word in raw_words:
        res, unexpected = Validator.validate_value(word, rules)
        if not res:
            errors.extend(unexpected)
    return errors


res = analize(sentence)
a = 1
