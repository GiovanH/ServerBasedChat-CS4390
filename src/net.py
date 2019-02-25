from Codes import Code
import byteutil
import traceback
import socket
# import timeout_decorator


def newUDPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def newTCPSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def reprTCPSocket(sock):
    closed = getattr(sock, '_closed', False)
    return "<{}{} --> {}>".format(
        "[closed] " if closed else "",
        sock.getsockname(),
        sock.getpeername()
    )


def getOwnIP():
    for addrinfo in socket.getaddrinfo(socket.gethostname(), 0):
        family, __, __, __, address = addrinfo
        if family == socket.AddressFamily.AF_INET:
            return address[0]


def sendUDP(sock, message, dest_address):
    print("┌ Sending UDP message to server")
    print("│ Server: {}:{}".format(*dest_address))
    print("│ ┌Message (bytes): '{}'".format(message))
    print("└ └Message (print): {}".format(byteutil.formatBytesMessage(message)))

    try:
        sock.sendto(message, dest_address)
    except Exception as e:
        if e.errno == 10051:  # Winerror 10051: unreachable network
            traceback.print_exc(limit=0)
        else:
            raise


def sendTCP(sock, message):
    print("┌ Sending TCP message via socket", reprTCPSocket(sock))
    print("│ ┌Message (bytes): '{}'".format(message))
    print("└ └Message (print): {}".format(byteutil.formatBytesMessage(message)))

    try:
        sock.sendall(message)
    except Exception as e:
        if e.errno == 10051:  # Winerror 10051: unreachable network
            traceback.print_exc(limit=0)
        else:
            raise

# @timeout_decorator.timeout(10, use_signals=False)


def awaitUDP(sock, size):
    sock.settimeout(SOCK_TIMEOUT)
    return sock.recvfrom(size)


# @timeout_decorator.timeout(10, use_signals=False)
def awaitTCP(sock, size):
    sock.settimeout(SOCK_TIMEOUT)
    return sock.recv(size)


SERVER_IP = getOwnIP()  # "192.168.1.1"
SERVER_UDP_PORT = 64
CLIENT_UDP_PORT = 65
SERVER_TCP_PORT = 66
SOCK_TIMEOUT = 1
