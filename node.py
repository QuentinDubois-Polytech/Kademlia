import argparse
import logging
import asyncio

from kademlia.network import Server

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

server = Server()

def parse_arguments():
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("-P", "--port", help="port number of the node", type=int, required=True)
    parser.add_argument("-i", "--bip", help="IP address of existing node", type=str, default="0.0.0.0")
    parser.add_argument("-p", "--bport", help="port number of existing node", type=int, default=None)

    return parser.parse_args()


def connect_to_bootstrap_node(bip, bport, port):
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.listen(port))
    bootstrap_node = (bip, int(bport))
    loop.run_until_complete(server.bootstrap([bootstrap_node]))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def create_bootstrap_node(port):
    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.run_until_complete(server.listen(port))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        loop.close()


def main():
    args = parse_arguments()

    if args.bip and args.bport:
        connect_to_bootstrap_node(args.bip, args.bport, args.port)
    else:
        create_bootstrap_node(args.port)


if __name__ == "__main__":
    main()
