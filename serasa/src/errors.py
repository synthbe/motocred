# errors.py
class RequestError(Exception):
    """ Execption for the request received """
    def __init__(self, message: str="Request error", status_code: int=400) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(f"{self.message}, {self.status_code}")

class CPFError(Exception):
    """ Execption for CPF errors """
    def __init__(self, message: str="cpf error", status_code: int=404) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(f"{self.message}, {self.status_code}")

class AuthError(Exception):
    """ Exeception for any authentication error """
    def __init__(self, message: str="Authentication error", status_code: int=401) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(f"{self.message}, {self.status_code}")

class ReportError(Exception):
    """ Execption for any error in the report """
    def __init__(self, message: str="Serasa report error", status_code: int=502) -> None:
        self.message = message
        self.status_code = status_code

class EmailError(Exception):
    """ Execption for sending email """
    def __init__(self, message: str="Email error", status_code: int=500) -> None:
        self.message = message
        self.status_code = status_code

class SheetError(Exception):
    """ Execption for writing in google sheet """
    def __init__(self, message: str="Google sheet error", status_code: int=500) -> None:
        self.message = message
        self.status_code = status_code

