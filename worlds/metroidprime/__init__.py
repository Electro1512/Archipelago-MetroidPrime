from BaseClasses import Item
from .Items import MetroidPrimeItem, suit_upgrade_table, artifact_table, item_table
from .PrimeOptions import MetroidPrimeOptions
from .Locations import every_location
from .Regions import create_regions
from .Rules import set_rules
from worlds.AutoWorld import World


class MetroidPrimeWorld(World):
    """
    Metroid Prime is a first-person action-adventure game originally for the Gamecube. Play as
    the bounty hunter Samus Aran as she traverses the planet Tallon IV and uncovers the plans
    of the Space Pirates.
    """
    game = "Metroid Prime"
    options_dataclass = MetroidPrimeOptions
    options: MetroidPrimeOptions
    topology_present = True
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = every_location

    def generate_early(self):
        reqarts = int(self.options.required_artifacts)
        # starting inventory
        self.multiworld.precollected_items += [self.create_item("Power Beam")]
        self.multiworld.precollected_items += [self.create_item("Scan Visor")]
        self.multiworld.precollected_items += [self.create_item("Combat Visor")]
        self.multiworld.precollected_items += [self.create_item("Power Suit")]
        artcount = 12
        for i in artifact_table:
            if artcount <= reqarts:
                self.multiworld.precollected_items += [self.create_item(i)]
            artcount -= 1

    def create_regions(self) -> None:
        create_regions(self)

    def create_item(self, name: str) -> "Item":
        createdthing = item_table[name]
        return MetroidPrimeItem(name, createdthing.progression, createdthing.code, self.player)

    def create_items(self) -> None:
        # add remaining artifacts
        reqarts = int(self.options.required_artifacts)
        artcount = 12
        for i in artifact_table:
            if artcount >= reqarts:
                self.multiworld.itempool += [self.create_item(i)]
            artcount -= 1
        excluded = self.options.exclude_items
        spring = bool(self.options.spring_ball)
        items_added = 0
        for i in suit_upgrade_table:
            if i == "Power Beam" or i == "Scan Visor" or i == "Power Suit" or i == "Combat Visor":
                continue
            elif i in excluded.keys():
                continue
            elif i == "Spring Ball" and spring:
                self.multiworld.itempool += [self.create_item("Spring Ball")]
                items_added += 1
                continue
            elif i == "Missile Expansion":
                continue
            elif i == "Energy Tank":
                for j in range(0, 14):
                    self.multiworld.itempool += [self.create_item("Energy Tank")]
                items_added += 14
                continue
            elif i == "Ice Trap":
                continue
            elif i == "Power Bomb Expansion":
                for j in range(0, 4):
                    self.multiworld.itempool += [self.create_item("Power Bomb Expansion")]
                items_added += 4
            else:
                self.multiworld.itempool += [self.create_item(i)]
                items_added += 1
        # add missiles in whatever slots we have left
        while 100 - items_added > 0:
            self.multiworld.itempool += [self.create_item("Missile Expansion")]
            items_added += 1

    def set_rules(self) -> None:
        set_rules(self.multiworld, self.player)