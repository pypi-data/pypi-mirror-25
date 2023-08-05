# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
# -*- coding: utf-8 -*-
#
# In applying this licence, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

"""Model test cases."""

from __future__ import unicode_literals

from invenio_db import db
from invenio_records.api import Record

from invenio_collections.models import Collection


def test_collection_tree_matcher(app):
    """Test database backend."""
    #                               a
    #                             (None)
    #            +------------------+--------------------+
    #            |                                       |
    #            b                                       e
    #         (None)                        (title:Test2 OR title:Test3)
    #     +------+-----+                    +------------+------------+
    #     |            |                    |            |            |
    #     c            d                    f            g            h
    # (title:Test0) (title:Test1)     (title:Test2)    (None)       (None)
    #                                                    |            |
    #                                                    i            j
    #                                             (title:Test3) (title:Test4))

    with app.test_request_context():
        a = Collection(name="a")
        b = Collection(name="b", parent=a)
        e = Collection(
            name="e", dbquery="title:Test2 OR title:Test3", parent=a)
        c = Collection(name="c", dbquery="title:Test0", parent=b)
        d = Collection(name="d", dbquery="title:Test1", parent=b)
        f = Collection(name="f", dbquery="title:Test2", parent=e)
        g = Collection(name="g", parent=e)
        h = Collection(name="h", parent=e)
        i = Collection(name="i", dbquery="title:Test3", parent=g)
        j = Collection(name="j", dbquery="title:Test4", parent=h)

        with db.session.begin_nested():
            for coll in [a, b, c, d, e, f, g, h, i, j]:
                db.session.add(coll)

        db.session.commit()

        # start tests

        schema = {
            'type': 'object',
            'properties': {
                'title': {'type': 'string'},
                'field': {'type': 'boolean'},
                'hello': {'type': 'array'},
            },
            'required': ['title'],
        }

        record0 = Record.create({'title': 'Test0', '$schema': schema})
        record1 = Record.create({'title': 'Test1', '$schema': schema})
        record2 = Record.create({'title': 'Test2', '$schema': schema})
        record3 = Record.create({'title': 'Test3', '$schema': schema})
        record4 = Record.create({'title': 'Test4', '$schema': schema})

        assert set(record0['_collections']) == set(['a', 'c', 'b'])
        assert set(record1['_collections']) == set(['a', 'b', 'd'])
        assert set(record2['_collections']) == set(['a', 'e', 'f'])
        assert set(record3['_collections']) == set(['a', 'e', 'g', 'i'])
        assert set(record4['_collections']) == set(['h', 'j'])
