import click
from icheckin import connections, constants

@click.command('update', short_help='check for updates')
def command():
   click.echo('Current version: %s' % constants.VERSION)
   click.echo('Checking for updates...')
   update = connections.update_status()
   if update == True:
      click.echo('Up to date.')
   elif update == False:
      click.echo('Failed.')
   else:
      click.echo(
         'A newer version (%s) is available.\n' % update + 
         '$ pip install --upgrade icheckin')
