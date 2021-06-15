class WaterLevel(object):
    """A WaterLevel in ml"""

    def __init__(self, water_level):
        super(WaterLevel, self).__init__()
        self.__water_level = 0

    @staticmethod
    def int_to_water_level(self, water_level):
        """Creates an object of type WaterLevel"""
        assert is_valid(water_level), 'prerequisite invalid. water_level cant be negative'
        return self.__water_level(water_level)


    def is_valid(self, water_level):
        return water_level >= 0


    def __eq__(self, other):
        if not isinstance(other, WaterLevel):
            return False

        return self.__water_level == other.__water_level

    def __hash__(self):
        return hash(self.__water_level)


    def water_level_to_int():
        """return :int: the water_level as integer"""
        return self.__water_level
