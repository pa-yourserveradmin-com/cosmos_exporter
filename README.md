# cosmos_exporter

A Python script to query Cosmos SDK and Tendermint endpoints for information
about validator node's status and convert this information in Prometheus
metrics format to make them accessible to compatible scrapers.

## Status

Work In Progress: metrics names, command line arguments and configuration
options can be changed at any time.

## Limitations

Currently, no exceptions handled, so script can fail and exit depending on
the responses provided by API and RPC endpoints, the same as depending on
the endpoints health.

Exceptions handling planned, but still: recommended way to run the script
is to use `systemd` unit with automatic restart in case of failures.

In case `systemd` is not available, consider to use `monit`, `supervisord`
and any other process manager which supports process restart on failures.

## Requirements

1. Operating system with Python 3.5+ installed.
2. Basic understanding of what is going on.

## Dependencies

### Ubuntu

In case you use modern Ubuntu distributions, required Python packages can be
easily installed using APT:

```bash
git clone https://github.com/pa-yourserveradmin-com/cosmos_exporter.git
pushd cosmos_exporter
apt update && \
apt install \
  python3-prometheus-client \
  python3-requests
```

### Source

In case your system lacks packaged Python Prometheus client (or in case packaged
version is too old), it is recommended to install it into virtual environment:

```bash
git clone https://github.com/pa-yourserveradmin-com/cosmos_exporter.git
pushd cosmos_exporter
python3 -m venv venv
source venv/bin/activate
pip3 install -U -r requirements.txt
```

Please note: in case of using virtual environment `venv/bin/python3` should be
used to invoke [cosmos_exporter](cosmos_exporter) script.

### Containers

Example [Dockerfile](Dockerfile) is provided to show how to quickly build container
image with all dependencies installed and ready to use:

```bash
git clone https://github.com/pa-yourserveradmin-com/cosmos_exporter.git
pushd cosmos_exporter
podman build -t localhost/cosmos_exporters:0.1.0 .
```

_Feel free to replace `podman` with `docker` in case you more familiar with the last one._

## Configuration

Currently, all configuration expected to be done by using arguments passed to
the script on start-up.

### Required arguments

| Option              | Description                                      | Example shell command to query values     |
|---------------------|--------------------------------------------------|-------------------------------------------|
| `consensus_address` | Node's tendermint validator consensus address.   | `<simd> tendermint show-address`          |
| `delegator_address` | Reward wallet address associated with validator. | `<simd> keys show -a <wallet>`            |
| `validator_address` | Node's validator address to query information.   | `<simd> keys show -a --bech val <wallet>` |

### Optional arguments

| Option                  | Description                                           |
|-------------------------|-------------------------------------------------------|
| `validator_hex_address` | Validator node HEX address to check uptime and ranks. |

### Notable arguments

The `validator_hex_address` argument needed to override automatically discovered
node's HEX address in case the script will be connected not directly to validator
node's API endpoint, but to a full node. This can be useful to avoid exposing API
port on validator node and/or starting API service at all.

For sure, it will be nice to be able to query it via API/RCP or calculate from the
rest of arguments (such as `validator_address`), but currently such functional not
implemented (yet).

You can query your validator node HEX address by running the next command locally
on the node (please adjust RPC address and port according to your configuration):

```bash
curl -s localhost:26657/status | jq -r .result.validator_info.address
```

## Examples

Example of script run from source and using Python virtual environment:

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
