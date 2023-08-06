# -*- coding: utf-8 -*-

"""
Created on 2016-10-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti_contenttypes import _, fanstatic
from kotti_contenttypes.resources import Folder
from kotti_contenttypes.views import BaseView


@view_defaults(context=Folder, permission='view')
class FolderViews(BaseView):
    """ Views for :class:`kotti_contenttypes.resources.Folder` """

    @view_config(name='view', permission='view',
                 renderer='kotti_contenttypes:templates/folder.pt')
    def default_view(self):
        """ Default view for :class:`kotti_contenttypes.resources.Folder`

        :result: Dictionary needed to render the template.
        :rtype: dict
        """
        fanstatic.folder_js.need()
        return {
        }
