# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  userdesk.py                                (\(\
# Func:    Modeling data about users and sessions     (^.^)
# # ## ### ##### ######## ############# #####################

import ramtable, bureaucrat, user 


class UserDesk(bureaucrat.Bureaucrat):

    def __init__(self, chief):

        super().__init__(chief)


    def insert_user(self, usr):

        return self


    def get_user_by_uuid(self, uuid):

        return user.User(self).quick_load("uuid", uuid)


    def get_user_by_username(self, username):

        return user.User(self).quick_load("username", username)
