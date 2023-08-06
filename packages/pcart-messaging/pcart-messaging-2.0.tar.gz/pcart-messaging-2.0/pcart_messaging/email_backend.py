
class PCartBaseEmailBackend:
    def __init__(self, message_obj):
        self.message_obj = message_obj

    def send(self):
        pass


class PCartSimpleEmailBackend(PCartBaseEmailBackend):
    def send(self):
        from django.core.mail import EmailMultiAlternatives
        mail = EmailMultiAlternatives(
            subject=self.message_obj.subject(),
            body=self.message_obj.text_body(),
            from_email=self.message_obj.sender(),
            to=self.message_obj.recipients(),
        )
        mail.attach_alternative(self.message_obj.html_body(), 'text/html')

        try:
            mail.send()
            self.message_obj.sent = True
            self.message_obj.save()
        except Exception as e:
            self.message_obj.data['error'] = str(e)
            self.message_obj.save()
