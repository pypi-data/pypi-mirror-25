try:
    from urllib.parse import urlsplit, unquote, parse_qs
except ImportError:
    from urlparse import urlsplit, unquote, parse_qs

from ._bool import to_bool


SCHEMES = {
    'submit': 'django.core.mail.backends.smtp.EmailBackend',
    'console': 'django.core.mail.backends.console.EmailBackend',
    'file': 'django.core.mail.backends.filebased.EmailBackend',
    'memory': 'django.core.mail.backends.locmem.EmailBackend',
    'dummy': 'django.core.mail.backends.dummy.EmailBackend'
}


class Config(object):
    pass


def parse_email_url(url):
    c = Config()

    url = urlsplit(url)

    # BC with dj-email-url
    if url.scheme in ('smtp', 'smtps'):
        url = url._replace(scheme='submit')

    query = parse_qs(url.query)

    c.EMAIL_BACKEND = SCHEMES[url.scheme]
    c.EMAIL_HOST = url.hostname
    c.EMAIL_PORT = url.port if url.port else 587 if url.scheme == 'submit' else None
    c.EMAIL_HOST_USER = unquote(url.username) if url.username else None
    c.EMAIL_HOST_PASSWORD = unquote(url.password) if url.password else None
    c.EMAIL_FILE_PATH = url.path
    c.EMAIL_USE_SSL = to_bool(query['ssl'][0]) if query.get('ssl') else False
    c.EMAIL_USE_TLS = to_bool(query['tls'][0]) if query.get('tls') else (url.scheme == 'submit' and not c.EMAIL_USE_SSL)

    return c.__dict__
