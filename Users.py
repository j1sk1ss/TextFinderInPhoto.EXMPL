class Users:
    def __init__(self, users):
        self.users = users

    def get_user(self, chat_id):
        for user in self.users:
            if user.chat_id == chat_id:
                return user

        return None

    def add_user(self, user):
        self.users.append(user)