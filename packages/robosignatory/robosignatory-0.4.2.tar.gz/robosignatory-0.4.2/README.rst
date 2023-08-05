=============
robosignatory
=============

A fedmsg consumer that automatically signs artifacts.

RoboSignatory is composed of multiple consumers:
- TagConsumer is a consumer that listens for tags into a specific koji tag,
  then signs the build and moves it to a different koji tag.
- AtomicConsumer is a consumer that listens for messages about composed
  rpmostree trees and signs those, optionally updating the tag.


Signing Configuration
---------------------

For an example configuration file, look in config/example-config.py.
This should be placed in /etc/fedmsg.d/robosignatory.py (or some other name in
that directory).

The only generic part in there is the signing part, for the other options
please check the parts below in this document.

For signing, the one argument you always provide is "backend".
This is the name of a robosignatory.signing.helpers setuptools entry point.

Pre-shipped are "echo" and "sigul".

The other arguments in this section are passed as keyword arguments to the
helper's __init__ method, so are specific for the module you choose to use.


Koji Tag Consumer
-----------------

To enable TagConsumer, set robosignatory.enabled.tagsigner to True.

Then you will need to add all the koji "instances" your setup should be aware
of under robosignatory.koji_instances. The url is the link to the kojihub main
url of the instance.

Options contains authentication information.
There are two authmethods available:
ssl, which takes arguments cert and serverca (both required).
kerberos, which takes arguments principal, keytab and ccache (all optional).

In the tags part of the instance configuration is the real configuration for
the TagConsumer.
It is a list, with each entry being a dict with the tag that should be watched,
a key name (passed to the signing module to indicate which key to use) and
keyid (passed to koji to indicate which signatures need to be written out).
The entry also has a "to" tag, to indicate where builds need to be moved to
after being signed.

Note that "from" and "to" can be the same tag, in this case builds will not be
moved after being signed.

Example:
::
  {
    "from": "f26-pending",
    "to": "f26",
    "key": "fedora-26",
    "keyid": "64dab85d"
  }

This example would watch for any builds tagged into the f26-pending tag.
After it sees a build tagged in this tag, it will look up which RPMs need to be
signed, and pass their names together with the koji instance name and key name
to the signing module.
After the signing module acknowledges that it signed the packages, robosignatory
will tell koji to write the signed RPMs out with the keyid.
If that is done and the "from" tag is different from the "to" tag, it will
issue a koji moveBuild operation, moving the build from "f26-pending" to "f26".
After this, it is done signing the package, and continues to the next step.


Testing Koji Tag Consumer
-------------------------

To test the configuration, you can create the full configuration, and run the
robosignatory-signtagbuild command, providing the name of the koji instance, the
build NVR and the current tag, and whether or not to skip the tag moving.
This will follow the exact same procedures as outlined in the previous section,
printing a lot of information along the way so you can follow what it's doing
exactly.
