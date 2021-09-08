## Ubuntu Quick Start

```
git clone https://github.com/pa-yourserveradmin-com/cosmos_exporter.git
pushd cosmos_exporter
apt update && \
apt install --assume-yes \
  python3-prometheus-client \
  python3-requests
./cosmos_exporter --help

install -v -m 0755 -o root -g root cosmos_exporter /usr/local/sbin/cosmos_exporter
cat > /etc/systemd/system/cosmos_exporter.service <<EOF
[Unit]
Description=CosmosSDK Prometheus Exporter
After=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/sbin/cosmos_exporter \\
  --consensus_address=$(omniflixhubd tendermint show-address) \\
  --delegator_address=$(omniflixhubd keys show -a blocknode) \\
  --validator_address=$(omniflixhubd keys show -a --bech val blocknode)
Restart=always
RestartSec=5s
User=root

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cosmos_exporter.service
systemctl start cosmos_exporter.service

systemctl status cosmos_exporter.service
```
