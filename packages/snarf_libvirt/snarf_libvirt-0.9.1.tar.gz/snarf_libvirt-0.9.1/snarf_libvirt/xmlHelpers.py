def xml_compare(x1, x2, reporter=None):
    if x1.tag != x2.tag:
        if reporter:
            reporter('Tags do not match: %s and %s' % (x1.tag, x2.tag))
        return False
    for name, value in x1.attrib.items():
        if x2.attrib.get(name) != value:
            if reporter:
                reporter('Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
            return False
    for name in x2.attrib.keys():
        if name not in x1.attrib:
            if reporter:
                reporter('x2 has an attribute x1 is missing: %s'
                         % name)
            return False
    if x1.tag != 'uuid':
        if not text_compare(x1.text, x2.text):
            if reporter:
                reporter('text: %r != %r' % (x1.text, x2.text))
            return False
    if not text_compare(x1.tail, x2.tail):
        if reporter:
            reporter('tail: %r != %r' % (x1.tail, x2.tail))
        return False
    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    if len(cl1) != len(cl2):
        if reporter:
            reporter('children length differs, %i != %i'
                     % (len(cl1), len(cl2)))
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not xml_compare(c1, c2, reporter=reporter):
            if reporter:
                reporter('children %i do not match: %s'
                         % (i, c1.tag))
            return False
    return True


def text_compare(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()


def getDiskImageURLs(devicesElement):
    diskImageURLs = []
    from . import logger
    diskElements = devicesElement.findall('disk')

    logger.debug("devicesElements : %r" % (devicesElement))
    logger.debug("diskElements : %r" % (diskElements))

    for diskElement in diskElements:
        diskType = diskElement.get('type')

        if diskType == 'file':
            sourceElement = diskElement.find('source')

            if sourceElement is not None:
                logger.debug("Found sourceElement. Adding %s to diskImageURLs" % (sourceElement.get('file')))
                diskImageURLs.append(sourceElement.get('file'))
            else:
                logger.error("Unable to find source element in disk definition")
        else:
            logger.error("Unable to process disks of type %s" % (diskType))

    logger.debug("diskImageURLs: %r" % (diskImageURLs))

    return diskImageURLs


def getNetworkMacAddr(devicesElement):
    from . import logger
    macAddress = []
    interfaceElements = devicesElement.findall('interface')

    logger.debug("devicesElements : %r" % (devicesElement))
    logger.debug("interfaceElements : %r" % (interfaceElements))

    if len(interfaceElements) == 0:
        logger.error("No interfaceElements found in device definition")
        return []

    for interfaceElement in interfaceElements:
        macAddrElement = interfaceElement.find('mac')

        if macAddrElement is not None:
            logger.debug('Found the macAddrElement')
            macAddress.append(macAddrElement.get('address'))
        else:
            logger.info("Unable to find Mac Address Element in interface definition")
            macAddress.append("#####")

    return macAddress


def getMemory(serverElement):
    from . import logger

    memoryElement = serverElement.find('memory')

    if memoryElement is None:
        logger.error('Unable to find memory element in server definition')
        return None

    return int(memoryElement.text), memoryElement.get('unit')


def getCPU(serverElement):
    from . import logger

    cpuElement = serverElement.find('vcpu')

    if cpuElement is None:
        logger.error('Unable to find CPU element in server definition')
        return None

    return int(cpuElement.text)
