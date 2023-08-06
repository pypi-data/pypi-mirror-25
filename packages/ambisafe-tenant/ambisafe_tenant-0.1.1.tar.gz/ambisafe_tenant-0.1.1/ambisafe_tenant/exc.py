class AmbiTenantError(Exception):
    def __init__(self, message, error):
        self.message = message
        self.error = error

    def __str__(self):
        return str(self.message)


class ClientError(AmbiTenantError):
    def __repr__(self):
        return '<AmbiTenantClientError error="{}" message="{}">'.format(self.error, self.message)


class ServerError(AmbiTenantError):
    def __repr__(self):
        return '<AmbiTenantServerError error="{}" message="{}">'.format(self.error, self.message)