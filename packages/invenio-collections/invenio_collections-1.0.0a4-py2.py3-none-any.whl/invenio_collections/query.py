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
# 59 Temple Place, Suite 330, Boston, MA 02D111-1307, USA.

"""Query parser."""

import pypeg2
from invenio_query_parser.walkers.match_unit import MatchUnit

from .utils import parser, query_walkers


class Query(object):
    """Query object."""

    def __init__(self, query):
        """Init."""
        self._query = query

    @property
    def query(self):
        """Parse query string using given grammar.

        :returns: AST that represents the query in the given grammar.
        """
        tree = pypeg2.parse(self._query, parser(), whitespace="")
        for walker in query_walkers():
            tree = tree.accept(walker)
        return tree

    def match(self, record):
        """Check if the record match the query.

        :param record: Record to test.
        :returns: True if record match the query.
        """
        return self.query.accept(MatchUnit(record))
