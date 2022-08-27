import flwr as fl
import sys
import numpy as np
import json
import BFEL_api as Fisco
import IPFS_module as IPFS
from flwr.common import parameters_to_ndarrays, ndarrays_to_parameters
from datetime import datetime

# global variables
uid = "aggregator"
workers = ["worker1", "worker2", "worker3"]
contract_addr = sys.argv[1]
min_num_clients = len(workers)

# BFEL functions
fisco_client = Fisco.FiscoMetadataClient(contract_addr)
ipfs_client = IPFS.IPFSClient()

def uploadParams(round, params):
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
    print("BFEL uploaded.", '\033[0m')
    return

def fetchMultiParams(round):
    params_dict = {}
    for worker_id in workers:
        res = fisco_client.call("getCid", [worker_id,round])
        hash = res[0]
        metadata = ipfs_client.fetch(hash)
        params_str = metadata["params"]
        uid = metadata["uid"]
        temp_params = json.loads(params_str)
        nd_params = list(map(lambda x: np.array(json.loads(x),dtype=np.float32), temp_params))
        params_dict[uid] = nd_params
    print("BFEL fetched.", '\033[0m')
    return (params_dict)

def compareFetched(fetched, results):
    isSame = True
    for i in range(len(results)):
        worker_id = results[i][1].metrics['uid']
        parameters = parameters_to_ndarrays(results[i][1].parameters)
        for i in range(len(fetched[worker_id])):
            # print(type(fetched[worker_id][i][50]))
            # print(len(fetched[worker_id][i]))
            # for j in range(len(fetched[worker_id][i])):
            #     if fetched[worker_id][i][j] != parameters[i][j]:
            #         print("nah")
            if not np.allclose(fetched[worker_id][i] , parameters[i]):
                isSame = False
                break
    if isSame:
        print('\033[32m', "Data integrity is preserved.", '\033[0m')
    else:
        print('\033[31m', "Data integrity is not preserved.", '\033[0m')

class SaveModelStrategy(fl.server.strategy.FedAvg):
    def __init__(self, *args, **kwargs):
        super(SaveModelStrategy, self).__init__(*args, **kwargs)

        self.min_available_clients = min_num_clients
        self.min_evaluate_clients = min_num_clients
        self.min_fit_clients = min_num_clients
    def configure_fit(self, server_round: int, parameters, client_manager):
        print('\033[34m', "\nRound ", server_round, '\033[0m')
        # if(server_round == 1):
        #     uploadParams(server_round, parameters)
        # print(fetchParams(server_round) == parameters)
        # if server_round == 2:
        #     print("og", parameters_to_ndarrays(parameters))
        #     print("fetched", parameters_to_ndarrays(fetchParams(server_round)))
        client_instructions = super().configure_fit(server_round, parameters, client_manager)
        for i in range(len(client_instructions)):
            _, evaluate_ins = client_instructions[i]  # First (ClientProxy, FitIns) pair
            evaluate_ins.config["round"] = server_round  # Change config for this client only

        return client_instructions
    
    def configure_evaluate(self, server_round: int, parameters, client_manager):
        # uploadParams(server_round+1, parameters)
        client_instructions = super().configure_fit(server_round, parameters, client_manager)
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
        # fetched = fetchMultiParams(rnd)
        # print(fetched)
        # compareFetched(fetched, results)
        # l = ([result[1].parameters for result in results])
        # print("len:", len(l))
        # print('l param', type(l[1]))
        # print(results[0][1].metrics['uid'])
        # print(results[1][1].metrics['uid'])
        aggregated_weights = super().aggregate_fit(rnd, results, failures)
        # Save aggregated_weights
        # if aggregated_weights is not None:
        #     print(f"Saving round {rnd} aggregated_weights...")
        #     np.savez(f"round-{rnd}-weights.npz", *aggregated_weights)
        return aggregated_weights

# Create strategy and run server
strategy = SaveModelStrategy()

start = datetime.now()
# Start Flower server for three rounds of federated learning
fl.server.start_server(
        server_address = 'localhost:'+str(10000) , 
        config=fl.server.ServerConfig(num_rounds=3) ,
        grpc_max_message_length = 1024*1024*1024,
        strategy = strategy,
)
end = datetime.now()
time_taken = str((end-start).total_seconds())
print('\033[32m', "Time taken (s): " ,time_taken, '\033[0m')
