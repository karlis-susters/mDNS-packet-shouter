import socket
from time import sleep

def get_local_ip_addr():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_hostname():
    return socket.gethostname()
    
def get_message_bytes(hostname, ip_addr):
    ip_parts = ip_addr.split(".")
    ip_hex_str = "".join(map( #Convert the IP address to 4 hex bytes
        (lambda x: hex(int(x))[2:]), 
        ip_parts))
    hostname_hex_str = "".join(map( #Convert the hostname to hex bytes
        (lambda x: hex(ord(x))[2:]),
        hostname))
    hostname_len_hex = hex(len(hostname))[2:] #Convert the length of the hostname to one hex byte
    return bytearray.fromhex("000084000000000100000000" +
        hostname_len_hex.rjust(2, '0') +  #Pad the length with zeros
        hostname_hex_str +
        "056c6f63616c0000018001" +   #add ".local" and more 
        "00000e10" +   # TTL in seconds, currently set to 3600 (1 hour)
        "0004" +   #length of the remaining data (4)
        ip_hex_str)


#Original bytes: "000084000000000100000000056176656e65056c6f63616c000001800100000e100004ac1cc0f4" 
if __name__=="__main__":
    num_packets_sent = 50
    packet_interval = 0.2
    serverAddressPort   = ("224.0.0.251", 5353) #mDNS multicast address and port
    bytesToSend = get_message_bytes(get_hostname(), get_local_ip_addr())
    udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udp_socket.bind(('', 5353)) # Set sending port. For this to work can't have avahi running
    for i in range(num_packets_sent):
        udp_socket.sendto(bytesToSend, serverAddressPort)
        sleep(packet_interval)
