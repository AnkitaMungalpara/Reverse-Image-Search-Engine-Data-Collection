## Docker install In ubuntu 22.04  lts
sudo apt-get update
sudo apt-get upgrade -y

sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce -y
sudo systemctl status docker

sudo usermod -aG docker ubuntu
newgrp docker

## AWS cli installation
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
sudo apt install unzip
unzip awscliv2.zip
sudo ./aws/install

## Github Runner configuration
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.317.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.317.0/actions-runner-linux-x64-2.317.0.tar.gz
echo "9e883d210df8c6028aff475475a457d380353f9d01877d51cc01a17b2a91161d  actions-runner-linux-x64-2.317.0.tar.gz" | shasum -a 256 -c
tar xzf ./actions-runner-linux-x64-2.317.0.tar.gz

## Configure and Run
./config.sh --url https://github.com/AnkitaMungalpara/Reverse-Image-Search-Engine-Data-Collection --token <put-your-token-here>
./run.sh

## Add Github runner as a service
sudo ./svc.sh install
sudo ./svc.sh start
sudo ./svc.sh status

## To stop the service
sudo ./svc.sh stop
sudo ./svc.sh uninstall