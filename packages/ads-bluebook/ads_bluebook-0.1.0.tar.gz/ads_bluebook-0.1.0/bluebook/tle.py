import math

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