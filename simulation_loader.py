from typing import Dict, List, Union
import json

WalkerParameters = Dict[str, Union[int, float]]
WalkerConfiguration = Dict[str, Dict[str, Union[int, WalkerParameters]]]
BarrierConfiguration = Dict[str, Dict[str, int]]
PortalGateConfiguration = Dict[str, Dict[str, int]]
SimulationConfiguration = Dict[str, Union[int, WalkerConfiguration, BarrierConfiguration, PortalGateConfiguration]]


def load_from_json(filename: str) -> SimulationConfiguration:
    """
    This function opens a JSON file and loads its content.
    :param filename: path to the json file.
    :return: A dictionary containing the content of the JSON file.
    """
    with open(filename, 'r') as json_file:
        simulation_config: SimulationConfiguration = json.load(json_file)
    # now simulation_config is a dictionary equivalent to the JSON file
    return simulation_config
