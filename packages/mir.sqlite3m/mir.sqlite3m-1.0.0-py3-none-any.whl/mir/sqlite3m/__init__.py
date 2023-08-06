# Copyright (C) 2017 Allen Li
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Simple monotonic SQLite database migration manager

sqlite3m works with any DB-API 2.0 compliant SQLite library, using the
standard library sqlite3 as a reference.

Migration functions are registered with a MigrationManager, which can
then be used to migrate any DB-API 2.0 connection to a SQLite database.
The version of the database is tracked using SQLite user_version.

>>> import sqlite3
>>> manager = MigrationManager()
>>> @manager.migration(0, 1)
... def create_table(conn):
...     conn.execute('CREATE TABLE foo ( bar )')
>>> conn = sqlite3.connect(':memory:')
>>> manager.migrate(conn)
"""

__version__ = '1.0.0'

import contextlib
import logging
from typing import NamedTuple

logger = logging.getLogger(__name__)


class MigrationManager:

    """Simple monotonic SQLite migration manager."""

    def __init__(self, initial_ver=0):
        self._migrations = {}
        self._final_ver = initial_ver
        self._wrappers = []

    def __repr__(self):
        cls = type(self).__qualname__
        return (f'<{cls} with migrations={self._migrations!r},'
                f' final_ver={self._final_ver!r}>')

    def register_migration(self, migration: 'Migration'):
        """Register a migration.

        You can only register migrations in order.  For example, you can
        register migrations from version 1 to 2, then 2 to 3, then 3 to
        4.  You cannot register 1 to 2 followed by 3 to 4.
        """
        if migration.from_ver >= migration.to_ver:
            raise ValueError('Migration cannot downgrade verson')
        if migration.from_ver != self._final_ver:
            raise ValueError('Cannot register disjoint migration')
        self._migrations[migration.from_ver] = migration
        self._final_ver = migration.to_ver

    def migration(self, from_ver: int, to_ver: int):
        """Decorator to create and register a migration.

        >>> manager = MigrationManager()
        >>> @manager.migration(0, 1)
        ... def migrate(conn):
        ...     pass
        """
        def decorator(func):
            migration = Migration(from_ver, to_ver, func)
            self.register_migration(migration)
            return func
        return decorator

    def register_wrapper(self, wrapper: 'Callable[[Connection], Any]'):
        """Register a wrapper."""
        self._wrappers.append(wrapper)

    def migrate(self, conn):
        """Migrate a database as needed.

        This method is safe to call on an up-to-date database, on an old
        database, on a newer database, or an uninitialized database
        (version 0).

        This method is idempotent.
        """
        while self.should_migrate(conn):
            current_version = get_user_version(conn)
            migration = self._get_migration(current_version)
            assert migration.from_ver == current_version
            logger.info(f'Migrating database from {migration.from_ver}'
                        f' to {migration.to_ver}')
            self._migrate_single(conn, migration)
            set_user_version(conn, migration.to_ver)
            logger.info(f'Migrated database to {migration.to_ver}')

    def should_migrate(self, conn) -> bool:
        """Check if the database needs migration."""
        return get_user_version(conn) < self._final_ver

    def _migrate_single(self, conn, migration):
        """Perform a single migration starting from the given version."""
        with contextlib.ExitStack() as stack:
            for wrapper in self._wrappers:
                stack.enter_context(wrapper(conn))
            migration.func(conn)

    def _get_migration(self, version: int) -> 'Migration':
        try:
            return self._migrations[version]
        except KeyError:
            raise MissingMigrationError(version)


class Migration(NamedTuple):
    """Migration describes one migration operation."""
    from_ver: int
    to_ver: int
    func: 'Callable[[Connection], Any]'


class MigrationError(Exception):
    """Class for all migration errors."""


class MissingMigrationError(MigrationError):
    """The required Migration for the current database version is missing."""

    def __init__(self, version: int):
        super().__init__(f'No registered migration for version {version:d}')
        self.version = version


class ForeignKeyError(MigrationError):
    """The database has failing foreign key checks."""

    def __init__(self, errors):
        super().__init__(f'Foreign key check found errors: {errors}')
        self.errors = errors


@contextlib.contextmanager
def CheckForeignKeysWrapper(conn):
    """Migration wrapper that checks foreign keys.

    Note that this may raise different exceptions depending on the
    underlying database API.
    """
    yield
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_key_check')
    errors = cur.fetchall()
    if errors:
        raise ForeignKeyError(errors)


def get_user_version(conn):
    cur = conn.cursor()
    cur.execute('PRAGMA user_version')
    return cur.fetchone()[0]


def set_user_version(conn, value: int):
    cur = conn.cursor()
    cur.execute(f'PRAGMA user_version={value:d}')
