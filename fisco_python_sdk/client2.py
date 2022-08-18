import flwr as fl
import tensorflow as tf
from tensorflow import keras
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import json
import BFEL_api as Fisco
import IPFS_module as IPFS
from flwr.common import parameters_to_ndarrays, ndarrays_to_parameters

# sys args
uid = "worker2"
server_uid = "aggregator"
dist = [0, 10, 10, 10, 4000, 3000, 4000, 5000, 10, 4500]
contract_addr = sys.argv[1]

# AUxillary methods
def getDist(y):
    ax = sns.countplot(y)
    ax.set(title="Count of data classes")
    plt.show()

def getData(dist, x, y):
    dx = []
    dy = []
    counts = [0 for i in range(10)]
    for i in range(len(x)):
        if counts[y[i]]<dist[y[i]]:
            dx.append(x[i])
            dy.append(y[i])
            counts[y[i]] += 1
        
    return np.array(dx), np.array(dy)

# Load and compile Keras model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(256, activation='relu'),
    keras.layers.Dense(10, activation='softmax')
])
model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

# Load dataset
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train[..., np.newaxis]/255.0, x_test[..., np.newaxis]/255.0
x_train, y_train = getData(dist, x_train, y_train)
getDist(y_train) 

# BFEL functions
fisco_client = Fisco.FiscoMetadataClient(contract_addr)
ipfs_client = IPFS.IPFSClient()

def uploadParams(round, params):
    print('\033[33m', "BFEL uploading... ", '\033[0m')
    temp_params = list(map(lambda x: json.dumps(x.tolist()), (params)))

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

def fetchNdParams(round):
    print('\033[33m', "BFEL fetching...", '\033[0m')
    res = fisco_client.call("getCid", [server_uid,round])
    hash = res[0]
    metadata = ipfs_client.fetch(hash)
    params_str = metadata["params"]
    temp_params = json.loads(params_str)
    nd_params = list(map(lambda x: np.array(json.loads(x),dtype=np.float32), temp_params))
    return (nd_params)

# Define Flower client
class FlowerClient(fl.client.NumPyClient):
    # run once at the start
    def get_parameters(self, config):
        return model.get_weights()

    def fit(self, parameters, config):
        # print((fetchNdParams(config["round"])) == parameters)
        # print(type(fetchNdParams(config["round"])))
        print("\nfit round",config["round"])
        fetched = fetchNdParams(config["round"])
        for i in range(len(fetched)):
            print("comparing...", np.array_equal(fetched[i] , parameters[i]))

        model.set_weights(parameters)
        
        r = model.fit(x_train, y_train, epochs=1, validation_data=(x_test, y_test), verbose=0)
        hist = r.history
        print('\033[32m', "Fit history : " ,hist, '\033[0m')
        uploadParams(config["round"], parameters)
        return model.get_weights(), len(x_train), {}

    def evaluate(self, parameters, config):
        # print((fetchNdParams(config["round"])) == parameters)
        print("eval round",config["round"])
        fetched = fetchNdParams(config["round"]+1)
        for i in range(len(fetched)):
            print("comparing...", np.array_equal(fetched[i] , parameters[i]))

        model.set_weights(parameters)
        loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
        print('\033[32m', "Eval accuracy : ", accuracy, '\033[0m')
        return loss, len(x_test), {"accuracy": accuracy}

# Start Flower client
fl.client.start_numpy_client(
        server_address="localhost:"+str(10000), 
        client=FlowerClient(), 
        grpc_max_message_length = 1024*1024*1024
)
