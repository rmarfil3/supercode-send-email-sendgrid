import json
import sendgrid
from sendgrid.helpers.mail import Mail, Email, Personalization, Content


def main(sendgrid_key, from_email, to_emails, content, from_email_name="", subject=""):
    """Sends HTML email via SendGrid API v3.

    :param sendgrid_key: the SendGrid API Key
    :param from_email: the email address of the sender
    :param to_emails: array of email addresses / string email address of the receiver/s
    :param content: the content in HTML
    :param from_email_name: (optional) the name of the sender
    :param subject: (optional) the subject of the email
    """

    assert type(to_emails) in (list, tuple, str, unicode)
    if type(to_emails) in (str, unicode):
        to_emails = [to_emails]

    sg = sendgrid.SendGridAPIClient(apikey=sendgrid_key)
    mail = Mail()
    mail.set_from(Email(from_email, name=from_email_name))
    mail.set_subject(subject)

    personalization = Personalization()
    for to_email in to_emails:
        personalization.add_to(Email(to_email))
    personalization.set_subject(subject)
    mail.add_personalization(personalization)

    mail.add_content(Content("text/html", content))

    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code >= 400:
        raise exceptions.SendGridError(response_object=response)

    return {
        "statusCode": 200,
        "body": "SUCCESS"
    }
