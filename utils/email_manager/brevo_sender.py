from utils.email_manager.base import EmailSender


class BrevoEmailSender(EmailSender):

    def __init__(self, api_key: str):
        self.api_key = api_key

    def send(self, to, subject, template, context) -> bool:
        print("Brevo sender not implemented yet")
        return False