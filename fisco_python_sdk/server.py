import flwr as fl
import sys
import numpy as np
import json
import BFEL_api as Fisco
import IPFS_module as IPFS
from flwr.common import parameters_to_ndarrays, ndarrays_to_parameters

# sys args
uid = "aggregator"
workers = ["worker1", "worker2"]
contract_addr = sys.argv[1]

# BFEL functions
fisco_client = Fisco.FiscoMetadataClient(contract_addr)
ipfs_client = IPFS.IPFSClient()

def uploadParams(round, params):
    print('\033[33m', '\nround ', round, '\033[0m')
    print('\033[33m', "BFEL uploading... ", '\033[0m')
    temp_params = list(map(lambda x: json.dumps(x.tolist()), parameters_to_ndarrays(params)))
    # for i in temp_params:
    #     print(type(i), type())
        # for c in ['UTF-8', 'UTF-16', 'cp1252']:
        #     try:
        #         print('yay',type(i.decode(c)), chardet.detect(i))
        #         break
        #     except UnicodeDecodeError:
        #         print(c, "cmi", type(i), chardet.detect(i))

    # print(type(temp_params))
    params_str = json.dumps(temp_params)
    # print(type(params_str))
    metadata = {
        "uid": uid,
        "round": round,
        "params": params_str
    }
    # print(sys.getsizeof(metadata))
    hash = ipfs_client.upload(metadata)
    fisco_client.call("insertCid", [uid,round,hash])
    return

# def fetchMultiParams(round):
#     print('\033[33m', "BFEL fetching...", '\033[0m')
#     weights = []
#     for worder_id in workers:
#         res = fisco_client.call("getCid", [worder_id,round])
#         hash = res[0]
#         temp_metadata_str = ipfs_client.fetch(hash)
#         temp_metadata_json = json.loads(temp_metadata_str)
#         temp_weights_str = temp_metadata_json["weights"]
#         temp_weights_json = np.fromstring(temp_weights_str)
#         weights.append(temp_weights_json)
#     return weights

# def fetchParams(round):
#     print("BFEL fetching...")
#     res = fisco_client.call("getCid", [uid,round])
#     hash = res[0]
#     metadata = ipfs_client.fetch(hash)
#     params_str = metadata["params"]
#     temp_params = json.loads(params_str)
#     nd_params = list(map(lambda x: np.array(json.loads(x),dtype=np.float32), temp_params))
#     params = ndarrays_to_parameters(nd_params)
#     return (params)

class SaveModelStrategy(fl.server.strategy.FedAvg):
    def configure_fit(self, server_round: int, parameters, client_manager):
        if(server_round == 1):
            uploadParams(server_round, parameters)
        # print(fetchParams(server_round) == parameters)
        # if server_round == 2:
        #     print("og", parameters_to_ndarrays(parameters))
        #     print("fetched", parameters_to_ndarrays(fetchParams(server_round)))
        client_instructions = super().configure_fit(server_round, parameters, client_manager)
        # Add special "hello": "world" config key/value pair,
        # but only to the first client in the list
        for i in range(len(client_instructions)):
            _, evaluate_ins = client_instructions[i]  # First (ClientProxy, FitIns) pair
            evaluate_ins.config["round"] = server_round  # Change config for this client only

        return client_instructions
    
    def configure_evaluate(self, server_round: int, parameters, client_manager):
        uploadParams(server_round+1, parameters)
        client_instructions = super().configure_fit(server_round, parameters, client_manager)
        # Add special "hello": "world" config key/value pair,
        # but only to the first client in the list
        for i in range(len(client_instructions)):
            _, fit_ins = client_instructions[i]  # First (ClientProxy, FitIns) pair
            fit_ins.config["round"] = server_round  # Change config for this client only

        return client_instructions

    def aggregate_fit(
        self,
        rnd,
        results,
        failures
    ):
    # fetch here
        print('results fitres', type(results[0][1].parameters))
        aggregated_weights = super().aggregate_fit(rnd, results, failures)
        if aggregated_weights is not None:
            # Save aggregated_weights
            print(f"Saving round {rnd} aggregated_weights...")
            np.savez(f"round-{rnd}-weights.npz", *aggregated_weights)
        return aggregated_weights

# Create strategy and run server
strategy = SaveModelStrategy()

# Start Flower server for three rounds of federated learning
fl.server.start_server(
        server_address = 'localhost:'+str(10000) , 
        config=fl.server.ServerConfig(num_rounds=3) ,
        grpc_max_message_length = 1024*1024*1024,
        strategy = strategy
)
