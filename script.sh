netconvert --node-files node.nod.xml --edge-files edge.edg.xml --type-files type.type.xml --connection-files=connection.con.xml -o net.net.xml
python3 prog.py
# sumo-gui -n net.net.xml -r route.rou.xml