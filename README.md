# Traffic Classification System

SDN-based traffic classifier using POX controller and Mininet.
Classifies packets as TCP, UDP, ICMP, or OTHER and displays live stats every 5 seconds.

## Setup

### Prerequisites
- WSL2 (Ubuntu 24.04)
- Mininet: sudo apt install mininet
- POX: git clone https://github.com/noxrepo/pox.git

### Files
- traffic_classifier.py — POX controller (classification logic)
- topo.py — Mininet topology (1 switch, 3 hosts)

## Run

Terminal 1 — Start POX controller:
  cd ~/pox
  python3 pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning traffic_classifier

Terminal 2 — Start Mininet:
  sudo mn --controller=remote,port=6633 --topo=single,3

## Generate Test Traffic (inside Mininet CLI)

  pingall                            # ICMP
  h2 iperf -s &
  h1 iperf -c 10.0.0.2 -t 5         # TCP
  h3 iperf -s -u &
  h1 iperf -c 10.0.0.3 -u -t 5      # UDP

## Expected Output

=== Traffic Classification Stats ===
  TCP   :     9 packets  (39.1%)
  UDP   :     2 packets  ( 8.7%)
  ICMP  :    12 packets  (52.2%)
  OTHER :     0 packets  ( 0.0%)
====================================
