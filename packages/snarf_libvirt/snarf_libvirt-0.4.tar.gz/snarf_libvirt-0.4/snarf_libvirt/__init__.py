import logging
import sys
from contextlib import contextmanager
from pprint import pformat

import libvirt
from lxml import etree

from .xmlHelpers import getDiskImageURLs, getNetworkMacAddr, xml_compare

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)


class KVMLibvirt:
    def __init__(self, connURL, user):
        self.connURL = connURL
        self.user = user

    @property
    def connURLBrief(self):
        return self.connURL[:15] + ' ...'

    @contextmanager
    def openConnection(self):
        """Attempts to open a connection to KVMHost"""
        if self.connURL is None:
            logger.warning('KVMLibvirt.connURL is None')
            return None

        conn = None
        try:
            connString = 'qemu+ssh://%s@%s/system?socket=/var/run/libvirt/libvirt-sock' % \
                (self.user, self.connURL)
            conn = libvirt.open(connString)

            if conn is not None:
                logger.debug(
                    "Successfully opened connection to conn %r" % (conn))
                yield conn
            else:
                logger.warning(
                    "Unable to establish connection to libvirt at %s" % (connString))
                yield None
        except libvirt.libvirtError as err:
            logger.error("Libvirt Error while trying to connect : %r" % (err))
            yield None
        finally:
            if conn is not None:
                conn.close()

    def hasXMLDiff(self, serverXMLPath):
        # First lets get the name of the server we are looking at
        serverETree = etree.parse(serverXMLPath)

        root = serverETree.getroot()

        domainName = root.find('name').text

        logger.debug("Trying to find server name")
        logger.debug('domainName : %s' % (domainName))

        if domainName:
            logger.debug("Searching for domain %s on %s" %
                         (domainName, self.connURLBrief))

            with self.openConnection() as conn:
                if conn is not None:
                    domain = conn.lookupByName(domainName)

                    if domain is not None:
                        logger.debug("Found domain on %s" %
                                     (self.connURLBrief))

                        domainXMLRaw = domain.XMLDesc(0)

                        logger.debug("domainXMLRaw : %s" % (domainXMLRaw))

                        domainXML = etree.fromstring(domainXMLRaw)

                        logger.debug("domainXML : %r" % (domainXML))

                        if xml_compare(root, domainXML, logger.debug):
                            logger.debug('XML Config matches')
                        else:
                            logger.debug('XML Config does not match')
                    else:
                        logger.warning('Unable to find domain %s on %s' %
                                       (domainName, self.connURLBrief))
        else:
            logger.error("Could not find domain name in xml definition")

        return False

    def hasDiskChanges(self, serverXMLPath):
        # First lets get the name of the server we are looking at
        serverETree = etree.parse(serverXMLPath)

        root = serverETree.getroot()

        domainName = root.find('name').text

        logger.debug("Trying to find server name")
        logger.debug('domainName : %s' % (domainName))

        if domainName:
            with self.openConnection() as conn:
                if conn:
                    domain = conn.lookupByName(domainName)

                    if domain:
                        logger.debug("Found domain %s on %s" % (domainName, self.connURLBrief))

                        domXMLRaw = domain.XMLDesc(0)
                        domXML = etree.fromstring(domXMLRaw)

                        return self.compareDiskImages(domXML, root)

                    else:
                        logger.error("Unable to find domain %s on %s" % (domainName, self.connURLBrief))
        else:
            logger.error("Could not find domain name in xml definition")

        logger.info("No new disks elements found")
        return False

    def hasNetworkChanges(self, serverXMLPath):
        # First lets get the name of the server we are looking at
        serverETree = etree.parse(serverXMLPath)

        root = serverETree.getroot()

        domainName = root.find('name').text

        logger.debug("Trying to find server name")
        logger.debug('domainName : %s' % (domainName))

        if domainName:
            with self.openConnection() as conn:
                if conn:
                    domain = conn.lookupByName(domainName)

                    if domain:
                        logger.debug("Found domain %s on %s" % (domainName, self.connURLBrief))

                        domXMLRaw = domain.XMLDesc(0)
                        domXML = etree.fromstring(domXMLRaw)

                        return self.compareNetworkMac(domXML, root)

                    else:
                        logger.error("Unable to locate domain %s on host %s" % (domainName, self.connURLBrief))
                else:
                    logger.error("Unable to connect to Host at %s" % (self.connURL))
        else:
            logger.error("Unable to find a domain name in serverXML")

        logger.info("No new network elements were found")
        return False

    @staticmethod
    def compareDiskImages(currentXML, newXML):
        currentDiskImages = []
        newDiskImages = []
        devicesElement = currentXML.find('devices')
        currentDiskImages = getDiskImageURLs(devicesElement)

        newDeviceElement = newXML.find('devices')
        newDiskImages = getDiskImageURLs(newDeviceElement)

        for image in newDiskImages:
            if image not in currentDiskImages:
                logger.info("Found disk image %s not found in currentDiskImages" % (image))
                return True
            else:
                currentDiskImages.remove(image)

        # Also have to check to remove disks as well
        if len(currentDiskImages) > 0:
            logger.info("There is a disk still in currentDiskImages not found in serverXML. currentDiskImages : %r" % (currentDiskImages))
            return True

        logger.info("No new disks elements were found")
        return False

    @staticmethod
    def compareNetworkMac(currentXML, newXML):
        currentMacAddresses = getNetworkMacAddr(currentXML.find('devices'))
        newMacAddresses = getNetworkMacAddr(newXML.find('devices'))

        for macAddr in newMacAddresses:
            if macAddr in currentMacAddresses:
                logger.debug("Found mac addr %s in machine's current mac addresses" % (macAddr))
                currentMacAddresses.remove(macAddr)

            # This will be our case for a new network interface
            # or an interface w/out a mac address so we can't check
            # if it exists or not
            elif macAddr == "#####":
                logger.info("There is a new network interface in newMacAddresses")
                return True

            # Now there is a mac address definition in our new address
            # that doesn't exist in the current. This shouldn't ever really
            # happen as the MAC are dynamically updated. I think....
            else:
                logger.warning("Mac Address %s found in newMacAddresses but not in the currentMacAddresses" % (macAddr))
                return True

        if len(currentMacAddresses) > 0:
            logger.info("There is a mac address in current that wasn't found in the old. currentMacAddresses : %r" % (currentMacAddresses))
            return True

        logger.info("No new network elements were found")
        return False
