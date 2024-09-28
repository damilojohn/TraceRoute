# import socket
# import os
# import struct
# import time

# ICMP_ECHO_REQUEST = 8  # ICMP Echo Request type
# ICMP_ECHO_REPLY = 0    # ICMP Echo Reply type

# # Function to create a raw ICMP socket
# def create_raw_socket():
#     try:
#         # Create a raw socket using the ICMP protocol
#         sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
#         sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, 2)
#         sock.settimeout(30)  # Set timeout for socket to 5 seconds
#         return sock
#     except PermissionError:
#         print("You need to run this script with administrative privileges.")
#         exit(1)

# # Function to create an ICMP Echo Request packet
# def create_icmp_packet(packet_id):
#     # ICMP Header: Type (8), Code (0), Checksum (0), ID, Sequence
#     icmp_header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, packet_id, 1)
#     data = struct.pack('d', time.time())  # Payload: Current time
#     # Add a checksum of 0 for simplicity
#     return icmp_header + data

# # Function to send an ICMP Echo Request (ping)
# def send_icmp_request(sock, target_ip):
#     packet_id = os.getpid() & 0xFFFF  # Use process ID for ICMP packet ID
#     packet = create_icmp_packet(packet_id)
#     sock.sendto(packet, (target_ip, 33454))  # Send the ICMP packet to the target IP
#     print(f"Sent ICMP Echo Request to {target_ip}")

# # Function to receive ICMP responses
# def receive_icmp_response(sock):
#     try:
#         # Receive the packet and address of the sender
#         packet, addr = sock.recv(1024)
#         icmp_header = packet[20:28]  # Extract ICMP header (skipping IP header)
#         type, code, checksum, packet_id, sequence = struct.unpack('bbHHh', icmp_header)

#         if type == ICMP_ECHO_REPLY:
#             print(f"Received ICMP Echo Reply from {addr[0]}")
#         else:
#             print(f"Received ICMP message type {type} from {addr[0]}")
#     except socket.timeout:
#         print("Request timed out.")

# if __name__ == "__main__":
#     target_ip = "8.8.8.8"  # Google's public DNS for testing

#     # Create the raw socket
#     sock = create_raw_socket()

#     # Send ICMP Echo Request
#     send_icmp_request(sock, target_ip)

#     # Wait for the ICMP response (or timeout)
#     receive_icmp_response(sock)

# import socket
# import struct


# class IcmpPacketSender:
#     def __init__(self, target_ip, port=33434, data=None, ttl=3, icmp_id = 12345):
#         self.target_ip = target_ip
#         self.port = port
#         self.data = data
#         self.ttl = ttl
#         self.icmp_id = icmp_id

#     def send_icmp_packet(self):
#         icmp_type = 8
#         icmp_code = 0
#         icmp_checksum = 0
#         icmp_sequence = 1

#         if self.data:
#             icmp_payload = self.data.encode()
#         else:
#             icmp_payload = b'hellooooo'

#         icmp_header = struct.pack("!bbHHH", icmp_type, icmp_code, 
#                                   icmp_checksum, self.icmp_id, icmp_sequence)

#         icmp_checksum = self.calculate_checksum(icmp_header + icmp_payload)

#         icmp_header = struct.pack("!bbHHH", icmp_type, icmp_code,
#                                   socket.htons(icmp_checksum), self.icmp_id, 
#                                   icmp_sequence)

#         icmp_packet = icmp_header + icmp_payload

#         with socket.socket(socket.AF_INET, socket.SOCK_RAW,
#                            socket. IPPROTO_ICMP) as sock:
#             sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL,
#                             struct.pack("I", self.ttl))
#             sock.settimeout(20)
#             msg = ''
#             try:
#                 if self.port:
#                     target_ip = socket.getaddrinfo(self.target_ip)
#                     sock.sendto(icmp_packet, (target_ip[0][4][0], self.port))
#                 else:
#                     sock.sendto(icmp_packet, (self.target_ip, 33434))
#                 msg = sock.recv(1024)
#             except Exception as e:
#                 print(f"failed with exception {e}")
#             if msg:
#                 print("icmp successfully received....")
#                 print(msg)
 

#     def calculate_checksum(self, data):
#         checksum = 0

#         if len(data) % 2 != 0:
#             data += b"\x00"
#         for i in range(0, len(data), 2):
#             checksum += (data[i] << 8) + data[i+1]
        
#         checksum = (checksum >> 16) + (checksum & 0xffff)
#         checksum += checksum >> 16

#         return (~checksum) & 0xffff

# import socket
# import struct
# import select

# class IcmpPacketSender:
#     def __init__(self, target_ip, port=33434, data=None, ttl=3, icmp_id = 12345):
#         self.target_ip = target_ip
#         self.port = port
#         self.data = data
#         self.ttl = ttl
#         self.icmp_id = icmp_id

#     def send_icmp_packet(self):
#         icmp_type = 8
#         icmp_code = 0
#         icmp_checksum = 0
#         icmp_sequence = 1

#         if self.data:
#             icmp_payload = self.data.encode()
#         else:
#             icmp_payload = b'hellooooo'

#         icmp_header = struct.pack("!bbHHH", icmp_type, icmp_code, 
#                                   icmp_checksum, self.icmp_id, icmp_sequence)

