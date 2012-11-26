from dovetail.timeline.slot import Slot

def update_days(start_day, width):
    return start_day, start_day + width

class Timeline():

    def __init__(self, cur_date):
        self.slots = [Slot(0, float('inf'))]
        self.cur_date = cur_date

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


