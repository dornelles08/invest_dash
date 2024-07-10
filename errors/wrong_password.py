class WrongPassword(Exception):
    def __init__(self):
        self.message = "Password is wrong"
        super().__init__(self.message)
