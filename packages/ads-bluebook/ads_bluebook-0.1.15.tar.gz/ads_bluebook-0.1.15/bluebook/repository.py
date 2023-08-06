from bluebook import tle, validate
from datetime import datetime


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
            "SATCAT ID": tle.get_satcat_number(line_1_obj["designator"])
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
        tle_objects = tle.get_tle_objects(lines)
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
