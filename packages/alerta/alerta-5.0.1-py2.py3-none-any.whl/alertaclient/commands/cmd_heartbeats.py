
import click

from tabulate import tabulate


@click.command('heartbeats', short_help='List heartbeats')
@click.option('--purge', is_flag=True, help='Delete stale heartbeats')
@click.pass_obj
def cli(obj, purge):
    """List heartbeats."""
    client = obj['client']
    timezone = obj['timezone']
    headers = {
        'id': 'ID', 'origin': 'ORIGIN', 'customer': 'CUSTOMER', 'tags': 'TAGS', 'createTime': 'CREATED',
        'receiveTime': 'RECEIVED', 'latency': 'LATENCY', 'timeout': 'TIMEOUT', 'since': 'SINCE', 'status': 'STATUS'
    }
    heartbeats = client.get_heartbeats()
    click.echo(tabulate([h.serialize(timezone) for h in heartbeats], headers=headers, tablefmt=obj['output']))

    expired = [hb for hb in heartbeats if hb.status == 'expired']
    if purge:
        with click.progressbar(expired, label='Purging {} heartbeats'.format(len(expired))) as bar:
            for b in bar:
                client.delete_heartbeat(b.id)
