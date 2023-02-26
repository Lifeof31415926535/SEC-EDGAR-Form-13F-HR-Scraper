import argparse

from abc import ABC, abstractmethod

import src.cli.base as base

from .register import register
from src.db.create_db import DbCreator
from .parsers import Parser, ParserOption
from src.db.create_tables import TableCreator


@register
class CreateDb(base.Command):
    command_name = 'create-db'

    def execute(self, argv: dict):
        creator = DbCreator()
        creator.create_db_user()
        creator.create_db()
        creator.grant_privileges()


@register
class CreateTables(base.Command):
    command_name = 'create-tables'
    _parser_options = [
        ParserOption(
            flag='t',
            long_flag='Tables',
            values=['all', 'source', 'filing', 'filing-info'],
            default_value='all'
        )
    ]

    _method_map = {
        'all': 'create_all',
        'source': 'create_source',
        'filing': 'create_filing',
        'filing-info': 'create_filing_info',
    }

    def execute(self, argv: list):
        parser = Parser(argv, options=self._parser_options)
        option = parser.parse()[0]

        table_creator = TableCreator()
        method = getattr(table_creator, self._method_map[option.argument])
        method()
