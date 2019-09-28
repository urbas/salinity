# Salinity [![Build](https://travis-ci.org/urbas/salinity.svg?branch=master)](https://travis-ci.org/urbas/salinity) [![pypi](https://badge.fury.io/py/salinity.svg)](https://pypi.org/project/salinity/)
Analyzes Salt's highstate output and produces a report.

## Installation
```
pip install salinity
```

## Usage
```bash
salt-call state.highstate | tee salt.output
salinity salt.output
```