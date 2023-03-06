from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from prey_predator.agents import Wolf, Sheep, GrassPatch
from prey_predator.model import WolfSheep


def wolf_sheep_portrayal(agent):
    if agent is None:
        return

    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if type(agent) is Sheep:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.5

    elif type(agent) is Wolf:
        portrayal["Color"] = "ref"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.8

    elif type(agent) is GrassPatch:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        if agent.fully_grown == True:
            portrayal["r"] = 1
        else:
            portrayal["r"] = 0

    return portrayal


canvas_element = CanvasGrid(wolf_sheep_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Wolves", "Color": "#AA0000"}, {"Label": "Sheep", "Color": "#666666"}],
    data_collector_name='datacollector'
)

model_params = {
    'height': 20,
    'width': 20,
    'initial_sheep': 100,
    'initial_wolves': 50,
    'sheep_reproduce': 0.04,
    'wolf_reproduce': 0.05,
    'wolf_gain_from_food': 20,
    'grass': False,
    'grass_regrowth_time': 5,
    'sheep_gain_from_food': 4,
    'wolf_loss_from_movement': 10,
    'sheep_loss_from_movement': 2
    }

server = ModularServer(
    WolfSheep, [canvas_element, chart_element], "Prey Predator Model", model_params
)
server.port = 8521
