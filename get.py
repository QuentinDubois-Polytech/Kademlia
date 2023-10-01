import logging
import asyncio
import random
import argparse

from kademlia.network import Server

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--bip", help="IP address of existing node", type=str, default="0.0.0.0")
    parser.add_argument("-p", "--bport", help="port number of existing node", type=int, default=None)
    parser.add_argument("-k", "--key", help="key to find", type=str, required=True)

    return parser.parse_args()

async def run(bip, bport, key):
    server = Server()

    while True:
        try :
            start_port = 5000
            end_port = 65535
            port = random.randint(start_port, end_port)
            await server.listen(port)
            break
        except:
            pass

    bootstrap_node = (bip, int(bport))
    await server.bootstrap([bootstrap_node])

    result = await server.get(key)

    if not result:
        print("Key not found !")
    else :
        print(f"Key found ! -> {key} = {result}")
    server.stop()


def main():
    args = parse_arguments()
    asyncio.run(run(args.bip, args.bport, args.key))

if __name__ == "__main__":
    main()