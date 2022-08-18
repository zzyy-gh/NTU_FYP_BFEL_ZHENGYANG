from ipyfs import Files, Cat
import json
import uuid

class IPFSClient():
    def __init__(self):
        # You can customize the host and port on any controller.
        self.files = Files(
            host="http://localhost",  # Set IPFS Daemon Host
            port=5001  # Set IPFS Daemon Port
        )

        self.cat = Cat(
            host="http://localhost",  # Set IPFS Daemon Host
            port=5001  # Set IPFS Daemon Port
        )

    def upload(self, metadata):
        uuidOne = uuid.uuid1()
        path = '/'+json.dumps(str(uuidOne))
        # print("path created.")
        self.files.write(
            path=path,
            file=json.dumps(metadata),
            create=True,
            truncate=True
        )
        # print("written.")
        info = self.files.stat(path)
        # print("info fetched.")
        hash = info["result"]["Hash"]
        return hash

    def fetch(self, hash):
        res = self.cat.__call__(path=hash)
        return res["result"]

# Generate NFT metadata.
# metadata = {
#     "uid": "GG",
#     "runId": "runId1",
#     "round": 1,
#     "weights": "adfldsl"
# }

# metadata2 = {
#     "asdfasdfa": "ASDFADSFASDFADSFadsfasfddsa"
# }

# ipfs = IPFSClient()
# hash = ipfs.upload(metadata2)

# res = ipfs.fetch(hash)
# print(res)

# ipfs pin ls --type recursive | cut -d' ' -f1 | xargs -n1 ipfs pin rm
# https://docs.ipfs.tech/reference/kubo/cli/
# https://docs.ipfs.tech/reference/http/gateway/#api
# ipfs daemon
# ipfs repo gc
