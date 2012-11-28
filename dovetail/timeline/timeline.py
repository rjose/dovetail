from dovetail.timeline.slot import Slot
from datetime import timedelta

def update_days(start_day, width):
    return start_day, start_day + width

def increment_date(date):
    delta1 = timedelta(1) # 1 day
    return date + delta1

class Timeline():

    def __init__(self, cur_date):
        self.slots = [Slot(0, float('inf'))]
        self.cur_date = cur_date
        self.dates = []

    def find_slot(self, earliest_start_day, width):
        # Default to the last, infinite slot
        start_day, end_day = update_days(self.slots[-1].start_day, width)
        new_slot = Slot(start_day, end_day)
        containing_slot_index = len(self.slots) - 1

        modify_start_date = False
        start_day, end_day = update_days(earliest_start_day, width)
        for i, s in enumerate(self.slots):
            if modify_start_date:
                start_day, end_day = update_days(s.start_day, width)
            if s.contains(start_day, end_day):
                new_slot = Slot(start_day, end_day)
                containing_slot_index = i
                break
            else:
                modify_start_date = True

        # Set slot dates
        new_slot.start_date = self.date_from_day(new_slot.start_day)
        new_slot.end_date = self.date_from_day(new_slot.end_day)
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
            self.add_dates_to(date)

        # Keep incrementing date until we find one in the timeline.
        # This is guaranteed because add_dates will add at least one date
        # at or after the specified date.
        while not date in self.dates:
            date = increment_date(date)
        return self.dates.index(date)

    def need_to_add_dates(self, date):
        return self.dates == [] or date > self.dates[-1]

    def is_workday(self, date):
        # TODO: Check holiday or OOO
        if date.weekday() in [5, 6]:
            result = False
        else:
            result = True
        return result

    def add_dates_to(self, end_date, min_dates_added = 1):
        if end_date < self.cur_date:
            return

        num_dates_added = 0
        delta1 = timedelta(1) # 1 day
        if self.dates == []:
            date = self.cur_date - delta1
        else:
            date = self.dates[-1]

        while date < end_date:
            date += delta1
            if self.is_workday(date):
                self.dates.append(date)
                num_dates_added += 1
            if date == end_date and num_dates_added < min_dates_added:
                end_date += delta1
        return

    def add_days_to(self, day):
        num_days_to_add = day - len(self.dates) + 1
        if num_days_to_add <= 0:
            return

        start_date = None
        if self.dates == []:
            start_date = self.cur_date
        else:
            start_date = increment_date(self.dates[-1])
        self.add_dates_to(start_date, num_days_to_add)
        return

    def date_from_day(self, day):
        # int() takes the floor of a float. This is what we want here since
        # integers correspond to the start of a day.
        day = int(day)
        if day < 0:
            return
        self.add_days_to(day)
        return self.dates[day]

    def find_slot_with_ending_date(self, end_date, width):
        # Target ending halfway through the end date
        end_day = self.day_from_date(end_date) + 0.5
        start_day = end_day - width
        return self.find_slot(start_day, width)

    def schedule_at_start_date(self, start_date, effort_left_d):
        day = self.day_from_date(start_date)
        slot, parent_index = self.find_slot(day, effort_left_d)
        slot = self.claim_slot(slot, parent_index)
        return slot

    def schedule_at_end_date(self, end_date, effort_left_d):
        slot, index = self.find_slot_with_ending_date(end_date, effort_left_d)
        slot = self.claim_slot(slot, index)
        return slot
