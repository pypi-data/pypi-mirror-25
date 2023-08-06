from distutils.core import setup

setup(
    name = 'hibp-pwlookup',
    version = '0.1.0',
    description = 'Local lookup tool for the HIBP password database',
    author = 'Francois Marier',
    author_email = 'francois@fmarier.org',
    url = 'https://launchpad.net/hibp-pwlookup',
    scripts = ['hibp-pwlookup'],
    keywords = ['passwords', 'security'],
    license = 'AGPL-3.0+',
    requires = ['psycopg2'],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Topic :: Security",
        ],
    long_description = """\
HIBP Password Lookup uses a local copy of the Have I been pwned?
list of password hashes to enable quick local lookups. It allows
users to check all of the passwords they currently use without the
risk of leaking them out to a third-party service.

It requires a copy of the hashed password database from HIBP:

  https://haveibeenpwned.com/Passwords

.. _project page: https://launchpad.net/hibp-pwlookup
"""
    )
