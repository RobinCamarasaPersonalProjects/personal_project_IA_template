import os
from general_tools import *


def path_dictionnary(json_path='../../config/paths.json'):
    # Create a dictionnary contating all the project paths
    tmp_path_dictionnary = json_to_dictionnary(json_path)
    final_path_dictionnary = {}
    project_path = tmp_path_dictionnary['project']
    for key in tmp_path_dictionnary:
        if key != 'project':
            final_path_dictionnary[key] = os.path.join(project_path, tmp_path_dictionnary[key])
    return final_path_dictionnary


def new_experiment_files_update(experiment_name):
    # Update config and dashboard files
    paths = path_dictionnary()
    json_config_path = paths[experiment_name + '_config']
    csv_dashboard_path = paths[experiment_name + '_dashboard']
    dictionnary = json_to_dictionnary(json_config_path)
    dictionnary['id'] += 1
    save_json(dictionnary, json_config_path)
    csv_update(dictionnary, csv_dashboard_path)
