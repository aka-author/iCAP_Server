# # ## ### ##### ######## ############# #####################
# Product: iCAP platform
# Layer:   Kernel
# Module:  status.py                                  (\(\
# Func:    Defining status and error codes            (^.^)
# # ## ### ##### ######## ############# #####################


# Status and error codes

OK                          = 0
ERR_APP_INIT_FAILED         = 1
ERR_DB_CONNECTION_FAILED    = 2
ERR_DB_QUERY_FAILED         = 3
ERR_NOT_FOUND               = 4
ERR_LOGIN_FAILED            = 5
ERR_NOT_AUTHORIZED          = 6
ERR_INCORRECT_REQUEST       = 7
ERR_UNKNOWN_REQUEST_TYPE    = 8
ERR_UNKNOWN_PERFORMER       = 9
ERR_UNKNOWN_TASK            = 10


# Messages

MSG_START                   = "Start"
MSG_FINISH                  = "Finish"
MSG_SUCCESS                 = "OK"
MSG_LOGIN_OK                = "Logged into the system"
MSG_LOGIN_FAILED            = "Failed to login into the system"
MSG_INCORRECT_REQUEST       = "The request is incorrect"
MSG_NOT_AUTHORIZED          = "Not authorized"
MSG_REQUEST                 = "Request"
MSG_RESPONSE                = "Response"
MSG_FATAL                   = "Fatal error"
MSG_DATABASE_ERROR          = "Database error"
MSG_APP_INIT_FAILED         = "Failed to initialize the application"
MSG_UNKNOWN_REQUEST_TYPE    = "Unknown request type"
MSG_UNKNOWN_PERFORMER       = "Unknown performer"
MSG_UNKNOWN_TASK            = "Unknown task" 