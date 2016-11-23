from djbase.exceptions import BaseError

class AccountError(BaseError):
    em = {1101: "Account external no email error."}

class AccountLoginError(AccountError):
    """ Raised when the login email or password is invalid. """
    pass

class AccountMissingError(AccountError):
    """ Raised when the login email or username does not exist. """
    pass

class AccountNoPasswordError(AccountError):
    """ Raised when the account has no password set which happens
        when the user logins using an external account.
    """
    pass

class AccountEmailTakenError(AccountError):
    """ Raised when the chosen email is already taken. """
    pass

class AccountUsernameTakenError(AccountError):
    """ Raised when the chosen username is already taken. """
    pass
