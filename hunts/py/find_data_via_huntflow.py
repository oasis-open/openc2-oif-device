import toml
from kestrel.session import Session


def hunt_via_file(huntflow_file: str, get_var: str = "results"):

    config_data = toml.load("config.toml")
    is_sample_data = config_data["KESTREL"]["is_sample_data"]

    with Session() as session:
        with open(huntflow_file) as hff:
            huntflow = hff.read()
        session.execute(huntflow)
        return_data = session.get_variable(get_var)

        rsp = {}
        if is_sample_data:
            for data_item in return_data:
                rsp = data_item
                break
        else:
            rsp = return_data

    print(rsp) 
    return rsp