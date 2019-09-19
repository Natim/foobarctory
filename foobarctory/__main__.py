import asyncio
import argparse
import random

from .factory import Factory

def main():
    parser = argparse.ArgumentParser(description="Start the factory")
    parser.add_argument("--time-speeder", type=int, default=1,
                        help="Run the factory faster by settings the number of times "
                        "you can fit a factory seconds in an actual seconds."
    )
    parser.add_argument("--nb-robots", type=int, default=2,
                        help="Initial number of robots"
    )
    parser.add_argument("--money", type=int, default=0,
                        help="Initial factory money"
    )
    args = parser.parse_args()
    random.seed()
    loop = asyncio.get_event_loop()

    factory = Factory(loop=loop,
                      initial_number_of_robots=args.nb_robots,
                      time_speeder=args.time_speeder,
                      initial_money=args.money,
    )
    loop.create_task(factory.run_factory())
    loop.run_forever()
    print("Bye bye!")
