import random
import Classes

def generate_cars(grid, city_size, time, max_cars):
    # list of car objects
    cars = []

    # time zones
    if time == 1: time_zone_car_percentage = 0.1  # 0-6
    if time == 2: time_zone_car_percentage = 1    # 6-12
    if time == 3: time_zone_car_percentage = 1    # 12-18
    if time == 4: time_zone_car_percentage = 0.5  # 18-24

    # calculate number of cars based on time
    max_cars *= time_zone_car_percentage

    # city zones
    city_zone1 = {'bound': city_size/6, 'probability': 0.3, 'roads': 0} 
    city_zone2 = {'bound': city_size/3, 'probability': 0.2, 'roads': 0}
    city_zone3 = {'bound': city_size/2, 'probability': 0.5, 'roads': 0}

    # number of roads in each zone
    for x in range(city_size):
        for y in range(city_size):
            if grid(x,y) == 'road':
                if x < city_zone1['bound'] or x > city_size - city_zone1['bound'] and y < city_zone1['bound'] or y > city_size - city_zone1['bound']:
                    city_zone1['roads'] += 1
                elif x < city_zone2['bound'] or x > city_size - city_zone2['bound'] and y < city_zone2['bound'] or y > city_size - city_zone2['bound']:
                    city_zone2['roads'] += 1
                else:
                    city_zone3['roads'] += 1

    # calculate new probabilities
    city_zone1['probability'] = max_cars * city_zone1['probability'] / city_zone1['roads']
    city_zone2['probability'] = max_cars * city_zone2['probability'] / city_zone2['roads']
    city_zone3['probability'] = max_cars * city_zone3['probability'] / city_zone3['roads']

    #generate cars based on the probability for each zone
    for x in range(city_size):
        for y in range(city_size):
            if grid(x,y) == 'road':
                if x < city_zone1['bound'] or x > city_size - city_zone1['bound'] and y < city_zone1['bound'] or y > city_size - city_zone1['bound']:
                    if random.random() < city_zone1['probability']:
                        if random.random() < 0.5:
                            car = Classes.Gasolin_Car()
                        else:
                            car - Classes.Diesel_Car()
                        cars.append(car)
                elif x < city_zone2['bound'] or x > city_size - city_zone2['bound'] and y < city_zone2['bound'] or y > city_size - city_zone2['bound']:
                    if random.random() < city_zone2['probability']:
                        if random.random() < 0.5:
                            car = Classes.Gasolin_Car()
                        else:
                            car - Classes.Diesel_Car()
                        cars.append(car)
                else:
                    if random.random() < city_zone3['probability']:
                        if random.random() < 0.5:
                            car = Classes.Gasolin_Car()
                        else:
                            car - Classes.Diesel_Car()
                        cars.append(car)
            
    return cars