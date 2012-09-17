#!/usr/bin/python
# -*- coding: utf-8 -*-

""" The pyptlib.easy.client module includes a convenient API for writing pluggable transport clients. """

from pyptlib.config import EnvException
from pyptlib.client_config import ClientConfig


def init(transports):
    """
    Initialize the pluggable transport by parsing the environment
    variables and generating output to report any errors.  The given
    transports are checked against the transports enabled by a
    dictionary containing information for the managed proxy is
    returned.

    The dictionary contains the following keys and values:

    'state_loc' : Directory where the managed proxy should dump its
    state files (if needed).

    'transports' : The names of the transports that must be launched.

    Returns None if something went wrong.
    """

    supportedTransportVersion = '1'

    try:
        config = ClientConfig()
    except EnvException:
        return None

    if config.checkManagedTransportVersion(supportedTransportVersion):
        config.writeVersion(supportedTransportVersion)
    else:
        config.writeVersionError()
        return None

    matchedTransports = []
    for transport in transports:
        if config.checkTransportEnabled(transport):
            matchedTransports.append(transport)

    # XXX the XXXs from server.py are valid here too.

    retval = {}
    retval['state_loc'] = config.getStateLocation()
    retval['transports'] = matchedTransports

    return retval


def reportSuccess(
    name,
    socksVersion,
    address,
    args,
    optArgs,
    ):
    """
        This method should be called to report when a transport has been successfully launched.
        It generates output to Tor informing that the transport launched successfully and can be used.
        After all transports have been launched, the client should call reportEnd().
    """

    config = ClientConfig()
    config.writeMethod(name, socksVersion, address, args, optArgs)


def reportFailure(name, message):
    """
        This method should be called to report when a transport has failed to launch.
        It generates output to Tor informing that the transport failed to launch and cannot be used.
        After all transports have been launched, the client should call reportEnd().
    """

    config = ClientConfig()
    config.writeMethodError(name, message)


def reportEnd():
    """
        This method should be called after all transports have been launched.
        It generates output to Tor informing that all transports have been launched.
    """

    config = ClientConfig()
    config.writeMethodEnd()

