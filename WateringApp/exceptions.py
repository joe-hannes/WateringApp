from werkzeug.exceptions import HTTPException

class AssertionError(HTTPException):
    code = 402
    description = '<p>Assertion Error. Unexpected Sensor Value</p>'
