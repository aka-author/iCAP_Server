# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  userdesk.py                                (\(\
# Func:    Modeling data about users and sessions     (^.^)
# # ## ### ##### ######## ############# #####################

import uuid
import workers, desks, users 


class UserDesk(desks.Desk):

    def __init__(self, chief: workers.Worker):

        super().__init__(chief)

        self.users, self.users_by_uuids, self.users_by_names = self.load_users()


    def insert_user(self, user: users.User) -> 'UserDesk':

        return self


    def load_users(self) -> 'UserDesk':

        loaded_users = users.User(self).load_all() 

        users_by_uuids = {}
        users_by_names = {}

        for user in loaded_users:
            users_by_uuids[user.get_field_value("uuid")] = user
            users_by_names[user.get_field_value("username")] = user

        return loaded_users, users_by_uuids, users_by_names
    

    def get_user_by_uuid(self, user_uuid: uuid.UUID) -> users.User:

        return self.users_by_uuids.get(user_uuid)


    def get_user_by_name(self, username: str) -> users.User:

        return self.users_by_names.get(username)