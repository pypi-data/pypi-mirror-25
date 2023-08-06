#! /usr/bin/env python
#
#   Copyright (c) 2017 Quentin Stafford-Fraser.   
#   All rights reserved, subject to the following:
#
#   This is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This software is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this software; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307,
#   USA.
#
"""
Abandon Redmine tickets which have not been updated for some time.

Usage:
  redmine-tidy.py [options] [PROJECT]

Options:
  -h --help           Show this help message and exit
  -u --url URL        Base URL for Redmine instance 
  -k --key KEY        API key for Redmine user
  -l --list           List projects and exit
  -w --weeks N        Issues older than this will be abandoned [default: 108]
  -s --status STATUS  Status to use for abandoned issues [default: Closed]
  -n --dry-run        Don't actually do it, just report
  -c --config CONFIG_FILE  JSON file containing arguments [default: /etc/redmine-tidy.json]

If you specify a PROJECT, then only it will be checked (non-recursively).
Otherwise all projects will be examined.

A config file will be read if it exists, and should contain a dictionary
mapping the long-form option names to values, e.g.

    {
        "--url": "http://redmine.mycompany.com",
        "--key": "4e4a7cf4aa37752fbcca0c8969471d406c31d6bc",
        "--weeks": 200,
        "--status": "Abandoned"
    }

NOTE that values in the config file will OVERRIDE values specified on the
command line if both are specified: not really ideal.
"""

from datetime import datetime, timedelta
import json
import os
import sys

from docopt import docopt
from redminelib import Redmine

JOURNAL_NOTE = """
This ticket is being closed automatically since there have been no updates for a long time.

Please re-open it if you feel it still to be important.
"""

def tidy_project(redmine, project, threshold_date, new_status, dry_run=True):
    print("Tidying project '{}' ({})".format(project.name, project.identifier))

    # After doing the following, I discovered an alternative:
    # using filters.  Not needed except if performance becomes an issue.

    for issue in project.issues:
        # Only deal with top-level issues: don't recurse at this point
        if issue.project.id == project.id:
            if issue.updated_on < threshold_date:
                print("  {:4d}: {} {}".format(issue.id, issue.updated_on, issue.subject))
                if not dry_run:
                    print("        Changing to '{}'.".format(new_status.name))
                    redmine.issue.update(issue.id, status_id=new_status.id, notes=JOURNAL_NOTE)
                else:
                    print("        Would change to '{}', if dry run not requested.".format(new_status.name))


def main():
    args = docopt(__doc__)

    config_file_name = args['--config']
    if os.path.exists(config_file_name):
        with open(config_file_name, 'r') as fp:
            print("Reading {}".format(config_file_name))
            args.update(json.load(fp))

    redmine = Redmine(args['--url'], key=args['--key'])
    threshold_date = datetime.now() - timedelta(weeks=int(args['--weeks']))
    dry_run = args.get('--dry-run', False)

    # List projects if requested
    if args.get('--list'):
        projects = redmine.project.all()
        for project in projects:
            print("{} ({})".format(project.identifier, project.name))
        return

    # What status shall we use for old issues?
    new_status_name = args.get('--status')
    new_status = None
    statuses = redmine.issue_status.all()
    for status in statuses:
        if status.name == new_status_name:
            new_status = status
            break
    if new_status is None:
        print("Status '{}' not found".format(new_status_name))
        sys.exit(1)

    # OK - let's get tidying
    if args.get('PROJECT'):
        tidy_project(redmine, redmine.project.get(args['PROJECT']), threshold_date, new_status, dry_run)
    else:
        projects = redmine.project.all()
        for project in projects:
            tidy_project(redmine, project, threshold_date, new_status, dry_run)


if __name__ == '__main__':
    main()
