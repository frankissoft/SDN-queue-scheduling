import gtk
import re
import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
import os
import time
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.cli import CLI
from gtk.keysyms import period
COL_PATH = 0
COL_PIXBUF = 1
COL_IS_DIRECTORY = 2
filename = "No file available"
class Win(gtk.Window):
    def __init__(self):
        super(Win, self).__init__()
        self.set_title("NEU-SDN")
        self.set_size_request(1100, 600)
        self.set_position(gtk.WIN_POS_CENTER)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(65535, 65535, 65535))
        #quit
        bnquit = gtk.ToolButton(gtk.STOCK_QUIT)
        bnquit.connect("clicked", gtk.main_quit)
        #graph
        bandwidth = gtk.Button("Bandwidth")
        bandwidth.set_size_request(100, 50)
        bandwidth.connect("clicked", self.graph_bandwidth)
        jitter = gtk.Button("Jitter")
        jitter.set_size_request(100, 50)
        jitter.connect("clicked", self.graph_jitter)
        lost = gtk.Button("Lost")
        lost.set_size_request(100, 50)
        lost.connect("clicked", self.graph_lost)
        #open file
        opentb = gtk.ToolButton(gtk.STOCK_OPEN)
        opentb.connect("clicked", self.on_file)
        self.label = gtk.Label(filename)
        self.text = gtk.Label("file")
        #file dir
        self.sourceDir = "/home/xsk/learn/log"
        self.targetDir_SFQ = "/home/xsk/learn/log_SFQ"
        self.targetDir_PQ = "/home/xsk/learn/log_PQ"
        self.targetDir_CBWFQ = "/home/xsk/learn/log_CBWFQ"
        self.targetDir_LLQ = "/home/xsk/learn/log_LLQ"
        #choose queue
        self.SFQ = gtk.ToggleButton("SFQ")
        self.SFQ.set_size_request(100, 50)
        self.SFQ.connect("clicked", self.on_SFQ)
        self.PQ = gtk.ToggleButton("PQ")
        self.PQ.set_size_request(100, 50)
        self.PQ.connect("clicked", self.on_PQ)
        self.CBWFQ = gtk.ToggleButton("CBWFQ")
        self.CBWFQ.set_size_request(100, 50)
        self.CBWFQ.connect("clicked", self.on_CBWFQ)
        self.LLQ = gtk.ToggleButton("LLQ")
        self.LLQ.set_size_request(100, 50)
        self.LLQ.connect("clicked", self.on_LLQ)
        #image
        str_image = ["/home/xsk/switch.png", "/home/xsk/host.png", 
                     "/home/xsk/controller.png", "/home/xsk/s1_s2.png", 
                     "/home/xsk/c0.png", "/home/xsk/s_vhs.png", "/home/xsk/s_vhc.png"]
        self.str_name = ['s1', 's2', 'vhc1', 'vhc2', 'vhc3', 'vhc4', 
                    'vhs1', 'vhs2', 'vhs3', 'vhs4', 'c0']
        self.str_IP = ['', '', '10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', 
                       '10.0.0.5', '10.0.0.6', '10.0.0.7', '10.0.0.8', '']
        self.str_Mac = ['', '',
                        '00:00:00:00:00:01', '00:00:00:00:00:02', 
                        '00:00:00:00:00:03', '00:00:00:00:00:04',
                        '00:00:00:00:00:05', '00:00:00:00:00:06',
                        '00:00:00:00:00:07', '00:00:00:00:00:08', '']
        self.tag_s2 = []
        self.tag_s1 = []
        image_s1 = gtk.Image()
        image_s1.set_from_file(str_image[0])
        image_s2 = gtk.Image()
        image_s2.set_from_file(str_image[0])
        image_h1 = gtk.Image()
        image_h1.set_from_file(str_image[1])
        image_h2 = gtk.Image()
        image_h2.set_from_file(str_image[1])
        image_h3 = gtk.Image()
        image_h3.set_from_file(str_image[1])
        image_h4 = gtk.Image()
        image_h4.set_from_file(str_image[1])
        image_h5 = gtk.Image()
        image_h5.set_from_file(str_image[1])
        image_h6 = gtk.Image()
        image_h6.set_from_file(str_image[1])
        image_h7 = gtk.Image()
        image_h7.set_from_file(str_image[1])
        image_h8 = gtk.Image()
        image_h8.set_from_file(str_image[1])
        image_c0 = gtk.Image()
        image_c0.set_from_file(str_image[2])
        image_s1_s2 = gtk.Image()
        image_s1_s2.set_from_file(str_image[3])
        image_c0_switch = gtk.Image()
        image_c0_switch.set_from_file(str_image[4])
        image_s_vhs = gtk.Image()
        image_s_vhs.set_from_file(str_image[5])
        image_s_vhc = gtk.Image()
        image_s_vhc.set_from_file(str_image[6])
        self.button_s1 = gtk.Button()
        self.button_s1.set_image(image_s1)
        self.button_s2 = gtk.Button()
        self.button_s2.set_image(image_s2)
        self.button_h1 = gtk.ToggleButton()
        self.button_h1.set_image(image_h1)
        self.button_h2 = gtk.ToggleButton()
        self.button_h2.set_image(image_h2)
        self.button_h3 = gtk.ToggleButton()
        self.button_h3.set_image(image_h3)
        self.button_h4 = gtk.ToggleButton()
        self.button_h4.set_image(image_h4)
        self.button_h5 = gtk.ToggleButton()
        self.button_h5.set_image(image_h5)
        self.button_h6 = gtk.ToggleButton()
        self.button_h6.set_image(image_h6)
        self.button_h7 = gtk.ToggleButton()
        self.button_h7.set_image(image_h7)
        self.button_h8 = gtk.ToggleButton()
        self.button_h8.set_image(image_h8)
        self.button_c0 = gtk.Button()
        self.button_c0.set_image(image_c0)
        self.label_s1 = gtk.Label(self.str_name[0])
        self.label_s2 = gtk.Label(self.str_name[1])
        self.label_h1 = gtk.Label(self.str_name[2])
        self.label_h2 = gtk.Label(self.str_name[3])
        self.label_h3 = gtk.Label(self.str_name[4])
        self.label_h4 = gtk.Label(self.str_name[5])
        self.label_h5 = gtk.Label(self.str_name[6])
        self.label_h6 = gtk.Label(self.str_name[7])
        self.label_h7 = gtk.Label(self.str_name[8])
        self.label_h8 = gtk.Label(self.str_name[9])
        self.label_c0 = gtk.Label(self.str_name[10])
        self.labels = [self.label_s1, self.label_s2, self.label_h1,
                       self.label_h2, self.label_h3, self.label_h4,
                       self.label_h5, self.label_h6, self.label_h7,
                       self.label_h8, self.label_c0]
        #button
        self.button_h1.connect("clicked", self.on_h1)
        self.button_h2.connect("clicked", self.on_h2)
        self.button_h3.connect("clicked", self.on_h3)
        self.button_h4.connect("clicked", self.on_h4)
        self.button_h5.connect("clicked", self.on_h5)
        self.button_h6.connect("clicked", self.on_h6)
        self.button_h7.connect("clicked", self.on_h7)
        self.button_h8.connect("clicked", self.on_h8)
        self.button_s1.connect("clicked", self.on_s1)
        self.button_s2.connect("clicked", self.on_s2)
        #menu
        mb = gtk.MenuBar()
        filemenu = gtk.Menu()
        filem = gtk.ImageMenuItem(gtk.STOCK_PROPERTIES)
        filem.set_size_request(65, 35)
        filem.set_submenu(filemenu)
        agr = gtk.AccelGroup()
        self.add_accel_group(agr)
        self.ms1 = gtk.MenuItem(self.str_name[0], agr)
        key, mod = gtk.accelerator_parse("A")
        self.ms1.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.ms1.connect("activate", self.on_ms1)
        filemenu.append(self.ms1)
        self.ms2 = gtk.MenuItem(self.str_name[1], agr)
        key, mod = gtk.accelerator_parse("B")
        self.ms2.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.ms2.connect("activate", self.on_ms2)
        filemenu.append(self.ms2)
        self.mh1 = gtk.MenuItem(self.str_name[2], agr)
        key, mod = gtk.accelerator_parse("1")
        self.mh1.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.mh1.connect("activate", self.on_mh1)
        filemenu.append(self.mh1)
        self.mh2 = gtk.MenuItem(self.str_name[3], agr)
        key, mod = gtk.accelerator_parse("2")
        self.mh2.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.mh2.connect("activate", self.on_mh2)
        filemenu.append(self.mh2)
        self.mh3 = gtk.MenuItem(self.str_name[4], agr)
        key, mod = gtk.accelerator_parse("3")
        self.mh3.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.mh3.connect("activate", self.on_mh3)
        filemenu.append(self.mh3)
        self.mh4 = gtk.MenuItem(self.str_name[5], agr)
        key, mod = gtk.accelerator_parse("4")
        self.mh4.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.mh4.connect("activate", self.on_mh4)
        filemenu.append(self.mh4)
        self.mh5 = gtk.MenuItem(self.str_name[6], agr)
        key, mod = gtk.accelerator_parse("5")
        self.mh5.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.mh5.connect("activate", self.on_mh5)
        filemenu.append(self.mh5)
        self.mh6 = gtk.MenuItem(self.str_name[7], agr)
        key, mod = gtk.accelerator_parse("6")
        self.mh6.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.mh6.connect("activate", self.on_mh6)
        filemenu.append(self.mh6)
        self.mh7 = gtk.MenuItem(self.str_name[8], agr)
        key, mod = gtk.accelerator_parse("7")
        self.mh7.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.mh7.connect("activate", self.on_mh7)
        filemenu.append(self.mh7)
        self.mh8 = gtk.MenuItem(self.str_name[9], agr)
        key, mod = gtk.accelerator_parse("8")
        self.mh8.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.mh8.connect("activate", self.on_mh8)
        filemenu.append(self.mh8)
        self.mc0 = gtk.MenuItem(self.str_name[10], agr)
        key, mod = gtk.accelerator_parse("C")
        self.mc0.add_accelerator("activate", agr, key, mod, gtk.ACCEL_VISIBLE)
        self.mc0.connect("activate", self.on_mc0)
        filemenu.append(self.mc0)
        self.menuitems = [self.ms1, self.ms2, self.mh1, self.mh2, 
                          self.mh3, self.mh4, self.mh5, self.mh6, 
                          self.mh7, self.mh8, self.mc0]
        mb.append(filem)
        #qos type
        self.qos_SFQ = 'sudo ovs-vsctl set port '+self.str_name[1]+'-eth5 qos=@newqos -- \
            --id=@newqos create qos type=linux-htb other-config:max-rate=8000000 queues=0=@q0,1=@q1,2=@q2,3=@q3 -- \
            --id=@q0 create queue other-config:min-rate=80 other-config:max-rate=8000000 -- \
            --id=@q1 create queue other-config:min-rate=80 other-config:max-rate=8000000 -- \
            --id=@q2 create queue other-config:min-rate=80 other-config:max-rate=8000000 -- \
            --id=@q3 create queue other-config:min-rate=80 other-config:max-rate=8000000'
        self.qos_PQ = 'sudo ovs-vsctl set port '+self.str_name[1]+'-eth5 qos=@newqos -- \
            --id=@newqos create qos type=linux-htb other-config:max-rate=8000000 queues=0=@q0,1=@q1,2=@q2,3=@q3 -- \
            --id=@q0 create queue other-config:min-rate=80000 other-config:max-rate=8000000 other-config:priority=1 -- \
            --id=@q1 create queue other-config:min-rate=80000 other-config:max-rate=8000000 other-config:priority=2 -- \
            --id=@q2 create queue other-config:min-rate=80000 other-config:max-rate=8000000 other-config:priority=2 -- \
            --id=@q3 create queue other-config:min-rate=80000 other-config:max-rate=8000000 other-config:priority=3'
        self.qos_CBWFQ = 'sudo ovs-vsctl set port '+self.str_name[1]+'-eth5 qos=@newqos -- \
            --id=@newqos create qos type=linux-htb other-config:max-rate=8000000 queues=0=@q0,1=@q1,2=@q2,3=@q3 -- \
            --id=@q0 create queue other-config:min-rate=800000 other-config:max-rate=8000000 -- \
            --id=@q1 create queue other-config:min-rate=1600000 other-config:max-rate=8000000 -- \
            --id=@q2 create queue other-config:min-rate=2400000 other-config:max-rate=8000000 -- \
            --id=@q3 create queue other-config:min-rate=3200000 other-config:max-rate=8000000'
        self.qos_LLQ = 'sudo ovs-vsctl set port '+self.str_name[1]+'-eth5 qos=@newqos -- \
            --id=@newqos create qos type=linux-htb other-config:max-rate=8000000 queues=0=@q0,1=@q1,2=@q2,3=@q3 -- \
            --id=@q0 create queue other-config:min-rate=8000000 other-config:max-rate=8000000 other-config:priority=1 -- \
            --id=@q1 create queue other-config:min-rate=80000 other-config:max-rate=8000000 other-config:priority=2 -- \
            --id=@q2 create queue other-config:min-rate=160000 other-config:max-rate=8000000 other-config:priority=2 -- \
            --id=@q3 create queue other-config:min-rate=240000 other-config:max-rate=8000000 other-config:priority=2'
        #position
        fixed = gtk.Fixed()
        fixed.put(self.button_s2, 207, 220)
        fixed.put(self.button_s1, 317, 220)
        fixed.put(self.button_h1, 60, 90)
        fixed.put(self.button_h2, 60, 170)
        fixed.put(self.button_h3, 60, 250)
        fixed.put(self.button_h4, 60, 329)
        fixed.put(self.button_h5, 460, 90)
        fixed.put(self.button_h6, 460, 170)
        fixed.put(self.button_h7, 460, 250)
        fixed.put(self.button_h8, 460, 326)
        fixed.put(self.button_c0, 253, 107)
        fixed.put(self.label_s1, 340, 270)
        fixed.put(self.label_s2, 230, 270)
        fixed.put(self.label_h1, 20, 105)
        fixed.put(self.label_h2, 20, 185)
        fixed.put(self.label_h3, 20, 265)
        fixed.put(self.label_h4, 20, 340)
        fixed.put(self.label_h5, 520, 105)
        fixed.put(self.label_h6, 520, 185)
        fixed.put(self.label_h7, 520, 265)
        fixed.put(self.label_h8, 520, 340)
        fixed.put(self.label_c0, 280, 90)
        fixed.put(image_s1_s2, 267, 220)
        fixed.put(image_c0_switch, 208, 185)
        fixed.put(image_s_vhs, 375, 92)
        fixed.put(image_s_vhc, 110, 92)
        fixed.put(self.SFQ, 60, 430)
        fixed.put(self.PQ, 175, 430)
        fixed.put(self.CBWFQ, 290, 430)
        fixed.put(self.LLQ, 405, 430)
        fixed.put(bandwidth, 60, 495)
        fixed.put(jitter, 175, 495)
        fixed.put(lost, 290, 495)
        fixed.put(opentb, 600,20)
        fixed.put(self.label, 640, 30)
        fixed.put(self.text, 620, 80)
        fixed.put(mb, 55, 20)
        fixed.put(bnquit, 20, 20)
        self.connect("destroy", gtk.main_quit)
        self.add(fixed)
        self.show_all()
    def qos_queque(self, qos_str, udp_str):
        net=Mininet(host=CPULimitedHost,link=TCLink,cleanup=True)
        #creating nodes in the network
        c0=net.addController(self.str_name[10])
        s1 = net.addSwitch(self.str_name[0])
        s2 = net.addSwitch(self.str_name[1])
        #add hosts
        vhc1 = net.addHost( self.str_name[2],cpu=0.5/5,mac=self.str_Mac[2], ip=self.str_IP[2])
        vhc2 = net.addHost( self.str_name[3],cpu=0.5/5,mac=self.str_Mac[3], ip=self.str_IP[3])
        vhc3 = net.addHost( self.str_name[4],cpu=0.5/5,mac=self.str_Mac[4], ip=self.str_IP[4])
        vhc4 = net.addHost( self.str_name[5],cpu=0.5/5,mac=self.str_Mac[5], ip=self.str_IP[5])
        vhs1 = net.addHost( self.str_name[6],cpu=0.5/5,mac=self.str_Mac[6], ip=self.str_IP[6])
        vhs2 = net.addHost( self.str_name[7],cpu=0.5/5,mac=self.str_Mac[7], ip=self.str_IP[7])
        vhs3 = net.addHost( self.str_name[8],cpu=0.5/5,mac=self.str_Mac[8], ip=self.str_IP[8])
        vhs4 = net.addHost( self.str_name[9],cpu=0.5/5,mac=self.str_Mac[9], ip=self.str_IP[9])
        net.addLink( vhs1, s1 )
        net.addLink( vhs2, s1 )
        net.addLink( vhs3, s1 )
        net.addLink( vhs4, s1 )
        net.addLink( vhc1, s2 )
        net.addLink( vhc2, s2 )
        net.addLink( vhc3, s2 )
        net.addLink( vhc4, s2 )
        net.addLink( s1, s2)
        net.start()
        s2_htb_QoS= qos_str
        s2.cmd(s2_htb_QoS)
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[1]+' in_port=1,actions=enqueue:5:0')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[1]+' in_port=2,actions=enqueue:5:1')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[1]+' in_port=3,actions=enqueue:5:2')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[1]+' in_port=4,actions=enqueue:5:3')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[1]+' dl_src='+self.str_Mac[6]+',actions=output:1')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[1]+' dl_src='+self.str_Mac[7]+',actions=output:2')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[1]+' dl_src='+self.str_Mac[8]+',actions=output:3')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[1]+' dl_src='+self.str_Mac[9]+',actions=output:4')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[0]+' in_port=1,actions=output:5')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[0]+' in_port=2,actions=output:5')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[0]+' in_port=3,actions=output:5')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[0]+' in_port=4,actions=output:5')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[0]+' dl_src='+self.str_Mac[2]+',actions=output:1')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[0]+' dl_src='+self.str_Mac[3]+',actions=output:2')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[0]+' dl_src='+self.str_Mac[4]+',actions=output:3')
        c0.cmd('sudo ovs-ofctl add-flow '+self.str_name[0]+' dl_src='+self.str_Mac[5]+',actions=output:4')
        #CLI(net)
        c0.cmd('sh ovs-vsctl add-port s1 enp2s0')
        c0.cmd('sh ifconfig s1 10.0.0.106 netmask 255.255.255.248')
        c0.cmd('sh ovs-vsctl -- --id=@sflow create sFlow agent=s1 target=\"10.0.0.106:6343\" header=128 sampling=64 polling=1 -- set bridge s1 sflow=@sflow')
        CLI(net)
        '''print "sflow begin---sleep"
        time.sleep(120)
        print "sflow begin---awake"'''
        net.iperf_single_ipv6(hosts=(vhc4, vhs4), udpBw=udp_str[3], period = 600)
        time.sleep(10)
        net.iperf_single_ipv6(hosts=(vhc3, vhs3), udpBw=udp_str[2], period = 600)
        time.sleep(10)
        net.iperf_single_ipv6(hosts=(vhc2, vhs2), udpBw=udp_str[1], period = 600)
        time.sleep(10)
        net.iperf_single_ipv6(hosts=(vhc1, vhs1), udpBw=udp_str[0], period = 600)
        time.sleep(40)
        s2.cmd('ovs-vsctl clear Port '+self.str_name[1]+'-eth5 qos')
        s2.cmd('ovs-vsctl --all destroy qos')
        s2.cmd('ovs-vsctl --all destroy queue')
        net.stop()
        print "net stopped"
    def on_SFQ(self, wdget):
        if self.SFQ.get_active():
            self.qos_queque(self.qos_SFQ, ['8000k', '8000k', '8000k', '8000k'])
        else:
            for datafile in os.listdir(self.sourceDir): 
                sourceFile = os.path.join(self.sourceDir, datafile) 
                targetFile = os.path.join(self.targetDir_SFQ, datafile) 
                if os.path.isfile(sourceFile): 
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
    def on_PQ(self, wdget):
        if self.PQ.get_active():
            self.qos_queque(self.qos_PQ, ['5000k', '5000k', '5000k', '5000k'])
        else:
            for datafile in os.listdir(self.sourceDir): 
                sourceFile = os.path.join(self.sourceDir, datafile) 
                targetFile = os.path.join(self.targetDir_PQ, datafile) 
                if os.path.isfile(sourceFile): 
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
    def on_CBWFQ(self, wdget):
        if self.CBWFQ.get_active():
            self.qos_queque(self.qos_CBWFQ, ['8000k', '8000k', '8000k', '8000k'])
        else:
            for datafile in os.listdir(self.sourceDir): 
                sourceFile = os.path.join(self.sourceDir, datafile) 
                targetFile = os.path.join(self.targetDir_CBWFQ, datafile) 
                if os.path.isfile(sourceFile): 
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
    def on_LLQ(self, wdget):
        if self.LLQ.get_active():
            self.qos_queque(self.qos_LLQ, ['5000k', '5000k', '5000k', '5000k'])
        else:
            for datafile in os.listdir(self.sourceDir): 
                sourceFile = os.path.join(self.sourceDir, datafile) 
                targetFile = os.path.join(self.targetDir_LLQ, datafile) 
                if os.path.isfile(sourceFile): 
                    open(targetFile, "wb").write(open(sourceFile, "rb").read())
    def on_file(self, wdget):
        self.filew = gtk.FileSelection("File selection")
        self.filew.connect("destroy", lambda w: self.filew.destroy)
        self.filew.ok_button.connect("clicked", lambda w: Win.loadfile(self))
        self.filew.cancel_button.connect("clicked", lambda w: Win.back(self))
        self.filew.set_filename("")
        self.filew.show()
    def loadfile(self):
        self.label.set_text(self.filew.get_filename())
        self.filew.destroy()
        route = self.label.get_text()
        f = open(route, 'r')
        self.text.set_text(f.read())
    def back(self):
        self.filew.destroy()
    def graph_client(self, tag_s2):
        count = len(tag_s2)
        for i in range(count):
            k = 221
            plt.figure(tag_s2[i])
            for j in range(1, 5):
                if os.path.exists('/home/xsk/learn/log/client_vhc'+str(tag_s2[i])+'-vhs'+str(j)+'.out'):
                    fobj=open('/home/xsk/learn/log/client_vhc'+str(tag_s2[i])+'-vhs'+str(j)+'.out','r')
                    data='';
                    for line in fobj:
                        data+=(str(line))
                    pattern=re.compile(']\W+(\d+)\..*?sec.*?KBytes\W+([0-9\.]+)\W+[MK]bits',re.S)
                    items=re.findall(pattern,data)
                    x=[]
                    y=[]
                    for item in items:
                        seq=int(item[0])
                        b=float(item[1])
                        if b>1000:
                            b=b/1000
                        print '%d\t%.1f' % (seq,b)
                    #print '%d\t%.3f\t%.3f\t%.3f' % (seq,b,j,loss)
                        x.append(seq)
                        y.append(b)
                    fobj.close()
                    x=x[0:-1]
                    y=y[0:-1]
                    plt.subplot(k)
                    plt.plot(x,y)
                    plt.title(self.str_name[tag_s2[i]+1]+'-'+self.str_name[j+5])
                    k += 1
                    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, 
                                        hspace=0.35, wspace=0.45)
        plt.show()
    def graph_server(self):
        flow = ['flow4', 'flow3', 'flow2', 'flow1']
        for i in range(1, 5):
            fobj=open('/home/xsk/learn/log/server_vhc'+str(5-i)+'-vhs'+str(5-i)+'.out','r')
            data='';
            for line in fobj:
                data+=(str(line))
            pattern=re.compile(
                    ']\W+(\d+)\..*?sec.*?KBytes\W+([0-9\.]+)\W+[MK]bits.*?([0-9\.]+)\W+ms.*?([0-9\.]+)%'
                    ,re.S)
            items=re.findall(pattern,data)
            x=[]
            y=[]
            z=[]
            w=[]
            for item in items:
                seq=int(item[0])+(i-1)*10
                b=float(item[1])
                if b>10:
                    b=b/1000
                j=float(item[2])
                loss=float(item[3])/100.0
                print '%d\t%.3f\t%.3f\t%.3f' % (seq,b,j,loss)
                x.append(seq)
                y.append(b)
                z.append(j)
                w.append(loss)
            fobj.close()
            x=x[0:-1]
            y=y[0:-1]
            z=z[0:-1]
            w=w[0:-1]
            if self.SFQ.get_active():
                ptr = "SFQ"
            elif self.PQ.get_active():
                ptr = "PQ"
            elif self.CBWFQ.get_active():
                ptr = "CBWFQ"
            else:
                ptr = "LLQ"
            plt.figure(ptr, figsize=(12, 8))
            plt.subplot(221)
	    plt.xticks(fontsize=15)
	    plt.yticks(fontsize=15)
            plt.plot(x, z, label = flow[i-1], linewidth = 2)
	    #plt.legend(bbox_to_anchor=(0.58,0.95),fontsize=12,ncol=2)
            plt.legend(ncol=2)
	    plt.ylim(0, 50)
	    plt.xlim(0, 60)
            plt.title("Jitter", size = 20)
            plt.xlabel("time/s", size = 20)
            plt.ylabel("ms", size = 20)
            plt.subplot(222)
	    plt.xticks(fontsize=15)
	    plt.yticks(fontsize=15)
	    plt.xlim(0, 60)
            plt.plot(x, w, label = flow[i-1], linewidth = 2)
	    #plt.legend(bbox_to_anchor=(0.40,0.95),fontsize=12,ncol=2)
            plt.legend(ncol=2)
	    plt.title("Lost", size = 20)
            plt.xlabel("time/s", size = 20)
            plt.subplot(212)
	    plt.axvline(10,ls="--",color="r")
	    plt.axvline(20,ls="--",color="r")
	    plt.axvline(30,ls="--",color="r")
	    plt.xticks(fontsize=15)
	    plt.yticks(fontsize=15)
            plt.plot(x, y, label = flow[i-1], linewidth = 2)
            #plt.legend(bbox_to_anchor=(0.45,0.95),fontsize=12,ncol=2)
	    plt.legend(ncol=2)
            plt.xlim(0, 60)
            plt.ylim(0, 8)
            plt.xlabel("time/s", size = 20)
            plt.ylabel("Mbit/s", size = 20)
            plt.title('Bandwidth', size = 20)
            plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, 
                                        hspace=0.35, wspace=0.45)
        plt.show()
    def graph_bandwidth(self, wdget):
        flow = ['flow4', 'flow3', 'flow2', 'flow1']
        filedir = ['log_SFQ', 'log_PQ', 'log_CBWFQ', 'log_LLQ']
        figure_name = ['SFQ', 'PQ', 'CBWFQ', 'LLQ']
        for i in range(1, 5):
            k = 221
            for a in range(4):
                fobj=open('/home/xsk/learn/'+filedir[a]+'/server_vhc'+str(5-i)+'-vhs'+str(5-i)+'.out','r')
                data='';
                for line in fobj:
                    data+=(str(line))
                pattern=re.compile(
                    ']\W+(\d+)\..*?sec.*?KBytes\W+([0-9\.]+)\W+[MK]bits.*?([0-9\.]+)\W+ms.*?([0-9\.]+)%'
                    ,re.S)
                items=re.findall(pattern,data)
                x=[]
                y=[]
                for item in items:
                    seq=int(item[0])+(i-1)*10
                    b=float(item[1])
                    if b>10:
                        b=b/1000
                    print '%d\t%.3f' % (seq,b)
                    x.append(seq)
                    y.append(b)
                fobj.close()
                x=x[0:-1]
                y=y[0:-1]
                plt.figure('Bandwidth', figsize=(12, 8))
                plt.subplot(k)
                k += 1
                plt.plot(x, y, label = flow[i-1], linewidth=2)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
                plt.legend(bbox_to_anchor=(0.6,0.95),fontsize=12,ncol=2)
		plt.legend(fontsize=12,ncol=2)
		plt.axvline(10,ls="--",color="r")
		plt.axvline(20,ls="--",color="r")
		plt.axvline(30,ls="--",color="r")
                plt.xlim(0, 60)
                plt.ylim(0, 8)
                plt.xlabel("time/s", size=20)
                plt.ylabel("Mbit/s", size=20)
                plt.title(figure_name[a]+'-Bandwidth', size=20)
                plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95,
                                        hspace=0.35, wspace=0.15)
        plt.show()
    def graph_jitter(self, wdget):
        flow = ['flow4', 'flow3', 'flow2', 'flow1']
        filedir = ['log_SFQ', 'log_PQ', 'log_CBWFQ', 'log_LLQ']
        figure_name = ['SFQ', 'PQ', 'CBWFQ', 'LLQ']
        for i in range(1, 5):
            k = 221
            for a in range(4):
                fobj=open('/home/xsk/learn/'+filedir[a]+'/server_vhc'+str(5-i)+'-vhs'+str(5-i)+'.out','r')
                data='';
                for line in fobj:
                    data+=(str(line))
                pattern=re.compile(
                    ']\W+(\d+)\..*?sec.*?KBytes\W+([0-9\.]+)\W+[MK]bits.*?([0-9\.]+)\W+ms.*?([0-9\.]+)%'
                    ,re.S)
                items=re.findall(pattern,data)
                x=[]
                y=[]
                for item in items:
                    seq=int(item[0])+(i-1)*10
                    j=float(item[2])
                    print '%d\t%.3f' % (seq,j)
                    x.append(seq)
                    y.append(j)
                fobj.close()
                x=x[0:-1]
                y=y[0:-1]
                plt.figure("Jitter", figsize=(12, 8))
                plt.subplot(k)
                k += 1
                plt.plot(x, y, label = flow[i-1], linewidth=2)
		plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
                #plt.legend(bbox_to_anchor=(0.55, 1.0),fontsize=12,ncol=2)
		plt.legend(ncol=2)
                plt.xlim(0, 60)
                plt.ylim(0, 50)
                plt.xlabel("time/s", size=20)
                plt.ylabel("ms", size=20)
                plt.title(figure_name[a]+'-Jitter', size=20)
                plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95,
                                        hspace=0.35, wspace=0.15)
        plt.show()
    def graph_lost(self, wdget):
        flow = ['flow4', 'flow3', 'flow2', 'flow1']
        filedir = ['log_SFQ', 'log_PQ', 'log_CBWFQ', 'log_LLQ']
        figure_name = ['SFQ', 'PQ', 'CBWFQ', 'LLQ']
        for i in range(1, 5):
            k = 221
            for a in range(4):
                fobj=open('/home/xsk/learn/'+filedir[a]+'/server_vhc'+str(5-i)+'-vhs'+str(5-i)+'.out','r')
                data='';
                for line in fobj:
                    data+=(str(line))
                pattern=re.compile(
                    ']\W+(\d+)\..*?sec.*?KBytes\W+([0-9\.]+)\W+[MK]bits.*?([0-9\.]+)\W+ms.*?([0-9\.]+)%'
                    ,re.S)
                items=re.findall(pattern,data)
                x=[]
                y=[]
                for item in items:
                    seq=int(item[0])+(i-1)*10
                    loss=float(item[3])/100.0
                    x.append(seq)
                    y.append(loss)
                fobj.close()
                x=x[0:-1]
                y=y[0:-1]
                plt.figure("Lost", figsize=(12, 8))
                plt.subplot(k)
                k += 1
                plt.plot(x, y, label = flow[i-1], linewidth=2)
                plt.xticks(fontsize=15)
		plt.yticks(fontsize=15)
                #plt.legend(bbox_to_anchor=(0.55, 1.0),fontsize=12,ncol=2)
		plt.legend(ncol=2)
                plt.xlim(0, 60)
                plt.ylim(0, 1)
                plt.xlabel("time/s", size=20)
                plt.ylabel(" ")
                plt.title(figure_name[a]+'-Lost', size=20)
                plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95,
                                        hspace=0.35, wspace=0.15)
        plt.show()
    def on_h1(self, wdget):
        if self.button_h1.get_active():
            self.tag_s2.append(1)
        else:
            self.tag_s2.remove(1)
    def on_h2(self, wdget):
        if self.button_h2.get_active():
            self.tag_s2.append(2)
        else:
            self.tag_s2.remove(2)
    def on_h3(self, wdget):
        if self.button_h3.get_active():
            self.tag_s2.append(3)
        else:
            self.tag_s2.remove(3)
    def on_h4(self, wdget):
        if self.button_h4.get_active():
            self.tag_s2.append(4)
        else:
            self.tag_s2.remove(4)
    def on_h5(self, wdget):
        if self.button_h5.get_active():
            self.tag_s1.append(1)
        else:
            self.tag_s1.remove(1)
    def on_h6(self, wdget):
        if self.button_h6.get_active():
            self.tag_s1.append(2)
        else:
            self.tag_s1.remove(2)
    def on_h7(self, wdget):
        if self.button_h7.get_active():
            self.tag_s1.append(3)
        else:
            self.tag_s1.remove(3)
    def on_h8(self, wdget):
        if self.button_h8.get_active():
            self.tag_s1.append(4)
        else:
            self.tag_s1.remove(4)
    def on_s1(self, wdget):
        self.graph_server()
    def on_s2(self, wdget):
        self.graph_client(self.tag_s2)
    def on_ms1(self, wdget):
        self.sub_win(0)
    def on_ms2(self, wdget):
        self.sub_win(1)
    def on_mh1(self, wdget):
        self.sub_win(2)
    def on_mh2(self, wdget):
        self.sub_win(3)
    def on_mh3(self, wdget):
        self.sub_win(4)
    def on_mh4(self, wdget):
        self.sub_win(5)
    def on_mh5(self, wdget):
        self.sub_win(6)
    def on_mh6(self, wdget):
        self.sub_win(7)
    def on_mh7(self, wdget):
        self.sub_win(8)
    def on_mh8(self, wdget):
        self.sub_win(9)
    def on_mc0(self, wdget):
        self.sub_win(10)
    def save(self, wdget1, wdget2, wdget3, i):
        self.str_name[i] = wdget1.get_text()
        self.str_IP[i] = wdget2.get_text()
        self.str_Mac[i] = wdget3.get_text()
        self.labels[i].set_text(self.str_name[i])
        self.menuitems[i].set_label(self.str_name[i])
    def sub_win(self, i):
        win = gtk.Window()
        win.set_title("properties")
        win.set_size_request(300, 300)
        savetb = gtk.ToolButton(gtk.STOCK_SAVE)
        quittb = gtk.ToolButton(gtk.STOCK_QUIT)
        quittb.connect("clicked", lambda w: win.destroy())
        name = gtk.Label('name :')
        IP = gtk.Label('IP :')
        Mac = gtk.Label('Mac :')
        get_name = gtk.Entry()
        get_name.set_text(self.str_name[i])
        get_IP = gtk.Entry()
        get_IP.set_text(self.str_IP[i])
        get_Mac = gtk.Entry()
        get_Mac.set_text(self.str_Mac[i])
        fixed = gtk.Fixed()
        fixed.put(savetb, 0, 0)
        fixed.put(quittb, 35, 0)
        fixed.put(name, 20, 60)
        fixed.put(IP, 20, 105)
        fixed.put(Mac, 20, 150)
        fixed.put(get_name, 65, 55)
        fixed.put(get_IP, 65, 100)
        fixed.put(get_Mac, 65, 140)
        win.add(fixed)
        savetb.connect("clicked", lambda w: self.save(get_name, get_IP, get_Mac, i))
        win.show_all()
Win()
gtk.main()
