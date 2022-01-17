class Entry:
    """Responsible for building a journal entry object
    """

    def __init__(self, id, concept, entry, mood_id, date) -> None:
        self.id = id
        self.concept = concept
        self.entry = entry
        self.mood_id = mood_id
        self.date = date
        self.mood = None
