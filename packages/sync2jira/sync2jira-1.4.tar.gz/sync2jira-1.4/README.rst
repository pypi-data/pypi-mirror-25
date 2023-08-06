sync2jira
=========

This is a process that listens to activity on upstream repos on pagure and
github via fedmsg, and syncs new issues there to a Jira instance elsewhere.

Configuration
-------------
Configuration is in ``fedmsg.d/``.

You can maintain a mapping there that allows you to match one upstream repo
(say, 'pungi' on pagure) to a downstream project/component pair in Jira (say,
'COMPOSE', and 'Pungi').

On startup, if the ``initialize`` option is set to ``True`` in the
``fedmsg.d/`` config, then all open issues from all upstream repos will be
scraped and added to Jira if they are absent.

If the ``testing`` option is set to ``True``, then the script will perform a
"dry run" and not actually add any new issues to Jira.

Caveats
-------

Here are some things that this program *does not do*:

- This program does not close Jira tickets when their corresponding ticket is
  closed upstream, although that would be cool.
- This program does not attempt to copy comments from upstream tickets to their
  corresponding downstream tickets, although that would be cool.

If there is interest in having those things, please file an RFE or comment on
an existing one `here <https://pagure.io/sync-to-jira/issues>`_ and we'll see
about prioritizing it.

Tests
-----

We have decent test coverage.

Run the tests with::

    $ sudo dnf install detox
    $ detox
