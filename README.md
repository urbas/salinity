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

Example output:
```
Top changes:
1. 61404.014 ms: file.managed: /data/grafana/etc/provisioning/dashboard_specs/node_exporter_full.json
2. 5428.821 ms: docker_container.running: prometheus
3. 5262.512 ms: docker_container.running: nginx
4. 4609.715 ms: docker_container.running: foo
5. 4211.843 ms: docker_container.running: grafana
6. 3013.05 ms: raid.present: /dev/md0
7. 1848.018 ms: service.running: foo.service
8. 1528.225 ms: file.managed: /var/downloads/jenkins.deb
9. 1467.314 ms: service.running: bar.service
10. 1466.487 ms: service.running: node_exporter
```

## Limitations
- currently supports only local salt-call runs
- currently supports only `--state-output=changes`
