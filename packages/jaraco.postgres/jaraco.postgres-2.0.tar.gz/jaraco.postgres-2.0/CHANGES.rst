2.0
===

PostgresServer now creates all databases with a default
locale of ``en_US.UTF-8``. Now, databases will be
Unicode-capable by default. To restore the original
behavior, deferring to the system locale, pass
``locale=None`` to ``initdb``.

1.6
===

Add ``.create`` convenience method to PostgresServer.

1.5
===

Project is now released automatically through Travis
Continuous Integration.

Add Trove classifier for Pytest Framework.

1.4
===

Moved hosting to Github and updated skeleton.

1.3
===

Add ``postgresql_instance`` fixture.

1.2
===

Added some logging info to initdb, start, stop.

Substantial improvements for test suite.

1.1
===

Allow the POSTGRESQL_HOME environment variable to stipulate where
the Postgres binaries must be found, overriding heuristic search.

1.0
===

Initial release, using models from yg.test 4.1.
