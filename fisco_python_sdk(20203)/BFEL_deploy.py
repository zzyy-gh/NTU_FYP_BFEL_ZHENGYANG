#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
  FISCO BCOS/Python-SDK is a python client for FISCO BCOS2.0 (https://github.com/FISCO-BCOS/)
  FISCO BCOS/Python-SDK is free software: you can redistribute it and/or modify it under the
  terms of the MIT License as published by the Free Software Foundation. This project is
  distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even
  the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. Thanks for
  authors and contributors of eth-abi, eth-account, eth-hash，eth-keys, eth-typing, eth-utils,
  rlp, eth-rlp , hexbytes ... and relative projects
  @author: kentzhang
  @date: 2019-06
'''
from client.contractnote import ContractNote
from client.bcosclient import BcosClient
import os
from eth_utils import to_checksum_address
from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from client.bcoserror import BcosException, BcosError
from client_config import client_config
import sys
import traceback
# 从文件加载abi定义
if os.path.isfile(client_config.solc_path) or os.path.isfile(client_config.solcjs_path):
    Compiler.compile_file("contracts/Metadata.sol")

abi_file = "contracts/Metadata.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi

try:
    client = BcosClient()
    print(client.getinfo())
    # 部署合约
    print("\n>>Deploy:----------------------------------------------------------")
    with open("contracts/Metadata.bin", 'r') as load_f:
        contract_bin = load_f.read()
        load_f.close()
    result = client.deploy(contract_bin)
    print("deploy", result)
    print("new address : ", result["contractAddress"])
    contract_name = os.path.splitext(os.path.basename(abi_file))[0]
    memo = "tx:" + result["transactionHash"]
    # 把部署结果存入文件备查
    ContractNote.save_address_to_contract_note(contract_name,
                                               result["contractAddress"])

except BcosException as e:
    print("execute demo_transaction failed ,BcosException for: {}".format(e))
    traceback.print_exc()
except BcosError as e:
    print("execute demo_transaction failed ,BcosError for: {}".format(e))
    traceback.print_exc()
except Exception as e:
    client.finish()
    traceback.print_exc()
client.finish()
sys.exit(0)
