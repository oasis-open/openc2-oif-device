import json
import os
from kestrel.session import Session

# Ref
# https://kestrel.readthedocs.io/en/stable/source/kestrel.session.html

working_directory = os.getcwd()
huntflow_file = working_directory + '/hunts/huntflow/find_data_via_stixshifter.hf'
default_get_cmd = "process"
default_from_cmd = "stixshifter://bh22-linux"
default_where_cmd = "name = 'bash' AND pid LIKE '13333'"
default_start_cmd = "2022-07-01T00:00:00Z"
default_stop_cmd = "2022-08-01T00:00:00Z"

# huntflow = """results = GET process
# FROM stixshifter://bh22-linux
# WHERE [process:name = 'cmd.exe']"""

def hunt_via_variables(is_sample: bool = True, 
                       get_cmd: str = None, 
                       from_cmd: str = None, 
                       where_cmd: str = None,
                       start_cmd: str = None,
                       stop_cmd: str = None):
    
    if get_cmd is None:
        get_cmd = default_get_cmd

    if from_cmd is None:
        from_cmd = default_from_cmd

    if where_cmd is None:
        where_cmd = default_where_cmd            

    return_data = {}
    return_sample_data = {}

    if start_cmd and stop_cmd:
        hunt = f"results = GET {get_cmd} FROM {from_cmd} WHERE {where_cmd} START {start_cmd} STOP {stop_cmd}"
    else:
        hunt = f"results = GET {get_cmd} FROM {from_cmd} WHERE {where_cmd}"

    # hunt = """results = GET process
    #              FROM stixshifter://bh22-linux
    #              WHERE name = 'bash' AND pid LIKE '13333'
    #	          START 2022-07-01T00:00:00Z STOP 2022-08-01T00:00:00Z
    #       """

    with Session() as session:
        session.execute(hunt)
        return_data = session.get_variable("results")
    for data_item in return_data:
        # return_sample_data = json.dumps(data_item, indent=4)
        return_sample_data = data_item
        print(return_sample_data) 
        break

    if is_sample:
        return_data = return_sample_data

    return return_data


if __name__ == '__main__':
    hunt_data = hunt_via_variables(True)