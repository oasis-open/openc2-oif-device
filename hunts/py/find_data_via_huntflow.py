# import json
import os
from kestrel.session import Session

# Ref
# https://kestrel.readthedocs.io/en/stable/source/kestrel.session.html

# working_directory = os.getcwd()
# huntflow_file = working_directory + '/hunts/huntflow/find_data_via_stixshifter.hf'
# default_get_cmd = "process"
# default_from_cmd = "stixshifter://bh22-linux"
# default_where_cmd = "name = 'bash' AND pid LIKE '13333'"
# default_start_cmd = "2022-07-01T00:00:00Z"
# default_stop_cmd = "2022-08-01T00:00:00Z"

# # huntflow = """results = GET process
# # FROM stixshifter://bh22-linux
# # WHERE [process:name = 'cmd.exe']"""

def hunt_via_file(huntflow_file: str, get_var: str = "results"):

    with Session() as session:
        with open(huntflow_file) as hff:
            huntflow = hff.read()
        session.execute(huntflow)
        return_data = session.get_variable(get_var)

        return_sample_data = {}
        for data_item in return_data:
            # return_sample_data = json.dumps(data_item, indent=4)
            return_sample_data = data_item
            print(return_sample_data) 
            break

    return return_sample_data


if __name__ == '__main__':

    working_directory = os.getcwd()
    # huntflow_file = working_directory + '/hunts/huntflow/query_local_stixdata.hf'
    huntflow_file = working_directory + '/hunts/huntflow/query_data_via_stixshifter.hf'

    hunt_data = hunt_via_file(huntflow_file)