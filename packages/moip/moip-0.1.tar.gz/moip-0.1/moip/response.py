class Response(object):
    def __init__(self, status=None, ok=False, content={}):
        if not status:
            raise ValueError('Invalid status.')

        self.content = content
        self.status = status
        self.ok = ok

    def __getitem__(self, key):
        return self.content[key]

    def __contains__(self, key):
        return key in self.content
