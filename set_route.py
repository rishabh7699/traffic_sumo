def set(p1,p2,p3,p4):
    f = open("route.rou.xml","w")
    data = """<routes>
<vType accel="1.0" decel="5.0" id="car" length="3.0" maxspeed="100.0" sigma="0.0"/>
<vType accel="1.0" decel="5.0" id="bus" length="5.0" maxspeed="80.0" sigma="0.0"/>

<route id="r11" edges="e10 e01"/>
<route id="r12" edges="e10 e02"/>
<route id="r13" edges="e10 e03"/>
<route id="r14" edges="e10 e04"/>

<route id="r21" edges="e20 e01"/>
<route id="r22" edges="e20 e02"/>
<route id="r23" edges="e20 e03"/>
<route id="r24" edges="e20 e04"/>

<route id="r31" edges="e30 e01"/>
<route id="r32" edges="e30 e02"/>
<route id="r33" edges="e30 e03"/>
<route id="r34" edges="e30 e04"/>

<route id="r41" edges="e40 e01"/>
<route id="r42" edges="e40 e02"/>
<route id="r43" edges="e40 e03"/>
<route id="r44" edges="e40 e04"/>\n\n"""
    f.write(data)
    f.write('<flow id="type1" begin="0" end="7200" probability="'+str(p1/4)+'" route="r11" type="car"/>\n')
    f.write('<flow id="type2" begin="0" end="7200" probability="'+str(p1/4)+'" route="r12" type="car"/>\n')
    f.write('<flow id="type3" begin="0" end="7200" probability="'+str(p1/4)+'" route="r13" type="car"/>\n')
    f.write('<flow id="type4" begin="0" end="7200" probability="'+str(p1/4)+'" route="r14" type="car"/>\n\n')

    f.write('<flow id="type5" begin="0" end="7200" probability="'+str(p2/4)+'" route="r21" type="car"/>\n')
    f.write('<flow id="type6" begin="0" end="7200" probability="'+str(p2/4)+'" route="r22" type="car"/>\n')
    f.write('<flow id="type7" begin="0" end="7200" probability="'+str(p2/4)+'" route="r23" type="car"/>\n')
    f.write('<flow id="type8" begin="0" end="7200" probability="'+str(p2/4)+'" route="r24" type="car"/>\n\n')

    f.write('<flow id="type9" begin="0" end="7200" probability="'+str(p3/4)+'" route="r31" type="car"/>\n')
    f.write('<flow id="type10" begin="0" end="7200" probability="'+str(p3/4)+'" route="r32" type="car"/>\n')
    f.write('<flow id="type11" begin="0" end="7200" probability="'+str(p3/4)+'" route="r33" type="car"/>\n')
    f.write('<flow id="type12" begin="0" end="7200" probability="'+str(p3/4)+'" route="r34" type="car"/>\n\n')

    f.write('<flow id="type13" begin="0" end="7200" probability="'+str(p4/4)+'" route="r41" type="car"/>\n')
    f.write('<flow id="type14" begin="0" end="7200" probability="'+str(p4/4)+'" route="r42" type="car"/>\n')
    f.write('<flow id="type15" begin="0" end="7200" probability="'+str(p4/4)+'" route="r43" type="car"/>\n')
    f.write('<flow id="type16" begin="0" end="7200" probability="'+str(p4/4)+'" route="r44" type="car"/>\n\n')

    f.write('</routes>')
    f.close()