How to contribute
=================

Write a patch
-------------

Help yourself with the `documentation <http://docs.weboob.org/>`_.

Find an opened issue on `this website <https://git.weboob.org/weboob/devel/issues>`_, or write your own bugfix or feature.
Then, once it is necessary, commit with::

    $ git commit -a

Do not forget to write a helpful commit message.

Check your patch
----------------

You can run these scripts to be sure your patch doesn't break anything::

    $ tools/pyflakes.sh
    $ tools/weboob_lint.sh
    $ tools/run_tests.sh yourmodulename  # or without yourmodulename to test everything

Perhaps you should also write or fix tests. These tests are automatically run by
`Gitlab CI <https://git.weboob.org/weboob/devel/pipelines>`_ at each commit and merge requests.

Create a merge request or send a patch
--------------------------------------

The easiest way to send your patch is to create a fork on `the Weboob Gitlab <https://git.weboob.org>`_ and create a merge
request from there. This way, the code review process is easier and continuous integration is run automatically (see
previous section).

If you prefer good old email patches, just use

::

    $ git format-patch -n -s origin

Then, send them with this command::

    $ git send-email --to=weboob@weboob.org *.patch

You can also send the files by yourself if you haven't any configured MTA on your system.
