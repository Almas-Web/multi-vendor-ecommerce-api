from utils.email_manager.base import EmailSender


class AWSESEmailSender(EmailSender):

    def __init__(self, access_key, secret_key, region):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def send(self, to, subject, template, context) -> bool:
        print("AWS SES sender not implemented yet")
        return False