# HIBP Password Lookup

HIBP Password Lookup uses a local copy of the Have I been pwned? list of
password hashes to enable quick local lookups. It allows users to check all
of the passwords they currently use without the risk of leaking them out to
a third-party service.

## Dependencies

- The [password list](https://haveibeenpwned.com/Passwords) from *Have I been pwned?*
- A local [PostgreSQL](https://www.postgresql.org/) database server
- [Psycopg](http://initd.org/psycopg/) (`python3-psycopg2` on Debian)

### Load the database

Create a new database:

    createdb hibp-passwords

then [populate the DB](https://www.postgresql.org/docs/current/static/populate.html):

    psql hibp-passwords
    BEGIN;
    CREATE TABLE password ( hash VARCHAR(40) NOT NULL );
    COPY password FROM '/passwords/pwned-passwords-1.0.txt';
    COPY password FROM '/passwords/pwned-passwords-update-1.txt';
    COPY password FROM '/passwords/pwned-passwords-update-2.txt';
    CREATE INDEX ON password ( hash );
    COMMIT;

That should give you 320M hashes:

    > select count(*) from password;
       count   
    -----------
     320335236

Note: the index takes a lot of space (more than 20 GB). You can remove it
once you are done checking all of your passwords, but be advised that
lookups may take up to a minute:

    DROP INDEX password_hash_idx;

## Usage

    hibp-pwlookup [-h] [-q] [-V] [password]

If you don't specify the password on the command line, it will default to
reading from STDIN, which means you can type the password followed by enter.

**Warning**: if you specify your password as an argument, it will likely be
saved in your shell history (e.g. `~/.bash_history`).

## License

Copyright (C) 2017  Francois Marier <francois@fmarier.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
francois@akranes:~/devel/remote/hibp-pwlookup| 
