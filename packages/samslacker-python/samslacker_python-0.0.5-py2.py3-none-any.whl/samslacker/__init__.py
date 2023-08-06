from samslacker.resources import Events

api_base = 'https://samplify.io/slacker/api'
api_version = 'v1'
token = None
project = None


def event(_name, *args, **kwargs):

    if token is None:
        raise Exception('Please specify samslacker.token')

    data = {
        'event': _name,
        'arguments': kwargs
    }

    if project is not None:
        data['project_id'] = project

    return Events.create(data)
