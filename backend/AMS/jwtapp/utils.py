from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_mail(data):
        print("data from ser - ",   data)
        email=EmailMessage(subject=data.get('subject'),body=data.get('body'),from_email=data.get('EMAIL_FROM'),to=[data['to_email']])
        email.send()