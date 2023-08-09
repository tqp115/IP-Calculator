import argparse

parser = argparse.ArgumentParser(description = "Determine subnet info using IP address and subnet mask in CIDR notation.")
parser.add_argument("-i", "--ipaddress", dest = "ipAddress", metavar = "IPADDRESS", required = True, help = "Enter an IPv4 address.")
parser.add_argument("-s", "--subnet", dest = "subnet", metavar = "SUBNET", required = True, help = "Enter subnet mask in CIDR notation (ex. /2 or 2).")
args = parser.parse_args()

ipAddress = args.ipAddress
subnet = int(args.subnet.replace("/", ""))

def networkMask(cidr):
    mask = ""
    for i in range(4):
        if cidr > 7:
            mask += "255."
        else:
            lastOctet = 255 - (2 ** (8 - cidr) - 1)
            mask += str(lastOctet) + "."
        cidr -= 8
        if cidr < 0:
            cidr = 0

    return mask[:-1]

def dec2bin(ip_address):
    binary_ip = "".join([bin(int(octet))[2:].zfill(8) for octet in ip_address.split('.')])
    return(binary_ip)

def networkAddress():
    binaryIP = dec2bin(ipAddress)
    binarySubnet = dec2bin(networkMask(subnet))
    andOperation = ""
    for i in range(32):
        if int(binaryIP[i]) and int(binarySubnet[i]):
            andOperation += "1"
        else:
            andOperation += "0"
    #print(".".join(andOperation[i:i + 8] for i in range(0, len(andOperation), 8)))
    octet1 = andOperation[0:8]
    octet2 = andOperation[8:16]
    octet3 = andOperation[16:24]
    octet4 = andOperation[24:32]
    decOctet1 = str(int(octet1, 2))
    decOctet2 = str(int(octet2, 2))
    decOctet3 = str(int(octet3, 2))
    decOctet4 = str(int(octet4, 2))
    #print(".".join([decOctet1, decOctet2, decOctet3, decOctet4]))
    return ".".join([decOctet1, decOctet2, decOctet3, decOctet4])

def broadcastAddress():
    binaryIP = dec2bin(ipAddress)
    binarySubnet = dec2bin(networkMask(subnet))
    inverseBinarySubnet = ""
    orOperation = ""
    for i in range(len(binarySubnet)):
        if binarySubnet[i] == "1":
            inverseBinarySubnet += "0"
        else:
            inverseBinarySubnet += "1"
    for i in range(32):
        if int(binaryIP[i]) or int(inverseBinarySubnet[i]):
            orOperation += "1"
        else:
            orOperation += "0"
    #print(".".join(orOperation[i:i + 8] for i in range(0, len(orOperation), 8)))
    octet1 = orOperation[0:8]
    octet2 = orOperation[8:16]
    octet3 = orOperation[16:24]
    octet4 = orOperation[24:32]
    decOctet1 = str(int(octet1, 2))
    decOctet2 = str(int(octet2, 2))
    decOctet3 = str(int(octet3, 2))
    decOctet4 = str(int(octet4, 2))
    return ".".join([decOctet1, decOctet2, decOctet3, decOctet4])   
            
def usableHosts():
    hostBits = 32 - subnet
    return 2 ** hostBits - 2

def rangeOfIPs():
    lastNumNetwork = int(networkAddress()[-1])
    newNumNetwork = str(lastNumNetwork + 1)
    lastNumBroadcast = int(broadcastAddress()[-1])
    newNumBroadcast = str(lastNumBroadcast - 1)
    lower = networkAddress()[:-1] + newNumNetwork
    upper = broadcastAddress()[:-1] + newNumBroadcast
    return f"{lower} - {upper}"
    
def classOfIP():
    firstOctet = int(ipAddress.partition(".")[0])
    if firstOctet <= 127:
        return "A"
    elif firstOctet >= 128 and firstOctet <= 191:
        return "B"
    elif firstOctet >= 192 and firstOctet <= 223:
        return "C"
    elif firstOctet >= 224 and firstOctet <= 239:
        return "D"
    else:
        return "E"

def main():
    #userInput = input("Enter an IPv4 address and subnet in CIDR notation: ")
    print(f"Network Mask: {networkMask(subnet)}")
    print(f"Range of IP Addresses: {rangeOfIPs()}")
    print(f"Network Address: {networkAddress()}")
    print(f"Broadcast Address: {broadcastAddress()}")
    print(f"Number of Usable Hosts: {usableHosts()}")
    print(f"Class of IP Address: {classOfIP()}")

if __name__ == "__main__":
    main()