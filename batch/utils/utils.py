import urllib.parse
import simplejson as json


def get_database_connection_string(config_path='config.json'):
    with open(config_path) as config_file:
        conf_str = config_file.read()
        config = json.loads(conf_str)
        config = config['SQL_DATABASE']

    connection_string = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(
        f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={config['sqlserver']};DATABASE={config['database']};"
        f"UID={config['user']};PWD={config['password']}")

    return connection_string
