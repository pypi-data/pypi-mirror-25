# -*- coding: utf-8 -*-

"""
Created on 2016-10-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from kotti.resources import File, Document
from pyramid.i18n import TranslationStringFactory

from kotti_pdf.resources import PDF

_ = TranslationStringFactory('kotti_contenttypes')


def kotti_configure(settings):
    """ Add a line like this to you .ini file::

            kotti.configurators =
                kotti_contenttypes.kotti_configure

        to enable the ``kotti_contenttypes`` add-on.

    :param settings: Kotti configuration dictionary.
    :type settings: dict
    """

    settings['pyramid.includes'] += ' kotti_contenttypes'
    settings['kotti.alembic_dirs'] += ' kotti_contenttypes:alembic'
    settings['kotti.available_types'] += (
        ' kotti_contenttypes.resources.Folder'
    )

    settings['kotti.fanstatic.view_needed'] += ' kotti_contenttypes.fanstatic.css_and_js'
    File.type_info.addable_to.append('Folder')
    PDF.type_info.addable_to.append('Folder')
    Document.type_info.addable_to.append('Folder')


def includeme(config):
    """ Don't add this to your ``pyramid_includes``, but add the
    ``kotti_configure`` above to your ``kotti.configurators`` instead.

    :param config: Pyramid configurator object.
    :type config: :class:`pyramid.config.Configurator`
    """

    config.add_translation_dirs('kotti_contenttypes:locale')
    config.add_static_view('static-kotti_contenttypes', 'kotti_contenttypes:static')

    config.scan(__name__)
