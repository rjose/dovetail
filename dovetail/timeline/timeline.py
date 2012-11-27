from dovetail.timeline.slot import Slot
from datetime import timedelta

def update_days(start_day, width):
    return start_day, start_day + width

class Timeline():

    def __init__(self, cur_date):
        self.slots = [Slot(0, float('inf'))]
        self.cur_date = cur_date
        self.dates = []

    def find_slot(self, earliest_start_day, width):
        new_slot = None
        containing_slot_index = None
        update_start_date_from_slot = False

        start_day, end_day = update_days(earliest_start_day, width)
        for i, s in enumerate(self.slots):
            if update_start_date_from_slot:
                start_day, end_day = update_days(s.start_day, width)
            if s.contains(start_day, end_day):
                new_slot = Slot(start_day, end_day)
                containing_slot_index = i
                break
            else:
                update_start_date_from_slot = True

        return new_slot, containing_slot_index

    # index is the index of the containing slot
    def claim_slot(self, slot, index):
        new_slots = self.slots[index].fill(slot.start_day, slot.end_day)
        self.slots = self.slots[:index] + new_slots + self.slots[index+1:]
        return slot

    def day_from_date(self, date):
        if date < self.cur_date:
            return None
        if self.need_to_add_dates(date):
            self.add_dates(date)

        # Keep incrementing date until we find one in the timeline.
        # This is guaranteed because add_dates will add at least one date
        # at or after the specified date.
        delta1 = timedelta(1) # 1 day
        while not date in self.dates:
            date += delta1
        return self.dates.index(date)

    def need_to_add_dates(self, date):
        return self.dates == [] or date > self.dates[-1]

    def is_workday(self, date):
        # TODO: Check holiday or OOO
        result = True
        if date.weekday() in [5, 6]:
            result = False
        else:
            result = True
        return result

    def add_dates(self, end_date):
        if end_date < self.cur_date:
            return

        has_added_date = False
        delta1 = timedelta(1) # 1 day
        date = None
        if self.dates == []:
            date = self.cur_date - delta1
        else:
            date = self.dates[-1]

        while date < end_date:
            date += delta1
            if self.is_workday(date):
                self.dates.append(date)
                has_added_date = True
            elif date == end_date and has_added_date == False:
                end_date += delta1
        return

