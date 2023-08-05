#!/usr/bin/env python
"""
Show some basic information from IT4I PBS accounting
"""
import getopt
import getpass
import sys
import urllib2
import simplejson as json

from logger import LOGGER
from tabulate import tabulate

TABLE_ME_TITLE = 'Projects I am participating in'
TABLE_ME_AS_PI_TITLE = 'Projects I am Primarily Investigating'
TABLE_LEGENDS_TITLE = 'Legend'

def errmsg(msg, retval=1):
    """
    print help and exit
    """

    if not msg:
        my_name = __name__.split('.')[-1]
        LOGGER.error('usage: %s', my_name)
        LOGGER.error('       %s -h|--help', my_name)
        LOGGER.error('''
The command shows some basic information from IT4I PBS accounting. The
data is related to the current user and to all projects in which he/she
participates.

After the invocation, the user is asked for his/her IT4I login/password.

Columns of "%s":
         PID: Project ID/account string.
   Days left: Days till the given project expires.
       Total: Core-hours allocated to the given project.
        Used: Sum of core-hours used by all project members.
    ...by me: Core-hours used by the current user only.
        Free: Core-hours that haven't yet been utilized.

Columns of "%s" (if present):
         PID: Project ID/account string.
       Login: Project member's login name.
        Used: Project member's used core-hours.

''', TABLE_ME_TITLE, TABLE_ME_AS_PI_TITLE)
    else:
        LOGGER.error(msg)
    sys.exit(retval)

def main(argv=sys.argv[1:]):
    """
    main function
    """

    # parse opts and args
    try:
        opts, args = getopt.getopt(argv, "h", ["help"])
    except getopt.GetoptError as err:
        LOGGER.error(str(err))
        errmsg(None)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            errmsg(None)

    from config import config_files
    from config import config
    from config import api_url
    from config import it4ifreetoken

    if not api_url.startswith('https://'):
        LOGGER.error("The API URL is not secured using https://")
        sys.exit(1)

    username = getpass.getuser()
    username = username.strip()
    #password = getpass.getpass()
    #remote = re.sub('://', '://%s:%s@' % (username, password), api_url, 1)
    remote = ('%s/it4ifree/%s' % (api_url, username))
    data = {'it4ifreetoken' : it4ifreetoken}
    try:
        req = urllib2.Request(remote)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
    except Exception:
        errmsg('Sorry, there was a problem accessing the service. Please try again later.')

    #print response.getcode()
    #print response.read()
    try:
        jsonout_raw = response.read()
    except Exception:
        errmsg('Sorry, there was a problem accessing the service. Please try again later.')

    jsonout = json.loads(jsonout_raw)

    table_me = []
    for row in jsonout['me']:
        table_me.append([row['pid'],
                         row['days_left'],
                         row['total'],
                         row['used'],
                         row['used_with_factor'],
                         row['used_by_me'],
                         row['used_by_me_with_factor'],
                         row['free']])
    table_me_headers = ['PID',
                        'Days left',
                        'Total',
                        'Used WCHs',
                        'Used NCHs',
                        'WCHs by me',
                        'NCHs by me',
                        'Free']

    table_me_as_pi = []
    row_previous = ''
    for row in jsonout['me_as_pi']:
        table_me_as_pi.append([row['pid'] if row['pid'] != row_previous else '',
                               row['login'],
                               row['core_hours'],
                               row['core_hours_with_factor']])
        row_previous = row['pid']
    table_me_as_pi_headers = ['PID',
                              'Login',
                              'Used WCHs',
                              'Used NCHs']

    if table_me:
        print >> sys.stdout, '\n%s\n%s' % (TABLE_ME_TITLE,
                                           len(TABLE_ME_TITLE) * '=')
        print tabulate(table_me, table_me_headers)

    if table_me_as_pi:
        print >> sys.stdout, '\n%s\n%s' % (TABLE_ME_AS_PI_TITLE,
                                           len(TABLE_ME_AS_PI_TITLE) * '=')
        print tabulate(table_me_as_pi, table_me_as_pi_headers)

    print >> sys.stdout, '\n%s\n%s' % (TABLE_LEGENDS_TITLE,
                                       len(TABLE_LEGENDS_TITLE) * '=')
    print 'WCH   =    Wall-clock Core-Hour'
    print 'NCH   =    Normalized Core-Hour'


if __name__ == "__main__":
    main()
