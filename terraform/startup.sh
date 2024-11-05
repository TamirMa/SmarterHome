#!/bin/bash
# terraform/startup.sh

# Install Docker
apt-get update
apt-get install -y apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io

# Install WireGuard
apt-get install -y wireguard

# Set up WireGuard
cat > /etc/wireguard/wg0.conf << EOL
[Interface]
PrivateKey = $(wg genkey)
Address = 10.8.0.1/24
ListenPort = 51820
SaveConfig = true

[Peer]
PublicKey = 5GHpaTcj2VktEwtTYMy0znL1EuKfFAPlMnuNpmMugSA=
AllowedIPs = 10.8.0.2/32, 10.0.0.1/24, 192.168.1.1/24
EOL

# Enable IP forwarding
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p

# Start WireGuard
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0

sudo mkdir -p /opt/config/dev
# Download some configuration files from GCS
gsutil cp gs://smarter-home-credentials-bucket/mayer/config/dev/* /opt/config/dev

# Pull and run your container
docker pull ghcr.io/tamirma/smarter-home:latest
docker run -d --restart always --env-file /opt/config/dev/.env -v /opt/config/dev:/config ghcr.io/tamirma/smarter-home:latest