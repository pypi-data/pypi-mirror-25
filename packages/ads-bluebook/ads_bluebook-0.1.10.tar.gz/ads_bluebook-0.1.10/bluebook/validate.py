import bluebook.tle as tle

def transform(doc):
    add_tle_properties(doc)
def add_tle_properties(doc):
    if (doc and "Orbit Data" in doc and
            "Astrometric Data" in doc["Orbit Data"] and
            "TLE Data" in doc["Orbit Data"]["Astrometric Data"]):
        tle_datas = doc["Orbit Data"]["Astrometric Data"]["TLE Data"]
        for data in tle_datas:
            if ("Elements" in data and "Mean Motion" in data["Elements"]):
                # Get period
                mean_motion = data["Elements"]["Mean Motion"]
                period = tle.get_period_in_minutes(mean_motion)

                # Get semi major axis in meters
                semi_major_axis_in_kilometers = tle.get_semi_major_axis_in_kilometers(period)

                # Store semi major axis in kelmoeters and period in document
                data["Elements"]["Semi Major Axis"] = semi_major_axis_in_kilometers
                data["Elements"]["Period"] = period

                if ("Eccentricity" in data["Elements"]):
                    # Eccentricity provided so store apogee/perigee altutudes in document
                    eccentricity = data["Elements"]["Eccentricity"]
                    apogee_altitude = tle.get_apogee_altitude_in_kelometers(semi_major_axis_in_kilometers, eccentricity)
                    perigee_altitude = tle.get_perigee_altitude_in_kelometers(semi_major_axis_in_kilometers, eccentricity)
                    data["Elements"]["Apogee Altitude"] = apogee_altitude
                    data["Elements"]["Perigee Altitude"] = perigee_altitude