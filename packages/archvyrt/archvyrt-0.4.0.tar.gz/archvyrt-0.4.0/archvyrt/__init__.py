#!/usr/bin/python3

"""
Libvirt provisioning for ArchLinux host system.
"""

import argparse
import json
import logging
import os

from archvyrt.domain import Domain
from archvyrt.provisioner.archlinux import ArchlinuxProvisioner
from archvyrt.provisioner.plain import PlainProvisioner
from archvyrt.provisioner.ubuntu import UbuntuProvisioner

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def main():
    """
    main function.

    parse command line arguments, create VM and run the appropriate
    provisioner
    """

    parser = argparse.ArgumentParser(
        description="LibVirt VM provisioner",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--proxy', dest='proxy',
        default=None,
        help='Proxy to use when running provisioning commands'
    )
    parser.add_argument(
        '--mountpoint', dest='mountpoint',
        default='/provision',
        help='Temporary mountpoint for provisioning'
    )
    parser.add_argument(
        'vmdefinition',
        help='Path to VM definition file'
    )
    args = parser.parse_args()

    with open(args.vmdefinition) as jsonfile:
        domain = Domain(json.load(jsonfile))

    if domain.guesttype == 'archlinux':
        os.mkdir(args.mountpoint)
        provisioner = ArchlinuxProvisioner(domain, proxy=args.proxy)
        provisioner.cleanup()
        domain.autostart(True)
        domain.start()
        os.rmdir(args.mountpoint)
    elif domain.guesttype == 'ubuntu':
        os.mkdir(args.mountpoint)
        provisioner = UbuntuProvisioner(domain, proxy=args.proxy)
        provisioner.cleanup()
        domain.autostart(True)
        domain.start()
        os.rmdir(args.mountpoint)
    elif domain.guesttype == 'plain':
        provisioner = PlainProvisioner(domain)
        provisioner.cleanup()
        domain.autostart(True)
    else:
        raise RuntimeError('Unsupported guest type: %s' % domain.guesttype)

    domain.close()
