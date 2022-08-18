python server.py server worker1,worker2 contractaddr &
python client.py worker1 server 4000,4000,4000,3000,10,10,10,10,4000,10 contractaddr &
python client.py worker2 server 0,10,10,10,4000,3000,4000,5000,10,4500 contractaddr
