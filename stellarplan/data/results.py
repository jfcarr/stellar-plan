class ResultObject:
    """
    Holds information about an object for display in the observing plan.
    """

    def __init__(
        self, description, constellation, object_type, altitude, azimuth, magnitude
    ):
        self.description = description
        self.constellation = constellation
        self.object_type = object_type
        self.altitude = altitude
        self.azimuth = azimuth
        self.magnitude = magnitude
