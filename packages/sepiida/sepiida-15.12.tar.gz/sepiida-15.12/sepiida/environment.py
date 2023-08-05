import attrdict
import os
import sys

class Undefined():
    pass

class UndefinedError(Exception):
    "Raised when a required setting is not provided"
    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

class ParseError(Exception):
    def __init__(self, errors):
        super().__init__()
        self.errors = errors

class Specification():
    "The full specification of all variables in the environment"
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def parse(self):
        "Parse the variables that are defined in the given spec from the environment"
        results = attrdict.AttrDict()
        errors = set()
        for k, v in self.kwargs.items():
            try:
                results[k] = v.parse(os.environ.get(k))
            except ValueError as e:
                errors.add(ValueError("The value for {} was invalid: {}".format(k, e)))
            except UndefinedError:
                errors.add(UndefinedError("The variable {} was undefined and has no default value".format(k)))
        if errors:
            raise ParseError(errors)
        return results

class Variable():
    "A single environment variable"
    def __init__(self, default=Undefined, docs=None):
        self.default = default
        self.docs    = docs

    def parse(self, value):
        "Parse the given value or raise ValueError"
        if value is None and self.default is Undefined:
            raise UndefinedError
        return value

class VariableInteger(Variable):
    def parse(self, value):
        return int(super().parse(value))

class VariableBoolean(VariableInteger):
    def parse(self, value):
        value = super().parse(value)
        if value not in (0, 1):
            raise ValueError("Boolean variables should be either '0' or '1'")
        return bool(value)

class VariableFloat(Variable):
    def parse(self, value):
        return float(super().parse(value))

def parse(spec):
    try:
        settings = spec.parse()
        parse.settings = settings
        return settings
    except ParseError as parse_error:
        message = (
            "The program cannot start because there were errors parsing the "
            "settings from environment variables: \n\t{}"
        ).format('\n\t'.join([str(e) for e in parse_error.errors]))
        sys.exit(message)
parse.settings = None

def get():
    if not parse.settings:
        raise Exception((
            "You have attempted to access the environment settings without having "
            "first parsed them from a specification. Please first call parse(spec) "
            "with a valid environment specification before calling the get() function"
        ))
    return parse.settings
