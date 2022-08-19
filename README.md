# NTU_FYP_BFEL_ZHENGYANG

last updated on: 19 August 2022

## Setup (Ubuntu)

1. Clone this repository: `git clone git@github.com:zzyy-gh/NTU_FYP_BFEL_ZHENGYANG.git`
2. Install packages for FISCO BCOS Blockchain: `sudo apt install -y openssl curl default-jdk`
3. Install Python packages for FISCO Python SDK: `cd <parent directory>/fisco_python_sdk && pip install --upgrade pip && pip install -r requirements.txt`
4. Install IPFS:
   1. Download the Linux binary from [dist.ipfs.tech](https://dist.ipfs.tech/#kubo): `wget https://dist.ipfs.tech/kubo/v0.14.0/kubo_v0.14.0_linux-amd64.tar.gz`
   2. Unzip the file: `tar -xvzf kubo_v0.14.0_linux-amd64.tar.gz`
   3. Move into the `kubo` folder and run the install script: `cd kubo && sudo bash install.sh`

## Run (Ubuntu)

1. Start IPFS: `ipfs daemon`
2. Start FISCO BCOS blockchain: `cd <parent directory>/fisco/nodes/127.0.0.1 && bash start_all.sh`
3. Deploy smart contract: `cd <parent directory>/fisco_python_sdk && python BFEL_deploy.py`
4. Start aggregator: `cd <parent directory>/fisco_python_sdk && python server.py <smart contract address returned from deploying smart contract (Step 3)>`
5. Start worker 1: `cd <parent directory>/fisco_python_sdk && python client1.py <smart contract address returned from deploying smart contract (Step 3)>`
6. Start worker 2: `cd <parent directory>/fisco_python_sdk && python client2.py <smart contract address returned from deploying smart contract (Step 3)>`

## Key Files and Directories

1. To store smart contracts: `<parent directory>/fisco_python_sdk/contracts`
2. To deploy smart contracts: `<parent directory>/fisco_python_sdk/BFEL_deploy.py`
3. Python module to communicate with FISCO blockchain: `<parent directory>/fisco_python_sdk/BFEL_api.py`
4. Python module to communicate with IPFS: `<parent directory>/fisco_python_sdk/IPFS_module.py`
5. FL aggregator Sample: `<parent directory>/fisco_python_sdk/server.py`
6. FL client sample: `<parent directory>/fisco_python_sdk/client1.py` (or client2.py)

## References

- [IPFS](https://docs.ipfs.tech/)
- [FISCO BCOS](https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/index.html)
- [IPYFS](https://github.com/837477/IPyFS)
- [flower](https://flower.dev/docs/index.html)
