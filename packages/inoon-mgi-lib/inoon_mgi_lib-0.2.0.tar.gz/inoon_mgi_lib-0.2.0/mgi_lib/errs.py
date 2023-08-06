class WrongCredentialException(Exception):
    def __init__(self):
        super(self.__class__, self).__init__('Wrong Credential Info')


class NonExistException(Exception):
    def __init__(self):
        super(self.__class__, self).__init__('Non-exist detail info.')


'''
class NotSupportVersionException(Exception):
    def __init__(self):
        super(self.__class__, self).__init__('Wrong API Version')
'''
