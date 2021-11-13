class StatusCodeError(Exception):
    """Exception used when the status code of a http response is not as expected."""
    
    def __init__(self, message, detail, status):
        self.message = message
        self.detail = detail
        self.status = status

    def __str__(self):
        return f"\n  Message: {self.message}\n  Detail: {self.detail}\n  Status: {self.status}"