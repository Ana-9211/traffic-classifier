# Traffic Classification System

## Problem Statement

In traditional networks, routers and switches make forwarding decisions independently with no centralized visibility into traffic patterns. This makes it difficult to monitor, classify, or respond to different types of network traffic in real time.

This project implements an **SDN-based Traffic Classification System** using a POX OpenFlow controller and Mininet. The controller inspects every packet entering the network, classifies it by protocol (TCP, UDP, ICMP, or OTHER), maintains running statistics, and displays a live classification report every 5 seconds. A separate L2 learning switch module handles packet forwarding.

## Architecture

- **Controller:** POX (Python-based OpenFlow controller)
- **Topology:** Single OpenFlow switch with 3 hosts (Mininet)
- **Classification Logic:** The `traffic_classifier.py` module listens for `PacketIn` events, extracts the IPv4 header, and increments per-protocol counters based on `ip.protocol`.
- **Forwarding:** Handled by POX's built-in `forwarding.l2_learning` module, which installs MAC-based flow rules on the switch.

## Files

| File | Description |
|------|-------------|
| `traffic_classifier.py` | POX controller module — classifies packets by protocol and prints stats |
| `topo.py` | Mininet topology script (1 switch, 3 hosts) |
| `screenshots/` | Execution proof — POX stats output and Mininet test results |

## Prerequisites

- WSL2 (Ubuntu 24.04) or any Linux environment
- Python 3.x
- Mininet: `sudo apt install mininet -y`
- Open vSwitch: `sudo apt install openvswitch-switch -y`
- POX controller: `git clone https://github.com/noxrepo/pox.git ~/pox`

## Setup & Execution

### Step 1 — Install the classifier module

Copy `traffic_classifier.py` into your POX directory:

```bash
cp traffic_classifier.py ~/pox/pox/traffic_classifier.py
```

### Step 2 — Start the POX controller (Terminal 1)

```bash
cd ~/pox
python3 pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning traffic_classifier
```

You should see:
```
INFO:traffic_classifier:Traffic Classifier started
DEBUG:openflow.of_01:Listening on 0.0.0.0:6633
```

### Step 3 — Start Mininet (Terminal 2)

```bash
sudo mn --controller=remote,port=6633 --topo=single,3
```

### Step 4 — Generate test traffic (inside Mininet CLI)

```bash
pingall                            # ICMP traffic
h2 iperf -s &
h1 iperf -c 10.0.0.2 -t 5         # TCP traffic
h3 iperf -s -u &
h1 iperf -c 10.0.0.3 -u -t 5      # UDP traffic
```

### Step 5 — Verify flow rules

```bash
sudo ovs-ofctl dump-flows s1
```

## Test Scenarios

### Scenario A: ICMP-Only Traffic

Run only `pingall` — the stats table shows 100% ICMP packets. This confirms the classifier correctly identifies ICMP protocol (protocol number 1).

### Scenario B: Mixed Protocol Traffic

After running TCP (iperf) and UDP (iperf -u) alongside ping, the stats table shows a distribution across all three protocols, confirming the classifier distinguishes between TCP (protocol 6), UDP (protocol 17), and ICMP (protocol 1).

## Expected Output

### Classification Stats (Terminal 1)
```
=== Traffic Classification Stats ===
  TCP   :     9 packets  (39.1%)
  UDP   :     2 packets  ( 8.7%)
  ICMP  :    12 packets  (52.2%)
  OTHER :     0 packets  ( 0.0%)
====================================
```

### Connectivity Test (Terminal 2)
```
*** Ping: testing ping reachability
h1 -> h2 h3
h2 -> h1 h3
h3 -> h1 h2
*** Results: 0% dropped (6/6 received)
```

### Performance Observations

| Metric | Value | Notes |
|--------|-------|-------|
| Ping latency | < 1ms | Expected for emulated single-switch topology |
| TCP throughput (iperf) | ~27.7 Gbps | Virtual switch, no real bottleneck |
| UDP throughput (iperf) | ~1.05 Mbits/sec | Default iperf UDP bandwidth |
| UDP jitter | 0.045 ms | Minimal in emulated environment |
| UDP packet loss | 0% (0/449) | No congestion |

The high TCP throughput is expected in Mininet since traffic stays within the kernel. UDP defaults to 1 Mbps unless overridden with `-b`. Latency is sub-millisecond because no physical network is involved.

## Screenshots

See the `screenshots/` folder for execution proof:
- `YOUR_SCREENSHOT_1.png` — ICMP-only classification (100%)
- `YOUR_SCREENSHOT_2.png` — TCP and UDP traffic appearing in stats
- `YOUR_SCREENSHOT_3.png` — Final mixed-protocol distribution

## References

1. Mininet Overview — https://mininet.org/overview/
2. Mininet Walkthrough — https://mininet.org/walkthrough/
3. POX Controller Wiki — https://noxrepo.github.io/pox-doc/html/
4. OpenFlow Specification v1.0 — https://opennetworking.org/software-defined-standards/specifications/
5. POX GitHub Repository — https://github.com/noxrepo/pox
6. Mininet GitHub Repository — https://github.com/mininet/mininet
