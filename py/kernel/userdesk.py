# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  userdesk.py                                (\(\
# Func:    Modeling data about users and sessions     (^.^)
# # ## ### ##### ######## ############# #####################

import uuid
import controllers, desks, users 


class UserDesk(desks.Desk):

    def __init__(self, chief: controllers.Controller):

        super().__init__(chief)


    def insert_user(self, user: users.User) -> 'UserDesk':

        return self


    def get_user_by_uuid(self, uuid: uuid.UUID) -> users.User:

        return users.User(self).load(self.get_db(), "uuid", uuid)


    def get_user_by_username(self, username: str) -> users.User:

        return users.User(self).load(self.get_db(), "username", username)