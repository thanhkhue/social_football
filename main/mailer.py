
from celery import task

from email.header import Header

from server_scripts.EmailService import EmailMailgun


@task()
def _send_in_queue(mailer, to_email, to_name, subject, content, reply_to=None, direct=False, **param):

    send_from = param.get('send_from')
    recipient = (to_name, to_email)
    mailgun.addRecipient(recipient)

    if send_from:
        mailgun.setSender(send_from)

    mailgun.setBody(content)

    mailgun.send()

    else:
        error = 'Need to specify a mailer service'
        _logger.error(error)
        raise Exception(error)

class Mailer(object):

    @classmethod
    def make_name_and_email(cls, name, email):
        encoded_name = str(Header(to_utf8(name), 'utf-8'))
        return '%s <%s>' % (encoded_name, email)

    @classmethod
    def send_mailgun(cls, to_email, to_name, subject, tpl_name, data, reply_to=None, direct=False, **kwargs):
        tmpl = get_template("emails/%s.html" % tpl_name)
        context = Context(data)
        html = tmpl.render(context)

        delay = kwargs.get('delay') or not settings.DEBUG

        # Use Justgola
        kwargs = kwargs or {}


         _send_in_queue(MAILER_DEFAULT, to_email, to_name, subject, html, reply_to, direct, **kwargs)

        res = 200
        return res == 200


    @classmethod
    def send(cls, to, subject, tpl_name, data, reply_to=None, send_from=None):

        tpl_html = get_template('emails/%s.html' % tpl_name)
        ctx = Context(data)
        body_text = "Please use an email client that supports HTML" # tpl_text.render(ctx)
        body_html = tpl_html.render(ctx)
        if not send_from:
            from_email = cls.make_name_and_email(settings.EMAIL_FROM_NAME,settings.EMAIL_FROM)
        else:
            from_email = cls.make_name_and_email(send_from[0], send_from[1])

        if reply_to:
            if isinstance(reply_to, basestring):
                reply_to_email = reply_to
            else:
                reply_to_email = cls.make_name_and_email(reply_to[0], reply_to[1])
        else:
            reply_to_email = from_email

        msg = EmailMultiAlternatives(
            subject=subject,
            body=body_text,
            from_email=from_email,
            to=[to],
            headers={'Reply-To': reply_to_email})
        msg.content_subtype = "plain" # Main body is text/plain
        msg.attach_alternative(body_html, "text/html")
        num_sent = 0

        try:
            num_sent = msg.send(fail_silently=False)
        except smtplib.SMTPException:
            return False

        return num_sent == 1

class AccountMailer(Mailer):

    @classmethod
    def send_activate_email(cls, account, token, password=False):


        data = {
            'account'     : account,
            'token'       : token,
            'password'    : password,
        }

        subject = 'Activate your account'
        send_from = None
        tpl_name = 'email_account_activate'

        ok = cls.send_mailgun(
            to_email=account.email,
            to_name=account.get_short_name(),
            subject=subject,
            tpl_name=tpl_name,
            send_from=send_from,
            data=data
        )

        return ok


    @classmethod
    def send_password_reset(cls, account, token):

        send_from = None
        tpl_name = 'email_account_password_forgot'

        data = {
            'account'       : account,
            'token'         : token,
        }
        ok = cls.send_mailgun(
            to_email=account.email,
            to_name=account.get_short_name(),
            subject='Reset password',
            tpl_name=tpl_name,
            send_from=send_from,
            data=data
        )

        return ok