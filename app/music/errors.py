class InvalidNoteError(Exception):

    def __init__(self, note):
        self.message = f'Invalid note: "{note}".'
        super().__init__(self.message)