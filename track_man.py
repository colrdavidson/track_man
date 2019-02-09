import serial

class Car:
    def __init__(self, car_id):
        self.car_id = car_id
        self.track_time = 9.999
        self.position = 7

    def __repr__(self):
        return "car id: {} time: {} position: {}".format(self.car_id, self.track_time, self.position)
    
def gimme_test_data():
    return open("track_data.txt", mode="r")

def gimme_real_data():
    ser = serial.Serial(port="COM4", baudrate=9600)
    ser.open()
    return ser

def generate_heat_map(heat_filename):
    heat_map = {}   
    
    car_file = open(heat_filename, mode="r")
    car_map = car_file.readlines()
    
    for i, race in enumerate(car_map):
        race = race.rstrip()
        race_data = race.split(',')
        
        heat = i
        heat_map[heat] = {}

        for j, car in enumerate(race_data):
            car_id = car
            track_id = chr(ord('A') + j)
            heat_map[heat][track_id] = Car(car_id)

    return heat_map

def main():
    heat_map = generate_heat_map("car_layout.txt")
    
    try:
        f = gimme_test_data()
    except:
        print("Can't find the droid you were looking for!")
        return

    heat = 0
    input_data = "foo"
    while heat < len(heat_map):
        input_data = f.readline()

        if '@' in input_data:
            positions = input_data[1:].split(',')
            for position in positions:
                track_id = position[0]
                track_time = round(float(position[2:7]), 3)
                position = ord(position[7]) - 32

                car = heat_map[heat][track_id]
                car.track_time = track_time
                car.position = position

            heat += 1

    total_car_times = {}

    for heat in heat_map:
        for track_id, car in heat_map[heat].items():
            if car.car_id not in total_car_times:
                total_car_times[car.car_id] = car.track_time
            else:
                total_car_times[car.car_id] += car.track_time

    for car_id in sorted(total_car_times, key=total_car_times.get):
        print("Car: {}, total time {:.3f}".format(car_id, total_car_times[car_id]))
        
main()
