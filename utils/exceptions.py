class CredentialError(Exception):
    def __init__(self, message="Invalid credentials"):
        super().__init__(message)

class ButtonError(Exception):
    def __init__(self, message="Unrecognised button clicked"):
        super().__init__(message)

class DatabaseError(Exception):
    def __init__(self, message="Exception encountered whilst interacting with the database"):
        super().__init__(message)