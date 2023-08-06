import subprocess
from django.conf import settings


def mjml_to_html(mjml_code):
    cmd_args = getattr(settings, 'PCART_MJML_COMMAND', 'mjml')
    if not isinstance(cmd_args, list):
        cmd_args = [cmd_args]
        cmd_args.extend(['-i', '-s'])

    try:
        p = subprocess.Popen(cmd_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        html = p.communicate(mjml_code.encode('utf8'))[0].decode('utf8')
    except (IOError, OSError) as e:
        raise RuntimeError(
            'Problem to run command "{}"\n'.format(' '.join(cmd_args)) +
            '{}\n'.format(e) +
            'Check that mjml is installed and allow permissions for execute.\n' +
            'See https://github.com/mjmlio/mjml#installation'
        )
    return html


def create_email_message(template_name, recipients, sender, context=None, request=None):
    from .models import EmailMessage, EmailTemplate
    from django.contrib.sites.shortcuts import get_current_site

    if context is None:
        context = {}

    if request is not None:
        site = get_current_site(request)
    else:
        from django.contrib.sites.models import Site
        site = Site.objects.get_current()

    try:
        template = EmailTemplate.objects.get(name=template_name)

        data = {
            'recipients': recipients,
            'sender': sender,
            'subject': template.render_subject(context),
            'html': template.render_html(context),
            'text': template.render_text(context),
        }

        message = EmailMessage(
            site=site,
            template=template,
            data=data,
        )
        message.save()
        return message
    except EmailTemplate.DoesNotExist:
        pass


def send_email_message(template_name, recipients, sender, context=None, request=None):
    msg = create_email_message(template_name, recipients, sender, context, request)
    msg.send()


def send_email_to_group(template_name, group_name, sender, context=None, request=None, extra_recipients=None):
    from pcart_customers.models import User
    users = User.objects.filter(groups__name=group_name)
    if users:
        recipients = list(users.values_list('email', flat=True))
        if extra_recipients is not None:
            recipients += extra_recipients
        send_email_message(template_name, recipients, sender, context, request)

