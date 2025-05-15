class CodeRoom:
    def __init__(self, name, host_user):
        self.name = name
        self.host = host_user
        self.members = []

    def add_member(self, user):
        self.members.append(user)

class UserSession:
    def __init__(self, user_id, ip):
        self.user_id = user_id
        self.ip = ip
