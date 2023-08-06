import click
import time

cards = [
            "2s","3s","4s","5s","6s","7s","8s","9s","10s","Js","Qs","Ks","As"
            "2h","3h","4h","5h","6h","7h","8h","9h","10h","Jh","Qh","Kh","Ah"
            "2d","3d","4d","5d","6d","7d","8d","9d","10d","Jd","Qd","Kd","Ad"
            "2c","3c","4c","5c","6c","7c","8c","9c","10c","Jc","Qc","Kc","Ac"
           ]
###################################################################################
####################### CASSANDRA CLUSTER MANAGEMENT ##############################
###################################################################################
@click.group()
@click.version_option(version='0.1.0')
def cli():
    """HRL Laboratory Manager.
    This is the client manager for the laboratory infraestructure
    """

@cli.group()
def upgrade_venv():
    """Manages Cassandra Cluster."""


@upgrade_venv.command('new')
@click.argument('keyspace', type=str)
@click.option('--host', metavar='H', default=['127.0.0.1'], help='Hosts for Cassandra Connection')
@click.option('--port', metavar='P', default=9042, help='Port for Cassandra Connection')
@click.option('--username', metavar='u', default='', help='Username for Cassandra Connection')
@click.option('--password', metavar='pwd', default='', help='Password for Cassandra Connection')
def ship_new(keyspace, host, port, username, password):
    """Creates a new upgrade_venv keyspace."""
    click.secho("Connecting to Cassandra Cluster with: ", fg='green', bold=True)
    click.secho(" Host: {}".format(host), fg='yellow')
    click.secho(" Port: {}".format(port), fg='yellow')
    click.secho(" Username: {}".format(username), fg='yellow')
    click.secho(" Password: {}".format(password), fg='yellow')


    with click.progressbar(cards,
                       label='Creating the database model',
                       length=len(cards)) as bar:
        for user in bar:
            time.sleep(0.1)
    click.echo('Created keyspace {0}'.format(keyspace))


@upgrade_venv.command('list')
@click.argument('upgrade_venv')
@click.argument('x', type=float)
@click.argument('y', type=float)
@click.option('--speed', metavar='KN', default=10,
              help='Speed in knots.')
def ship_move(ship, x, y, speed):
    """Moves SHIP to the new location X,Y."""
    click.echo('Moving upgrade_venv %s to %s,%s with speed %s' % (ship, x, y, speed))


@upgrade_venv.command('shoot')
@click.argument('upgrade_venv')
@click.argument('x', type=float)
@click.argument('y', type=float)
def ship_shoot(ship, x, y):
    """Makes SHIP fire to X,Y."""
    click.echo('Ship %s fires to %s,%s' % (ship, x, y))


if __name__ == '__main__':
    cli()
    