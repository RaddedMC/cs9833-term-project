# cs9833-term-project
## James N. and Brodey M.

A probablistic few-shot learning method to detect compromised IoT devices within a local network.

## Dataset

### Download
We used the CICIoT2023 dataset
https://www.unb.ca/cic/datasets/iotdataset-2023.html

- Direct download (full .PCAP, 243.5 GB)
    - https://cicresearch.ca/IOTDataset/CIC_IOT_Dataset2023/download.php?file=PCAP%2FPCAP.zip
    - Unzip and place this in `/.data/PCAP/`
    - Don't make the mistake we did. Don't download this.

- Direct download (full .CSV, 1.43 GB)
    - https://cicresearch.ca/IOTDataset/CIC_IOT_Dataset2023/download.php?file=CSV%2FCSV.zip
    - Unzip and place this in `/.data/CSV/`

- Direct download (merged .CSV, 1.6 GB)
    - All attack types are contained within one file
    - https://cicresearch.ca/IOTDataset/CIC_IOT_Dataset2023/download.php?file=CSV%2FMERGED_CSV.zip
    - Unzip and place this in `/.data/MERGED_CSV/`
    - Features:
        - Header_Length, Protocol type, Time_To_Live, Rate, fin_flag_number, syn_flag_number, rst_flag_number, psh_flag_number, ack_flag_number, ece_flag_number, cwr_flag_number, ack_count, syn_count, fin_count, rst_count, HTTP, HTTPS, DNS, Telnet, SMTP, SSH, IRC, TCP, UDP, DHCP, ARP, ICMP, IPv, LLC, Tot_sum, Min, Max, AVG, Std, Tot_size, IAT, Number, Variance, Label

- Example Jupyter notebook
https://cicresearch.ca/IOTDataset/CIC_IOT_Dataset2023/download.php?file=example%2Fexample.ipynb