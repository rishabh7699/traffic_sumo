netconvert --node-files ./sumo/node.nod.xml --edge-files ./sumo/edge.edg.xml --type-files ./sumo/type.type.xml --connection-files ./sumo/connection.con.xml -o ./sumo/network.net.xml
python3 ./source/runner.py
# python3 ./source/Train.py