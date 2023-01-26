# Nagios / Shinken check for Sectigo's Domain Control Validation (DCV)

[![reuse compliant](https://reuse.software/badge/reuse-compliant.svg)](https://reuse.software/) 
[![Trigger: Shell Check](https://github.com/DSI-Universite-Rennes2/check-sectigo-dcv/actions/workflows/main.yml/badge.svg?event=push)](https://github.com/DSI-Universite-Rennes2/check-sectigo-dcv/actions/workflows/main.yml)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This script checks Sectigo's Domain Control Validation (DCV) expiration via the REST API.

## Install

```bash
git clone https://github.com/DSI-Universite-Rennes2/check-sectigo-dcv.git
cd check-sectigo-dcv
cp config/config.env-dist config/config.env
[Edit and configure API REST credentials and proxy if needed]
./build/install.sh
```

The install.sh script just :

- install needed packages (if on Debian)
- create python venv, get needed python libs and patch [cert_manager](https://github.com/broadinstitute/python-cert_manager) lib to add DCV capabilities.
- build an NRPE config in main directory

## Usage

```text
usage: check-dcv.py [-h] [-w WARN] [-c CRIT] [-v]

Check Sectigo DCV expiration

Options:
  -h, --help            show this help message and exit
  -w WARN, --warning WARN
                        warning delay in days
  -c CRIT, --critical CRIT
                        critical delay in days
  -v, --verbose         enable verbose output
```

## Contribute

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

We add DCV Class to the python lib [cert_manager](https://github.com/broadinstitute/python-cert_manager). This part is published under [BSD-3-Clause](https://spdx.org/licenses/BSD-3-Clause.html) license.

All other parts are published under the [GNU General Public License v3.0 or later](LICENSE)

This program is free software: you can redistribute it and/or modify
it under the terms of the [GNU General Public License v3.0 or later](LICENSE)
as published by the Free Software Foundation.

The program in this repository meet the requirements to be REUSE compliant,
meaning its license and copyright is expressed in such as way so that it
can be read by both humans and computers alike.

For more information, see https://reuse.software/
