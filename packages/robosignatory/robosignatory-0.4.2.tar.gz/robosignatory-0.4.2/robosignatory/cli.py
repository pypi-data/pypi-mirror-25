import fedmsg.config
import koji
import sys

from robosignatory.tagconsumer import TagSignerConsumer
import robosignatory.utils as utils
import robosignatory.work

import logging
logging.basicConfig(level=logging.INFO)


def tagsigner():
    if len(sys.argv) != 5:
        print 'Usage: %s <koji-instance> <build-nvr> <curtag> <skiptag>' % sys.argv[0]
        print 'skiptag: yes or no'
        sys.exit(1)

    koji_instance = sys.argv[1]
    build_nvr = sys.argv[2]
    curtag = sys.argv[3]
    skiptag = sys.argv[4] == 'yes'

    signer = TagSignerConsumer(None)
    signer.dowork(build_nvr, None, curtag, koji_instance, skiptag)


def atomicsigner():
    if len(sys.argv) not in [3, 4]:
        print 'Usage: %s <ref> <commitid> [--skip-ref-update]' % sys.argv[0]
        sys.exit(1)

    ref = sys.argv[1]
    commitid = sys.argv[2]

    doref = True
    if len(sys.argv) == 4:
        if sys.argv[3] != '--skip-ref-update':
            print 'Usage: %s <ref> <commitid> [--skip-ref-update]' % sys.argv[0]
            sys.exit(1)
        doref = False

    config = fedmsg.config.load_config([], None)

    signing_config = self.hub.config['robosignatory.signing']
    signer = utils.get_signing_helper(**signing_config)

    if ref not in config['robosignatory.ostree_refs']:
        print 'Ref %s not found' % ref
        sys.exit(1)

    val = config['robosignatory.ostree_refs'][ref]

    robosignatory.work.process_atomic(signer, ref, commitid, doref=doref, **val)

def modulesigner():
    if len(sys.argv) != 3:
        print 'Usage: %s <koji-instance> <module-tag>' % sys.argv[0]
        sys.exit(1)

    koji_instance = sys.argv[1]
    tag = sys.argv[2]

    signer = TagSignerConsumer(None)
    signer.sign_modular_tag(koji_instance, tag)
