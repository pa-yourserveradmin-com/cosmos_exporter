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

1. Runtime environment with Python 3.5+ installed.
2. Basic understanding of what is going on.

## Usage

### Containers

Container images are available to pull them from Github Container registry.
This could be the easiest, and the fastest way to start exporting validator
metrics  especially in case you already have required infrastructure and/or
tools.

Please see the list of actual image tags by the [link][images].

Example usage:

```bash
podman run --rm ghcr.io/pa-yourserveradmin-com/cosmos_exporter:latest --help
```

_Feel free to replace `podman` with `docker` in case you more familiar with the last one._

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
./cosmos_exporter --help
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
./cosmos_exporter --help
```

Please note: in case of using virtual environment `venv/bin/python3` should be
used to invoke [cosmos_exporter](cosmos_exporter) script.

## Configuration

Currently, all configuration expected to be done by using arguments passed to
the script on start-up.

### Required arguments

| Option              | Description                                      | Example shell command to query values     |
|---------------------|--------------------------------------------------|-------------------------------------------|
| `consensus_address` | Node's tendermint validator consensus address.   | `<simd> tendermint show-address`          |
| `delegator_address` | Reward wallet address associated with validator. | `<simd> keys show -a <wallet>`            |
| `validator_address` | Node's validator address to query information.   | `<simd> keys show -a --bech val <wallet>` |

## Examples

### Running as container

Example of script run using pre-build container image with automatic
restart and host networking (to simplify the example):

```bash
podman run --network=host --restart=always ghcr.io/pa-yourserveradmin-com/cosmos_exporter:latest \
  --consensus_address=tkivalcons158ms2lcacdtu78270uef9ayth7lfkuvxq4lnms \
  --delegator_address=tki1mw7kd8e4t44q8jklrhdne8uyqmlmmxpw07csmc \
  --validator_address=tkivaloper1mw7kd8e4t44q8jklrhdne8uyqmlmmxpwu7snym
```

_Feel free to replace `podman` with `docker` in case you more familiar with the last one._

### Running from source

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
depend on instance ports and `job` values set in Prometheus scrape settings.

It should not be a huge problem to adopt example dashboard to any configuration, so
mentioned above just a note to highlight problematic places.

[images]: https://github.com/pa-yourserveradmin-com/cosmos_exporter/pkgs/container/cosmos_exporter
