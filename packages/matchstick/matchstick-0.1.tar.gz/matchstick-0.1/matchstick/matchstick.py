functions = {}

message = """
No match for function {function} in module {module} with arguments {args} and
keyword arguments {kwargs}
""".strip('\n')

class NoMatchException(Exception):
    def __init__(self, key, args, kwargs):
        module, name = key
        super(NoMatchException, self).__init__(message.format(
            function=name,
            module=module,
            args=args,
            kwargs=kwargs
        ))

def generate_condition_check(condition, function):
    defaults = function.__defaults__ or []
    kwdefaults = function.__kwdefaults__ or {}
    names = function.__code__.co_varnames
    required_count = function.__code__.co_argcount - len(defaults)
    # Get positional parameters with no default value
    parameters = [names[i] for i in range(required_count)]
    # Add optionally-positional parameters with default values
    parameters += ['{}={}'.format(names[i + required_count], repr(defaults[i]))
        for i in range(len(defaults))]
    # If there are keyword-only parameters, add an asterisk
    if function.__code__.co_kwonlyargcount:
        parameters.append('*')
    # Add keyword-only parameters with available defaults
    parameters += ['{}={}'.format(names[i], repr(kwdefaults[names[i]]))
        if names[i] in kwdefaults else names[i]
        for i in range(function.__code__.co_argcount, len(names))]
    # Create a function that evaluates condition
    return eval('lambda {}: {}'.format(','.join(parameters), condition))

def generate_triage(key, siblings):
    def triage(*args, **kwargs):
        for check, function in siblings:
            try:
                if check(*args, **kwargs):
                    return function(*args, **kwargs)
            except:
                pass
        raise NoMatchException(key, args, kwargs)
    return triage

def match(condition):
    def decorate(function):
        check = generate_condition_check(condition, function)
        key, siblings = store(check, function)
        return generate_triage(key, siblings)
    return decorate

def store(check, function):
    key = (function.__module__, function.__qualname__)
    siblings = functions.setdefault(key, [])
    siblings.append((check, function))
    return key, siblings
