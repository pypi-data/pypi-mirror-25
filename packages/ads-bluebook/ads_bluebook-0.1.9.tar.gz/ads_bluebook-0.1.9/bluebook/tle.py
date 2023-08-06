import math
from datetime import datetime
from bluebook import validate

U = math.pow(10, 14) * 3.986004418
EARTHS_RADIUS_IN_KELOMETERS = 6378.137

def get_period_in_minutes(mean_motion):
    return 1440 / mean_motion

def get_semi_major_axis_in_kilometers(period_in_minutes): 
    # variables in global module-level scope are read-only. Use global word to 
    # change that...
    # global U
    semi_major_axis = 0.0
    semi_major_axis = ((period_in_minutes * 60.0) / (2 * math.pi))**2.0
    semi_major_axis = (semi_major_axis * U)**(1.0/3.0)
    return semi_major_axis / 1000 # convert to kelometers

def get_apogee_radius_in_kilometers(semi_major_axis_in_kilometers, eccentricity):
    return semi_major_axis_in_kilometers * (1.0 + eccentricity)
def get_perigee_radius_in_kilometers(semi_major_axis_in_kilometers, eccentricity):
    return semi_major_axis_in_kilometers * (1.0 - eccentricity)

def get_perigee_altitude_in_kelometers(semi_major_axis_in_kilometers, eccentricity):
    perigee_radius_in_kelometers = \
        get_perigee_radius_in_kilometers(semi_major_axis_in_kilometers, eccentricity)
    return perigee_radius_in_kelometers - EARTHS_RADIUS_IN_KELOMETERS

def get_apogee_altitude_in_kelometers(semi_major_axis_in_kilometers, eccentricity):
    apogee_radius_in_kilometers = \
        get_apogee_radius_in_kilometers(semi_major_axis_in_kilometers, eccentricity)
    return apogee_radius_in_kilometers - EARTHS_RADIUS_IN_KELOMETERS

def get_line_0_obj(line):
    obj = {
        "line": line[:24],
        "line_number": 0, 
        "name": line[:24].strip() 
    }
    return obj
def get_line_1_obj(line):
    obj = {
        # The line is 69 columns, so take up to the 69th index
        # Form is: line[startIndex:endIndex+1]
        "line": line[:69],
        "line_number": line[0],
        "satcat": line[2:7],
        "classification": line[7],
        "designator": line[9:17],
        "epoch": line[18:32],
        "first_mean_motion_derivitive": line[33:43],
        "second_mean_motion_derivitive": line[44:52],
        "b_star": line[53:61],
        "set_type": line[62],
        "number": line[64:68],
        "checksum": line[68]
    }
    return obj
def get_line_2_obj(line):
    obj = {
        "line": line[:69],
        "line_number": line[0],
        "satcat": line[2:7],
        "inclination": line[8:16],
        "right_ascension": line[17:25],
        "perigee": line[34:42],
        "mean_anomaly": line[43:51],
        "mean_motion": line[52:63],
        "revolution_epoch": line[63:68],
        "checksum": line[68]
    }
    return obj

def get_tle_object(line):
    obj = {}
    length = len(line)
    if length == 24:
        obj = get_line_0_obj(line)
    elif length == 69 and line[:1] == "1":
        obj = get_line_1_obj(line)
    elif length == 69 and line[:1] == "2":
        obj = get_line_2_obj(line)
    else:
        raise Exception("Invalid line length")
    return obj

def get_tle_objects(lines):
    """Read in all the lines in the list of lines and return
       a list of objects"""
    tle_objects = []

    for line in [x.strip() for x in lines]:
        length = len(line)
        if (length == 24 or length == 69):
            obj = get_tle_object(line)
            tle_objects.append(obj)

    return tle_objects

def get_four_digit_year(two_digit_year):
    four_digit_year = ""
    if two_digit_year[0] == "0" or two_digit_year[0] == "1":
        four_digit_year = "20" + two_digit_year
    else:
        four_digit_year = "19" + two_digit_year
    return four_digit_year
def get_satcat_number(designator):
    satcat = ""
    two_digit_year = designator[:2]
    four_digit_year = get_four_digit_year(two_digit_year)
    number_of_launch_in_year = designator[2:5]
    letter = designator[5]
    satcat = four_digit_year + "-" + number_of_launch_in_year + letter
    return satcat

def update_object_from_tle_lines(line_1_obj, line_2_obj, collection):
    tle_elements = {
        "Line 1": line_1_obj["line"],
        "Line 2": line_2_obj["line"]
    }

    if line_1_obj["line"][15:17].strip():
        tle_elements["Piece of Launch"] = line_1_obj["line"][15:17]
    if line_1_obj["line"][18:20]:
        tle_elements["Epoch Year"] = int(line_1_obj["line"][18:20])
    if line_1_obj["line"][20:32]:
        tle_elements["Epoch DOY"] = float(line_1_obj["line"][20:32])
    if line_1_obj["first_mean_motion_derivitive"]:
        tle_elements["Time_d1"] = line_1_obj["first_mean_motion_derivitive"]
    if line_1_obj["second_mean_motion_derivitive"]:
        tle_elements["Time_d2"] = line_1_obj["second_mean_motion_derivitive"]
    if line_1_obj["checksum"]:
        tle_elements["Checksum_1"] = line_1_obj["checksum"]
    if line_1_obj["b_star"]:
        tle_elements["B_star"] = line_1_obj["b_star"]

    if line_2_obj["checksum"]:
        tle_elements["Checksum_2"] = int(line_2_obj["checksum"])
    if line_2_obj["inclination"]:
        tle_elements["Inclination"] = float(line_2_obj["inclination"])
    if line_2_obj["perigee"]:
        tle_elements["Perigee"] = float(line_2_obj["perigee"])
    if line_2_obj["mean_anomaly"]:
        tle_elements["Mean Anomaly"] = float(line_2_obj["mean_anomaly"])
    if line_2_obj["mean_motion"]:
        tle_elements["Mean Motion"] = float(line_2_obj["mean_motion"])
    if line_2_obj["revolution_epoch"]:
        tle_elements["Revolution Number"] = int(line_2_obj["revolution_epoch"])

    push_obj = {
        "Orbit Data.Astrometric Data.TLE Data": {
            "Source ID": 0,
            "Date of Collection": datetime.now().isoformat(),
            "Elements": tle_elements
        }
    }
    query = { "NORAD ID": line_1_obj["satcat"] }
    update = {
        "$set": {
            "NORAD ID": line_1_obj["satcat"],
            "Classification": line_1_obj["classification"],
            "SATCAT ID": get_satcat_number(line_1_obj["designator"])
        },
        "$push": push_obj
    }
    collection.update_one(query, update, upsert=True)
    doc = collection.find_one(query)
    validate.transform(doc)
    collection.replace_one(query, doc)

def update_from_tle_file(path_to_file, collection):
    with open(path_to_file, "r") as file_handle:
        # Get all lines but remove all whitespace and blank lines
        #lines = filter(lambda x: len(x) == 69 or len(x) == 24, [line.strip() for line in file_handle.readlines()])
        lines = file_handle.readlines()
        tle_objects = get_tle_objects(lines)
        index = 0
        length = len(tle_objects)
        while index < length:
            if (index + 1 < length and
                    tle_objects[index]["line"][0] == "1" and
                    tle_objects[index + 1]["line"][0] == "2"):
                update_object_from_tle_lines(tle_objects[index],
                    tle_objects[index+1], collection)
                index = index + 1

                    
            index = index + 1
