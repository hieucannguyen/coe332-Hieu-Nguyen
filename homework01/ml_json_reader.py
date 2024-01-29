import json

def get_dataclass(data, dataclass):
    result = []
    for meteor in data:
        result.append(meteor[dataclass])

    return result

def get_recclass(data):
    result = {}

    for meteor in data:
        result[meteor["recclass"]] = result.get(meteor["recclass"], 0) + 1
    return result

def most_common_recclass(recclasses):
    highest_freq = 0
    most_common = ""
    for recclass in recclasses:
        if recclasses[recclass] > highest_freq:
            highest_freq = recclasses[recclass]
            most_common = recclass

    if highest_freq > 0:
        return most_common
    else:
        return "No meteors"
    
def average_mass(data):
    masses = get_dataclass(data, "mass (g)")
    sum = 0.
    for mass in masses:
        sum+=float(mass)
    return sum/len(masses)

def check_hemisphere(latitude, longitude):
    location = ''
    if (latitude > 0):
        location = 'Northern'
    else:
        location = 'Southern'
    if (longitude > 0):
        location = f'{location} & Eastern'
    else:
        location = f'{location} & Western'

    return(location)

def location_distribution(data):
    latitude = get_dataclass(data, "reclat")
    longitude = get_dataclass(data, "reclong")
    result = {}
    for i in range(len(latitude)):
        hemisphere = check_hemisphere(float(latitude[i]), float(longitude[i]))
        if hemisphere == "Northern & Eastern":
            result["Northern & Eastern"] = result.get("Northern & Eastern", 0) + 1

        if hemisphere == "Northern & Western":
            result["Northern & Western"] = result.get("Northern & Western", 0) + 1

        if hemisphere == "Southern & Eastern":
            result["Southern & Eastern"] = result.get("Southern & Eastern", 0) + 1

        if hemisphere == "Southern & Western":
            result["Southern & Western"] = result.get("Southern & Western", 0) + 1

    return result

# number of meteorites
# number of classes
# most common class
# average mass
# number north east
# number north west
# number south east
# number south west
def summary_statistics(data):
    print("Summary Statistics: \n")
    print(f'Number of meteorites: {len(data)}')

    recclasses = get_recclass(data)

    print(f'Number of classes: {len(recclasses)}')
    print(f'Most common class: {most_common_recclass(recclasses)}')

    print(f'Average mass: {average_mass(data)}')

    locations = location_distribution(data)
    print(f'Number Northern & Eastern: {locations.get("Northern & Eastern", 0)}')
    print(f'Number Northern & Western: {locations.get("Northern & Western", 0)}')
    print(f'Number Southern & Eastern: {locations.get("Southern & Eastern", 0)}')
    print(f'Number Southern & Western: {locations.get("Southern & Western", 0)}')

def main():
    with open('Meteorite_Landings.json', 'r') as f:
        ml_data = json.load(f)

    summary_statistics(ml_data["meteorite_landings"])

if __name__ == '__main__':
    main()