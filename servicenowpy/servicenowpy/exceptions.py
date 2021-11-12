class StatusCodeError(Exception):
    def __init__(self, message, detail, status):
        self.message = message
        self.detail = detail
        self.status = status

    def __str__(self):
        return f"\n  Message: {self.message}\n  Detail: {self.detail}\n  Status: {self.status}"