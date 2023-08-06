# -*- coding: utf-8 -*-

"""
Created on 2016-10-18
:author: Oshane Bailey (b4.oshany@gmail.com)
"""

from pytest import raises


def test_model(root, db_session):
    from kotti_contenttypes.resources import Folder

    cc = Folder()
    assert cc.custom_attribute is None

    cc = Folder(custom_attribute=u'Foo')
    assert cc.custom_attribute == u'Foo'

    root['cc'] = cc = Folder()
    assert cc.name == 'cc'

    with raises(TypeError):
        cc = Folder(doesnotexist=u'Foo')
