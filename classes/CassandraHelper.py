from cassandra.cluster import Cluster
from cassandra.query import dict_factory
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel

from cassandra import InvalidRequest

class CassandraHelper:
    def __init__(self, ip, port=9001):
        self.client = Cluster([ip], port=port)

    def check(self):
        try:
            self.client.connect()
            return True
        except Exception as e:
            return " ".join(str(e).splitlines())

    def parse(self, outputFile):
        session = self.client.connect()
        session.row_factory = dict_factory
        cql_str = 'SELECT * FROM system_schema.keyspaces;'
        simple_statement = SimpleStatement(cql_str, consistency_level=ConsistencyLevel.ONE)
        execute_result = session.execute(simple_statement, timeout=None)
        rows = execute_result._current_rows

        for keyspace in rows:
            keyspace_name  = keyspace["keyspace_name"]

            outputFile.write(f"Keyspace {keyspace_name}\n\n")

            cql_str = f"SELECT * FROM system_schema.tables WHERE keyspace_name = '{keyspace_name}';"
            simple_statement = SimpleStatement(cql_str, consistency_level=ConsistencyLevel.ONE)
            execute_result = session.execute(simple_statement, timeout=None)
            tables = execute_result._current_rows
            for table in tables:
                table_name = table["table_name"]

                outputFile.write(f"Table {table_name}\n")

                cql_str = f"SELECT * FROM {keyspace_name}.{table_name};"
                simple_statement = SimpleStatement(cql_str, consistency_level=ConsistencyLevel.ONE, fetch_size = 100)
                try:
                    execute_result = session.execute(simple_statement, timeout=None)
                    outputFile.write(f"{execute_result._current_rows}\n\n")
                except Exception as e:
                    outputFile.write(f"{' '.join(str(e).splitlines())}\n\n")
