import datetime

class BitMask:
    """A class that describes a bitmask and its associated operations
    """
    def __init__(self, bits, length) -> None:
        self.bits = bits
        self.length = length
    
    def __or__(self, other):
        if isinstance(other, BitMask):
            new_bits = self.bits | other.bits
            return BitMask(new_bits)
        else:
            raise TypeError("Operand must be an instance of BitMask")
    
    def readout(self, prev) -> tuple:
        """Reads out the values of the BitMask. Returns a list of values that
          indicate the indices where the bits change from 0 to 1 and vice versa.
          The bit before the initial bit is assumed to be the value 'prev'.

          Example: When reading out 1101 with prev set to 0, the string changes
          from 0 to 1 at bit 0, changing again from 1 to 0 at bit 1 and again from
          0 to 1 at bit 2. The last bit is 1. Hence, the output is: 

        :param prev: What the bit before the initial bit is assumed to be
        :type prev: int
        :return: A list of indices where the bits change between 0 and 1, and the 
        bit value of the last bit
        :rtype: tuple
        """
        curr_val = prev
        curr_bits = self.bits
        result = []
        for i in range(self.length):
            if curr_bits & 0b1 != curr_val:
                result.append(i)
                if curr_val == 0:
                    curr_val = 1
                else:
                    curr_val = 0
            curr_bits >>= 1
        return result, curr_val
        
class HourMask(BitMask):
    """A class that describes an hour in terms of a 60-bit bitmask. 1s represent 
    that that minute is busy while 0s represent that that minute is free. Time runs
    from right to left
    (i.e. LSB represents the 0th minute and MSB represents the 59th minute)
    """
    def __init__(self, start_hour, bits=0x000000000000000) -> None:
        super().__init__(bits, 60)
        self.start_hour = start_hour
    
    def __hash__(self) -> int:
        return self.start_hour
    
    def combine(self, other) -> None:
        if not isinstance(other, HourMask):
            raise TypeError("Operand should be of type HourMask")
        if other.start_hour != self.start_hour:
            raise ValueError(f"Incompatible times: {other.start_hour} and {self.start_hour}")
        self.bits |= other.bits

class DayMasks:
    """A class that represents the availability in a day.
    """
    def __init__(self, date:datetime.date, 
                 hour_masks:list[HourMask] = [HourMask(i) for i in range(24)]) -> None:
        for i in range(24):
            if hour_masks[i].start_hour != i:
                raise ValueError(f"Hour {hour_masks[i].start_hour} found where Hour {i} is expected")
        self.hour_masks = hour_masks
        self.date = date

    def combine_daymasks(self, other):
        """Combines availability based on 2 given DayMasks

        :param other: DayMasks to compare with
        :type other: DayMasks
        :raises TypeError: If given argument is not of type DayMasks
        :raises Exception: If DayMasks are of different date
        :return: A new combined DayMasks object
        :rtype: DayMasks
        """
        if not isinstance(other, DayMasks):
            raise TypeError("Operand must be an instance of DayMasks")
        if other.date != self.date:
            raise Exception("Date of DayMasks are incompatible")
        new_hour_masks = []
        for i in range(24):
            new_hour_masks.append(self.hour_masks[i] | other.hour_masks[i])
        return DayMasks(new_hour_masks, self.date)
    
    def insert_event_hourmask(self, hourmask_list:list[HourMask]):
        for i in hourmask_list:
            curr = i.start_hour
            self.hour_masks[curr].combine(i)
    
    def get_intervals(self, get_free = False):
        """Gets the intervals of free/busy times in the day based on the given
        DayMasks

        :param get_free: Boolean that determines if free timeslots are read out, defaults to False
        :type get_free: bool, optional
        :return: A tuple. The first element of the tuple is a list containing tuples where
        the first element is a list of minutes where the state switches between
        free and busy and the second is the hour. The second element of the tuple is
        the state of the last minute, 1 being busy, 0 being free
        :rtype: tuple
        """
        curr_val = int(get_free)
        result = list()
        for i in self.hour_masks:
            output = i.readout(curr_val)
            time_tuple = (output[0], i.start_hour)
            result.append(time_tuple)
            curr_val = output[1]
        return result, curr_val


if __name__ == "__main__":
    print(BitMask(13,3).readout(0))