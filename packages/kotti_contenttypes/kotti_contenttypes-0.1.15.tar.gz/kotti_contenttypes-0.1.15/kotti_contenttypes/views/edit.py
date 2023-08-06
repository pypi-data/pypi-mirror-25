# -*- coding: utf-8 -*-

"""
Created on 2016-10-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

import colander
from kotti.views.edit import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config

from kotti_contenttypes import _
from kotti_contenttypes.resources import Folder


class FolderSchema(ContentSchema):
    """ Schema for Folder. """
    pass


@view_config(name=Folder.type_info.add_view,
             permission=Folder.type_info.add_permission,
             renderer='kotti:templates/edit/node.pt')
class FolderAddForm(AddFormView):
    """ Form to add a new instance of Folder. """

    schema_factory = FolderSchema
    add = Folder
    item_type = _(u"Folder")


@view_config(name='edit', context=Folder, permission='edit',
             renderer='kotti:templates/edit/node.pt')
class FolderEditForm(EditFormView):
    """ Form to edit existing Folder objects. """

    schema_factory = FolderSchema
