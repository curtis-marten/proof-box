import yaml
import time


def load_config():
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    return cfg


def read_temp():
    with open("temp.yaml", "r") as ymlfile:
        temp = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return temp["temp"]


def heat_on():
    print("Heat On!")


def heat_off():
    print("Heat Off!")


def main_loop(cfg):

    heat = False

    min_temp = cfg["min_temp"]
    max_temp = cfg["max_temp"]

    current_temp = read_temp()
    session_max_temp = current_temp
    session_min_temp = current_temp

    while(True):
        time.sleep(1)
        current_temp = read_temp()
        session_max_temp = max(current_temp, session_max_temp)
        session_min_temp = min(current_temp, session_min_temp)

        if current_temp < min_temp and heat is False:
            heat = True
            heat_on()
        elif current_temp > max_temp and heat is True:
            heat = False
            heat_off()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    conf = load_config()
    print(conf)
    main_loop(conf)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
