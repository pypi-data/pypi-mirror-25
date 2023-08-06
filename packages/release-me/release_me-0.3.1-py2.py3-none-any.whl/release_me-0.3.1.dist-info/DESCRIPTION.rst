releaseme - small CLI client for Github release API
===================================================

Creating releases from browser can be a bit tedious if you already wrote the
release notes and prepared packages in your beloved terminal. But fear not my
friend, this simple wrapper makes it possible to do the finishing touches
without having to switch to the browser.


Quickstart
----------

Installing this package is as simple as running::

    $ pip install release-me

This being out of the way, we must now obtain the personal access token that
this client will use to interact with Github's API. How to get one is neatly
described on `Github's personal access token page`_.

.. _Github's personal access token page:
    https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/

Now that we created the token, we must inform our tool about it. We do this by
setting ``RELEASEME_TOKEN`` environment variable that contains the token::

    $ export RELEASEME_TOKEN=our-token-from-github

Now we are ready to create some releases (and then delete them once we
discover that our code sucks and create them again once we fix most of the
bugs). But before we can proceed, we must write down release notes::

    $ cd /home/tadej/personal/release-me
    $ cat <<EOF > release.notes
    > This is the initial release of release-me package.
    >
    > I would like to say thank you to my kids for being a good sports and
    > getting to bed early, which gives me time to write dummy release notes.
    > EOF

That should do it. Now, we would also like to host our python package on
release page, just because we can. So we will build a tarball that will be
added to release. You can leave out this step if adding assets to release is
not something you would like to do. So, building a package::

    $ python setup.py sdist
    running sdist
    [pbr] Writing ChangeLog
    [pbr] Generating ChangeLog
    [pbr] ChangeLog complete (0.0s)
    ...
    Creating tar archive
    removing 'release-me-0.3.0' (and everything under it)

Now we can finally promote ``0.3.0`` tag in ``tadeboro/release-me`` repository
to full release named *The best release ever*::

    $ releaseme create -r tadeboro/release-me -t 0.3.0 -n release.notes \
    >   -l "The best release ever" -a dist/release-me-0.3.0.tar.gz
    [INFO] - Creating release for tag tadeboro/release-me 0.3.0
    [INFO] - Uploading asset dist/release-me-0.3.0.tar.gz for 5837083

And this is it. We are done.

We can have a look at the fruits of our labor by running ``get`` command. Yep,
we have a get command to::

    $ releaseme get -r tadeboro/release-me -t 0.3.0
    [INFO] - Getting release for tag 0.3.0
    {
      "created_at": "2016-07-17T16:58:03Z",
    ...
      "url": "https://api.github.com/repos/tadeboro/release-me/releases/5837083",
      "zipball_url": "https://api.github.com/repos/tadeboro/release-me/zipball/0.3.0"
    }

And when we realize that releasing our code after drinking n beers was not the
brightest idea we had this week, we can remove the release by running::

    $ releaseme delete -r tadeboro/release-me -t 0.3.0
    [INFO] - Getting release for tag 0.3.0
    [INFO] - Deleting release for tag 0.3.0


More documentation
------------------

There is no more documentation. If you feel you need more information, feel
free to read the sources.



