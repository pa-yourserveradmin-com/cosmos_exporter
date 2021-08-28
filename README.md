# cosmos_exporter

A Python script to query Cosmos SDK and Tendermint endpoints for information
about validator node's status and convert this information in Prometheus
metrics format to make them accessible to compatible scrapers.

## Status

Work In Progress: metrics names, command line arguments and configuration
options can be changed at any time.

## Limitations

Currently, the script expected to be executed directly on validator machine.
This is not a requirement and will be changed soon, to make it possible to
run script remotely and use either validator or full node RPC endpoints to
fetch information from a chain.

## Requirements

1. Operating system with Python 3.5+ installed.
2. Basic understanding of what is going on.

## Dependencies

### Ubuntu

In case you use modern Ubuntu distributions, Python Prometheus client package
can be easily installed using APT:

```bash
apt update && \
apt install python3-prometheus-client
```

### Source

In case your system lacks packaged Python Prometheus client (or in case packaged
version is too old), it is recommended to install it into virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -U -r requirements.txt
```

Please note: in case of using virtual environment `venv/bin/python3` should be
used to invoke [cosmos_exporter](cosmos_exporter) script.

## Configuration

Currently, all configuration expected to be done by using arguments passed to
the script on start-up.

| Option              | Description                                      | Example shell command to query values     |
|---------------------|--------------------------------------------------|-------------------------------------------|
| `consensus_address` | Node's tendermint validator consensus address.   | `<simd> tendermint show-address`          |
| `delegator_address` | Reward wallet address associated with validator. | `<simd> keys show -a <wallet>`            |
| `validator_address` | Node's validator address to query information.   | `<simd> keys show -a --bech val <wallet>` |

## Examples

Example of script run using Python virtual environment:

```bash
venv/bin/python3 cosmos_exporter \
  --consensus_address=tkivalcons158ms2lcacdtu78270uef9ayth7lfkuvxq4lnms \
  --delegator_address=tki1mw7kd8e4t44q8jklrhdne8uyqmlmmxpw07csmc \
  --validator_address=tkivaloper1mw7kd8e4t44q8jklrhdne8uyqmlmmxpwu7snym
```

The command above will start metrics exporter on http://0.0.0.0:8000.

## Grafana

Example Grafana dashboard is available [here](example-testnet.json) and it can be
imported into Grafana via UI/API. Please note that a lot of expressions currently
depend on instance ports and `job` value configured in Prometheus scrape configuration.

It should not be a huge problem to adopt example dashboard to any configuration, so
mentioned above just a note to highlight problematic places.
