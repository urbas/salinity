# Salinity [![Build](https://travis-ci.org/urbas/salinity.svg?branch=master)](https://travis-ci.org/urbas/salinity) [![pypi](https://badge.fury.io/py/salinity.svg)](https://pypi.org/project/salinity/)
Analyzes Salt's highstate output and produces a report.

## Installation
```
pip install salinity
```

## Usage
```bash
salt-call --local --state-output=changes state.highstate | tee salt.output
salinity salt.output
```

## Limitations
- currently supports only local salt-call runs
- currently supports only `--state-output=changes`
