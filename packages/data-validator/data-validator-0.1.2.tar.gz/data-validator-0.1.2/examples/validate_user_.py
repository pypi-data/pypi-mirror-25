import time

import numpy

from data_validator import Validator
from data_validator import validators


class Address(object):
    def __init__(self, state, city=None):
        self.state = state
        self.city = city


class Career(object):
    def __init__(self, name, from_=None, until=None):
        self.name = name
        self.from_ = from_
        self.until = until


class User:
    def __init__(self, first_name, last_name, email=None, second_email=None, address=None, career=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.second_email = second_email
        self.address = address
        self.career = career


# user to validate
user = {
        'user': 'Very long name to validate',
        'last_name': 'Smith',
        'email': 'smith@gmail.com',
        'second_email': 'bad email',
        'address': {'state': 'Texas', 'city': 'Dallas'},
        # 'address': Address(state='Texas',city='Dallas'),
        'career': [Career(name='google',from_=2012,until='now'), {'name': 'facebook', 'from': -1,
                                                                      'until': 44444444444444}]
    }

ouser = User(first_name='Vasyatttttttttttttttttttttttttttttttttttt',last_name='Ivanov')

# We want to validate:

# user['first_name'] and user['last_name'] length must be more then 2 and less then 10
# user['email'] and user['second_email'] must match regex pattern r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$"
# user['address']['state'] may be Texas, Alabama or Alaska and it case sensitive
# user['address']['city'] may be New York, Los Angeles or Washington and it not case sensitive
# user['career'][*]['from'] and user['career'][*]['until'] must be int16. P.s. * is list index

# And if we have unexpected values we need to change them with handler function - lambda x: -1
# and if user['career']['until'] is unexpected we need to change this with handler function - lambda x: -2

# user validation rules
rules = {
    'first_name': [validators.StringLength([2, 10])],
    'last_name': [validators.StringLength([2, 10])],
    'email': [validators.Regex(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")],
    'second_email': [validators.Regex(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$")],
    'address.state': [validators.Variants(['Texas', 'Alabama', 'Alaska'])],
    'address.city': [validators.Variants(['New York', 'Los Angeles', 'Washington'], case_sensitive=False)],
    'career.from': [validators.IntNumberType(numpy.int16)],
    'career.until': [validators.IntNumberType(numpy.int16, handler=lambda x: -2)]
}

# validate user
validator = Validator(rules, common_handler=lambda x: -1)


start_time = time.time()
r = validator.validate(user)
# [print(r.unexpected_values) for r in validator.validate_iter(users)]
print("--- %s seconds ---" % (time.time() - start_time))
# validator_result = validator.validate(user)
# if not validator_result:
#     [print(unexpected) for unexpected in validator.unexpected_values]

# result will be
# path: address.city, value: Dallas, validator: <data_validator.validators.variants.Variants object at 0x7f382b159a20>, expected: ['new york', 'los angeles', 'washington'], unexpected: dallas
# path: second_email, value: bad email, validator: <data_validator.validators.regex.Regex object at 0x7f382b159990>, expected: ^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$, unexpected: bad email
# path: career.0.until, value: now, validator: <data_validator.validators.types.IntNumberType object at 0x7f382b159ab0>, expected: <class 'numpy.int16'>, unexpected: <class 'str'>
# path: career.1.until, value: 44444444444444, validator: <data_validator.validators.types.IntNumberType object at 0x7f382b159ab0>, expected: <class 'numpy.int16'>, unexpected: <class 'numpy.int64'>
# path: first_name, value: Very long name to validate, validator: <data_validator.validators.length.StringLength object at 0x7f382b19f120>, expected: [2, 10], unexpected: 26

# We can find original item in validator.original_item and changed dict in validator.processed_item:
# {
#     'first_name': -1,
#     'last_name': 'Smith',
#     'email': 'smith@gmail.com',
#     'second_email': -1,
#     'address': {'state': 'Texas', 'city': -1},
#     'career': [{'name': 'google', 'from': -1, 'until': -2}, {'name': 'facebook', 'from': -1, 'until': -2}]
# }
