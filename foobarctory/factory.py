import asyncio
import logging

from .robot import Robot

logger = logging.getLogger("foobarctory")

MAX_ROBOTS = 30


class Factory:
    def __init__(
        self, *, loop=None, initial_number_of_robots=2, time_speeder=1, initial_money=0
    ):
        """Create a factory.

        time_speeder = How much faster does a second elapse.
        """
        self.robots = []
        self.foo = []
        self.bar = []
        self.foobar = []
        self.money = initial_money

        if loop is None:
            loop = asyncio.get_event_loop()

        self.loop = loop
        self.running = True
        self.initial_number_of_robots = initial_number_of_robots
        self.time_speeder = time_speeder

    async def run_factory(self):
        print(f"Factory creating {self.initial_number_of_robots} robots")
        for number in range(self.initial_number_of_robots):
            self.add_new_robot()

        self.loop.create_task(self.show_factory_stats())

    async def run_robot(self, robot):
        while True:
            if len(self.robots) >= MAX_ROBOTS:
                # Stop as soon as we reach 30 robots
                if self.running:
                    print(f"\n We've reach {MAX_ROBOTS} robots, gathering robots. \n\n")
                    self.running = False
                    self.loop.stop()
                return

            if self.running:
                # If the factory is still running, we can ask one more
                # task at our robot
                try:
                    await robot.run_once()
                except Exception:
                    logger.exception("Robot died")
                    pass

    def add_new_robot(self):
        new_robot = Robot(self, len(self.robots) + 1)
        print(f"--------------- NEW ROBOT HIRED: {new_robot} ------------------------")
        self.robots.append(new_robot)
        self.loop.create_task(self.run_robot(new_robot))
        self.print_factory_stats()

    def get_foo(self):
        return self.foo.pop()

    def get_bar(self):
        return self.bar.pop()

    def get_foobar(self):
        return self.foobar.pop()

    def print_factory_stats(self):
        print(
            f"""
+------------------------
| FACTORY STATS
|   - FOO: {len(self.foo)} objects
|   - BAR: {len(self.bar)} objects
|   - FOOBAR : {len(self.foobar)} objects
|   - MONEY : {self.money} euros
|   - ROBOTS : {len(self.robots)} robots running
+------------------------
"""
        )

    async def show_factory_stats(self):
        while True:
            self.print_factory_stats()
            await asyncio.sleep(2)
