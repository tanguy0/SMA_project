"""
Prey-Predator Model
================================

Replication of the model found in NetLogo:
    Wilensky, U. (1997). NetLogo Wolf Sheep Predation model.
    http://ccl.northwestern.edu/netlogo/models/WolfSheepPredation.
    Center for Connected Learning and Computer-Based Modeling,
    Northwestern University, Evanston, IL.
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import random

from prey_predator.agents import Sheep, Wolf, GrassPatch
from prey_predator.schedule import RandomActivationByBreed


class WolfSheep(Model):
    """
    Wolf-Sheep Predation Model
    """

    description = (
        "A model for simulating wolf and sheep (predator-prey) ecosystem modelling."
    )

    def __init__(
            self, 
            height, 
            width, 
            initial_sheep, 
            initial_wolves, 
            sheep_reproduce, 
            wolf_reproduce, 
            wolf_gain_from_food, 
            grass, 
            grass_regrowth_time, 
            sheep_gain_from_food,
            wolf_loss_from_movement,
            sheep_loss_from_movement
            ):
        """
        Create a new Wolf-Sheep model with the given parameters.

        Args:
            initial_sheep: Number of sheep to start with
            initial_wolves: Number of wolves to start with
            sheep_reproduce: Probability of each sheep reproducing each step
            wolf_reproduce: Probability of each wolf reproducing each step
            wolf_gain_from_food: Energy a wolf gains from eating a sheep
            grass: Whether to have the sheep eat grass for energy
            grass_regrowth_time: How long it takes for a grass patch to regrow once it is eaten
            sheep_gain_from_food: Energy sheep gain from grass, if enabled.
            wolf_loss_from_movement: Energy wolf lose by moving.
            sheep_loss_from_movement: Energy sheep lose by moving.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_sheep = initial_sheep
        self.initial_wolves = initial_wolves
        self.sheep_reproduce = sheep_reproduce
        self.wolf_reproduce = wolf_reproduce
        self.wolf_gain_from_food = wolf_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.sheep_gain_from_food = sheep_gain_from_food
        self.wolf_loss_from_movement = wolf_loss_from_movement
        self.sheep_loss_from_movement = sheep_loss_from_movement

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_breed_count(Wolf),
                "Sheep": lambda m: m.schedule.get_breed_count(Sheep),
            }
        )

        # Create sheep:
        for i in range(self.initial_sheep):
            # Randomly choose an initial position
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            pos = (x, y)
            # Initialiaze the agent
            energy = self.sheep_gain_from_food
            moore = True
            sheep = Sheep(i, pos, energy, moore, self)
            self.schedule.add(sheep)
            # Add the agent to his grid cell
            self.grid.place_agent(sheep, (x, y))

        
        # Create wolves
        for i in range(self.initial_wolves):
            # Randomly choose an initial position
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            pos = (x, y)
            # Initialiaze the agent
            energy = self.wolf_gain_from_food
            moore = True
            wolf = Wolf(i, pos, energy, moore, self)
            self.schedule.add(wolf)
            # Add the agent to his grid cell
            self.grid.place_agent(wolf, (x, y))
        

        # Create grass patches
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                # Define position and unique id of the grass patch in (x, y)
                pos = (x, y)
                unique_id = y + x * self.grid.height
                # Iniziatize fully_grown randomly
                fully_grown = random.randint(0, 1)
                # Initialize countdown to 0 if fully_grown, randomly between 1 and grass_regrowth_time otherwise
                countdown = random.randint(1, grass_regrowth_time) * (1 - fully_grown)
                # Initialize grass patch
                grass_patch = GrassPatch(unique_id, pos, fully_grown, countdown, self)
                self.schedule.add(grass_patch)
                # Place this initial grass_patch in its position
                self.grid.place_agent(grass_patch, (x, y))

    def step(self):
        self.schedule.step()

        # Collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        for i in range(step_count):
            self.step()