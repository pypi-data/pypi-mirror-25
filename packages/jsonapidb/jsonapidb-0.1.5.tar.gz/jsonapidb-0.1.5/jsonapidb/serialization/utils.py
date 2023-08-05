import json


class InvalidFormat(Exception):
    pass


def invalid_format():
    return InvalidFormat('Provided data is not valid json-api document')


def handle_invalid_format(to_decorate):
    def decorated(*args, **kwargs):
        try:
            return to_decorate(*args, **kwargs)
        except (KeyError, json.JSONDecodeError) as e:
            raise invalid_format()

    return decorated


@handle_invalid_format
def unpack_data(data: str):
    return to_json(data)['data']


@handle_invalid_format
def to_json(data: str):
    return json.loads(data)