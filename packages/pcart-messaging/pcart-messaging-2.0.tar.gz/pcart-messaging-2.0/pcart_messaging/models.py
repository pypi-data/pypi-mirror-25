from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
# from mptt.models import MPTTModel, TreeForeignKey
# from django.urls import reverse, NoReverseMatch
import uuid


class EmailTemplate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('Name'), max_length=255, unique=True)

    subject = models.CharField(_('Subject'), max_length=255)
    mjml_template = models.TextField(_('MJML template'), default='', blank=True)
    html_template = models.TextField(_('HTML template'), default='', blank=True)
    text_template = models.TextField(_('Text template'), default='', blank=True)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('Email template')
        verbose_name_plural = _('Email templates')
        ordering = ('name',)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from .utils import mjml_to_html
        from .html2text import html2text
        self.html_template = mjml_to_html(self.mjml_template)
        self.text_template = html2text(self.html_template)
        super(EmailTemplate, self).save(*args, **kwargs)

    def _template_header(self):
        CODE = '{% load i18n l10n pcart_core staticfiles %}\n'
        return CODE

    def _render_template(self, template, context={}):
        from django.template import Context, Template
        template = self._template_header() + template
        t = Template(template)
        c = Context(context)
        return t.render(c)

    def render_subject(self, context={}):
        return self._render_template(self.subject, context).replace('\n', '')

    def render_html(self, context={}):
        context.update({
            'format': 'html',
        })
        return self._render_template(self.html_template, context)

    def render_text(self, context={}):
        context.update({
            'format': 'text',
        })
        return self._render_template(self.text_template, context)


class EmailMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    site = models.ForeignKey(
        Site, verbose_name=_('Site'), related_name='email_messages', on_delete=models.PROTECT)

    template = models.ForeignKey(
        EmailTemplate, verbose_name=_('Template'), related_name='email_messages', on_delete=models.PROTECT)

    data = JSONField(_('Data'), default=dict, blank=True)

    sent = models.BooleanField(_('Sent'), default=False)

    added = models.DateTimeField(_('Added'), auto_now_add=True)
    changed = models.DateTimeField(_('Changed'), auto_now=True)

    class Meta:
        verbose_name = _('Email message')
        verbose_name_plural = _('Email messages')
        ordering = ('-added',)

    def __str__(self):
        return self.subject()

    def subject(self):
        return self.data.get('subject').replace('\n', '')

    def recipients(self):
        return self.data.get('recipients')

    def sender(self):
        return self.data.get('sender')

    def html_body(self):
        return self.data.get('html')

    def text_body(self):
        return self.data.get('text')

    def send(self):
        from .tasks import send_email
        send_email.delay(self.id)
