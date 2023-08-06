from pgreaper import PG_DEFAULTS
import pgreaper
import click

@click.command()
@click.option('--csv', default=False, help='Copy a CSV or other delimiter '
    'separated file')
@click.option('--delim', default=',', help='Delimiter')
@click.option('--dbname', default=PG_DEFAULTS['dbname'], help='PostgreSQL database')
@click.option('--user', default=PG_DEFAULTS['user'], help='PostgreSQL user')
@click.option('--host', default=PG_DEFAULTS['host'], help='PostgreSQL host')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
@click.argument('file')
def cli_copy(file, csv, delim, dbname, user, host, password):
    ''' Main interface to Postgres uploading functions '''
    
    if csv:
        pg_reaper.copy_csv(file, delimiter=delim,
            dbname=dbname, user=user, host=host, password=password)