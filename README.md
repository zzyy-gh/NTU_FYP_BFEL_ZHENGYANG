# NTU_FYP_BFEL_ZHENGYANG
last update: 18 August 2022

## Setup

## Run
1. Start IPFS: ``` ipfs daemon ```
2. Start FISCO BCOS blockchain: ``` cd <parent directory>/fisco/nodes/127.0.0.1 && bash start_all.sh ```
3. Deploy smart contract: ``` cd <parent directory>/fisco_python_sdk && python BFEL_deploy.py ```
4. Start aggregator: ``` cd <parent directory>/fisco_python_sdk && python server.py <smart contract address returned from deploying smart contract (Step 3)> ```
5. Start worker 1: ``` cd <parent directory>/fisco_python_sdk && python client1.py <smart contract address returned from deploying smart contract (Step 3)> ```
6. Start worker 2: ``` cd <parent directory>/fisco_python_sdk && python client2.py <smart contract address returned from deploying smart contract (Step 3)> ```
