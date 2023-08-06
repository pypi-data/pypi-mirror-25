"""
 # Copyright (c) 08 2016 | suryakencana
 # 8/13/16 nanang.ask@kubuskotak.com
 #  i18n
"""
import logging
from pyramid.settings import asbool
from pyramid.httpexceptions import HTTPFound
from pyramid.i18n import TranslationStringFactory, get_localizer, make_localizer
from pyramid.interfaces import ITranslationDirectories
from pyramid.response import Response
from pyramid.threadlocal import get_current_request, get_current_registry
from pyramid.view import view_config

log = logging.getLogger(__name__)


__all__ = (
    'translate'
)

registry = get_current_registry()
settings = registry.settings

log.info(settings)

tsf = TranslationStringFactory(settings.get('package'))
DEFAULT_LOCALE_NAME = settings.get('i18n')['default_local_name']



def add_renderer_globals(event):
    request = event.get('request') or get_current_request()
    event['_'] = request.translate
    event['localizer'] = request.localizer


def add_localizer(event):
    request = event.request
    localizer = get_localizer(request)

    def auto_translate(*args, **kwargs):
        return localizer.translate(tsf(*args, **kwargs))
    request.localizer = localizer
    request.translate = auto_translate


def _get_localizer_for_locale_name(locale_name):
    registry = get_current_registry()
    tdirs = registry.queryUtility(ITranslationDirectories, default=[])
    return make_localizer(locale_name, tdirs)


def translate(*args, **kwargs):
    request = get_current_request()
    if request is None:
        log.debug('request is none')
        localizer = _get_localizer_for_locale_name(DEFAULT_LOCALE_NAME)
    else:
        localizer = request.localizer
    return localizer.translate(tsf(*args, **kwargs))


@view_config(route_name='locale')
def set_locale_cookie(request):
    settings = request.registry.settings
    lang = settings.get('i18n')
    response = Response()
    if request.matchdict.get('language'):
        language = request.matchdict.get('language', 'en')
        response.set_cookie('_LOCALE_',
                            value=language,
                            max_age=31536000)  # max_age = year

    location = request.route_url(lang.get('base_route', 'baka_home'))
    return HTTPFound(location=location,
                     headers=response.headers)


def includeme(config):
    """
    Initialize the model for a Pyramid library.

    Activate this setup using ``config.include('garasu_i18n')``.

    """
    settings = config.registry.settings
    use = settings.get('package')

    # localization dir colander
    config.add_subscriber(add_renderer_globals,
                          'pyramid.events.BeforeRender')
    config.add_subscriber(add_localizer,
                          'pyramid.events.NewRequest')

    # config.set_locale_negotiator(custom_locale_negotiator)

    config.add_route('locale', '/locale/{language}')

    config.add_translation_dirs('{egg}:locale/'.format(egg=use))
    if asbool(settings.get('i18n').get('colander', False)):
        config.add_translation_dirs('colander:locale/')

    config.scan(__name__)
