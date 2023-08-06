import codecs
import os.path
from copy import copy
from typing import Optional

from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template
from plenario_core.models import MetaBase

from plenario_mailer_core import defaults


_dirname = os.path.dirname(__file__)
_template_dir = os.path.join(_dirname, 'templates', 'plenario_mailer_core')


ADMINS = [email for _, email in settings.ADMINS]


def _render_template(
        template_name: str,
        meta_model: MetaBase,
        sender_name: Optional[str]=None,
        sender_email: Optional[str]=None,
        **kwargs) -> str:
    """Interpolates an email context to be used as a plain text email body.

    :param template_name: the name of the template to use
    :param meta_model: the MetaBase model that is being acted on
    :param sender_name: the name of the sender in the signature
    :param sender_email: the email address of the sender in the signature
    :param kwargs: additional context key-word pairs
    :return: the interpolated template
    """
    path = os.path.join(_template_dir, template_name)
    with codecs.open(path, mode='r', encoding='utf8') as fh:
        template = Template(fh.read())

    ctx = kwargs
    ctx['meta_model'] = meta_model
    ctx['sender_name'] = sender_name or _get_sender_name()
    ctx['sender_email'] = sender_email or _get_sender_email()
    context = Context(ctx)

    return template.render(context)


def _get_sender_email() -> str:
    if hasattr(settings, 'EMAIL_SENDER_EMAIL'):  # NOQA
        return settings.EMAIL_SENDER_EMAIL
    return defaults.SENDER_EMAIL


def _get_sender_name() -> str:
    if hasattr(settings, 'EMAIL_SENDER_NAME'):  # NOQA
        return settings.EMAIL_SENDER_NAME
    return defaults.SENDER_NAME


def send_data_set_approved_email(
        meta_model: MetaBase,
        **template_kwargs) -> None:
    content = _render_template(
        'data-set-approved.j2', meta_model=meta_model, **template_kwargs)
    sender = _get_sender_email()
    recips = copy(ADMINS)
    recips.append(meta_model.contributor.email)
    subject = f'{meta_model} Approved'
    send_mail(subject, content, sender, recips)


def send_data_set_ready_email(
        meta_model: MetaBase,
        **template_kwargs) -> None:
    content = _render_template(
        'data-set-ready.j2', meta_model=meta_model, **template_kwargs)
    sender = _get_sender_email()
    recips = copy(ADMINS)
    recips.append(meta_model.contributor.email)
    subject = f'{meta_model} Ready'
    send_mail(subject, content, sender, recips)


def send_data_set_erred_email(
        meta_model: MetaBase,
        error_message: str,
        **template_kwargs) -> None:
    template_kwargs['error_message'] = error_message
    content = _render_template(
        'data-set-erred.j2', meta_model=meta_model, **template_kwargs)
    sender = _get_sender_email()
    recips = copy(ADMINS)
    recips.append(meta_model.contributor.email)
    subject = f'{meta_model} Erred'
    send_mail(subject, content, sender, recips)


def send_data_set_fixed_email(
        meta_model: MetaBase,
        fix_message: str,
        **template_kwargs) -> None:
    template_kwargs['fix_message'] = fix_message
    content = _render_template(
        'data-set-fixed.j2', meta_model=meta_model, **template_kwargs)
    sender = _get_sender_email()
    recips = copy(ADMINS)
    recips.append(meta_model.contributor.email)
    subject = f'{meta_model} Fixed'
    send_mail(subject, content, sender, recips)
