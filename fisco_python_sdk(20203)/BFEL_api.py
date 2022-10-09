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

class FiscoMetadataClient():
    def __init__(self, contract_addr):
        if os.path.isfile(client_config.solc_path) or os.path.isfile(client_config.solcjs_path):
            Compiler.compile_file("contracts/Metadata.sol")
        abi_file = "contracts/Metadata.abi"
        data_parser = DatatypeParser()
        data_parser.load_abi_file(abi_file)
        self.contract_abi = data_parser.contract_abi
        self.contract_addr = contract_addr
        ContractNote.save_address_to_contract_note("Metadata",
                                               contract_addr)
        try:
            self.client = BcosClient()
            print(self.client.getinfo())

        except BcosException as e:
            print("execute demo_transaction failed ,BcosException for: {}".format(e))
            traceback.print_exc()
        except BcosError as e:
            print("execute demo_transaction failed ,BcosError for: {}".format(e))
            traceback.print_exc()
        except Exception as e:
            self.client.finish()
            traceback.print_exc()

    def call(self, fn, args=None):
        try:            
            # 调用一下call，获取数据
            # print("\n>>Call:------------------------------------------------------------------------")
            res = None
            if fn == 'getCid':
                res = self.client.call(self.contract_addr, self.contract_abi, fn, args)
            if fn == "insertCid":
                res = self.client.sendRawTransactionGetReceipt(self.contract_addr, self.contract_abi, fn, args)
            # print("call {fn} result:".format(fn=fn), res)
            return res
        except BcosException as e:
            print("execute demo_transaction failed ,BcosException for: {}".format(e))
            traceback.print_exc()
        except BcosError as e:
            print("execute demo_transaction failed ,BcosError for: {}".format(e))
            traceback.print_exc()
        except Exception as e:
            self.client.finish()
            traceback.print_exc()

    def end_client(self):
        self.client.finish()

# c = FiscoMetadataClient("0x75673e6859e6a4f791d583a6874e97adafb9b923")
# c.call("insertCid", ["f",1,"fff"])
# c.call("getCid", ["f",1])
# c.end_client()

# temp = "ggghh"
# abi_file = "contracts/Metadata.abi"
# data_parser = DatatypeParser()
# data_parser.load_abi_file(abi_file)
# contract_abi = data_parser.contract_abi
# client = BcosClient()
# res = client.sendRawTransactionGetReceipt("0x4396f423671a21939820fc0d6a09ce65ca134ab9", contract_abi, "insertCid", [temp,1,temp])
# print(res)
# res = client.call("0x4396f423671a21939820fc0d6a09ce65ca134ab9", contract_abi, "getCid", [temp,1])
# print(res)
# client.finish()
