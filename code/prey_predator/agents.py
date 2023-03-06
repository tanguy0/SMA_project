from mesa import Agent
from prey_predator.random_walk import RandomWalker


class Sheep(RandomWalker):
    """
    A sheep that walks around, reproduces (asexually) and gets eaten.

    The init is the same as the RandomWalker.
    """

    def __init__(self, unique_id, pos, moore, energy, model):
        super().__init__(unique_id, pos, model, moore=moore)
        self.pos = pos
        self.energy = energy

    def eat_grass(self):
        """
        If there is grass on the patch and the sheep is not at 100% energy, it eats the patch.
        """
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

    def reproduce(self):
        """
        If the sheep has enough energy, it reproduces
        """
        if self.energy > 0:
            # Get current number of sheep
            number_of_sheep = self.datacollector.get_model_vars_dataframe()['Sheep']
            # Define unique_id 
            unique_id = number_of_sheep + 1
            # Randomly choose an initial position
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            pos = (x, y)
            # Initialiaze the agent
            sheep = Sheep(unique_id, pos, self)
            self.schedule.add(sheep)
            # Add the agent to his grid cell
            self.grid.place_agent(sheep, (x, y))

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        # Move
        self.random_move()
        # Eat grass
        #self.eat_grass()
        # Reproduce
        #self.reproduce()
        


class Wolf(RandomWalker):
    """
    A wolf that walks around, reproduces (asexually) and eats sheep.
    """

    energy = None

    def __init__(self, unique_id, pos, model, moore, energy=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.energy = energy

    def step(self):
        self.random_move()
        # ... to be completed


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by sheep
    """

    def __init__(self, unique_id, pos, fully_grown, countdown, model):
        """
        Creates a new patch of grass

        Args:
            fully_grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.pos = pos
        self.countdown = countdown

    def step(self):
        if self.fully_grown == 0:
            if self.countdown > 0:
                self.countdown -= 1
            else :
                self.fully_grown = 1