

class Account(object):
    def __init__(self, address, id, version, crypto):
        self.id = id
        self.address = address
        self.version = version
        self.user_container = Container(**crypto)

    def as_dict(self):
        return {
            'id': self.id,
            'address': self.address,
            'version': self.version,
            'container': self.user_container
        }


class Container(object):
    def __init__(self, public_key, data, salt, iv):
        self.public_key = public_key
        self.data = data
        self.salt = salt
        self.iv = iv

    def as_dict(self):
        return {
            'public_key': self.public_key,
            'data': self.data,
            'salt': self.salt,
            'iv': self.iv
        }