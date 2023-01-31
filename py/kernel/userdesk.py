# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  userdesk.py                                (\(\
# Func:    Modeling data about users and sessions     (^.^)
# # ## ### ##### ######## ############# #####################

import ramtable, bureaucrat, users 


class UserDesk(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)


    def insert_user(self, user):

        return self


    def get_user_by_uuid(self, uuid):

        return users.User(self).direct_load("uuid", uuid)


    def get_user_by_username(self, username):

        return users.User(self).direct_load("username", username)
