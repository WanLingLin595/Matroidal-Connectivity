# Matroidal-Connectivity
BCube DCNs

The .py files above are the simulation source codes for the paper "Link/Switch Failure Analysis of Data Center Networks on Matroidal Connectivity".

LBCube.py defines the logic graph of BCube (see Definition 2). 

BCube.py constructs the physical structure of BCube DCNs (see Definition 1).

Algorithm1.py is designed to verify whether a given faulty edge set is a minimum edge cut to meet the conditional matroidal connectivity.

LFR.py and SFR.py aim to measure the range of link and switch failures in different matroidal constraint situations \mathcal{B}_m, respectively (see Section V-A).

Next, we assess the performance of BCube networks under matroidal constraints, employing metrics such as aggregated bottleneck throughput (ABT for short), average path length (APL for short), and routing failure rate (RFR for short) (see Section V-B). 

(1) Performance_analysis_wires.py (resp. Performance_analysis_switch.py) aims to measure ABT, APL, and RFR of BCube in the occurrence of link failures (resp. switch failures);

(2) 
