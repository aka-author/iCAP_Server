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
ERR_REPORT_NOT_SUPPORTED    = 7
ERR_INCORRECT_REQUEST       = 8


# Messages

MSG_SUCCESS           = "Beseder"
MSG_LOGIN_OK          = "Logged into the system"
MSG_LOGIN_FAILED      = "Failed to login into the system"
MSG_INCORRECT_REQUEST = "The request is incorrect"
MSG_NOT_AUTHORIZED    = "Not authorized"
MSG_REQUEST           = "Request"
MSG_RESPONSE          = "Response"
MSG_FATAL             = "Fatal error"
MSG_DATABASE_ERROR    = "Database error"
MSG_APP_INIT_FAILED   = "Failed to initialize the application"