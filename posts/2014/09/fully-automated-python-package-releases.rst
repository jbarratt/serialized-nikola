.. title: Fully Automated Python Package Releases
.. slug: fully-automated-python-package-releases
.. date: 2014-09-04 05:30:26 UTC
.. tags: 
.. link: 
.. description: 
.. type: text

I've recently been working on a set of internal tools for automating common 
processes. It's leveraging some great open source projects 
(`Fabric <http://www.fabfile.org/>`_, `Ansible <http://www.ansible.com/home>`_, 
`Docker <https://www.docker.com/>`_, `Vagrant <http://www.vagrantup.com/>`_, and 
more) but the core functionality is in a python package which we're deploying to
a private PyPi repo. (Not `devpi <http://doc.devpi.net/latest/>`_ yet, but
hopefully soon.)

There are quite a few internal users of our package, so we were finding
ourselves needing to do point releases pretty often. Since we were already using 
fabric, we put a basic version of our release process into a `fabfile.py`, and it's 
grown to the point that a lot of useful things happen when you run `fab
release`.

* We use `bumpversion <https://github.com/peritus/bumpversion>`_ to figure out
  the current and next version numbers, configurably updating the right
  major/minor/point values.
* It opens your default `$EDITOR` with an already-added new section in the
  `HISTORY.rst`, then commits that edit.
* The version is bumped and the release is tagged.
* The software is built
* The build is shipped to the private PyPI Repo
* The documentation is built and then shipped
* Finally, the right channel in our `#slack <http://slack.com>`_ chat room is notified.

All that's left to do is push all the changes to `origin`. This is done manually
in case anything went horribly wrong; it's easy to revert the changes to your
local repository, much uglier when a mess has gone upstream.

You can view the whole `release fabfile.py as a gist
<https://gist.github.com/jbarratt/85c91d7b904462702892>`_. This feels like the
kind of thing that could be (and probably has been) abstracted and generalized,
but this works for now.

There's nothing too complicated in the file, but there are some nice tricks. One
of the most fun capabilities is the Slack integration, which we recently did.
All credit to slack, it was incredibly easy.

.. code-block:: python

    @task
    def notify_slack(version=None):
        """ Notify the slack channel of a new release """
     
        # hardcoded URI from the slack integration panel
        url = ("https://ourteam.slack.com/services/hooks/incoming-webhook"
               "?token=tokenid")
     
        payload = {
            'username': 'ourpackage-fabfile',
            'icon_emoji': ':shipit:',
            'text': 'Deployed version {} of ourpackage-python'.format(version)}
     
        requests.post(url, data=json.dumps(payload))

Automating the release process has made it take seconds and, more importantly,
work identically every time. It's well worth doing. (I just can't shake the
feeling that there's a more generic way to do it.)

**Update**: I was pointed to `zest.releaser
<http://zestreleaser.readthedocs.org/en/latest/>`_ which has the same basic
features, minus the slack integration. You can also use it with
`gocept.zestreleaser.customupload <https://pypi.python.org/pypi/gocept.zestreleaser.customupload>`_ to enable the scp uploading we're doing here via fabric.
