#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# SPDX-License-Identifier: GPL-3.0-or-later
# License-Filename: LICENSE 
# -----------------------------------------------------------------------------
# Authors :
#
#   - Yann 'Ze' Richard <yann.richard à univ-rennes2.fr> - DSI Université Rennes 2
#
# -----------------------------------------------------------------------------

import argparse
import time
import logging
import os
import sys
import traceback
from datetime import datetime
from datetime import date

from cert_manager import DCV
from cert_manager import Client

defaultLogLevel = logging.DEBUG
mylogger        = logging.getLogger(__name__)

OK       = 0
WARNING  = 1
CRITICAL = 2
UNKNOWN  = 3

def debug_factory(logger, debug_level):
    """
    Decorate logger in order to add custom levels for Nagios
    """
    def custom_debug(msg, *args, **kwargs):
        if logger.level >= debug_level:
            return
        logger._log(debug_level, msg, args, kwargs)
    return custom_debug

def get_args():
    parser = argparse.ArgumentParser(
        description = "Check Sectigo DCV expiration",
        epilog      = '''   Sources : https://github.com/DSI-Universite-Rennes2/check-sectigo-dcv.git
                      '''
    )
    parser._optionals.title = "Options"
    parser.add_argument('-w', '--warning',  required=False, help='warning delay in days',  dest='warn', type=int, default=30)
    parser.add_argument('-c', '--critical', required=False, help='critical delay in days', dest='crit', type=int, default=15)
    parser.add_argument('-v', '--verbose',  required=False, help='enable verbose output',  dest='verbose', action='store_true')
    args = parser.parse_args()
    return args

def getDomainExpireIn(days):

    SClient = Client(
        base_url  = os.getenv('SECTIGO_API_BASEURL'),
        login_uri = os.getenv('SECTIGO_API_LOGINURL'),
        username  = os.getenv('SECTIGO_API_USER'),
        password  = os.getenv('SECTIGO_API_PASS'),
    )

    dcv       = DCV(client=SClient)
    res       = dcv.search(expiresIn=days)
    domains   = []
    for domain in res:
        domainName      = domain["domain"]
        dcvStatus       = domain["dcvStatus"]
        dcvOrderStatus  = domain["dcvOrderStatus"]
        dcvMethod       = domain["dcvMethod"]
        expirationDate  = domain["expirationDate"]
        expirationDT    = datetime.strptime(expirationDate, '%Y-%m-%d').date()
        expireIn        = expirationDT - date.today()

        # Ignore wildcard subdomains
        if domainName.startswith('*.'):
            continue

        info = {
            'domain': domainName,
            'dcvStatus': dcvStatus,
            'dcvOrderStatus': dcvOrderStatus,
            'dcvMethod': dcvMethod,
            'expirationDate': expirationDate,
            'expireInDays': expireIn.days,
        }
        domains.append(info)

    return domains

def main():

    # Handling arguments
    args            = get_args()
    warn            = args.warn
    crit            = args.crit
    verbose         = args.verbose

    # Logging settings
    if verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Add custom level unknown
    logging.addLevelName(logging.DEBUG+1, 'UNKOWN')
    setattr(mylogger, 'unkown', debug_factory(mylogger, logging.DEBUG+1))
    # Change INFO LevelName to OK
    logging.addLevelName(logging.INFO, 'OK')
    # Setting output format for Nagios
    logging.basicConfig(stream=sys.stdout, format='%(levelname)s - %(message)s', level=log_level)

    if warn < crit:
        mylogger.unkown(f'Error : warning value must be greater than critical ( {warn} > {crit} )')
        sys.exit(UNKNOWN)

    # ------------------------------------------------------------------------ #
    # checking DCV
    try:
        domains = getDomainExpireIn(warn)

        nagiosExit = OK
        nagiosMessage = f'No domain will expire within {warn} days'

        warnDomains = []
        critDomains = []
        if domains:
            nagiosExit = WARNING
            delayAlert = warn 
            for d in domains:
                if d['expireInDays'] <= crit:
                    nagiosExit = CRITICAL
                    delayAlert = crit
                    critDomains.append('{} ({})'.format(d['domain'], d['expireInDays']))
                else:
                    warnDomains.append('{} ({})'.format(d['domain'], d['expireInDays']))

            listOfDomains = ', '.join(critDomains + warnDomains)
            nagiosMessage = f'{len(domains)} domain is about to expire within {delayAlert} days : {listOfDomains}'

            if nagiosExit == WARNING:
                mylogger.warning(nagiosMessage)
            else:
                mylogger.critical(nagiosMessage)
        else:
            mylogger.info("%s" % nagiosMessage)
            sys.exit(nagiosExit)
    except Exception as ex:
        mylogger.unkown(f'Exception raised: {ex}')
        traceback.print_exc()
        sys.exit(UNKNOWN)
    finally:
        sys.exit(nagiosExit)

if __name__ == "__main__":
    main()
