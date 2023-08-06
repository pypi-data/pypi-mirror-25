# Redmine Tidy

*Close Redmine tickets that have not been recently updated.*

This is a script that uses the Redmine API to close issues that have not been updated for a specified number of weeks.

USE AT YOUR OWN RISK!  Make sure you understand what is going on and the fact that this could change the status of every single ticket in your system if you give it the wrong arguments.  The '-n/--dry-run' argument is certainly one you should use a lot!

## Example use

    redmine-tidy.py --url http://issues.mycompany.com --key MY_REDMINE_API_KEY --weeks 52

Run the script with --help to see the full syntax.

You can find your API access key by logging into Redmine and looking at your account details.

## Installation & Configuration

Redmine Tidy is a single script (redmine-tidy.py) but makes use of a couple of other python packages.
It's easiest to install it with pip:

    pip install redmine-tidy

It should work under Python 2.7 or later.

Instead of putting arguments on the command line, you can put them in a JSON config file, or you can do a combination of both.  Putting your API key in the config file and making the file not-publicly-readable is a better idea than putting it on the command line.

See the output of 'redmine-tidy.py --help' for more information.

## Usage notes

We find it useful to have a new issue status called 'Abandoned' which is essentially the same as 'Closed' but which can be used to identify tickets tidied up by this system.  Note that if you create this in Redmine, you also need to edit the Workflow to allow valid transitions to and from the other states.

Then you can add '--status Abandoned' to your command line.

## Disclaimer

You use this at your own risk.  The author will not be liable for any unintended consequences of its use!

## Licence

This software is distributed under the terms of the GNU General Public License v2.

