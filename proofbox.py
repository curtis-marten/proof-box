import yaml
import time
from gpiozero import LED



def read_temp(id):
    try:
        f = open('/sys/bus/w1/devices/' + id + '/w1_slave')
        line = f.readline()
        crc = line.rsplit(' ', 1)
        crc = crc[1].replace('\n', '')
        if crc=='YES':
            line = f.readline()
            temp = line.rsplit('t=',1)
        else:
            temp = 999999
        f.close()
        
        tempF = (int(temp[1]) / 1000 * 1.8) + 32
        return tempF

    except:
        return 999999



def load_config():
    with open("config.yaml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

    return cfg


#def read_temp():
#    with open("temp.yaml", "r") as ymlfile:
#        temp = yaml.load(ymlfile, Loader=yaml.FullLoader)
#    return temp["temp"]

relay = LED(17)

def heat_on():
    # relay logic is reversed (active low)
    relay.off()
    print("Heat On!")


def heat_off():
    # relay logic is reversed (active low)
    relay.on()
    print("Heat Off!")


def main_loop(cfg):

    relay.on()

    heat = False

    min_temp = cfg["min_temp"]
    max_temp = cfg["max_temp"]
    temp_sense_id = cfg["temp_sense_id"]

    current_temp = read_temp(temp_sense_id)
    session_max_temp = current_temp
    session_min_temp = current_temp

    while(True):
        time.sleep(1)
        current_temp = read_temp(temp_sense_id)
        print(current_temp)    
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
