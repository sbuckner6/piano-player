class Range:

    def __init__(self, bottom_note, top_note):
        self.bottom = bottom_note
        self.top = top_note

    def __str__(self):
        return f"<{self.bottom}, {self.top}>"