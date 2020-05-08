

def good_zero(min_elevation, max_elevation):
    def worker(elevation):
        return elevation <= max_elevation
    return worker
    #return elevation >= min_elevation and elevation + half-diameter-of-bullet <= max_elevation 