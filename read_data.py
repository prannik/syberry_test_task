import yaml

def read_toys():
    with open('input_file/toys.yaml') as file:
        read_data = yaml.safe_load(file)

    return read_data

def read_games():
    with open('input_file/games.yaml') as file:
        read_data = yaml.safe_load(file)

    return read_data
