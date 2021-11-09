class StatusCodeError(Exception):
    def __init__(self, message, detail, status):
        self.message = message
        self.detail = detail
        self.status = status

    def __str__(self):
        return f"""
        Message: {self.message}
        Detail: {self.detail}
        Status: {self.status}
        """