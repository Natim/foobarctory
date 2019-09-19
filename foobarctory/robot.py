import asyncio
from enum import Enum
import random
from uuid import uuid4


# Robot config
class TaskType(Enum):
    MOVE = "move"
    MINE = "mine"
    ASSEMBLE = "assemble"
    SELL = "sell"
    BUY = "buy"


class MinerType(Enum):
    FOO = "foo"
    BAR = "bar"


class Robot:
    def __init__(self, factory, number, miner_type=None):
        """Create a robot.

        factory: The global factory store.
        number: Robot number
        miner_type: The thing the robot is mining.
        """
        self.factory = factory
        self.number = number

        if miner_type is None:
            miner_type = random.choice(
                [candidate.value for candidate in list(MinerType)]
            )
        self.miner_task = MinerType(miner_type)

    def say(self, message):
        print(f"Robot {self.number}: {message}")
        
    async def run_once(self):
        task = random.choice([t.value for t in list(TaskType)])
        self.say(f"Starting {task}")
        if not hasattr(self, task):
            raise NotImplementedError("Task {task} is unkown for this robot.")
        task_function = getattr(self, task)
        await task_function()

    async def wait(self, seconds):
        await asyncio.sleep(seconds / self.factory.time_speeder)
    
    async def move(self):
        """Switch miner type, takes 5 seconds."""
        await self.wait(5)
        previous_task = self.miner_task
        self.miner_task = random.choice(
            [candidate for candidate in list(MinerType) if candidate != self.miner_task]
        )
        self.say(f"Moved from task {previous_task} to task {self.miner_task}")

    async def mine(self):
        """Mine a thing."""
        if self.miner_task == MinerType.FOO:
            # Mine FOO objects
            await self.wait(1)
            new_foo = {"uuid": f"{uuid4()}"}
            self.say(f"Mining FOO: {new_foo}")
            self.factory.foo.append(new_foo)
        elif self.miner_task == MinerType.BAR:
            # Mine BAR objects
            await self.wait(random.randrange(1, 4) / 2)
            new_bar = {"uuid": f"{uuid4()}"}
            self.say(f"Mining BAR: {new_bar}")
            self.factory.bar.append(new_bar)
        else:
            raise NotImplementedError("The robot doesn't know how to mine {self.miner_task.value} things.")

    async def assemble(self):
        """Assemble a foo and a bar."""
        if not len(self.factory.foo) > 0 or not len(self.factory.bar) > 0:
            # We don't have enough things to assemble
            self.say("Not enough ressource to assemble")
            return
        
        foo = self.factory.get_foo()  # In case they are no 
        bar = self.factory.get_bar()

        await self.wait(2)  # It takes 2 seconds to assemble

        if random.randint(0, 9) < 6:
            # 60 % of the time it is a success
            new_foobar= {"foo": foo, "bar": bar}
            self.say(f"Assembling FOOBAR: {new_foobar}")
            self.factory.foobar.append(new_foobar)
        else:
            self.say(f"Assembling failed, keeping {bar}, dropping {foo}")
            # The rest of the time we can reuse the bar
            self.factory.bar.append(bar)

    async def sell(self):
        """Selling between 1 and 5 foobar."""
        if len(self.factory.foobar) > 0:
            how_many = min(len(self.factory.foobar), random.randint(1, 5))
            foobars = [self.factory.get_foobar() for x in range(how_many)]
            await self.wait(10)
            for foobar in foobars:
                self.say(f"Selling {foobar} for 1€")
                self.factory.money += 1
        else:
            self.say("Nothing to sell")

    async def buy(self):
        """Buying a robot"""
        if len(self.factory.foo) >= 6 and self.factory.money > 3:
            self.factory.money -= 3
            foos = [self.factory.get_foo() for x in range(6)]
            self.say(f"Buying a new robot spending 3€ and the following foo objects: {foos}")
            self.factory.add_new_robot()
        else:
            self.say("Not enough ressource to buy")
