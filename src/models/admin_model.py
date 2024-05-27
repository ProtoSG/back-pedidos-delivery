class Admin():
    def __init__(self, username, password, id = None) -> None:
        self.id = id
        self.username = username
        self.password = password

    def to_json(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'password' : self.password
        }
