def export_collection(collection):
    # TODO: export collection as a csv or pickle
    pass

def import_collection(file_name):
    # TODO: import collection from multiple file formats
    pass

class Collection:
    def __init__(self) -> None:
        self.cards = []
        self.value = 0

    def __sizeof__(self) -> int:
        return len(self.cards)

    def get_value(self):
        return self.value

    def update_values(self):
        for card in self.cards:
            card.update_value()
            self.value += card.get_value()

    def add_cards(self, card_list):
        for card in card_list:
            self.value += card.get_value
        
        self.cards.extend(card_list)


class Card:
    def __init__(
        self,
        year,
        group,
        set,
        listing,
        name,
        team,
        rc,
        photo=None,
        grade=None,
        value=None,
        serial=0,
        mem=False,
        auto=False,
    ) -> None:
        self.year = year
        self.group = group
        self.set = set
        self.listing = listing
        self.name = name
        self.team = team
        self.rc = rc
        self.photo = photo
        self.grade = grade
        self.value = value
        self.serial = serial
        self.mem = mem
        self.auto = auto

    def get_value(self):
        return self.value
    
    def update_value(self):
        # TODO: Scrape Ebay for comps or find website capable of accurate pricing
        self.value = 0

    def add_photo(self):
        # TODO: Support multiple file hosting websites for future web UI
        self.photo = None
