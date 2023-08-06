from samslacker.resources import Events

api_base = 'https://samplify.io/slacker/api'
api_version = 'v1'
token = None


def event(name, *args, **kwargs):
    return Events.create({
        'event': name,
        'arguments': kwargs
    })
