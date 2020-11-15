import itertools
import typing as t

import sqlparse
import networkx


class Parser:

    def __init__(self, queries: t.List[str]):
        self.graph: networkx.DiGraph = self.link(queries)

    @staticmethod
    def link(queries: t.List[str]) -> networkx.DiGraph:
        graph = networkx.DiGraph()

        for query in queries:
            edges = Parser._parse_query(query)
            graph.add_edges_from(edges)

        return graph

    @staticmethod
    def _parse_query(query: str) -> t.Iterator[t.Tuple[t.Any]]:
        parsed = sqlparse.parse(query)[0]

        target_clause = Parser._extract_target_clause(parsed)
        target_tables = list(Parser._extract_table_identifiers(target_clause))

        source_clause = Parser._extract_source_clause(parsed)
        source_tables = list(Parser._extract_table_identifiers(source_clause))

        return itertools.product(source_tables, target_tables)

    @staticmethod
    def _is_subselect(parsed: sqlparse.sql.Statement) -> bool:
        if not parsed.is_group:
            return False
        for item in parsed.tokens:
            if item.ttype is sqlparse.tokens.DML and item.value.upper() == 'SELECT':
                return True
        return False

    @staticmethod
    def _extract_target_clause(parsed: sqlparse.sql.Statement) -> t.Generator:
        insert_or_update_seen = False
        for item in parsed.tokens:
            if insert_or_update_seen:
                if item.ttype in {sqlparse.tokens.Keyword, sqlparse.tokens.DML}:
                    return
                else:
                    yield item
            elif item.ttype is sqlparse.tokens.Keyword and (item.value.upper() in {'INTO', 'UPDATE'}):
                insert_or_update_seen = True

    @staticmethod
    def _extract_source_clause(parsed: sqlparse.sql.Statement) -> t.Generator:
        from_seen = False
        for item in parsed.tokens:
            if from_seen:
                if Parser._is_subselect(item):
                    yield from Parser._extract_source_clause(item)
                elif item.ttype is sqlparse.tokens.Keyword:
                    if 'JOIN' in item.value.upper() or 'USING' in item.value.upper() or 'ON' in item.value.upper():
                        continue
                    else:
                        return
                else:
                    yield item
            elif item.ttype is sqlparse.tokens.Keyword and item.value.upper() == 'FROM':
                from_seen = True

    @staticmethod
    def _extract_table_identifiers(token_stream) -> t.Generator:
        for item in token_stream:
            if isinstance(item, sqlparse.sql.IdentifierList):
                for identifier in item.get_identifiers():
                    yield identifier.get_name()
            elif isinstance(item, sqlparse.sql.Identifier):
                yield item.get_name()
            elif item.ttype is sqlparse.tokens.Keyword:
                yield item.value
