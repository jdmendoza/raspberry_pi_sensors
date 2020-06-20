import Adafruit_DHT
import time
import datetime
import boto3
from decimal import Decimal


def read_temp():
    humidity_r, temp_r = Adafruit_DHT.read(Adafruit_DHT.DHT22, 4)
    temp_f = (temp_r*9/5)+32
    return humidity_r, temp_f


def store_data_in_table(table, name, value):
    id_gen = datetime.datetime.now()

    try:
        table.put_item(
           Item={
                'id': id_gen.strftime("%Y%m%d%H%M%S"),
                'name': name,
                'value': Decimal(str(value)),
                'datetime': id_gen.strftime("%m/%d/%Y %H:%M:%S")
            }
        )

        return True

    except:

        return False


if __name__ == "__main__":
    table = boto3.resource('dynamodb').Table('pi_sensors')

    while True:
        try:
            now = datetime.datetime.now()
            humidity, temp = read_temp()
            time.sleep(5)
            store_data_in_table(table, 'humidity', humidity)
            time.sleep(5)
            store_data_in_table(table, 'temp', temp)
            print('Temp {}F, Humidity {}%'.format(humidity, temp))

            time.sleep(300)

        except:
            print("Error")
            time.sleep(5)