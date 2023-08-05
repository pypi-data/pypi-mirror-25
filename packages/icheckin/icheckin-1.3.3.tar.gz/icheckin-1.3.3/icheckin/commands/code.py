import sys
import click
from icheckin import credentials, connections

@click.command('code', short_help='check-in with code')
@click.argument('checkincode')
@click.option('--multi', is_flag=True, help='Check-in multiple credentials.')
def command(checkincode, multi):
   # Check primary credentials
   primary = credentials.primary()
   if primary != ():
      click.echo()
      for cred in credentials.read():
         click.echo('Checking-in for %s... ' % cred[0], nl=False)
         status = connections.checkin(cred, checkincode)
         if status == 0:
            click.echo('[Successful]')
         elif status == 1:
            click.echo('[No internet connection]')
            sys.exit(0)
         elif status == 2:
            click.echo('[Invalid credentials]')
         elif status == 3:
            click.echo('[Not connected to SunwayEdu Wi-Fi]')
            sys.exit(0)
         elif status == 4:
            click.echo('[Invalid code]')
            sys.exit(0)
         elif status == 5:
            click.echo('[Wrong class]')
         elif status == 6:
            click.echo('[Already checked-in]')
         if not multi:
            break
      click.echo('\nDone.')
   else:
      click.echo('Save primary credentials first before checking-in.')