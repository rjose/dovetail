def sort_pair(start_day, end_day):
    if start_day > end_day:
        start_day, end_day = end_day, start_day
    return start_day, end_day 


class Slot():
    def __init__(self, start_day, end_day):
        self.start_day, self.end_day = sort_pair(start_day, end_day)

    def contains(self, start_day, end_day):
        result = False

        start_day, end_day = sort_pair(start_day, end_day)
        if start_day < self.start_day:
            result = False
        elif end_day > self.end_day:
            result = False
        else:
            result = True
        return result

    # Returns an array of slots that result if this slot were to be filled
    def fill(self, start_day, end_day):
        start_day, end_day = sort_pair(start_day, end_day)

        if not self.contains(start_day, end_day):
            raise Exception('Can\'t fill slot with (%f, %f)' % (start_day, end_day))

        #self.assertEqual(slot.fill(2, 3), [Slot(3, 7)])
        result = []
        if start_day == self.start_day and end_day < self.end_day:
            result = [Slot(end_day, self.end_day)]
        elif start_day > self.start_day and end_day < self.end_day:
            result = [Slot(self.start_day, start_day), Slot(end_day, self.end_day)]
        elif start_day > self.start_day and end_day == self.end_day:
            result = [Slot(self.start_day, start_day)]
        else:
            result = []

        return result



    def __eq__(self, other):
        return (self.start_day, self.end_day) == (other.start_day, other.end_day)