#         icmp_checksum = self.calculate_checksum(icmp_header + icmp_payload)

#         icmp_header = struct.pack("!bbHHH", icmp_type, icmp_code,
#                                   socket.htons(icmp_checksum), self.icmp_id, 
#                                   icmp_sequence)

#         icmp_packet = icmp_header + icmp_payload

#         # Create a socket to send the ICMP request
#         with socket.socket(socket.AF_INET, socket.SOCK_RAW,
#                            socket.IPPROTO_ICMP) as sock:
#             sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL,
#                             struct.pack("I", self.ttl))
#             # sock.bind(('localhost', 33434))
#             sock.settimeout(20)
#             try:
#                 if self.port:
#                     target_ip = socket.getaddrinfo(self.target_ip)
#                     sock.sendto(icmp_packet, (target_ip[0][4][0], self.port))
#                 else:
#                     sock.sendto(icmp_packet, (self.target_ip, 33434))
#             except Exception as e:
#                 print(f"failed with exception {e}")

#         # Create a socket to listen for ICMP responses
#         with socket.socket(socket.AF_INET, socket.SOCK_RAW,
#                            socket.IPPROTO_ICMP) as icmp_sock:
#             # icmp_sock.settimeout(20)
#             # icmp_sock.bind(('localhost',33434))
#             try:
#                 msg = icmp_sock.recv(1024)
#                 if msg:
#                     print("icmp successfully received....")
#                     print(msg)
#             except Exception as e:
#                 print(f"failed to receive icmp response with exception {e}")

#     def calculate_checksum(self, data):
#         checksum = 0

#         if len(data) % 2 != 0:
#             data += b"\x00"
#         for i in range(0, len(data), 2):
#             checksum += (data[i] << 8) + data[i+1]
        
#         checksum = (checksum >> 16) + (checksum & 0xffff)
#         checksum += checksum >> 16

#         return (~checksum) & 0xffff


# def main():
#     target_ip = input("Enter target IP:")
#     port = int(input("Enter port (optional, press Enter to skip): ") or 0)
#     data = input("Enter data (optional, press Enter to use default): ")
#     ttl = int(input("Enter TTL (optional, press Enter to use default): ") or 64)
#     icmp_id = int(input("Enter ICMP ID (optional, press Enter to use default): ") or 12345)
#     # target_ip = socket.getaddrinfo('www.google.com',80)
#     # print(target_ip)
#     icmp_packet_sender = IcmpPacketSender(target_ip, port, data, ttl, icmp_id)
#     icmp_packet_sender.send_icmp_packet()

import socket
import struct
import select

class IcmpPacketSender:
    def __init__(self, target_ip, port=33434, data=None, ttl=3, icmp_id = 12345):
        self.target_ip = target_ip
        self.port = port
        self.data = data
        self.ttl = ttl
        self.icmp_id = icmp_id

    def send_icmp_packet(self):
        icmp_type = 8
        icmp_code = 0
        icmp_checksum = 0
        icmp_sequence = 1

        if self.data:
            icmp_payload = self.data.encode()
        else:
            icmp_payload = b'hellooooo'

        icmp_header = struct.pack("!bbHHH", icmp_type, icmp_code, 
                                  icmp_checksum, self.icmp_id, icmp_sequence)

        icmp_checksum = self.calculate_checksum(icmp_header + icmp_payload)

        icmp_header = struct.pack("!bbHHH", icmp_type, icmp_code,
                                  socket.htons(icmp_checksum), self.icmp_id, 
                                  icmp_sequence)

        icmp_packet = icmp_header + icmp_payload

        # Create a socket to send the ICMP packet
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.IPPROTO_ICMP)
        send_sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL,
                             struct.pack("I", self.ttl))

        # Create a socket to listen for ICMP packets
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,
                                  socket.IPPROTO_ICMP)
        recv_sock.bind(("", 0))

        try:
            send_sock.sendto(icmp_packet, (self.target_ip, self.port))
            # Wait for an ICMP response
            readable, writable, errored = select.select([recv_sock], [], [], 20)
            if readable:
                # Receive the ICMP response
                data, addr = recv_sock.recvfrom(1024)
                print("icmp successfully received....")
                print(data)
            else:
                print("Timeout")
        except Exception as e:
            print(f"failed with exception {e}")
        finally:
            send_sock.close()
            recv_sock.close()

    def calculate_checksum(self, data):
        checksum = 0

        if len(data) % 2 != 0:
            data += b"\x00"
        for i in range(0, len(data), 2):
            checksum += (data[i] << 8) + data[i+1]
        
        checksum = (checksum >> 16) + (checksum & 0xffff)
        checksum += checksum >> 16

        return (~checksum) & 0xffff


def main():
    target_ip = input("Enter target IP:")
    port = int(input("Enter port (optional, press Enter to skip): ") or 0)
    data = input("Enter data (optional, press Enter to use default): ")
    ttl = int(input("Enter TTL (optional, press Enter to use default): ") or 64)
    icmp_id = int(input("Enter ICMP ID (optional, press Enter to use default): ") or 12345)
    # target_ip = socket.getaddrinfo('www.google.com',80)
    # print(target_ip)
    icmp_packet_sender = IcmpPacketSender(target_ip, port, data, ttl, icmp_id)
    icmp_packet_sender.send_icmp_packet()


if __name__ == "__main__":
    main()