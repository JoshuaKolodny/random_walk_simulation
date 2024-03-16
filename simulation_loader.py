from typing import Dict, Union
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

    # Check if the loaded content is a dictionary
    if not isinstance(simulation_config, dict):
        print(f"Error: The file {filename} does not contain a valid JSON object.")
        return {}

    # Check if the dictionary contains the keys 'num_simulations' and 'num_steps'
    if 'num_simulations' not in simulation_config or 'num_steps' not in simulation_config:
        print(f"Error: The file {filename} does not contain 'num_simulations' and 'num_steps'.")
        return {}

    # Check if 'num_simulations' and 'num_steps' are positive integers
    if not isinstance(simulation_config['num_simulations'], int) or simulation_config['num_simulations'] <= 0:
        print("Error: 'num_simulations' must be a positive integer.")
        return {}

    if not isinstance(simulation_config['num_steps'], int) or simulation_config['num_steps'] <= 0:
        print("Error: 'num_steps' must be a positive integer.")
        return {}

    # Check if the dictionary contains the key 'walkers'
    if 'walkers' not in simulation_config:
        print(f"Error: The file {filename} does not contain 'walkers'.")
        return {}

    # Check if 'walkers' is a dictionary and contains at least one valid walker
    if not isinstance(simulation_config['walkers'], dict) or not simulation_config['walkers']:
        print("Error: 'walkers' must be a non-empty dictionary.")
        return {}

    # now simulation_config is a dictionary equivalent to the JSON file
    return simulation_config
