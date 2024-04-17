import toml
from jinja2 import Environment, FileSystemLoader
from kestrel.session import Session

# References: 
# https://realpython.com/primer-on-jinja-templating/
# https://jinja.palletsprojects.com/en/3.1.x/


default_get_cmd = "process"
default_from_cmd = "file://./data/test_stixbundle.json"
default_where_cmd = "[process:name='compattelrunner.exe']"

environment = Environment(loader=FileSystemLoader("hunts/jinja/"))
template = environment.get_template("kestrel_jinja_template.hf")


def hunt_jinja_via_variables( get_cmd: str = None, 
                              from_cmd: str = None, 
                              where_cmd: str = None,
                              start_cmd: str = None,
                              stop_cmd: str = None):
    
    config_data = toml.load("config.toml")
    is_sample_data = config_data["KESTREL"]["is_sample_data"]    
    
    if get_cmd is None:
        get_cmd = default_get_cmd

    if from_cmd is None:
        from_cmd = default_from_cmd

    if where_cmd is None:
        where_cmd = default_where_cmd                   

    return_data = {}

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

        rsp = {}
        if is_sample_data:
            for data_item in return_data:
                rsp = data_item
                break
        else:
            rsp = return_data

    print(rsp) 
    return rsp        
       