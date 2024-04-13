class Admin():
    def __init__(self, username, password) -> None:
        self.username = username
        self.password = password

    def to_json(self):
        return {
            'username' : self.username,
            'password' : self.password
        }