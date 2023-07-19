import json
import os
from jinja2 import Environment, FileSystemLoader
from kestrel.session import Session

# References: 
# https://realpython.com/primer-on-jinja-templating/
# https://jinja.palletsprojects.com/en/3.1.x/

working_directory = os.getcwd()
huntflow_file = working_directory + '/hunts/huntflow/find_data_via_stixshifter.hf'
default_get_cmd = "process"
default_from_cmd = "stixshifter://bh22-linux"
default_where_cmd = "name = 'bash' AND pid LIKE '13333'"
default_start_cmd = "2022-07-01T00:00:00Z"
default_stop_cmd = "2022-08-01T00:00:00Z"

environment = Environment(loader=FileSystemLoader("hunts/jinja/"))
template = environment.get_template("kestrel_jinja_template.hf")


def hunt_jinja_via_variables(is_sample: bool = True, 
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

    hunt = template.render(
        get_cmd=get_cmd,
        from_cmd=from_cmd,
        where_cmd=where_cmd,
        start_cmd=start_cmd,
        stop_cmd=stop_cmd
    )

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
    hunt_data = hunt_jinja_via_variables(True)        