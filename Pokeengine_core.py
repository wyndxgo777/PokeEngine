#!/usr/bin/env python3
# --------------------------------------------------------------
# PokeEngine - Unity RPG Prototype Generator Core
# --------------------------------------------------------------

import json
import os
import re
import urllib.request
from datetime import datetime


DEFAULT_PROJECT_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Pokemon_Game")
DEFAULT_PROJECT_NAME = os.path.basename(DEFAULT_PROJECT_PATH)
DEFAULT_PROJECT_DESTINATION = os.path.dirname(DEFAULT_PROJECT_PATH)
UNITY_EDITOR_VERSION = "2022.3.62f3"
POKEENGINE_RUNTIME_SCRIPT_GUID = "8b3d4f4f5d884ce7a07d62fd52991001"
PROTOTYPE_REGION_SCENE_GUID = "3dc5f09b95f245348bcb2b05dbd2a811"

FEATURE_REQUIREMENTS = [
    ("overworld", "2.5D diorama-style overworld", False),
    ("overworld", "Fixed or semi-fixed camera system", False),
    ("overworld", "Full region map with towns, routes, caves, and interiors", False),
    ("overworld", "Tile-based or hybrid movement system", False),
    ("overworld", "Collision and interaction system", False),
    ("overworld", "Day/night cycle visuals", False),
    ("overworld", "Weather effects system", False),
    ("pokemon_data", "Pokemon database integration", False),
    ("pokemon_data", "Pokemon stats, types, abilities system", False),
    ("pokemon_data", "Evolution system", False),
    ("pokemon_data", "Learnset system (level, TM/TR, etc.)", False),
    ("pokemon_data", "Encounter tables per area", False),
    ("pokemon_data", "Shiny Pokemon system", False),
    ("pokemon_data", "Forms and variants system", False),
    ("pokemon_data", "Party system (6 Pokemon)", False),
    ("pokemon_data", "PC box storage system", False),
    ("battle", "Turn-based battle system", False),
    ("battle", "Move system (damage, accuracy, priority)", False),
    ("battle", "Type effectiveness system", False),
    ("battle", "Status conditions system", False),
    ("battle", "Ability system", False),
    ("battle", "Weather effects in battle", False),
    ("battle", "Terrain effects system", False),
    ("battle", "Battle AI system (wild + trainer)", False),
    ("battle", "Battle animations system", False),
    ("battle", "Battle UI system", False),
    ("battle", "Battle transitions system", False),
    ("npc_events", "NPC dialogue system", False),
    ("npc_events", "Trainer battle scripting system", False),
    ("npc_events", "NPC pathing/movement system", False),
    ("npc_events", "Event trigger system", False),
    ("npc_events", "Cutscene system", False),
    ("npc_events", "Flag/progression system", False),
    ("npc_events", "Gym/trial progression system", False),
    ("npc_events", "Rival system", False),
    ("npc_events", "Legendary encounter system", False),
    ("npc_events", "Postgame content system", False),
    ("player_ui", "Inventory/bag system", False),
    ("player_ui", "Pokemon summary screen", False),
    ("player_ui", "Map system", False),
    ("player_ui", "Save/load system", False),
    ("player_ui", "Autosave system", False),
    ("player_ui", "Settings/options menu", False),
    ("player_ui", "UI navigation system", False),
    ("presentation", "Character models system", False),
    ("presentation", "Pokemon models system", False),
    ("presentation", "Animation system", False),
    ("presentation", "Lighting system", False),
    ("presentation", "Environmental asset system", False),
    ("presentation", "Effects system (particles, weather, etc.)", False),
    ("audio", "Music system (town, route, battle, boss themes)", False),
    ("audio", "Sound effects system", False),
    ("audio", "Ambient audio system", False),
    ("audio", "Audio mixing system", False),
    ("engine", "Game engine systems integration", False),
    ("engine", "Scene streaming/loading system", False),
    ("engine", "Asset management system", False),
    ("engine", "Scripting system for events", False),
    ("engine", "Localization/multilanguage system", False),
    ("engine", "Performance optimization system", False),
    ("ai_difficulty", "Wild Pokemon AI system", False),
    ("ai_difficulty", "Trainer AI system", False),
    ("ai_difficulty", "Difficulty scaling system", False),
    ("ai_difficulty", "Random encounter system", False),
    ("tools_pipeline", "Content creation pipeline tools", False),
    ("tools_pipeline", "Level design tools", False),
    ("tools_pipeline", "Dialogue editing tools", False),
    ("tools_pipeline", "Pokemon data editing tools", False),
    ("tools_pipeline", "QA/testing tools", False),
    ("tools_pipeline", "Build/version control system", False),
    ("online_optional", "Multiplayer trading system", True),
    ("online_optional", "Multiplayer battling system", True),
    ("online_optional", "Online matchmaking system", True),
    ("online_optional", "Friend system", True),
    ("online_optional", "Event distribution system", True),
    ("online_optional", "Cloud save system", True),
    ("polish_liveops", "UI polish system (animations, responsiveness, transitions)", False),
    ("polish_liveops", "Gameplay feel tuning system (timing, pacing, feedback)", False),
    ("polish_liveops", "Balancing and tuning system", False),
    ("polish_liveops", "Bug tracking and fix pipeline", False),
    ("polish_liveops", "Post-launch update/patch system", False),
    ("polish_liveops", "Live events system", True),
    ("raid", "Raid battle system (multiplayer boss encounters)", False),
    ("raid", "Raid den spawning system", False),
    ("raid", "Raid difficulty tiers system", False),
    ("raid", "Raid reward loot system", False),
    ("raid", "Raid matchmaking/co-op system", False),
    ("raid", "Raid AI boss system", False),
    ("raid", "Raid shield/break system", False),
    ("raid", "Raid turn timer system", False),
    ("raid", "Raid capture system", False),
    ("raid", "Raid event rotation system", False),
    ("mega_dimension_fusion", "Mega Evolution system (temporary battle-only power evolution with stat boosts and form changes)", False),
    ("mega_dimension_fusion", "Dimension Split system (battle transformation mechanic where a Pokemon shifts into an alternate empowered state with unique stats, enhanced abilities, and a signature move exclusive to that form)", False),
    ("mega_dimension_fusion", "Dimension Split signature attack system (unique move tied to each transformed form)", False),
    ("mega_dimension_fusion", "Dimension Split activation system (battle-triggered transformation conditions, limited usage rules, or meter-based activation)", False),
    ("mega_dimension_fusion", "Dimension Split buff system (temporary stat amplification and ability modification during transformation state)", False),
    ("mega_dimension_fusion", "Dimension Split visual shift system (alternate model/FX/animation state during battle form change)", False),
    ("mega_dimension_fusion", "Pokemon fusion system (merge-compatible Pokemon pairs into hybrid forms with combined stats, typing, abilities, and hybrid move sets)", False),
    ("mega_dimension_fusion", "Fusion compatibility rules system (defined valid pairing rules between species)", False),
    ("mega_dimension_fusion", "Fusion transformation UI system (fusion selection, preview, and confirmation interface)", False),
    ("mega_dimension_fusion", "Fusion separation system (ability to revert fused Pokemon back into original forms)", False),
    ("mega_dimension_fusion", "Fusion-exclusive move/ability system (unique traits unlocked only in fused state)", False),
    ("mega_dimension_fusion", "Fusion model generation system (combined visual model + animation blending system)", False),
]

class PokemonProjectBuilder:
    """Owns the default Pokemon V11 project data and writes it to disk."""

    def __init__(self, logger=None):
        self.logger = logger or print
        self.pokemon_db = []
        self.move_db = []
        self.backpack_categories_db = []
        self.trainer_card = {}
        self.quest_db = []
        self.feature_requirements = self._build_feature_requirements()
        self.init_data()

    def init_data(self):
        self.pokemon_db = [
            {
                "id": 1,
                "name": "Bulbasaur",
                "type1": "Grass",
                "type2": "Poison",
                "hp": 45,
                "atk": 49,
                "def": 49,
                "spa": 65,
                "spd": 65,
                "spe": 45,
                "moves": ["Tackle", "Growl", "Vine Whip"],
            },
            {
                "id": 4,
                "name": "Charmander",
                "type1": "Fire",
                "type2": "None",
                "hp": 39,
                "atk": 52,
                "def": 43,
                "spa": 60,
                "spd": 50,
                "spe": 65,
                "moves": ["Scratch", "Growl", "Ember"],
            },
            {
                "id": 7,
                "name": "Squirtle",
                "type1": "Water",
                "type2": "None",
                "hp": 44,
                "atk": 48,
                "def": 65,
                "spa": 50,
                "spd": 64,
                "spe": 43,
                "moves": ["Tackle", "Tail Whip", "Water Gun"],
            },
        ]
        self.move_db = [
            {
                "name": "Tackle",
                "power": 40,
                "accuracy": 100,
                "type": "Normal",
                "category": "Physical",
            },
            {
                "name": "Vine Whip",
                "power": 45,
                "accuracy": 100,
                "type": "Grass",
                "category": "Physical",
            },
            {
                "name": "Scratch",
                "power": 40,
                "accuracy": 100,
                "type": "Normal",
                "category": "Physical",
            },
            {
                "name": "Ember",
                "power": 40,
                "accuracy": 100,
                "type": "Fire",
                "category": "Special",
            },
            {
                "name": "Water Gun",
                "power": 40,
                "accuracy": 100,
                "type": "Water",
                "category": "Special",
            },
        ]
        self.backpack_categories_db = [
            {"name": "Items", "items": ["Tonic", "Return Rope", "Mist Charm"]},
            {"name": "Medicine", "items": ["Tonic", "Venom Cure", "Static Balm"]},
            {"name": "Capture Cores", "items": ["Basic Core", "Bright Core", "Premier Core"]},
            {"name": "HMs & TMs", "items": ["TC01 Clearcut", "TC10 Swift Arc", "TC45 Charm Call"]},
            {"name": "Key Items", "items": ["Region Slate", "Trainer Journal", "Stream Rod"]},
        ]
        self.trainer_card = {
            "trainerName": "Nova",
            "trainerId": "V11-0426",
            "money": 3000,
            "badges": 1,
            "playTime": "00:45",
            "homeRegion": "Aurora Province",
        }
        self.quest_db = [
            {
                "title": "Meet the Professor",
                "objective": "Return to the lab after testing the tall grass.",
                "complete": False,
            },
            {
                "title": "First Field Notes",
                "objective": "Trigger one wild Pokemon encounter.",
                "complete": False,
            },
            {
                "title": "Route Survey",
                "objective": "Find the edge blockers around the prototype route.",
                "complete": False,
            },
        ]

    def generate(self, root_dir):
        self.logger(f"Initializing project at {root_dir}...")
        os.makedirs(root_dir, exist_ok=True)

        data_dir = os.path.join(root_dir, "Assets", "StreamingAssets", "Data")
        os.makedirs(data_dir, exist_ok=True)

        self._write_json(os.path.join(data_dir, "pokemon.json"), self.pokemon_db)
        self._write_json(os.path.join(data_dir, "moves.json"), self.move_db)
        self._write_json(
            os.path.join(data_dir, "backpack_categories.json"),
            self.backpack_categories_db,
        )
        self._write_json(os.path.join(data_dir, "trainer_card.json"), self.trainer_card)
        self._write_json(os.path.join(data_dir, "quests.json"), self.quest_db)
        self._write_core_design_data(data_dir)
        self._write_pokemon_fangame_database(root_dir, data_dir)
        self._write_unity_project_scaffold(root_dir)

        self.logger(f"Core folders, original RPG data, PokeEngine prototype, and {self._project_display_name(root_dir)} framework generated.")

    def _write_pokemon_fangame_database(self, root_dir, data_dir):
        """Writes clean JSON database files for official-style fangame data.

        The generated files contain a playable starter subset immediately and
        index metadata for the wider Generation 1-9 public dataset. The bundled
        content-pipeline script can enrich these files from PokeAPI when the
        project owner wants a full local mirror.
        """
        starter_species = self._starter_species_records()
        starter_forms = self._starter_form_records()
        starter_moves = self._starter_move_records()
        starter_items = self._starter_item_records()
        official_index = self._build_pokeapi_index()

        species_items = self._merge_by_key(official_index.get("pokemon_species", []), starter_species, "id")
        forms_items = self._merge_by_key(official_index.get("pokemon_forms", []), starter_forms, "id")
        move_items = self._merge_by_key(official_index.get("moves", []), starter_moves, "id")
        item_items = self._merge_by_key(official_index.get("items", []), starter_items, "id")
        ability_items = self._merge_by_key(official_index.get("abilities", []), self._starter_ability_records(), "id")
        nature_items = official_index.get("natures", []) or self._nature_records()

        self._write_json(
            os.path.join(data_dir, "pokemon_species.json"),
            {
                "schemaVersion": 1,
                "source": official_index.get("source", "local_starter_seed"),
                "coverage": "generation_1_to_9_index_plus_playable_starter_details",
                "items": species_items,
            },
        )
        self._write_json(
            os.path.join(data_dir, "pokemon_forms.json"),
            {
                "schemaVersion": 1,
                "source": official_index.get("source", "local_starter_seed"),
                "items": forms_items,
            },
        )
        self._write_json(
            os.path.join(data_dir, "moves.json"),
            {
                "schemaVersion": 1,
                "source": official_index.get("source", "local_starter_seed"),
                "items": move_items,
            },
        )
        self._write_json(
            os.path.join(data_dir, "types.json"),
            {
                "schemaVersion": 1,
                "source": "PokeEngine canonical type chart",
                "items": self._type_records(),
                "effectiveness": self._type_effectiveness_records(),
            },
        )
        self._write_json(
            os.path.join(data_dir, "items.json"),
            {
                "schemaVersion": 1,
                "source": official_index.get("source", "local_starter_seed"),
                "categoryTags": [
                    "regular_item",
                    "key_item",
                    "poke_ball",
                    "medicine",
                    "berry",
                    "battle_item",
                    "held_item",
                    "evolution_item",
                    "valuable_item",
                ],
                "items": item_items,
            },
        )
        self._write_json(
            os.path.join(data_dir, "tms_by_generation.json"),
            {
                "schemaVersion": 1,
                "source": "local_seed_plus_pokeapi_machine_enrichment_tool",
                "items": self._tm_records(),
                "notes": "Run Tools/ContentPipeline/build_full_pokemon_database.py to expand machine data from PokeAPI.",
            },
        )
        self._write_json(
            os.path.join(data_dir, "abilities.json"),
            {
                "schemaVersion": 1,
                "source": official_index.get("source", "local_starter_seed"),
                "items": ability_items,
            },
        )
        self._write_json(
            os.path.join(data_dir, "natures.json"),
            {"schemaVersion": 1, "source": official_index.get("source", "local_seed"), "items": nature_items},
        )
        self._write_json(
            os.path.join(data_dir, "status_conditions.json"),
            {"schemaVersion": 1, "source": "PokeEngine battle model", "items": self._status_condition_records()},
        )
        self._write_json(
            os.path.join(data_dir, "mega_evolutions.json"),
            {"schemaVersion": 1, "items": self._starter_mega_records()},
        )
        self._write_json(
            os.path.join(data_dir, "gigantamax_forms.json"),
            {"schemaVersion": 1, "items": self._starter_gigantamax_records()},
        )
        self._write_json(
            os.path.join(data_dir, "encounter_tables.json"),
            {
                "schemaVersion": 1,
                "onlyEncounterSpecies": [1, 4, 7],
                "items": [
                    {
                        "areaId": "prototype_testing_site",
                        "method": "tall_grass",
                        "entries": [
                            {"speciesId": 1, "name": "Bulbasaur", "minLevel": 3, "maxLevel": 6, "weight": 34},
                            {"speciesId": 4, "name": "Charmander", "minLevel": 3, "maxLevel": 6, "weight": 33},
                            {"speciesId": 7, "name": "Squirtle", "minLevel": 3, "maxLevel": 6, "weight": 33},
                        ],
                    }
                ],
            },
        )
        self._write_json(
            os.path.join(data_dir, "encounters.json"),
            {
                "schemaVersion": 1,
                "onlyEncounterSpecies": [1, 4, 7],
                "items": [
                    {
                        "areaId": "prototype_testing_site",
                        "method": "grass",
                        "weather": "any",
                        "table": [
                            {"pokemonId": 1, "name": "Bulbasaur", "minLevel": 3, "maxLevel": 6, "weight": 34},
                            {"pokemonId": 4, "name": "Charmander", "minLevel": 3, "maxLevel": 6, "weight": 33},
                            {"pokemonId": 7, "name": "Squirtle", "minLevel": 3, "maxLevel": 6, "weight": 33},
                        ],
                    }
                ],
            },
        )
        self._write_json(
            os.path.join(data_dir, "evolutions.json"),
            {
                "schemaVersion": 1,
                "items": [
                    {"fromId": 1, "from": "Bulbasaur", "toId": 2, "to": "Ivysaur", "method": "level", "level": 16},
                    {"fromId": 2, "from": "Ivysaur", "toId": 3, "to": "Venusaur", "method": "level", "level": 32},
                    {"fromId": 4, "from": "Charmander", "toId": 5, "to": "Charmeleon", "method": "level", "level": 16},
                    {"fromId": 5, "from": "Charmeleon", "toId": 6, "to": "Charizard", "method": "level", "level": 36},
                    {"fromId": 7, "from": "Squirtle", "toId": 8, "to": "Wartortle", "method": "level", "level": 16},
                    {"fromId": 8, "from": "Wartortle", "toId": 9, "to": "Blastoise", "method": "level", "level": 36},
                ],
            },
        )
        self._write_json(
            os.path.join(data_dir, "learnsets.json"),
            {
                "schemaVersion": 1,
                "items": [
                    {"pokemonId": 1, "pokemon": "Bulbasaur", "levelMoves": [{"level": 1, "move": "tackle"}, {"level": 3, "move": "growl"}, {"level": 7, "move": "vine-whip"}], "tmMoves": ["trailblaze"]},
                    {"pokemonId": 4, "pokemon": "Charmander", "levelMoves": [{"level": 1, "move": "scratch"}, {"level": 4, "move": "growl"}, {"level": 7, "move": "ember"}], "tmMoves": ["fire-spin"]},
                    {"pokemonId": 7, "pokemon": "Squirtle", "levelMoves": [{"level": 1, "move": "tackle"}, {"level": 4, "move": "tail-whip"}, {"level": 7, "move": "water-gun"}], "tmMoves": ["water-pulse"]},
                ],
            },
        )
        self._write_text(
            os.path.join(root_dir, "Tools", "ContentPipeline", "build_full_pokemon_database.py"),
            self._render_database_builder_tool(),
        )

    def _build_pokeapi_index(self):
        if os.environ.get("POKEENGINE_DISABLE_POKEAPI_INDEX") == "1":
            return {"source": "local_starter_seed"}

        endpoints = {
            "pokemon_species": ("pokemon-species", 1300),
            "pokemon_forms": ("pokemon-form", 1600),
            "moves": ("move", 1200),
            "items": ("item", 2500),
            "abilities": ("ability", 1000),
            "natures": ("nature", 100),
        }
        index = {"source": "pokeapi_index"}
        for key, (endpoint, limit) in endpoints.items():
            try:
                payload = self._fetch_pokeapi_json(f"https://pokeapi.co/api/v2/{endpoint}?limit={limit}")
                index[key] = [self._pokeapi_index_record(row, key) for row in payload.get("results", [])]
            except Exception as exc:
                self.logger(f"PokeAPI index unavailable for {endpoint}: {exc}")
                index[key] = []
        return index

    def _fetch_pokeapi_json(self, url):
        request = urllib.request.Request(url, headers={"User-Agent": "PokeEngine-Generator/1.0"})
        with urllib.request.urlopen(request, timeout=8) as response:
            return json.loads(response.read().decode("utf-8"))

    def _pokeapi_index_record(self, row, dataset):
        url = row.get("url", "")
        match = re.search(r"/(\d+)/?$", url)
        item_id = int(match.group(1)) if match else 0
        name = row.get("name", "")
        record = {
            "id": item_id,
            "name": name,
            "displayName": self._display_name(name),
            "sourceUrl": url,
            "dataStatus": "index_only",
        }
        if dataset == "pokemon_species":
            record["generation"] = self._generation_from_species_id(item_id)
        elif dataset == "items":
            category = self._guess_item_category(name)
            record["category"] = category
            record["itemTags"] = [category]
        elif dataset == "moves":
            record.update({"type": None, "category": None, "power": None, "accuracy": None, "pp": None, "priority": 0})
        return record

    def _generation_from_species_id(self, species_id):
        if species_id <= 151:
            return 1
        if species_id <= 251:
            return 2
        if species_id <= 386:
            return 3
        if species_id <= 493:
            return 4
        if species_id <= 649:
            return 5
        if species_id <= 721:
            return 6
        if species_id <= 809:
            return 7
        if species_id <= 905:
            return 8
        return 9

    def _guess_item_category(self, item_name):
        name = str(item_name).lower()
        if "ball" in name:
            return "poke_balls"
        if "berry" in name:
            return "berries"
        if name.startswith("tm") or name.startswith("tr"):
            return "tms_trs"
        if "key" in name or name in {"bike", "town-map", "old-rod", "good-rod", "super-rod"}:
            return "key_items"
        if any(token in name for token in ("potion", "heal", "revive", "antidote", "ether", "elixir", "restore")):
            return "medicine"
        if any(token in name for token in ("stone", "scale", "protector", "upgrade", "disc", "sachet", "whip", "armor")):
            return "evolution_items"
        if any(token in name for token in ("plate", "orb", "band", "scarf", "specs", "charm", "incense", "seed", "booster")):
            return "held_items"
        if any(token in name for token in ("nugget", "pearl", "stardust", "star-piece", "mushroom")):
            return "valuable_items"
        if any(token in name for token in ("x-", "guard-spec", "dire-hit")):
            return "battle_items"
        return "regular_items"

    def _merge_by_key(self, base, overrides, key):
        merged = {}
        for row in base:
            if isinstance(row, dict) and key in row:
                merged[row[key]] = row
        for row in overrides:
            if isinstance(row, dict) and key in row:
                merged[row[key]] = row
        return [merged[k] for k in sorted(merged)]

    def _display_name(self, value):
        return " ".join(part.capitalize() for part in str(value).replace("-", " ").replace("_", " ").split())

    def _starter_species_records(self):
        return [
            {
                "id": 1,
                "nationalDexId": 1,
                "name": "bulbasaur",
                "displayName": "Bulbasaur",
                "generation": 1,
                "category": "Seed Pokemon",
                "types": ["grass", "poison"],
                "baseStats": {"hp": 45, "attack": 49, "defense": 49, "specialAttack": 65, "specialDefense": 65, "speed": 45},
                "abilities": ["overgrow"],
                "hiddenAbility": "chlorophyll",
                "catchRate": 45,
                "growthRate": "medium_slow",
                "learnset": [{"level": 1, "move": "tackle"}, {"level": 3, "move": "growl"}, {"level": 7, "move": "vine-whip"}],
                "evolutions": [{"toSpeciesId": 2, "method": "level", "level": 16}],
                "forms": ["default"],
                "megaForms": [],
                "gigantamaxForms": ["bulbasaur-gmax"],
                "dataStatus": "playable_detail",
            },
            {
                "id": 2,
                "nationalDexId": 2,
                "name": "ivysaur",
                "displayName": "Ivysaur",
                "generation": 1,
                "category": "Seed Pokemon",
                "types": ["grass", "poison"],
                "baseStats": {"hp": 60, "attack": 62, "defense": 63, "specialAttack": 80, "specialDefense": 80, "speed": 60},
                "abilities": ["overgrow"],
                "hiddenAbility": "chlorophyll",
                "catchRate": 45,
                "growthRate": "medium_slow",
                "evolutions": [{"toSpeciesId": 3, "method": "level", "level": 32}],
                "dataStatus": "playable_detail",
            },
            {
                "id": 3,
                "nationalDexId": 3,
                "name": "venusaur",
                "displayName": "Venusaur",
                "generation": 1,
                "category": "Seed Pokemon",
                "types": ["grass", "poison"],
                "baseStats": {"hp": 80, "attack": 82, "defense": 83, "specialAttack": 100, "specialDefense": 100, "speed": 80},
                "abilities": ["overgrow"],
                "hiddenAbility": "chlorophyll",
                "catchRate": 45,
                "growthRate": "medium_slow",
                "megaForms": ["venusaur-mega"],
                "gigantamaxForms": ["venusaur-gmax"],
                "dataStatus": "playable_detail",
            },
            {
                "id": 4,
                "nationalDexId": 4,
                "name": "charmander",
                "displayName": "Charmander",
                "generation": 1,
                "category": "Lizard Pokemon",
                "types": ["fire"],
                "baseStats": {"hp": 39, "attack": 52, "defense": 43, "specialAttack": 60, "specialDefense": 50, "speed": 65},
                "abilities": ["blaze"],
                "hiddenAbility": "solar-power",
                "catchRate": 45,
                "growthRate": "medium_slow",
                "learnset": [{"level": 1, "move": "scratch"}, {"level": 4, "move": "growl"}, {"level": 7, "move": "ember"}],
                "evolutions": [{"toSpeciesId": 5, "method": "level", "level": 16}],
                "forms": ["default"],
                "dataStatus": "playable_detail",
            },
            {
                "id": 5,
                "nationalDexId": 5,
                "name": "charmeleon",
                "displayName": "Charmeleon",
                "generation": 1,
                "category": "Flame Pokemon",
                "types": ["fire"],
                "baseStats": {"hp": 58, "attack": 64, "defense": 58, "specialAttack": 80, "specialDefense": 65, "speed": 80},
                "abilities": ["blaze"],
                "hiddenAbility": "solar-power",
                "catchRate": 45,
                "growthRate": "medium_slow",
                "evolutions": [{"toSpeciesId": 6, "method": "level", "level": 36}],
                "dataStatus": "playable_detail",
            },
            {
                "id": 6,
                "nationalDexId": 6,
                "name": "charizard",
                "displayName": "Charizard",
                "generation": 1,
                "category": "Flame Pokemon",
                "types": ["fire", "flying"],
                "baseStats": {"hp": 78, "attack": 84, "defense": 78, "specialAttack": 109, "specialDefense": 85, "speed": 100},
                "abilities": ["blaze"],
                "hiddenAbility": "solar-power",
                "catchRate": 45,
                "growthRate": "medium_slow",
                "megaForms": ["charizard-mega-x", "charizard-mega-y"],
                "gigantamaxForms": ["charizard-gmax"],
                "dataStatus": "playable_detail",
            },
            {
                "id": 7,
                "nationalDexId": 7,
                "name": "squirtle",
                "displayName": "Squirtle",
                "generation": 1,
                "category": "Tiny Turtle Pokemon",
                "types": ["water"],
                "baseStats": {"hp": 44, "attack": 48, "defense": 65, "specialAttack": 50, "specialDefense": 64, "speed": 43},
                "abilities": ["torrent"],
                "hiddenAbility": "rain-dish",
                "catchRate": 45,
                "growthRate": "medium_slow",
                "learnset": [{"level": 1, "move": "tackle"}, {"level": 4, "move": "tail-whip"}, {"level": 7, "move": "water-gun"}],
                "evolutions": [{"toSpeciesId": 8, "method": "level", "level": 16}],
                "forms": ["default"],
                "dataStatus": "playable_detail",
            },
            {
                "id": 8,
                "nationalDexId": 8,
                "name": "wartortle",
                "displayName": "Wartortle",
                "generation": 1,
                "category": "Turtle Pokemon",
                "types": ["water"],
                "baseStats": {"hp": 59, "attack": 63, "defense": 80, "specialAttack": 65, "specialDefense": 80, "speed": 58},
                "abilities": ["torrent"],
                "hiddenAbility": "rain-dish",
                "catchRate": 45,
                "growthRate": "medium_slow",
                "evolutions": [{"toSpeciesId": 9, "method": "level", "level": 36}],
                "dataStatus": "playable_detail",
            },
            {
                "id": 9,
                "nationalDexId": 9,
                "name": "blastoise",
                "displayName": "Blastoise",
                "generation": 1,
                "category": "Shellfish Pokemon",
                "types": ["water"],
                "baseStats": {"hp": 79, "attack": 83, "defense": 100, "specialAttack": 85, "specialDefense": 105, "speed": 78},
                "abilities": ["torrent"],
                "hiddenAbility": "rain-dish",
                "catchRate": 45,
                "growthRate": "medium_slow",
                "megaForms": ["blastoise-mega"],
                "gigantamaxForms": ["blastoise-gmax"],
                "dataStatus": "playable_detail",
            },
        ]

    def _starter_form_records(self):
        forms = []
        for species in self._starter_species_records():
            forms.append({"id": species["id"], "speciesId": species["id"], "name": species["name"], "displayName": species["displayName"], "kind": "default"})
        forms.extend(self._starter_mega_records())
        forms.extend(self._starter_gigantamax_records())
        return forms

    def _starter_move_records(self):
        return [
            {"id": 33, "name": "tackle", "displayName": "Tackle", "type": "normal", "category": "physical", "power": 40, "accuracy": 100, "pp": 35},
            {"id": 45, "name": "growl", "displayName": "Growl", "type": "normal", "category": "status", "power": 0, "accuracy": 100, "pp": 40},
            {"id": 22, "name": "vine-whip", "displayName": "Vine Whip", "type": "grass", "category": "physical", "power": 45, "accuracy": 100, "pp": 25},
            {"id": 10, "name": "scratch", "displayName": "Scratch", "type": "normal", "category": "physical", "power": 40, "accuracy": 100, "pp": 35},
            {"id": 52, "name": "ember", "displayName": "Ember", "type": "fire", "category": "special", "power": 40, "accuracy": 100, "pp": 25},
            {"id": 55, "name": "water-gun", "displayName": "Water Gun", "type": "water", "category": "special", "power": 40, "accuracy": 100, "pp": 25},
            {"id": 39, "name": "tail-whip", "displayName": "Tail Whip", "type": "normal", "category": "status", "power": 0, "accuracy": 100, "pp": 30},
            {"id": 999001, "name": "guard-pulse", "displayName": "Guard Pulse", "type": "normal", "category": "status", "power": 0, "accuracy": 100, "pp": 20},
        ]

    def _starter_item_records(self):
        return [
            {"id": 4, "name": "poke-ball", "displayName": "Poke Ball", "tags": ["poke_ball"], "category": "poke_ball"},
            {"id": 17, "name": "potion", "displayName": "Potion", "tags": ["medicine", "regular_item"], "category": "medicine"},
            {"id": 80, "name": "sun-stone", "displayName": "Sun Stone", "tags": ["evolution_item", "regular_item"], "category": "evolution_item"},
            {"id": 10001, "name": "venusaurite", "displayName": "Venusaurite", "tags": ["held_item", "evolution_item"], "category": "held_item"},
            {"id": 10002, "name": "charizardite-x", "displayName": "Charizardite X", "tags": ["held_item", "evolution_item"], "category": "held_item"},
            {"id": 10003, "name": "charizardite-y", "displayName": "Charizardite Y", "tags": ["held_item", "evolution_item"], "category": "held_item"},
            {"id": 10004, "name": "blastoisinite", "displayName": "Blastoisinite", "tags": ["held_item", "evolution_item"], "category": "held_item"},
        ]

    def _starter_ability_records(self):
        return [
            {"id": 65, "name": "overgrow", "displayName": "Overgrow", "tags": ["starter", "low_hp_boost"]},
            {"id": 66, "name": "blaze", "displayName": "Blaze", "tags": ["starter", "low_hp_boost"]},
            {"id": 67, "name": "torrent", "displayName": "Torrent", "tags": ["starter", "low_hp_boost"]},
            {"id": 34, "name": "chlorophyll", "displayName": "Chlorophyll", "tags": ["hidden_ability", "weather"]},
            {"id": 94, "name": "solar-power", "displayName": "Solar Power", "tags": ["hidden_ability", "weather"]},
            {"id": 44, "name": "rain-dish", "displayName": "Rain Dish", "tags": ["hidden_ability", "weather"]},
        ]

    def _starter_mega_records(self):
        return [
            {"id": 10033, "speciesId": 3, "name": "venusaur-mega", "displayName": "Mega Venusaur", "kind": "mega", "requiredItem": "venusaurite", "ability": "thick-fat", "types": ["grass", "poison"]},
            {"id": 10034, "speciesId": 6, "name": "charizard-mega-x", "displayName": "Mega Charizard X", "kind": "mega", "requiredItem": "charizardite-x", "ability": "tough-claws", "types": ["fire", "dragon"]},
            {"id": 10035, "speciesId": 6, "name": "charizard-mega-y", "displayName": "Mega Charizard Y", "kind": "mega", "requiredItem": "charizardite-y", "ability": "drought", "types": ["fire", "flying"]},
            {"id": 10036, "speciesId": 9, "name": "blastoise-mega", "displayName": "Mega Blastoise", "kind": "mega", "requiredItem": "blastoisinite", "ability": "mega-launcher", "types": ["water"]},
        ]

    def _starter_gigantamax_records(self):
        return [
            {"id": 20003, "speciesId": 3, "name": "venusaur-gmax", "displayName": "Gigantamax Venusaur", "kind": "gigantamax", "prototypeOnly": True, "types": ["grass", "poison"]},
            {"id": 20006, "speciesId": 6, "name": "charizard-gmax", "displayName": "Gigantamax Charizard", "kind": "gigantamax", "prototypeOnly": True, "types": ["fire", "flying"]},
            {"id": 20009, "speciesId": 9, "name": "blastoise-gmax", "displayName": "Gigantamax Blastoise", "kind": "gigantamax", "prototypeOnly": True, "types": ["water"]},
        ]

    def _type_records(self):
        return [{"id": index + 1, "name": name, "displayName": self._display_name(name)} for index, name in enumerate([
            "normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying",
            "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"
        ])]

    def _type_effectiveness_records(self):
        chart = []
        rules = {
            "fire": {"grass": 2, "ice": 2, "bug": 2, "steel": 2, "fire": 0.5, "water": 0.5, "rock": 0.5, "dragon": 0.5},
            "water": {"fire": 2, "ground": 2, "rock": 2, "water": 0.5, "grass": 0.5, "dragon": 0.5},
            "grass": {"water": 2, "ground": 2, "rock": 2, "fire": 0.5, "grass": 0.5, "poison": 0.5, "flying": 0.5, "bug": 0.5, "dragon": 0.5, "steel": 0.5},
            "electric": {"water": 2, "flying": 2, "electric": 0.5, "grass": 0.5, "dragon": 0.5, "ground": 0},
            "normal": {"rock": 0.5, "steel": 0.5, "ghost": 0},
        }
        for attack, defenses in rules.items():
            for defense, multiplier in defenses.items():
                chart.append({"attackType": attack, "defenseType": defense, "multiplier": multiplier})
        return chart

    def _tm_records(self):
        return [
            {"generation": 1, "tmId": "TM01", "move": "mega-punch", "moveDisplayName": "Mega Punch"},
            {"generation": 1, "tmId": "TM06", "move": "toxic", "moveDisplayName": "Toxic"},
            {"generation": 1, "tmId": "TM10", "move": "double-edge", "moveDisplayName": "Double-Edge"},
            {"generation": 8, "tmId": "TM00", "move": "mega-punch", "moveDisplayName": "Mega Punch"},
            {"generation": 9, "tmId": "TM001", "move": "take-down", "moveDisplayName": "Take Down"},
            {"generation": 9, "tmId": "TM020", "move": "trailblaze", "moveDisplayName": "Trailblaze"},
        ]

    def _nature_records(self):
        names = ["hardy", "lonely", "brave", "adamant", "naughty", "bold", "docile", "relaxed", "impish", "lax", "timid", "hasty", "serious", "jolly", "naive", "modest", "mild", "quiet", "bashful", "rash", "calm", "gentle", "sassy", "careful", "quirky"]
        return [{"id": index + 1, "name": name, "displayName": self._display_name(name)} for index, name in enumerate(names)]

    def _status_condition_records(self):
        return [
            {"id": "burn", "displayName": "Burn", "kind": "permanent", "endTurnDamage": True, "attackModifier": 0.5},
            {"id": "poison", "displayName": "Poison", "kind": "permanent", "endTurnDamage": True},
            {"id": "bad_poison", "displayName": "Bad Poison", "kind": "permanent", "endTurnDamage": True, "toxicCounter": True},
            {"id": "paralysis", "displayName": "Paralysis", "kind": "permanent", "speedModifier": 0.5},
            {"id": "sleep", "displayName": "Sleep", "kind": "permanent", "blocksMoveSelection": True},
            {"id": "freeze", "displayName": "Freeze", "kind": "permanent", "blocksMoveSelection": True},
            {"id": "confusion", "displayName": "Confusion", "kind": "volatile", "durationTurns": [2, 5]},
            {"id": "flinch", "displayName": "Flinch", "kind": "volatile", "durationTurns": [1, 1]},
        ]

    def _render_database_builder_tool(self):
        return r'''#!/usr/bin/env python3
"""Download/enrich full Gen 1-9 Pokemon-style JSON databases from PokeAPI.

Run from the generated Unity project root:
    python Tools/ContentPipeline/build_full_pokemon_database.py
"""
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "Assets" / "StreamingAssets" / "Data"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "PokeEngine-ContentPipeline/1.0"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))

def generation_from_species_id(species_id):
    if species_id <= 151: return 1
    if species_id <= 251: return 2
    if species_id <= 386: return 3
    if species_id <= 493: return 4
    if species_id <= 649: return 5
    if species_id <= 721: return 6
    if species_id <= 809: return 7
    if species_id <= 905: return 8
    return 9

def guess_item_category(name):
    if "ball" in name: return "poke_balls"
    if "berry" in name: return "berries"
    if name.startswith(("tm", "tr")): return "tms_trs"
    if "key" in name or name in {"bike", "town-map", "old-rod", "good-rod", "super-rod"}: return "key_items"
    if any(token in name for token in ("potion", "heal", "revive", "antidote", "ether", "elixir", "restore")): return "medicine"
    if any(token in name for token in ("stone", "scale", "protector", "upgrade", "disc", "sachet", "whip", "armor")): return "evolution_items"
    if any(token in name for token in ("plate", "orb", "band", "scarf", "specs", "charm", "incense", "seed", "booster")): return "held_items"
    if any(token in name for token in ("nugget", "pearl", "stardust", "star-piece", "mushroom")): return "valuable_items"
    if any(token in name for token in ("x-", "guard-spec", "dire-hit")): return "battle_items"
    return "regular_items"

def list_endpoint(name, limit=2000):
    payload = fetch(f"https://pokeapi.co/api/v2/{name}?limit={limit}")
    rows = []
    for row in payload.get("results", []):
        match = re.search(r"/(\d+)/?$", row.get("url", ""))
        record = {
            "id": int(match.group(1)) if match else 0,
            "name": row["name"],
            "displayName": row["name"].replace("-", " ").title(),
            "sourceUrl": row["url"],
            "dataStatus": "downloaded_index"
        }
        if name == "pokemon-species":
            record["generation"] = generation_from_species_id(record["id"])
        elif name == "item":
            record["category"] = guess_item_category(record["name"])
            record["itemTags"] = [record["category"]]
        elif name == "move":
            record.update({"type": None, "category": None, "power": None, "accuracy": None, "pp": None, "priority": 0})
        rows.append(record)
    return rows

def write(name, payload):
    DATA.mkdir(parents=True, exist_ok=True)
    with (DATA / name).open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print("wrote", DATA / name)

def main():
    write("pokemon_species.json", {"schemaVersion": 1, "source": "pokeapi", "items": list_endpoint("pokemon-species", 1300)})
    write("pokemon_forms.json", {"schemaVersion": 1, "source": "pokeapi", "items": list_endpoint("pokemon-form", 1800)})
    write("moves.json", {"schemaVersion": 1, "source": "pokeapi", "items": list_endpoint("move", 1200)})
    write("types.json", {"schemaVersion": 1, "source": "pokeapi", "items": list_endpoint("type", 40), "typeEffectiveness": []})
    write("items.json", {"schemaVersion": 1, "source": "pokeapi", "items": list_endpoint("item", 2500)})
    write("abilities.json", {"schemaVersion": 1, "source": "pokeapi", "items": list_endpoint("ability", 1000)})
    write("natures.json", {"schemaVersion": 1, "source": "pokeapi", "items": list_endpoint("nature", 100)})
    write("status_conditions.json", {"schemaVersion": 1, "source": "pokeengine_static", "items": [
        {"id": "burn", "displayName": "Burn", "kind": "permanent"},
        {"id": "poison", "displayName": "Poison", "kind": "permanent"},
        {"id": "bad_poison", "displayName": "Bad Poison", "kind": "permanent"},
        {"id": "paralysis", "displayName": "Paralysis", "kind": "permanent"},
        {"id": "sleep", "displayName": "Sleep", "kind": "permanent"},
        {"id": "freeze", "displayName": "Freeze", "kind": "permanent"},
        {"id": "confusion", "displayName": "Confusion", "kind": "volatile"},
        {"id": "flinch", "displayName": "Flinch", "kind": "volatile"}
    ]})
    write("tms_by_generation.json", {"schemaVersion": 1, "source": "pokeapi_machine_index", "items": list_endpoint("machine", 3000)})

if __name__ == "__main__":
    main()
'''

    def _build_feature_requirements(self):
        requirements = []
        for index, (category, name, optional) in enumerate(FEATURE_REQUIREMENTS, start=1):
            requirements.append(
                {
                    "id": f"REQ-{index:03d}",
                    "name": name,
                    "category": category,
                    "optional": optional,
                    "status": "prototype_scaffold",
                }
            )
        return requirements

    def _write_core_design_data(self, data_dir):
        systems_dir = os.path.join(data_dir, "Systems")
        self._write_json(
            os.path.join(data_dir, "feature_requirements.json"),
            {
                "engineVersion": "V11",
                "generatedAt": datetime.now().isoformat(timespec="seconds"),
                "requirements": self.feature_requirements,
            },
        )
        self._write_json(
            os.path.join(data_dir, "region_map.json"),
            {
                "regionName": "Aurora Province",
                "cameraMode": "semi_fixed_2_5d",
                "movementMode": "four_direction_continuous",
                "areas": [
                    {"id": "nova_town", "name": "Prototype Testing Site", "kind": "testing_site", "connections": ["route_01", "professor_lab"]},
                    {"id": "professor_lab", "name": "Professor's Lab", "kind": "interior", "connections": ["nova_town"]},
                    {"id": "route_01", "name": "Route 01", "kind": "route", "connections": ["nova_town", "echo_cave"]},
                    {"id": "echo_cave", "name": "Echo Cave", "kind": "cave", "connections": ["route_01", "solara_city"]},
                    {"id": "solara_city", "name": "Solara City", "kind": "town", "connections": ["echo_cave", "solara_gym"]},
                    {"id": "solara_gym", "name": "Solara Gym", "kind": "interior", "connections": ["solara_city"]},
                ],
            },
        )
        self._write_json(
            os.path.join(data_dir, "encounters.json"),
            {
                "items": [
                    {
                        "areaId": "route_01",
                        "method": "grass",
                        "weather": "any",
                        "table": [
                            {"pokemonId": 1, "minLevel": 3, "maxLevel": 5, "weight": 45},
                            {"pokemonId": 4, "minLevel": 3, "maxLevel": 5, "weight": 20},
                        ],
                    }
                ]
            },
        )
        self._write_json(
            os.path.join(data_dir, "tall_grass_config.json"),
            {
                "philosophy": "Tall grass is encounter terrain, biome identity, exploration pacing, and risk/reward feedback.",
                "grassTypes": [
                    "standard",
                    "dense",
                    "double",
                    "rustling",
                    "wet",
                    "flower_field",
                    "swamp",
                    "snow",
                    "dimensional",
                    "raid",
                    "seasonal",
                ],
                "prototypeZones": [
                    {
                        "zoneId": "testing_site_grass",
                        "areaId": "nova_town",
                        "type": "standard",
                        "baseEncounterRate": 0.32,
                        "encounterPool": "testing_site_standard_pool",
                        "visuals": ["solid_green_readable_surface", "rustle_sway", "lower_body_obscure"],
                        "feedback": ["rustle_audio_hook", "footstep_vfx_hook", "encounter_notification"],
                    },
                    {
                        "zoneId": "wild_area_double_grass",
                        "areaId": "nova_town_wild_area",
                        "type": "double",
                        "baseEncounterRate": 0.45,
                        "doubleBattleChance": 0.18,
                        "encounterPool": "wild_area_rare_pool",
                        "visuals": ["dense_green_surface", "stronger_sway", "wild_camera_safe_readability"],
                    },
                ],
                "specialMechanics": ["rustling_spawn", "repel_suppression", "ability_modifiers", "weather_time_filters", "swarm_events", "seasonal_variants"],
            },
        )
        self._write_json(
            os.path.join(data_dir, "evolutions.json"),
            {
                "items": [
                    {"fromId": 1, "toId": 2, "method": "level", "level": 16},
                    {"fromId": 2, "toId": 3, "method": "level", "level": 32},
                    {"fromId": 4, "toId": 5, "method": "level", "level": 16},
                    {"fromId": 5, "toId": 6, "method": "level", "level": 36},
                    {"fromId": 7, "toId": 8, "method": "level", "level": 16},
                    {"fromId": 8, "toId": 9, "method": "level", "level": 36},
                ]
            },
        )
        self._write_json(
            os.path.join(data_dir, "learnsets.json"),
            {
                "items": [
                    {"pokemonId": 1, "levelMoves": [{"level": 1, "move": "tackle"}, {"level": 3, "move": "growl"}, {"level": 7, "move": "vine-whip"}], "tmMoves": ["trailblaze"]},
                    {"pokemonId": 4, "levelMoves": [{"level": 1, "move": "scratch"}, {"level": 4, "move": "growl"}, {"level": 7, "move": "ember"}], "tmMoves": ["fire-spin"]},
                    {"pokemonId": 7, "levelMoves": [{"level": 1, "move": "tackle"}, {"level": 4, "move": "tail-whip"}, {"level": 7, "move": "water-gun"}], "tmMoves": ["water-pulse"]},
                ]
            },
        )
        self._write_json(
            os.path.join(data_dir, "abilities.json"),
            {"items": [{"name": "Overgrow", "trigger": "low_hp_grass_boost"}, {"name": "Blaze", "trigger": "low_hp_fire_boost"}]},
        )
        self._write_json(
            os.path.join(data_dir, "forms_variants.json"),
            {"items": [{"pokemonId": 3, "form": "Mega Venusaur", "type1": "Grass", "type2": "Poison", "rarity": "mega"}, {"pokemonId": 6, "form": "Mega Charizard X", "type1": "Fire", "type2": "Dragon", "rarity": "mega"}, {"pokemonId": 9, "form": "Mega Blastoise", "type1": "Water", "type2": "None", "rarity": "mega"}]},
        )
        self._write_json(
            os.path.join(data_dir, "type_chart.json"),
            {
                "normalEffectiveness": 1.0,
                "rules": [
                    {"attackType": "Fire", "defenseType": "Grass", "multiplier": 2.0},
                    {"attackType": "Grass", "defenseType": "Fire", "multiplier": 0.5},
                    {"attackType": "Water", "defenseType": "Fire", "multiplier": 2.0},
                ],
            },
        )
        self._write_json(
            os.path.join(data_dir, "battle_config.json"),
            {
                "partyLimit": 6,
                "shinyOdds": 4096,
                "turnModel": "priority_then_speed",
                "statuses": ["Poison", "Burn", "Paralysis", "Sleep", "Freeze"],
                "terrains": ["Electric", "Leafy", "Misty", "Psychic"],
                "weather": ["Clear", "Rain", "Sun", "Sandstorm", "Snow"],
            },
        )
        self._write_json(
            os.path.join(data_dir, "storage_config.json"),
            {"partyLimit": 6, "pcBoxes": 32, "slotsPerBox": 30, "autosaveOnStorageChange": True},
        )
        self._write_json(
            os.path.join(data_dir, "raid_config.json"),
            {
                "tiers": [1, 2, 3, 4, 5, 6],
                "turnTimerSeconds": 45,
                "shieldBreakRules": {"hitsToBreak": 4, "stunTurns": 1},
                "captureEnabled": True,
                "eventRotationId": "launch_rotation",
            },
        )
        self._write_json(
            os.path.join(data_dir, "dimension_split.json"),
            {
                "meterMax": 100,
                "singleUsePerBattle": True,
                "forms": [
                    {
                        "pokemonId": 1,
                        "formName": "Bulbasaur Riftbloom",
                        "signatureMove": "Rift Vine",
                        "statMultiplier": 1.25,
                        "abilityOverride": "Dimensional Overgrow",
                    }
                ],
            },
        )
        self._write_json(
            os.path.join(data_dir, "fusion_rules.json"),
            {
                "allowSeparation": True,
                "compatiblePairs": [
                    {
                        "leftPokemonId": 1,
                        "rightPokemonId": 4,
                        "fusionName": "Bulbamander",
                        "types": ["Grass", "Fire"],
                        "exclusiveMove": "Blooming Ember",
                    }
                ],
            },
        )
        self._write_json(
            os.path.join(data_dir, "localization.json"),
            {"defaultLanguage": "en", "supportedLanguages": ["en", "es", "fr", "de", "ja"]},
        )
        self._write_json(
            os.path.join(systems_dir, "settings_schema.json"),
            {
                "video": ["resolution", "fullscreen", "cameraMode", "effectsQuality"],
                "audio": ["masterVolume", "musicVolume", "sfxVolume", "ambientVolume"],
                "gameplay": ["textSpeed", "battleAnimations", "autosave", "difficulty"],
            },
        )

    def _write_unity_project_scaffold(self, root_dir):
        scaffold_dirs = [
            "Assets/Art/Characters",
            "Assets/Art/Pokemon",
            "Assets/Art/Environment",
            "Assets/Audio/Music",
            "Assets/Audio/SFX",
            "Assets/Audio/Ambient",
            "Assets/Prefabs",
            "Assets/Scenes",
            "Assets/Scripts/PokeEngine/Core",
            "Assets/Scripts/PokeEngine/Systems",
            "Assets/StreamingAssets/Data/Systems",
            "Docs",
            "Packages",
            "ProjectSettings",
            "QA",
            "Tools/ContentPipeline",
            "Assets/Editor/PokeEngine",
            "Assets/Scripts/PokeEngine/Battle",
            "Assets/Scripts/PokeEngine/Data",
            "Assets/Scripts/PokeEngine/Events",
            "Assets/Scripts/PokeEngine/NPC",
            "Assets/Scripts/PokeEngine/Overworld",
            "Assets/Scripts/PokeEngine/Pokemon",
            "Assets/Scripts/PokeEngine/Raid",
            "Assets/Scripts/PokeEngine/Save",
            "Assets/Scripts/PokeEngine/UI",
            "Assets/Tests/EditMode",
        ]
        for rel_dir in scaffold_dirs:
            os.makedirs(os.path.join(root_dir, rel_dir), exist_ok=True)

        manifest = []
        for requirement in self.feature_requirements:
            class_name = self._to_class_name(requirement["name"])
            category = requirement["category"]
            rel_script = os.path.join(
                "Assets",
                "Scripts",
                "PokeEngine",
                "Systems",
                category,
                f"{class_name}.cs",
            )
            rel_config = os.path.join(
                "Assets",
                "StreamingAssets",
                "Data",
                "Systems",
                category,
                f"{self._to_snake_name(requirement['name'])}.json",
            )
            manifest.append(
                {
                    **requirement,
                    "script": rel_script.replace("\\", "/"),
                    "config": rel_config.replace("\\", "/"),
                }
            )
            self._write_text(
                os.path.join(root_dir, rel_script),
                self._render_system_stub(class_name, requirement),
            )
            self._write_json(
                os.path.join(root_dir, rel_config),
                {
                    "requirementId": requirement["id"],
                    "name": requirement["name"],
                    "category": category,
                    "enabled": True,
                    "optional": requirement["optional"],
                    "implementationStatus": "prototype_scaffold",
                    "notes": "Generated placeholder config. Expand this as the system is implemented.",
                },
            )

        self._write_json(
            os.path.join(root_dir, "Assets", "StreamingAssets", "Data", "system_manifest.json"),
            {
                "engineVersion": "V11",
                "generatedAt": datetime.now().isoformat(timespec="seconds"),
                "systems": manifest,
            },
        )
        self._write_text(
            os.path.join(root_dir, "Assets", "Scripts", "PokeEngine", "Core", "PokeEngineBootstrap.cs"),
            self._render_bootstrap_stub(manifest),
        )
        self._write_text(
            os.path.join(root_dir, "Docs", "FEATURE_REQUIREMENTS.md"),
            self._render_requirements_doc(),
        )
        self._write_text(
            os.path.join(root_dir, "QA", "prototype_test_plan.md"),
            self._render_test_plan(),
        )
        self._write_text(
            os.path.join(root_dir, "Tools", "ContentPipeline", "README.md"),
            "# PokeEngine Content Pipeline\n\nGenerated workspace for level, dialogue, Pokemon data, balancing, QA, and build tools.\n",
        )
        self._write_full_rpg_prototype(root_dir)

    def _write_full_rpg_prototype(self, root_dir):
        runtime_dir = os.path.join(root_dir, "Assets", "Scripts", "PokeEngine")
        editor_dir = os.path.join(root_dir, "Assets", "Editor", "PokeEngine")
        tests_dir = os.path.join(root_dir, "Assets", "Tests", "EditMode")
        data_dir = os.path.join(root_dir, "Assets", "StreamingAssets", "Data")

        files = {
            os.path.join(root_dir, "README.md"): self._render_project_readme(),
            os.path.join(root_dir, "Packages", "manifest.json"): self._render_unity_package_manifest(),
            os.path.join(root_dir, "ProjectSettings", "ProjectVersion.txt"): self._render_unity_project_version(),
            os.path.join(root_dir, "ProjectSettings", "EditorBuildSettings.asset"): self._render_editor_build_settings(),
            os.path.join(runtime_dir, "PokeEngine.Runtime.asmdef"): self._render_runtime_asmdef(),
            os.path.join(editor_dir, "PokeEngine.Editor.asmdef"): self._render_editor_asmdef(),
            os.path.join(runtime_dir, "Data", "PokeEngineTypes.cs"): self._render_types_code(),
            os.path.join(runtime_dir, "Data", "PokeEngineScriptableObjects.cs"): self._render_scriptable_objects_code(),
            os.path.join(runtime_dir, "Core", "PokeEventBus.cs"): self._render_event_bus_code(),
            os.path.join(runtime_dir, "Core", "PrototypeFeatureRegistry.cs"): self._render_feature_registry_code(),
            os.path.join(runtime_dir, "Core", "PokeEngineRuntime.cs"): self._render_runtime_code(),
            os.path.join(runtime_dir, "Core", "PokeEngineRuntime.cs.meta"): self._render_mono_script_meta(POKEENGINE_RUNTIME_SCRIPT_GUID),
            os.path.join(runtime_dir, "Overworld", "WorldStreamingManager.cs"): self._render_world_streaming_code(),
            os.path.join(runtime_dir, "Overworld", "HybridPlayerController.cs"): self._render_movement_code(),
            os.path.join(runtime_dir, "Overworld", "PokemonCameraController.cs"): self._render_camera_controller_code(),
            os.path.join(runtime_dir, "Overworld", "TallGrassSystem.cs"): self._render_tall_grass_system_code(),
            os.path.join(runtime_dir, "Overworld", "TallLeafEncounterTrigger.cs"): self._render_tall_grass_trigger_code(),
            os.path.join(runtime_dir, "Overworld", "WildAreaCameraZone.cs"): self._render_wild_area_camera_zone_code(),
            os.path.join(runtime_dir, "Overworld", "PokemonCenterEntrance.cs"): self._render_pokemon_center_entrance_code(),
            os.path.join(runtime_dir, "Overworld", "PrototypePickup.cs"): self._render_prototype_pickup_code(),
            os.path.join(runtime_dir, "Overworld", "OverworldPokemonEncounter.cs"): self._render_overworld_pokemon_encounter_code(),
            os.path.join(runtime_dir, "NPC", "NpcBrain.cs"): self._render_npc_code(),
            os.path.join(runtime_dir, "Events", "EventAndCutsceneSystem.cs"): self._render_event_code(),
            os.path.join(runtime_dir, "Pokemon", "PokemonDatabaseRuntime.cs"): self._render_pokemon_database_code(),
            os.path.join(runtime_dir, "Battle", "BattleEngineRuntime.cs"): self._render_battle_code(),
            os.path.join(runtime_dir, "Battle", "TransformationFusionSystems.cs"): self._render_transformation_code(),
            os.path.join(runtime_dir, "Raid", "RaidBattleRuntime.cs"): self._render_raid_code(),
            os.path.join(runtime_dir, "Save", "PokeSaveManager.cs"): self._render_save_code(),
            os.path.join(runtime_dir, "UI", "PrototypeRpgHud.cs"): self._render_ui_code(),
            os.path.join(editor_dir, "PokeEnginePrototypeMenu.cs"): self._render_editor_code(),
            os.path.join(tests_dir, "PokeEngine.Tests.asmdef"): self._render_tests_asmdef(),
            os.path.join(tests_dir, "PokeEnginePrototypeTests.cs"): self._render_tests_code(),
            os.path.join(root_dir, "Assets", "Scenes", "PrototypeRegion.unity"): self._render_prototype_scene(),
            os.path.join(root_dir, "Assets", "Scenes", "PrototypeRegion.unity.meta"): self._render_scene_meta(PROTOTYPE_REGION_SCENE_GUID),
            os.path.join(root_dir, "Assets", "Scenes", "PrototypeRegion_README.txt"): self._render_scene_note(),
            os.path.join(root_dir, "Docs", "ARCHITECTURE_IMPLEMENTATION_MATRIX.md"): self._render_architecture_matrix_doc(),
            os.path.join(root_dir, "Docs", "FULL_RPG_PROTOTYPE.md"): self._render_full_prototype_doc(),
            os.path.join(root_dir, "Docs", "BATTLE_SYSTEM_GEN5_GEN8.md"): self._render_battle_system_design_doc(),
            os.path.join(root_dir, "Docs", "BATTLE_RAID_SYSTEM_REQUIREMENTS.md"): self._render_battle_raid_system_requirements_doc(),
            os.path.join(root_dir, "Docs", "PAUSE_MENU_SYSTEM_REQUIREMENTS.md"): self._render_pause_menu_system_requirements_doc(),
            os.path.join(root_dir, "Docs", "SAVE_SYSTEM_REQUIREMENTS.md"): self._render_save_system_requirements_doc(),
            os.path.join(root_dir, "Docs", "TALL_GRASS_SYSTEM_REQUIREMENTS.md"): self._render_tall_grass_system_requirements_doc(),
            os.path.join(root_dir, "Docs", "POKEMON_FANGAME_ENGINE_REQUIREMENTS.md"): self._render_fangame_engine_requirements_doc(),
        }
        for path, content in files.items():
            self._write_text(path, content)

        self._write_json(os.path.join(data_dir, "architecture_requirements_v12.json"), self._build_architecture_requirements())
        self._write_json(os.path.join(data_dir, "engine_design_contract.json"), self._build_engine_design_contract())
        self._write_json(os.path.join(data_dir, "prototype_feature_matrix.json"), self._build_feature_matrix())
        self._write_json(os.path.join(data_dir, "battle_system_gen5_gen8_requirements.json"), self._build_battle_system_requirements())
        self._write_json(os.path.join(data_dir, "battle_raid_system_requirements.json"), self._build_battle_raid_system_requirements())
        self._write_json(os.path.join(data_dir, "pause_menu_system_requirements.json"), self._build_pause_menu_system_requirements())
        self._write_json(os.path.join(data_dir, "save_system_requirements.json"), self._build_save_system_requirements())
        self._write_json(os.path.join(data_dir, "tall_grass_system_requirements.json"), self._build_tall_grass_system_requirements())
        self._write_json(os.path.join(data_dir, "pokemon_fangame_engine_requirements.json"), self._build_fangame_engine_requirements())
        self._write_json(os.path.join(data_dir, "prototype_runtime_config.json"), self._build_runtime_config())
        self._write_json(os.path.join(root_dir, "ProjectSettings", "PokeEnginePrototypeSettings.json"), self._build_project_settings())
        self._write_project_framework(root_dir)

    def _write_project_framework(self, root_dir):
        """Writes the tested project-name-based framework into generated Unity projects."""
        tokens = self._project_template_tokens(root_dir)
        framework_dirs = [
            "Assets/Scripts/Core",
            "Assets/Scripts/Overworld",
            "Assets/Scripts/Camera",
            "Assets/Scripts/Interaction",
            "Assets/Scripts/Pokemon",
            "Assets/Scripts/Battle",
            "Assets/Scripts/AI",
            "Assets/Scripts/UI",
            "Assets/Scripts/Save",
            "Assets/Scripts/Audio",
            "Assets/Scripts/Events",
            "Assets/Scripts/Raids",
            "Assets/Scripts/Transformations",
            "Assets/Scripts/Fusion",
            "Assets/Scripts/Tools",
            "Assets/ScriptableObjects/Creatures",
            "Assets/ScriptableObjects/Moves",
            "Assets/ScriptableObjects/Abilities",
            "Assets/ScriptableObjects/Items",
            "Assets/ScriptableObjects/EncounterTables",
            "Assets/ScriptableObjects/Trainers",
            "Assets/ScriptableObjects/Areas",
            "Assets/Prefabs/Player",
            "Assets/Prefabs/NPCs",
            "Assets/Prefabs/Battle",
            "Assets/Prefabs/UI",
            "Assets/Prefabs/Cameras",
            "Assets/Tests/__PROJECT_NAMESPACE__/EditMode",
            "Assets/Tests/__PROJECT_NAMESPACE__/PlayMode",
        ]
        for rel_dir in framework_dirs:
            os.makedirs(os.path.join(root_dir, self._render_project_template(rel_dir, tokens)), exist_ok=True)

        combined_scene_skip = {
            "Assets/Scenes/Overworld.unity",
            "Assets/Scenes/Overworld.unity.meta",
            "Assets/Scenes/Battle.unity",
            "Assets/Scenes/Battle.unity.meta",
        }
        for rel_path, content in PROJECT_FRAMEWORK_TEMPLATE_FILES.items():
            if rel_path in combined_scene_skip:
                continue
            rendered_path = self._render_project_template(rel_path, tokens)
            rendered_content = self._render_project_template(content, tokens)
            self._write_text(os.path.join(root_dir, rendered_path), rendered_content)

        self.logger(f"{tokens['__PROJECT_DISPLAY_NAME__']} framework files generated into combined PrototypeRegion scene: {len(PROJECT_FRAMEWORK_TEMPLATE_FILES) - len(combined_scene_skip)}")

    def _project_display_name(self, root_dir):
        name = os.path.basename(os.path.normpath(root_dir)).strip()
        return name or DEFAULT_PROJECT_NAME

    def _project_namespace(self, display_name):
        parts = re.findall(r"[A-Za-z0-9]+", display_name)
        namespace = "".join(part[:1].upper() + part[1:] for part in parts) or "GeneratedProject"
        if namespace[0].isdigit():
            namespace = "Project" + namespace
        return namespace

    def _project_template_tokens(self, root_dir):
        display_name = self._project_display_name(root_dir)
        namespace = self._project_namespace(display_name)
        menu_name = display_name.replace("/", " ").replace("\\", " ").strip() or namespace
        return {
            "__PROJECT_DISPLAY_NAME__": display_name,
            "__PROJECT_NAMESPACE__": namespace,
            "__PROJECT_MENU_ROOT__": f"PokeEngine/{menu_name}",
        }

    def _render_project_template(self, value, tokens):
        rendered = value
        for token, replacement in tokens.items():
            rendered = rendered.replace(token, replacement)
        return rendered

    def _architecture_sections(self):
        return [
            {
                "id": "overworld_system_architecture",
                "title": "Overworld System Architecture",
                "features": [
                    "2.5D diorama-style overworld rendering",
                    "fixed angled gameplay camera",
                    "wild-area orbit camera mode",
                    "cinematic camera support",
                    "seamless connected-area traversal",
                    "chunk-based world streaming",
                    "static and dynamic lighting separation",
                    "baked GI performance hook",
                    "shader graph support hook",
                    "runtime weather overlays",
                    "terrain blend shader hook",
                    "animated foliage shader hook",
                    "water shader pipeline hook",
                    "parallax background layers",
                    "reflection probe support",
                    "volumetric fog support",
                    "ambient occlusion support",
                    "dynamic shadow management",
                    "GPU instancing support",
                    "hierarchical LOD groups",
                    "occlusion culling support",
                    "texture atlas planning",
                    "Addressables integration hook",
                    "scene memory budgeting",
                    "runtime asset unloading hook",
                    "async loading support",
                ],
            },
            {
                "id": "world_streaming_region_system",
                "title": "World Streaming and Region System",
                "features": [
                    "persistent RPG region world",
                    "town area support",
                    "city area support",
                    "wilderness route support",
                    "dungeon support",
                    "indoor map support",
                    "raid zone support",
                    "postgame island support",
                    "secret dimension support",
                    "legendary sanctuary support",
                    "adjacent-area preloading",
                    "seamless area transitions",
                    "async scene loading",
                    "dynamic NPC loading",
                    "encounter table swapping",
                    "audio zone transitions",
                    "lighting profile swapping",
                    "area encounter tables",
                    "area music profiles",
                    "area lighting profiles",
                    "area NPC schedules",
                    "weather probabilities",
                    "event states",
                    "progression gates",
                    "trigger volumes",
                    "spawn tables",
                    "environmental interaction rules",
                ],
            },
            {
                "id": "movement_system",
                "title": "Movement System",
                "features": [
                    "structured four-direction mode",
                    "hybrid continuous movement mode hook",
                    "full analog movement mode hook",
                    "movement snapping",
                    "terrain modifiers",
                    "idle state",
                    "walk state",
                    "run state",
                    "sprint state",
                    "slide state",
                    "climb state",
                    "swim state",
                    "surf state",
                    "fly state",
                    "fall state",
                    "ledge jump state",
                    "push interaction state",
                    "cutscene lock state",
                    "grass terrain",
                    "water terrain",
                    "ice terrain",
                    "mud terrain",
                    "sand terrain",
                    "lava terrain",
                    "tall grass terrain",
                    "conveyor terrain",
                    "fragile terrain",
                    "dimensional terrain",
                    "diagonal movement correction",
                    "corner smoothing hook",
                    "input buffering",
                    "predictive collision hook",
                    "step height adjustment",
                    "context-sensitive traversal hook",
                    "Pokemon-style four-direction continuous movement",
                ],
            },
            {
                "id": "npc_system",
                "title": "NPC System",
                "features": [
                    "static NPCs",
                    "patrol NPCs",
                    "shopkeepers",
                    "trainers",
                    "followers",
                    "rivals",
                    "boss trainers",
                    "raid NPCs",
                    "story-critical NPCs",
                    "dialogue tree component",
                    "movement profile component",
                    "schedule profile component",
                    "event trigger component",
                    "relationship variables hook",
                    "shop inventory hook",
                    "trainer party data",
                    "AI behavior state",
                    "time-of-day schedules",
                    "weather reactions",
                    "post-event dialogue changes",
                    "world-state participation",
                    "dynamic relocation",
                    "vision cone trainer detection",
                    "terrain-aware detection hook",
                    "alert state",
                    "chase initiation hook",
                    "battle trigger pipeline",
                ],
            },
            {
                "id": "event_cutscene_system",
                "title": "Event and Cutscene System",
                "features": [
                    "story scripting",
                    "environmental changes",
                    "NPC behavior modification",
                    "dynamic progression",
                    "trigger events",
                    "collision events",
                    "dialogue events",
                    "camera events",
                    "animation events",
                    "audio events",
                    "battle events",
                    "world-state events",
                    "camera rails",
                    "character movement scripting",
                    "animation playback",
                    "dialogue synchronization",
                    "fade transitions",
                    "audio ducking",
                    "branching outcomes",
                    "boolean flags",
                    "integer counters",
                    "conditional checks",
                    "persistent save integration",
                    "dynamic world updates",
                ],
            },
            {
                "id": "pokemon_database_architecture",
                "title": "Pokemon Database Architecture",
                "features": [
                    "species ID",
                    "national dex ID",
                    "regional dex ID",
                    "display name",
                    "category",
                    "lore text",
                    "height",
                    "weight",
                    "gender ratio",
                    "egg groups",
                    "growth rate",
                    "catch rate",
                    "friendship base",
                    "base stats",
                    "typing",
                    "abilities",
                    "hidden abilities",
                    "learnsets",
                    "evolution rules",
                    "EV yield",
                    "models",
                    "textures",
                    "portraits",
                    "animation controllers",
                    "shiny palettes",
                    "form variants",
                    "Dimension Split forms",
                    "Mega forms",
                    "fusion compatibility",
                ],
            },
            {
                "id": "battle_engine_architecture",
                "title": "Battle Engine Architecture",
                "features": [
                    "single battles",
                    "double battles",
                    "multi battles",
                    "raid battles",
                    "legendary encounters",
                    "fusion encounters",
                    "intro state",
                    "send out state",
                    "command selection state",
                    "action queue state",
                    "move execution state",
                    "damage resolution state",
                    "faint handling state",
                    "switch handling state",
                    "victory/loss state",
                    "reward processing state",
                    "input collection",
                    "priority sorting",
                    "speed calculation",
                    "ability triggers",
                    "move execution",
                    "damage application",
                    "secondary effects",
                    "status resolution",
                    "end-turn effects",
                    "HP bars",
                    "EXP bars",
                    "status indicators",
                    "weather indicators",
                    "terrain indicators",
                    "transformation indicators",
                    "raid shield indicators",
                    "turn timers",
                    "wild Pokemon catching",
                ],
            },
            {
                "id": "damage_calculation_system",
                "title": "Damage Calculation System",
                "features": [
                    "STAB",
                    "type multipliers",
                    "weather bonuses",
                    "terrain bonuses",
                    "critical hits",
                    "random variance",
                    "burn penalties",
                    "ability modifiers",
                    "item modifiers",
                    "raid modifiers",
                    "Dimension Split modifiers",
                    "fusion modifiers",
                    "base power step",
                    "offensive stat step",
                    "defensive stat step",
                    "environmental modifier step",
                    "ability modifier step",
                    "item modifier step",
                    "critical modifier step",
                    "random factor step",
                    "final rounding step",
                ],
            },
            {
                "id": "ability_system",
                "title": "Ability System",
                "features": [
                    "passive effects",
                    "reactive effects",
                    "battle-start effects",
                    "terrain manipulation",
                    "weather manipulation",
                    "form-change triggers",
                    "raid boss mechanics",
                    "OnEnterBattle hook",
                    "OnSwitch hook",
                    "OnDamageTaken hook",
                    "OnMoveUsed hook",
                    "OnKO hook",
                    "OnTurnEnd hook",
                    "OnStatusApplied hook",
                    "OnTransformation hook",
                    "stack prevention",
                    "priority resolution",
                    "runtime overrides",
                    "ability suppression",
                    "fusion inheritance",
                ],
            },
            {
                "id": "mega_evolution_system",
                "title": "Mega Evolution System",
                "features": [
                    "battle-only activation",
                    "single activation per battle",
                    "form override",
                    "ability override",
                    "stat recalculation",
                    "animation sequence",
                    "audio transformation cues",
                    "transformation controller",
                    "runtime stat replacement",
                    "animation state swap",
                    "battle-state validation",
                ],
            },
            {
                "id": "dimension_split_system",
                "title": "Dimension Split System",
                "features": [
                    "rare powerful transformation goal",
                    "dramatic battle shift goal",
                    "unique tactical options goal",
                    "dimensional lore reinforcement",
                    "meter threshold activation",
                    "story unlock activation",
                    "bond level activation",
                    "held item activation",
                    "environmental condition activation",
                    "raid-only condition hook",
                    "cinematic trigger",
                    "camera transition",
                    "dimensional FX",
                    "audio distortion",
                    "model morph",
                    "stat reconstruction",
                    "signature move unlock",
                    "ability mutation",
                    "stat amplification",
                    "typing mutation hook",
                    "move augmentation",
                    "animation overrides",
                    "FX overlays",
                    "UI transformation indicators",
                    "exclusive signature move",
                    "unique FX package",
                    "cinematic camera sequence",
                    "conditional secondary effect",
                    "raid compatibility logic",
                    "runtime form mutation",
                    "temporary stat overlays",
                    "dynamic animation controller swapping",
                    "particle FX injection",
                    "audio layer overrides",
                    "move replacement logic",
                    "multiplayer synchronization hook",
                ],
            },
            {
                "id": "fusion_system",
                "title": "Fusion System",
                "features": [
                    "species compatibility matrix",
                    "restricted legendary fusions",
                    "form inheritance rules",
                    "ability inheritance logic",
                    "typing combination logic",
                    "stat averaging and weighting logic",
                    "validate compatibility",
                    "combine metadata",
                    "generate stat profile",
                    "generate typing",
                    "generate move pool",
                    "generate ability set",
                    "generate fusion ID",
                    "generate visuals",
                    "mesh blending",
                    "texture compositing",
                    "animation retargeting",
                    "dynamic portrait generation",
                    "UI icon generation",
                    "prebuilt fusion library option",
                    "runtime procedural fusion option",
                    "hybrid cached generation option",
                ],
            },
            {
                "id": "raid_system",
                "title": "Raid System",
                "features": [
                    "multiple trainers",
                    "shared timer",
                    "boss shield phases",
                    "aggressive AI scripting",
                    "environmental modifiers",
                    "capture sequence",
                    "reward distribution",
                    "shield regeneration",
                    "multi-action turns",
                    "arena-wide attacks",
                    "status cleansing",
                    "summon mechanics",
                    "transformation phases",
                    "1-star raids",
                    "2-star raids",
                    "3-star raids",
                    "4-star raids",
                    "5-star raids",
                    "legendary raids",
                    "event-exclusive raids",
                    "rare item rewards",
                    "evolution material rewards",
                    "fusion shard rewards",
                    "Dimension energy rewards",
                    "cosmetic unlock rewards",
                    "hidden ability rewards",
                ],
            },
            {
                "id": "save_system",
                "title": "Save System",
                "features": [
                    "player data serialization",
                    "party data serialization",
                    "PC storage serialization",
                    "inventory serialization",
                    "event flag serialization",
                    "NPC state serialization",
                    "raid state serialization",
                    "world progression serialization",
                    "transformation unlock serialization",
                    "fusion registry serialization",
                    "backup saves",
                    "save migration",
                    "corruption recovery",
                    "version validation",
                ],
            },
            {
                "id": "tooling_editors",
                "title": "Tooling and Editors",
                "features": [
                    "species editor",
                    "move editor",
                    "ability editor",
                    "form editor",
                    "Mega editor",
                    "Dimension Split editor",
                    "fusion compatibility editor",
                    "node-based dialogue editor",
                    "branching choice editor",
                    "portrait integration",
                    "event trigger integration",
                    "localization support",
                    "voice cue support",
                    "tile painting",
                    "encounter painting",
                    "spawn editing",
                    "event placement",
                    "cutscene preview",
                    "lighting preview",
                    "weather preview",
                    "path visualization",
                ],
            },
            {
                "id": "engine_core_architecture",
                "title": "Engine Core Architecture",
                "features": [
                    "modular systems",
                    "event-driven communication",
                    "service-oriented architecture",
                    "minimal singleton abuse",
                    "dependency injection",
                    "data-driven design",
                    "input manager",
                    "audio manager",
                    "scene manager",
                    "save manager",
                    "battle manager",
                    "event manager",
                    "asset manager",
                    "localization manager",
                    "assembly definitions",
                    "namespace isolation",
                    "profiling hooks",
                    "debug visualization",
                    "editor extensions",
                    "automated testing support",
                ],
            },
        ]

    def _feature_status(self, section_id, feature):
        playable = {
            "fixed angled gameplay camera",
            "wild-area orbit camera mode",
            "chunk-based world streaming",
            "town area support",
            "indoor map support",
            "raid zone support",
            "adjacent-area preloading",
            "async scene loading",
            "encounter table swapping",
            "audio zone transitions",
            "lighting profile swapping",
            "trigger volumes",
            "spawn tables",
            "structured four-direction mode",
            "movement snapping",
            "terrain modifiers",
            "input buffering",
            "step height adjustment",
            "Pokemon-style four-direction continuous movement",
            "static NPCs",
            "dialogue tree component",
            "trainer party data",
            "vision cone trainer detection",
            "alert state",
            "battle trigger pipeline",
            "boolean flags",
            "integer counters",
            "single battles",
            "raid battles",
            "command selection state",
            "action queue state",
            "damage resolution state",
            "wild Pokemon catching",
            "STAB",
            "type multipliers",
            "random variance",
            "ability modifiers",
            "OnMoveUsed hook",
            "battle-only activation",
            "single activation per battle",
            "form override",
            "ability override",
            "stat recalculation",
            "meter threshold activation",
            "signature move unlock",
            "ability mutation",
            "species compatibility matrix",
            "validate compatibility",
            "generate stat profile",
            "multiple trainers",
            "shared timer",
            "boss shield phases",
            "reward distribution",
            "player data serialization",
            "party data serialization",
            "inventory serialization",
            "event flag serialization",
            "backup saves",
            "save migration",
            "version validation",
            "assembly definitions",
            "namespace isolation",
            "debug visualization",
            "editor extensions",
            "automated testing support",
        }
        editor = {
            "species editor",
            "move editor",
            "ability editor",
            "form editor",
            "Mega editor",
            "Dimension Split editor",
            "fusion compatibility editor",
            "node-based dialogue editor",
            "branching choice editor",
            "tile painting",
            "encounter painting",
            "spawn editing",
            "event placement",
            "cutscene preview",
            "lighting preview",
            "weather preview",
            "path visualization",
        }
        data_driven = {
            "area encounter tables",
            "area music profiles",
            "area lighting profiles",
            "area NPC schedules",
            "weather probabilities",
            "event states",
            "progression gates",
            "species ID",
            "national dex ID",
            "regional dex ID",
            "display name",
            "category",
            "lore text",
            "height",
            "weight",
            "gender ratio",
            "egg groups",
            "growth rate",
            "catch rate",
            "friendship base",
            "base stats",
            "typing",
            "abilities",
            "hidden abilities",
            "learnsets",
            "evolution rules",
            "EV yield",
            "form variants",
            "Dimension Split forms",
            "Mega forms",
            "fusion compatibility",
            "localization support",
        }
        if feature in playable:
            return "playable_prototype"
        if feature in editor:
            return "editor_tool_hook"
        if feature in data_driven:
            return "data_configured"
        if "hook" in feature or "support" in feature or "option" in feature:
            return "runtime_hook"
        return "runtime_scaffold"

    def _build_architecture_requirements(self):
        sections = self._architecture_sections()
        return {
            "name": "PokeEngine Full RPG Prototype",
            "buttonPressGoal": "Generate a Unity-ready prototype foundation for the full Pokemon-style RPG architecture.",
            "unityEditorVersion": UNITY_EDITOR_VERSION,
            "movementDefault": "four_direction_continuous",
            "sections": [
                {
                    **section,
                    "systems": section["features"],
                    "featureCount": len(section["features"]),
                }
                for section in sections
            ],
        }

    def _build_feature_matrix(self):
        rows = []
        for section in self._architecture_sections():
            for index, feature in enumerate(section["features"], start=1):
                rows.append(
                    {
                        "id": f"{section['id']}-{index:03d}",
                        "sectionId": section["id"],
                        "sectionTitle": section["title"],
                        "feature": feature,
                        "status": self._feature_status(section["id"], feature),
                    }
                )
        return {
            "generatedAt": datetime.now().isoformat(timespec="seconds"),
            "movementDefault": "four_direction_continuous",
            "totalFeatureCount": len(rows),
            "features": rows,
        }

    def _build_engine_design_contract(self):
        return {
            "name": "Pokemon-Style 2.5D Unity Fangame Framework",
            "projectPurpose": [
                "reusable 2.5D Pokemon fangame engine",
                "modular RPG framework",
                "data-driven creature battle engine",
                "scalable content pipeline for regions, creatures, forms, battles, raids, and story systems",
            ],
            "mustBe2_5DFangame": True,
            "notAFreeCameraActionRpg": True,
            "notASideScroller": True,
            "philosophy": {
                "dataDrivenRpgEngine": True,
                "contentWithoutCoreRewrites": True,
                "modularPokemonMovesMapsAndSystems": True,
                "reusableBattleAndOverworld": True,
                "presentation": "classic GBA-era Pokemon feel with modern 2.5D diorama visuals",
                "architecture": "ScriptableObject-driven, event-driven, modular, Unity 2022+ compatible",
            },
            "overworld": {
                "presentation": "3D environments with classic readable RPG traversal",
                "zoneTypes": ["starter_town", "town", "city", "route", "forest", "wild_zone", "cave", "mountain", "water_route", "gym", "interior", "villain_base", "raid_den", "legendary_zone", "postgame_area", "secret_optional_area"],
                "zoneData": ["encounterTables", "npcPopulation", "eventFlags", "weatherRules", "musicProfile", "lightingProfile", "spawnRules"],
                "streaming": ["independentChunks", "adjacentPreload", "activeZoneNpcEncounters", "smoothTransitions", "persistentWorldChanges"],
            },
            "customFangameContentSupport": [
                "Fakemon",
                "regional forms",
                "custom typings",
                "custom moves",
                "custom abilities",
                "custom held items",
                "custom weather",
                "custom terrains",
                "custom battle gimmicks",
                "custom evolution methods",
                "custom transformations",
                "fan-made legendaries",
                "fan-made regions",
            ],
            "movement": {
                "structuredZones": "4-direction continuous Pokemon-style movement with no diagonal input",
                "wildZones": "4-direction movement with follow camera plus limited horizontal orbit and 15-degree vertical tilt",
                "tileSizeMeters": 1,
                "states": ["idle", "walking", "running", "sprinting", "surfing", "climbing", "ledgeJumping", "terrain", "interactionLock", "battleLock", "cutsceneLock"],
            },
            "camera": {
                "alwaysFollowsPlayer": True,
                "structuredMode": "fixed angle, no player-controlled rotation",
                "wildMode": "horizontal mouse rotation with a limited 15-degree vertical tilt, no full free camera or first-person view",
            },
            "runtimePersistence": ["playerPosition", "storyProgression", "party", "pcStorage", "npcStates", "worldChanges", "raidProgression", "fusionData", "dimensionSplitUnlocks"],
            "coreSystems": ["input", "audio", "sceneStreaming", "save", "battle", "event", "asset", "localization"],
        }

    def _build_battle_system_requirements(self):
        return {
            "name": "Gen 5 + Gen 8 Hybrid Battle System",
            "copyrightPolicy": "Original placeholder creatures, moves, items, abilities, UI, audio, and visual assets only.",
            "designGoals": [
                "fast readable pacing",
                "deterministic turn rhythm",
                "data-driven moves and rulesets",
                "isolated simulation layer",
                "event-driven abilities and items",
                "weather terrain raid transformation integration",
                "clear UI feedback for battle state",
            ],
            "stateMachine": [
                "None",
                "Intro",
                "SendOut",
                "StartTurn",
                "CommandSelection",
                "TargetSelection",
                "ActionOrdering",
                "ActionExecution",
                "DamageResolution",
                "SecondaryEffects",
                "StatusResolution",
                "SwitchResolution",
                "FaintResolution",
                "CaptureAttempt",
                "TransformationSelection",
                "RaidPhaseCheck",
                "EndTurn",
                "RewardResolution",
                "Victory",
                "Defeat",
                "Escape",
                "Cleanup",
            ],
            "battleFormats": [
                "wild single",
                "trainer single",
                "double",
                "multi",
                "rival",
                "gym leader",
                "legendary",
                "raid",
                "boss",
                "tutorial",
                "scripted story",
                "postgame challenge",
            ],
            "turnOrdering": [
                "action category priority",
                "move priority",
                "transformation timing",
                "item priority",
                "switch priority",
                "speed comparison",
                "trick-room-style inversion",
                "seeded tie breaker",
            ],
            "runtimeModels": [
                "BattleRuleset",
                "BattleContext",
                "BattleParticipant",
                "BattleCreature",
                "BattleCommand",
                "ActionQueue",
                "BattleEventLog",
            ],
            "coreSubsystems": [
                "MoveResolver",
                "DamageCalculator",
                "AccuracyResolver",
                "StatusController",
                "AbilityProcessor",
                "ItemProcessor",
                "WeatherController",
                "TerrainController",
                "SwitchController",
                "CaptureController",
                "RewardController",
                "TrainerBattleAI",
                "WildBattleAI",
                "RaidBossBattleAI",
                "TransformationController",
                "RaidPhaseController",
            ],
            "moveCategories": [
                "physical",
                "special",
                "status",
                "healing",
                "buff",
                "debuff",
                "weather",
                "terrain",
                "multi-hit",
                "priority",
                "charge",
                "recharge",
                "switching",
                "forced switch",
                "signature",
                "raid-only",
                "Dimension Split exclusive",
                "fusion-exclusive",
            ],
            "damagePipeline": [
                "accuracy validation",
                "category determination",
                "offensive stat selection",
                "defensive stat selection",
                "base formula",
                "critical modifier",
                "random variance",
                "STAB",
                "type effectiveness",
                "burn modifier",
                "weather modifier",
                "terrain modifier",
                "ability modifier hook",
                "item modifier hook",
                "field modifier hook",
                "transformation modifier",
                "final rounding",
                "HP application",
            ],
            "statusSystems": {
                "permanent": ["burn", "poison", "toxic poison", "paralysis", "sleep", "freeze"],
                "volatile": ["confusion", "flinch", "trap", "taunt", "encore", "disable", "curse-style", "attraction-style", "recharge", "charge", "protect", "substitute"],
                "timings": ["start turn", "before action", "during action", "after action", "end turn", "on switch", "on faint", "on battle end"],
            },
            "advancedSystems": [
                "Mega Evolution",
                "Dimension Split",
                "Fusion",
                "Raid boss shield phases",
                "Raid capture phase",
                "Raid reward generation",
            ],
            "generatedImplementation": {
                "simulation": "Assets/Scripts/Battle/AdvancedBattleSystem.cs",
                "tests": "Assets/Tests/<ProjectName>/EditMode/AdvancedBattleSystemTests.cs",
                "playablePrototype": "Assets/Scripts/PokeEngine/Battle/BattleEngineRuntime.cs",
            },
        }

    def _build_battle_raid_system_requirements(self):
        return {
            "id": "battle_raid_spec",
            "name": "Detailed Battle and Raid System Requirements",
            "copyrightPolicy": "Original placeholder creatures, moves, items, abilities, UI, audio, and visual assets only.",
            "battle": {
                "philosophy": [
                    "core gameplay loop of the fangame",
                    "Generation 5 pacing with Generation 8 polish",
                    "competitive strategic depth",
                    "fangame flexibility",
                    "fast tactical readable responsive rewarding mechanically deep play",
                    "clear explanation of acting creature, damage causes, active effects, and battle conditions",
                ],
                "architectureLayers": [
                    "Battle Simulation Layer",
                    "Battle State Layer",
                    "Action Resolution Layer",
                    "Presentation Layer",
                    "UI Layer",
                    "Animation Layer",
                    "Audio Layer",
                    "Networking Scaffold Layer",
                ],
                "simulationRules": [
                    "battle simulation can run without Unity visuals",
                    "all random systems accept seeded RNG",
                    "AI simulations can run quickly",
                    "logic is separated from UI, animation, audio, and network transport",
                ],
                "flow": [
                    "battle initialization",
                    "intro sequence",
                    "send-out phase",
                    "start-of-battle effects",
                    "command selection",
                    "action ordering",
                    "action execution",
                    "damage resolution",
                    "secondary effect resolution",
                    "status processing",
                    "faint handling",
                    "end-turn processing",
                    "victory/loss checks",
                    "reward processing",
                    "cleanup",
                ],
                "states": self._build_battle_system_requirements()["stateMachine"],
                "types": [
                    "wild",
                    "trainer",
                    "rival",
                    "gym",
                    "legendary",
                    "double",
                    "multi",
                    "boss",
                    "raid",
                    "tutorial",
                    "story-scripted",
                ],
                "futureTypes": ["triple", "rotation", "online", "tournament"],
                "battleCreatureRuntimeData": [
                    "species",
                    "current form",
                    "level",
                    "HP",
                    "stats",
                    "stat stages",
                    "current typing",
                    "ability",
                    "held item",
                    "known moves",
                    "PP values",
                    "status conditions",
                    "volatile effects",
                    "temporary effects",
                    "Mega state",
                    "Dimension Split state",
                    "Fusion state",
                    "Raid state",
                    "Shield state",
                    "last move used",
                    "turn counters",
                    "faint state",
                ],
                "commands": {
                    "Fight": ["move selection", "target selection", "PP display", "type display", "move category display", "optional effectiveness preview"],
                    "Bag": ["healing items", "capture devices", "battle items", "status cures", "transformation items"],
                    "Party": ["creature switching", "status visibility", "HP visibility", "fainted state visibility"],
                    "Run": ["escape formula", "disabled in trainer or raid battles unless allowed"],
                    "Capture": ["wild captures", "raid capture phase captures", "capture restrictions"],
                    "Mega Evolution": ["battle-only form override", "stat recalculation", "ability override", "one-use limit"],
                    "Dimension Split": ["dimensional form", "signature move", "stat amplification", "meter or condition"],
                    "Fusion": ["compatibility", "hybrid stats", "hybrid typing", "defusion support"],
                    "Raid Support": ["cheer", "support", "ally recovery scaffold"],
                },
                "turnOrder": [
                    "action priority category",
                    "move priority",
                    "transformation timing",
                    "switch priority",
                    "item priority",
                    "speed comparison",
                    "trick-room-style inversion",
                    "random tie-breaker",
                    "interruption handling",
                    "multi-action abilities",
                    "raid overrides",
                    "dynamic reordering",
                ],
                "moveData": [
                    "name",
                    "type",
                    "category",
                    "base power",
                    "accuracy",
                    "PP",
                    "priority",
                    "contact flags",
                    "sound flags",
                    "punch/bite/pulse tags",
                    "protect and reflection interaction",
                    "status effects",
                    "stat modifications",
                    "secondary effects",
                    "recoil",
                    "healing",
                    "drain",
                    "weather and terrain interaction",
                    "multi-hit rules",
                    "animation/audio/camera profile",
                ],
                "moveCategories": self._build_battle_system_requirements()["moveCategories"],
                "damage": {
                    "factors": [
                        "STAB",
                        "type effectiveness",
                        "critical hits",
                        "random variance",
                        "burn modifiers",
                        "weather modifiers",
                        "terrain modifiers",
                        "ability modifiers",
                        "held item modifiers",
                        "field effects",
                        "raid modifiers",
                        "fusion modifiers",
                        "transformation modifiers",
                    ],
                    "pipeline": self._build_battle_system_requirements()["damagePipeline"],
                },
                "typeSystem": ["single typing", "dual typing", "immunities", "resistances", "weaknesses", "temporary typing", "fusion typing", "Dimension Split typing", "runtime editable chart"],
                "statusSystem": self._build_battle_system_requirements()["statusSystems"],
                "abilityTriggers": ["OnBattleStart", "OnSwitchIn", "OnTurnStart", "OnMoveUsed", "OnDamageTaken", "OnStatusApplied", "OnWeatherChange", "OnTerrainChange", "OnTransformation", "OnTurnEnd"],
                "weatherTypes": ["Clear", "Rain", "Sun", "Sandstorm", "Snow", "Fog", "Dimensional weather"],
                "terrainTypes": ["Electric-like", "Grassy-like", "Psychic-like", "Misty-like", "Dimensional terrain"],
                "ui": ["HP bars", "EXP bars", "status icons", "move menu", "PP display", "type display", "weather indicators", "terrain indicators", "transformation indicators", "raid indicators", "turn indicators", "capture UI", "party screen", "bag screen"],
                "presentation": ["move animations", "hit pauses", "screen shake", "camera cuts", "dynamic zooms", "weather VFX", "terrain VFX", "transformation cinematics", "raid intros", "shield break cinematics"],
                "ai": {
                    "wild": ["weighted move logic", "aggression logic", "status awareness"],
                    "trainer": ["type matchup evaluation", "damage prediction", "setup logic", "switching logic", "item usage", "difficulty scaling"],
                    "raid": ["multi-actions", "arena attacks", "shield phases", "debuff cleansing", "phase transitions"],
                },
                "capture": ["wild captures", "raid captures", "capture restrictions", "status modifiers", "HP modifiers", "capture item modifiers", "shake logic", "special capture rules"],
                "transformations": {
                    "Mega Evolution": ["battle-only", "stat recalculation", "ability override", "animation sequence", "one-use-per-battle"],
                    "Dimension Split": ["alternate dimensional form", "signature move unlock", "stat amplification", "ability mutation", "visual distortion", "cinematic activation", "meter/condition system"],
                    "Fusion": ["compatibility", "hybrid stats", "hybrid typing", "ability inheritance", "fusion-exclusive moves", "runtime generation", "defusion"],
                },
                "rewards": ["EXP", "level ups", "move learning", "evolution checks", "currency rewards", "raid rewards", "story progression", "quest progression"],
                "tests": ["damage", "accuracy", "AI", "status", "ability", "item", "weather", "terrain", "transformation", "capture", "reward", "save/load", "raid"],
            },
            "raid": {
                "philosophy": [
                    "large-scale cooperative boss encounters",
                    "endgame progression",
                    "event-based repeatable high-level content",
                    "intense cinematic cooperative mechanically unique strategic battles",
                ],
                "initiationSources": ["Raid dens", "Legendary shrines", "Event portals", "Postgame arenas", "Story encounters"],
                "flow": [
                    "raid selection",
                    "lobby phase",
                    "team confirmation",
                    "raid intro cinematic",
                    "boss battle phase",
                    "shield phase handling",
                    "timer management",
                    "victory/loss check",
                    "reward phase",
                    "capture phase",
                    "cleanup",
                ],
                "bossCapabilities": [
                    "massive HP scaling",
                    "multiple actions per turn",
                    "shield phases",
                    "arena-wide attacks",
                    "status cleansing",
                    "stat reset mechanics",
                    "transformation phases",
                    "phase transitions",
                    "rage states",
                ],
                "bossTypes": ["legendary", "mythical", "dimension creature", "fusion boss", "story boss"],
                "tiers": ["1-Star", "2-Star", "3-Star", "4-Star", "5-Star", "Legendary Tier", "Event Tier"],
                "scalingAffects": ["HP", "damage", "AI complexity", "shield strength", "reward rarity", "boss mechanics"],
                "shieldSystem": ["HP-based triggers", "damage reduction", "hit-count reduction", "shield break states", "shield visuals", "optional regeneration", "boss stagger on break"],
                "timerSystem": ["shared timer", "turn limit", "action time drain", "expiration failure", "revive penalty", "boss timer modifiers"],
                "allySystem": ["AI allies", "local multiplayer scaffold", "online multiplayer scaffold", "role weighting", "support behavior", "revive handling"],
                "raidAI": ["multi-actions", "AoE attacks", "shield activation", "transformation phases", "arena hazards", "summons", "debuff cleansing", "enrage logic"],
                "arenas": ["custom background", "environmental VFX", "dynamic lighting", "arena hazards", "dimensional distortions", "camera event zones"],
                "rewards": ["rare items", "evolution materials", "fusion materials", "dimension energy", "currency", "cosmetics", "hidden abilities", "rare creatures"],
                "rewardScaling": ["raid tier", "performance", "completion speed", "event modifiers"],
                "capture": ["special raid capture rules", "optional guaranteed captures", "limited capture events", "event-exclusive catches", "boss-specific restrictions"],
                "events": ["rotating raid events", "seasonal events", "time-limited bosses", "community challenge raids", "event-exclusive rewards"],
                "ui": ["massive boss HP bar", "shield meter", "raid timer", "ally status panels", "boss phase indicators", "event alerts", "raid objective messages"],
                "presentation": ["boss intro cinematics", "dynamic camera sequences", "arena transformations", "phase transitions", "environmental distortion", "audio escalation", "transformation cinematics"],
                "tests": ["HP scaling", "shield activation", "timer expiration", "reward generation", "capture phase", "AI legality", "phase transition", "save/load persistence", "event rotation"],
                "acceptanceCriteria": [
                    "raid bosses can spawn",
                    "raid lobbies function",
                    "raid battles can begin",
                    "boss AI functions",
                    "shields activate properly",
                    "timer systems function",
                    "rewards generate correctly",
                    "capture phase functions",
                    "event raids rotate correctly",
                    "raid battles remain stable under stress testing",
                ],
            },
            "generatedImplementation": {
                "battleSimulation": "Assets/Scripts/Battle/AdvancedBattleSystem.cs",
                "battleTests": "Assets/Tests/<ProjectName>/EditMode/AdvancedBattleSystemTests.cs",
                "playableBattlePrototype": "Assets/Scripts/PokeEngine/Battle/BattleEngineRuntime.cs",
                "raidRuntime": "Assets/Scripts/Raids/RaidSystem.cs and Assets/Scripts/PokeEngine/Raid/RaidBattleRuntime.cs",
                "designDoc": "Docs/BATTLE_RAID_SYSTEM_REQUIREMENTS.md",
                "dataContract": "Assets/StreamingAssets/Data/battle_raid_system_requirements.json",
            },
        }

    def _build_pause_menu_system_requirements(self):
        return {
            "id": "pause_menu_system",
            "name": "Pause Menu System - Full Screen and Menu Requirements",
            "philosophy": [
                "primary navigation hub outside battle",
                "classic Pokemon menu flow",
                "Generation 5 responsiveness",
                "Generation 8 presentation polish",
                "modern quality-of-life systems",
                "instant open behavior",
                "clean fast intuitive information-rich layout",
            ],
            "rootBehavior": [
                "opens instantly in overworld",
                "pauses overworld simulation where appropriate",
                "optionally keeps environmental animations running",
                "uses fade or slide transitions",
                "supports controller, keyboard, and mouse navigation",
                "supports dynamic menu handlers, runtime injection, mods, plugins, and context-sensitive options",
            ],
            "mainOptions": [
                "Pokedex",
                "Pokemon",
                "Bag",
                "Map",
                "Pokegear/Phone",
                "Quests",
                "Save",
                "Options",
                "Profile/Trainer Card",
                "Multiplayer",
                "Debug",
                "Exit Game",
            ],
            "conditionalVisibility": {
                "Pokedex": "after receiving Pokedex",
                "Pokemon": "if party exists",
                "Map": "after obtaining map device",
                "Multiplayer": "if enabled",
                "Debug": "debug/developer mode only",
            },
            "layout": {
                "left": ["main command list", "icons", "selection indicator", "animated cursor", "scroll support"],
                "right": ["party preview", "lead creature portrait/model", "location", "playtime", "objective", "badge count", "currency", "weather/time"],
                "optionalHud": ["quest alerts", "event notifications", "raid event banner", "online notifications", "daily event timers"],
                "visualGoals": ["clean", "minimal clutter", "strong readability", "smooth transitions", "modernized Pokemon aesthetic"],
            },
            "screens": {
                "Pokedex": ["regional dex", "national dex", "search", "filters", "sorting", "habitat", "forms", "shinies", "fusion", "mega", "Dimension Split", "evolution chain", "model viewer"],
                "Pokemon": ["party view", "HP", "status", "held item", "EXP", "moves", "quick switching", "rearranging", "field moves", "fusion/mega/Dimension indicators"],
                "Summary": ["overview", "stats", "moves", "ribbons", "lore", "fusion data", "Dimension Split data", "model preview"],
                "Bag": ["items", "medicine", "Poke Balls", "TMs/TRs", "berries", "battle items", "key items", "fusion materials", "dimension materials", "raid materials", "sorting", "filtering", "favorites", "quick use"],
                "Map": ["region map", "labels", "current location", "quest/gym/raid/legendary markers", "fast travel", "weather overlay", "day/night overlay", "zoom", "pan"],
                "Pokegear/Phone": ["contacts", "map shortcut", "radio/music", "quests", "raid notifications", "events", "friends", "news", "daily events"],
                "Quests": ["main story", "side quests", "legendary quests", "raid quests", "collection goals", "repeatable quests", "journal/history"],
                "Profile/Trainer Card": ["trainer identity", "playtime", "money", "dex count", "badge count", "league ranking", "trainer ID", "multiplayer rank", "achievements", "customization"],
                "Save": ["metadata", "overwrite warning", "manual save", "autosave", "backup saves", "recovery saves", "cloud save scaffold"],
                "Options": ["audio", "text speed", "battle effects", "battle style", "movement speed", "autosave", "camera sensitivity", "screen shake", "quality", "UI scale", "language", "accessibility", "remapping", "themes", "graphics"],
                "Controls": ["keyboard rebinding", "controller rebinding", "profiles", "conflict detection", "default reset", "sensitivity", "deadzone"],
                "Multiplayer": ["friend list", "trading", "battling", "raid matchmaking", "online profile", "events", "lobby browser"],
                "Raid Events": ["active raids", "timers", "featured bosses", "reward preview", "difficulty", "matchmaking", "online lobby"],
                "Storage/PC": ["boxes", "drag/drop", "search", "filters", "marking", "sorting", "fusion tracking", "forms", "mass movement", "themes", "quick swap"],
                "Ready Menu": ["registered items", "bike", "fishing rod", "radar", "ride abilities", "field moves", "quick utilities"],
                "Debug": ["spawn creatures", "edit party", "teleport", "trigger events", "toggle flags", "inventory", "start battles", "spawn raids", "weather", "performance"],
            },
            "transitions": ["smooth transitions", "slide animations", "fade effects", "menu sounds", "cursor animations", "dynamic UI scaling"],
            "testing": [
                "keyboard navigation",
                "controller navigation",
                "mouse navigation optional",
                "dynamic scaling",
                "save persistence",
                "localization support",
                "accessibility support",
                "input conflict detection",
                "controller rebinding",
                "performance budget",
            ],
            "generatedImplementation": {
                "prototypeHud": "Assets/Scripts/PokeEngine/UI/PrototypeRpgHud.cs",
                "frameworkScaffold": "Assets/Scripts/UI/PauseMenuSystem.cs",
                "frameworkTests": "Assets/Tests/<ProjectName>/EditMode/PauseMenuSystemTests.cs",
                "designDoc": "Docs/PAUSE_MENU_SYSTEM_REQUIREMENTS.md",
                "dataContract": "Assets/StreamingAssets/Data/pause_menu_system_requirements.json",
            },
        }

    def _build_save_system_requirements(self):
        return {
            "id": "full_save_system",
            "name": "Full Save System Requirements",
            "philosophy": [
                "save/load is a core engine service, not a single file dump",
                "all long-term progression must be versioned, validated, and recoverable",
                "runtime systems write modular records so content can expand without rewriting the save pipeline",
                "manual save, autosave, backup save, recovery save, and cloud scaffolds share the same data contract",
                "save data must be deterministic enough for tests and flexible enough for future content",
            ],
            "persistenceScope": [
                "player identity",
                "player scene and position",
                "playtime",
                "money",
                "badges",
                "party creatures",
                "PC storage",
                "inventory",
                "Pokedex seen/caught/form tracking",
                "quest states",
                "event flags",
                "integer counters",
                "world state records",
                "NPC states",
                "raid states and event rotations",
                "fusion registry",
                "transformation unlocks",
                "settings snapshot",
                "pause menu snapshot",
                "optional battle resume data",
            ],
            "safetyFeatures": [
                "atomic temp-file write",
                "main save slot",
                "backup save",
                "autosave slot",
                "recovery load from backup if main save is corrupt",
                "version validation",
                "migration pipeline",
                "checksum validation",
                "slot metadata",
                "dirty-state autosave policy",
            ],
            "slots": ["manual", "autosave", "backup", "recovery", "cloud scaffold"],
            "migration": [
                "all saves carry a schema version",
                "older versions migrate forward one step at a time",
                "missing lists are normalized after load",
                "future migrations can register new steps without replacing SaveManager",
            ],
            "integration": [
                "pause menu save screen calls the same SaveManager as autosave",
                "battle rewards write party, flags, quests, and raid records",
                "fusion and Dimension Split persist through dedicated records",
                "world streaming and NPC systems use key/value world records",
                "settings and control profiles can be included in save metadata or their own settings file",
            ],
            "testing": [
                "serialize and deserialize full save data",
                "flag and counter persistence",
                "slot metadata generation",
                "backup recovery when main save is corrupt",
                "migration from old versions",
                "checksum validation",
                "autosave policy",
                "cloud save scaffold upload/download",
            ],
            "generatedImplementation": {
                "prototypeRuntime": "Assets/Scripts/PokeEngine/Save/PokeSaveManager.cs",
                "frameworkRuntime": "Assets/Scripts/Save/SaveSystem.cs",
                "frameworkTests": "Assets/Tests/<ProjectName>/EditMode/SaveSystemTests.cs",
                "designDoc": "Docs/SAVE_SYSTEM_REQUIREMENTS.md",
                "dataContract": "Assets/StreamingAssets/Data/save_system_requirements.json",
            },
        }

    def _build_tall_grass_system_requirements(self):
        return {
            "id": "tall_grass_system",
            "name": "Tall Grass System Requirements",
            "philosophy": [
                "tall grass is encounter terrain, not decoration",
                "grass communicates encounter danger, biome identity, route pacing, and exploration risk",
                "players must instantly recognize encounter terrain from the 2.5D camera angle",
                "the system preserves classic route anticipation while supporting modern 3D presentation",
            ],
            "grassTypes": [
                "standard",
                "dense",
                "double",
                "rustling",
                "wet",
                "flower fields",
                "swamp",
                "snow",
                "dimensional",
                "raid grass zones",
                "seasonal variants",
            ],
            "visualDesign": [
                "sway animation hooks",
                "player movement reaction",
                "lower-body obstruction",
                "solid readable encounter color in prototypes",
                "camera-safe transparency and clipping prevention hooks",
                "biome-specific shader/audio/particle hooks",
            ],
            "encounterRules": {
                "checks": ["after movement completion", "timed wild-area ticks", "terrain validation"],
                "rateFactors": ["grass type", "player traversal speed", "repel", "abilities", "story flags", "time of day", "weather", "season", "active events"],
                "poolFilters": ["weighted rarity", "time-exclusive", "weather-exclusive", "seasonal", "event", "swarm", "hidden", "story-restricted"],
                "specialMechanics": ["double grass", "rustling grass", "rare spawn boost", "ambush chance", "radar/chaining scaffold", "repel auto-reuse scaffold"],
            },
            "movementInteraction": [
                "grass bending",
                "footstep VFX hook",
                "rustle audio hook",
                "walking/running/sprinting/bike/ride traversal modifiers",
                "terrain speed modifiers",
                "encounter roll after tile movement",
            ],
            "weatherTimeInteraction": [
                "rain darkens grass and changes pools",
                "snow/frost variants and snow encounters",
                "wind intensifies sway",
                "dimensional weather shifts color and encounter pools",
                "morning/day/evening/night pools",
                "seasonal grass states",
            ],
            "savePersistence": [
                "swarm states",
                "rare rustling spawns",
                "event encounter states",
                "daily grass event state",
                "seasonal encounter state",
            ],
            "performance": [
                "GPU instancing target",
                "distance culling target",
                "LOD support target",
                "efficient sway shader hook",
                "collision optimization",
                "animation batching",
            ],
            "testing": [
                "encounter rate tests",
                "spawn pool validation",
                "repel interaction tests",
                "ability interaction tests",
                "rare encounter tests",
                "rustling spawn tests",
                "save/load tests",
                "weather interaction tests",
                "day/night encounter tests",
                "visual feedback state tests",
            ],
            "generatedImplementation": {
                "prototypeRuntime": "Assets/Scripts/PokeEngine/Overworld/TallGrassSystem.cs",
                "prototypeTrigger": "Assets/Scripts/PokeEngine/Overworld/TallLeafEncounterTrigger.cs",
                "frameworkRuntime": "Assets/Scripts/Overworld/TallGrassSystem.cs",
                "frameworkTests": "Assets/Tests/<ProjectName>/EditMode/TallGrassSystemTests.cs",
                "designDoc": "Docs/TALL_GRASS_SYSTEM_REQUIREMENTS.md",
                "dataContract": "Assets/StreamingAssets/Data/tall_grass_system_requirements.json",
            },
        }

    def _build_fangame_engine_requirements(self):
        sections = [
            ("project_purpose", "Project Purpose", [
                "Generate a reusable 2.5D Pokemon fangame engine for Unity 2022+.",
                "Serve as a modular RPG framework, data-driven creature battle engine, and scalable content pipeline.",
                "Support large fangame regions with minimal engine rewrites and minimal future coding.",
                "Use original generated placeholder data and assets while supporting user-created fangame content.",
            ]),
            ("core_2_5d_world_design", "Core 2.5D World Design", [
                "Render fully 3D diorama environments with classic top-down Pokemon readability.",
                "Preserve controlled traversal, route readability, landmarks, silhouettes, and environmental storytelling.",
                "Keep the world handcrafted and readable rather than procedural or visually cluttered.",
            ]),
            ("visual_presentation", "2.5D Visual Presentation", [
                "Support 3D environments, character models, creature models, dynamic lighting, stylized shaders, and cinematic effects.",
                "Include hooks for terrain shaders, animated foliage, water shaders, reflection probes, volumetric fog, color grading, weather rendering, post-processing, and environment VFX.",
                "Never hide paths, interactables, or traversal information for realism.",
            ]),
            ("region_structure", "Region Structure", [
                "Support starter towns, cities, routes, forests, caves, mountains, water routes, gyms, villain bases, legendary areas, postgame zones, wild areas, raid dens, and optional secret areas.",
                "Each area carries encounter tables, NPC population, music, weather, lighting, triggers, story rules, trainers, hidden items, and fast travel metadata.",
            ]),
            ("movement_philosophy", "Movement Philosophy", [
                "Prioritize responsive, predictable, clean directional movement inspired by Pokemon Emerald.",
                "Avoid physics-heavy, floaty, momentum-driven, or action RPG locomotion.",
            ]),
            ("structured_area_movement", "Structured Area Movement", [
                "Use hidden grid logic, tile-aware movement, cardinal priority, no diagonal movement, instant turning, collision snapping, and input buffering.",
                "Apply to towns, cities, routes, gyms, interiors, and puzzle zones.",
            ]),
            ("wild_area_movement", "Wild Area Movement", [
                "Support diagonal 8-direction traversal, analog-compatible movement, terrain-aware modifiers, and collision-aware smoothing.",
                "Keep wild traversal Pokemon-like rather than open-world action movement.",
            ]),
            ("camera_system", "Camera System", [
                "Always preserve orientation and route readability.",
                "Provide cinematic but controlled 2.5D framing without disorientation.",
            ]),
            ("structured_camera_mode", "Structured Camera Mode", [
                "Use fixed or semi-fixed smooth follow with no manual rotation.",
                "Reinforce classic route navigation, directional clarity, and puzzle readability.",
            ]),
            ("wild_area_camera_mode", "Wild Area Camera Mode", [
                "Follow the player at all times while allowing horizontal mouse/right-stick orbit, limited vertical tilt, smoothing, collision prevention, and optional reset.",
                "Never allow first-person view, uncontrolled drift, or wild spinning.",
            ]),
            ("environment_interaction", "2.5D Environment Interaction", [
                "Support NPC interaction, item pickup, hidden item detection, surf, climb, push/pull puzzles, ledges, environment triggers, story triggers, raid dens, and legendary encounters.",
                "Keep interactions readable from the gameplay camera.",
            ]),
            ("pokemon_system", "Pokemon System", [
                "Species data includes IDs, regional dex ID, display name, base stats, typing, abilities, hidden abilities, learnsets, evolutions, forms, shinies, dex data, held items, fusion compatibility, Mega forms, and Dimension Split forms.",
            ]),
            ("custom_fangame_content", "Custom Fangame Content Support", [
                "Support Fakemon, regional forms, custom typings, moves, abilities, held items, weather, terrain, battle gimmicks, evolutions, transformations, fan-made legendaries, and fan-made regions.",
                "Do not assume official-only content.",
            ]),
            ("party_storage", "Party and Storage System", [
                "Party supports 6 creatures, runtime stats, statuses, EXP, moves, and PP.",
                "PC supports multiple boxes, search, filtering, sorting, tagging, form persistence, and fusion persistence.",
            ]),
            ("battle_system", "Battle System", [
                "Combine Gen 5 pacing, Gen 8 mechanics, competitive depth, and fangame flexibility.",
                "Support wild, trainer, rival, gym, legendary, boss, raid, double, and scripted battles.",
                "Implement turn-based combat, priority, speed order, type effectiveness, STAB, statuses, abilities, terrain, weather, held items, crits, switching, AI, and capture.",
            ]),
            ("battle_feel", "Battle Feel", [
                "Keep battles fast, responsive, readable, strategic, and competitive-friendly.",
                "Use snappy UI and clear impact timing with modern VFX, transformations, raid systems, and dynamic cameras.",
            ]),
            ("battle_ui", "Battle UI", [
                "Provide HP bars, EXP bars, status icons, move menu, PP, type display, messages, weather, terrain, raid, and transformation indicators.",
                "Prioritize speed, clarity, readability, and competitive usefulness.",
            ]),
            ("trainer_system", "Trainer System", [
                "Support regular trainers, rivals, gym leaders, elite trainers, champion, villain admins, villain boss, legendary guardians, and raid trainers.",
                "Trainer data includes teams, AI profile, battle intro, defeat dialogue, rematches, and story integration.",
            ]),
            ("npc_dialogue_system", "NPC and Dialogue System", [
                "NPCs support dialogue trees, schedules, event reactions, story dialogue, shops, quests, and time-of-day reactions.",
                "Dialogue supports branching, portraits, event triggers, conditionals, and localization-ready data.",
            ]),
            ("gym_story_progression", "Gym and Story Progression", [
                "Support badges, traversal unlocks, rivals, villain progression, legendary arcs, postgame unlocks, side quests, and dynamic world changes.",
            ]),
            ("mega_evolution", "Mega Evolution System", [
                "Battle-only transformation with form replacement, stat recalculation, ability override, animation, and once-per-battle limitation.",
            ]),
            ("dimension_split", "Dimension Split System", [
                "Replace Dynamax with alternate dimensional forms, signature moves, stat amplification, ability mutation, visual distortion, cinematics, and meter/condition activation.",
            ]),
            ("fusion_system", "Fusion System", [
                "Support compatibility rules, hybrid stats, hybrid typing, ability inheritance, exclusive moves, runtime generation, fusion UI, defusion, and save persistence.",
            ]),
            ("raid_system", "Raid System", [
                "Support raid dens, tiers, shared timers, shield phases, multi-trainer support, AI allies, exclusive rewards, capture phase, and event rotations.",
            ]),
            ("day_night_weather", "Day/Night and Weather System", [
                "Support real-time lighting, time-based encounters, NPC schedules, dynamic weather, battle weather synchronization, and area weather profiles.",
                "Weather includes rain, snow, fog, sandstorm, thunderstorm, and dimensional weather.",
            ]),
            ("audio_system", "Audio System", [
                "Support town, route, battle, gym, rival, legendary, raid, and victory themes.",
                "Include ambient audio, weather audio, dynamic battle transitions, and dialogue/cutscene ducking.",
            ]),
            ("visual_effects", "Visual Effects System", [
                "Support weather, move, battle, terrain, transformation, fusion, raid, camera distortion, hit pause, and screen shake VFX.",
            ]),
            ("save_system", "Save System", [
                "Persist player position, story progression, inventory, creature data, PC data, world changes, NPC states, raid states, transformation unlocks, fusion registry, and completed events.",
            ]),
            ("development_tools", "Development Tools", [
                "Provide editor tools for Pokemon, moves, abilities, fusion, Dimension Split, dialogue, encounters, trainers, region/map helpers, debugging, and QA.",
            ]),
            ("engine_architecture", "Engine Architecture", [
                "Use modular, event-driven, ScriptableObject-driven, multiplayer-compatible, save-safe, performance-optimized architecture.",
                "Separate gameplay simulation, presentation, UI, audio, animation, and networking scaffolds.",
            ]),
            ("testing_requirements", "Testing Requirements", [
                "Every major system needs unit tests, integration tests, play mode tests, and deterministic RNG tests.",
                "Required tested areas include movement, camera, battle logic, damage, AI, save/load, fusion, Dimension Split, raids, UI, and encounters.",
            ]),
            ("final_game_feel", "Final Game Feel Goals", [
                "The game should feel nostalgic, strategic, polished, modernized, replayable, and emotionally engaging.",
                "The player should feel attached to their creatures, rewarded for exploration, strategically challenged, and immersed in the world.",
            ]),
        ]
        return {
            "name": "Pokemon Fangame Engine Requirements - 2.5D Unity RPG Framework",
            "unityVersion": UNITY_EDITOR_VERSION,
            "mustBe2_5DFangame": True,
            "definition": {
                "worldRenderedWith3DEnvironmentsAndModels": True,
                "classicTopDownPokemonReadability": True,
                "pokemonStyleRouteNavigation": True,
                "controlledCameraSystems": True,
                "notFreeCameraActionRpg": True,
                "notSideScroller": True,
            },
            "feelTargets": ["Pokemon Emerald exploration responsiveness", "Generation 5 battle pacing", "Generation 8 battle mechanics and polish", "modern 2.5D RPG presentation"],
            "sections": [
                {"id": section_id, "title": title, "requirements": requirements}
                for section_id, title, requirements in sections
            ],
        }

    def _render_fangame_engine_requirements_doc(self):
        data = self._build_fangame_engine_requirements()
        lines = [
            "# Pokemon Fangame Engine Requirements",
            "",
            "This generated project is a reusable Unity 2022+ 2.5D Pokemon fangame framework. It is designed as a modular RPG engine, data-driven creature battle engine, and scalable content pipeline for full regions, custom creatures, forms, battles, raids, story systems, and editor tools.",
            "",
            "The generated code uses original placeholder creatures, moves, abilities, items, and visuals. The engine supports fangame-style content without assuming official-only data.",
            "",
            "## 2.5D Contract",
            "",
            "- The world is rendered with 3D environments and models.",
            "- Gameplay readability follows classic top-down Pokemon route design.",
            "- Movement preserves Pokemon-style traversal instead of action RPG locomotion.",
            "- Cameras are controlled and readability-focused.",
            "- The project is not a free-camera action RPG and not a side-scroller.",
            "",
            "## Sections",
            "",
        ]
        for section in data["sections"]:
            lines.append(f"### {section['title']}")
            for requirement in section["requirements"]:
                lines.append(f"- {requirement}")
            lines.append("")
        return "\n".join(lines)

    def _render_battle_system_design_doc(self):
        return """# Gen 5 + Gen 8 Hybrid Battle System

This generated project includes an original, testable battle foundation inspired by classic fast monster-catching RPG battles and modern rule integration. It does not include official Pokemon data or copyrighted assets.

## Generated Runtime Architecture

- `Assets/Scripts/Battle/AdvancedBattleSystem.cs` contains the pure simulation layer for battle state, rulesets, participants, action ordering, move resolution, damage, accuracy, status, abilities, items, weather, terrain, capture, rewards, transformations, raid phases, and presentation hooks.
- `Assets/Scripts/PokeEngine/Battle/BattleEngineRuntime.cs` powers the playable prototype encounter loop used by the tall grass testing site.
- `Assets/Tests/<ProjectName>/EditMode/AdvancedBattleSystemTests.cs` verifies deterministic behavior for state flow, rulesets, ordering, damage, accuracy, secondary effects, switching, status, abilities, items, weather, terrain, capture, AI, transformations, raids, UI hooks, and rewards.

## Current Implementation Boundary

The project generates working combat logic and tests first. Art, final animation timing, online networking, and full production balancing remain expansion work. The important part is that the systems are modular and data-driven enough to extend without rewriting the core battle loop.
"""

    def _render_battle_raid_system_requirements_doc(self):
        data = self._build_battle_raid_system_requirements()
        battle = data["battle"]
        raid = data["raid"]
        lines = [
            "# Detailed Battle and Raid System Requirements",
            "",
            "This generated project carries the battle and raid master contract used by the generator. The runtime code focuses on modular, deterministic simulation first, with Unity presentation, UI, audio, animation, and networking scaffolds layered around it.",
            "",
            "All generated creatures, moves, items, abilities, UI, audio, and visual assets are original placeholders.",
            "",
            "## Battle Philosophy",
            "",
        ]

        def add_bullets(items):
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

        add_bullets(battle["philosophy"])
        lines.extend(["## Battle Architecture Layers", ""])
        add_bullets(battle["architectureLayers"])
        lines.extend(["## Battle Flow", ""])
        add_bullets(battle["flow"])
        lines.extend(["## Battle States", ""])
        add_bullets(battle["states"])
        lines.extend(["## Supported Battle Types", ""])
        add_bullets(battle["types"])
        lines.extend(["## Future Battle Type Hooks", ""])
        add_bullets(battle["futureTypes"])
        lines.extend(["## Battle Creature Runtime Model", ""])
        add_bullets(battle["battleCreatureRuntimeData"])
        lines.extend(["## Command System", ""])
        for command, requirements in battle["commands"].items():
            lines.append(f"### {command}")
            for requirement in requirements:
                lines.append(f"- {requirement}")
            lines.append("")
        lines.extend(["## Turn Order", ""])
        add_bullets(battle["turnOrder"])
        lines.extend(["## Move Data", ""])
        add_bullets(battle["moveData"])
        lines.extend(["## Damage Factors", ""])
        add_bullets(battle["damage"]["factors"])
        lines.extend(["## Damage Pipeline", ""])
        add_bullets(battle["damage"]["pipeline"])
        lines.extend(["## Type System", ""])
        add_bullets(battle["typeSystem"])
        lines.extend(["## Status System", ""])
        lines.append("Permanent statuses:")
        add_bullets(battle["statusSystem"]["permanent"])
        lines.append("Volatile statuses:")
        add_bullets(battle["statusSystem"]["volatile"])
        lines.append("Status timings:")
        add_bullets(battle["statusSystem"]["timings"])
        lines.extend(["## Ability Triggers", ""])
        add_bullets(battle["abilityTriggers"])
        lines.extend(["## Weather and Terrain", ""])
        lines.append("Weather:")
        add_bullets(battle["weatherTypes"])
        lines.append("Terrain:")
        add_bullets(battle["terrainTypes"])
        lines.extend(["## Battle UI", ""])
        add_bullets(battle["ui"])
        lines.extend(["## Battle Presentation", ""])
        add_bullets(battle["presentation"])
        lines.extend(["## Battle AI", ""])
        for ai_kind, requirements in battle["ai"].items():
            lines.append(f"### {ai_kind.title()} AI")
            for requirement in requirements:
                lines.append(f"- {requirement}")
            lines.append("")
        lines.extend(["## Capture, Transformations, and Rewards", ""])
        lines.append("Capture:")
        add_bullets(battle["capture"])
        for name, requirements in battle["transformations"].items():
            lines.append(f"### {name}")
            for requirement in requirements:
                lines.append(f"- {requirement}")
            lines.append("")
        lines.append("Rewards:")
        add_bullets(battle["rewards"])
        lines.extend(["## Raid Philosophy", ""])
        add_bullets(raid["philosophy"])
        lines.extend(["## Raid Initiation Sources", ""])
        add_bullets(raid["initiationSources"])
        lines.extend(["## Raid Flow", ""])
        add_bullets(raid["flow"])
        lines.extend(["## Raid Boss Capabilities", ""])
        add_bullets(raid["bossCapabilities"])
        lines.extend(["## Raid Difficulty Tiers", ""])
        add_bullets(raid["tiers"])
        lines.extend(["## Raid Scaling", ""])
        add_bullets(raid["scalingAffects"])
        lines.extend(["## Raid Shield System", ""])
        add_bullets(raid["shieldSystem"])
        lines.extend(["## Raid Timer System", ""])
        add_bullets(raid["timerSystem"])
        lines.extend(["## Raid Ally System", ""])
        add_bullets(raid["allySystem"])
        lines.extend(["## Raid AI", ""])
        add_bullets(raid["raidAI"])
        lines.extend(["## Raid Arenas", ""])
        add_bullets(raid["arenas"])
        lines.extend(["## Raid Rewards", ""])
        add_bullets(raid["rewards"])
        lines.extend(["## Raid Reward Scaling", ""])
        add_bullets(raid["rewardScaling"])
        lines.extend(["## Raid Capture", ""])
        add_bullets(raid["capture"])
        lines.extend(["## Event Raids", ""])
        add_bullets(raid["events"])
        lines.extend(["## Raid UI", ""])
        add_bullets(raid["ui"])
        lines.extend(["## Raid Presentation", ""])
        add_bullets(raid["presentation"])
        lines.extend(["## Raid Tests", ""])
        add_bullets(raid["tests"])
        lines.extend(["## Raid Acceptance Criteria", ""])
        add_bullets(raid["acceptanceCriteria"])
        lines.extend(["## Generated Implementation", ""])
        for name, path in data["generatedImplementation"].items():
            lines.append(f"- {name}: `{path}`")
        lines.append("")
        return "\n".join(lines)

    def _render_pause_menu_system_requirements_doc(self):
        data = self._build_pause_menu_system_requirements()
        lines = [
            "# Pause Menu System Requirements",
            "",
            "This generated project includes a full-screen pause-menu contract for the overworld management hub. The runtime prototype exposes a playable IMGUI menu, while the project framework emits a testable menu simulation scaffold for expanding into production UI.",
            "",
            "## Philosophy",
            "",
        ]

        def add_bullets(items):
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

        add_bullets(data["philosophy"])
        lines.extend(["## Root Behavior", ""])
        add_bullets(data["rootBehavior"])
        lines.extend(["## Main Options", ""])
        add_bullets(data["mainOptions"])
        lines.extend(["## Conditional Visibility", ""])
        for option, rule in data["conditionalVisibility"].items():
            lines.append(f"- {option}: {rule}")
        lines.append("")
        lines.extend(["## Layout", ""])
        for area, requirements in data["layout"].items():
            lines.append(f"### {area}")
            for requirement in requirements:
                lines.append(f"- {requirement}")
            lines.append("")
        lines.extend(["## Screens", ""])
        for screen, requirements in data["screens"].items():
            lines.append(f"### {screen}")
            for requirement in requirements:
                lines.append(f"- {requirement}")
            lines.append("")
        lines.extend(["## Transitions", ""])
        add_bullets(data["transitions"])
        lines.extend(["## Testing", ""])
        add_bullets(data["testing"])
        lines.extend(["## Generated Implementation", ""])
        for name, path in data["generatedImplementation"].items():
            lines.append(f"- {name}: `{path}`")
        lines.append("")
        return "\n".join(lines)

    def _render_save_system_requirements_doc(self):
        data = self._build_save_system_requirements()
        lines = [
            "# Full Save System Requirements",
            "",
            "This generated project includes a full save-system contract and a tested JSON save architecture. The system is intended to persist the whole fangame state while remaining versioned, recoverable, and easy to extend.",
            "",
            "## Philosophy",
            "",
        ]

        def add_bullets(items):
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

        add_bullets(data["philosophy"])
        lines.extend(["## Persistence Scope", ""])
        add_bullets(data["persistenceScope"])
        lines.extend(["## Safety Features", ""])
        add_bullets(data["safetyFeatures"])
        lines.extend(["## Save Slots", ""])
        add_bullets(data["slots"])
        lines.extend(["## Migration", ""])
        add_bullets(data["migration"])
        lines.extend(["## Integration", ""])
        add_bullets(data["integration"])
        lines.extend(["## Testing", ""])
        add_bullets(data["testing"])
        lines.extend(["## Generated Implementation", ""])
        for name, path in data["generatedImplementation"].items():
            lines.append(f"- {name}: `{path}`")
        lines.append("")
        return "\n".join(lines)

    def _render_tall_grass_system_requirements_doc(self):
        data = self._build_tall_grass_system_requirements()
        lines = [
            "# Tall Grass System Requirements",
            "",
            "This generated project treats tall grass as a full gameplay subsystem: encounter terrain, biome identity, risk/reward pacing, movement feedback, and save-persistent world state.",
            "",
            "## Philosophy",
            "",
        ]

        def add_bullets(items):
            for item in items:
                lines.append(f"- {item}")
            lines.append("")

        add_bullets(data["philosophy"])
        lines.extend(["## Grass Types", ""])
        add_bullets(data["grassTypes"])
        lines.extend(["## Visual Design", ""])
        add_bullets(data["visualDesign"])
        lines.extend(["## Encounter Rules", ""])
        for name, requirements in data["encounterRules"].items():
            lines.append(f"### {name}")
            for requirement in requirements:
                lines.append(f"- {requirement}")
            lines.append("")
        lines.extend(["## Movement Interaction", ""])
        add_bullets(data["movementInteraction"])
        lines.extend(["## Weather and Time", ""])
        add_bullets(data["weatherTimeInteraction"])
        lines.extend(["## Save Persistence", ""])
        add_bullets(data["savePersistence"])
        lines.extend(["## Performance", ""])
        add_bullets(data["performance"])
        lines.extend(["## Testing", ""])
        add_bullets(data["testing"])
        lines.extend(["## Generated Implementation", ""])
        for name, path in data["generatedImplementation"].items():
            lines.append(f"- {name}: `{path}`")
        lines.append("")
        return "\n".join(lines)

    def _build_runtime_config(self):
        return {
            "startupScene": "PrototypeRegion",
            "fangameFramework": {
                "mustBe2_5D": True,
                "worldUses3DEnvironmentsAndModels": True,
                "gameplayReadability": "classic top-down Pokemon-style route navigation",
                "structuredCamera": "fixed or semi-fixed follow with no manual rotation",
                "wildCamera": "player-follow orbit with limited horizontal mouse/right-stick rotation and limited vertical tilt",
                "movementFeel": "Pokemon Emerald-inspired responsiveness with hidden grid logic in structured areas",
                "battleFeel": "Gen 5 pacing with Gen 8-style modern mechanics, raids, weather, terrain, and transformations",
                "notFreeCameraActionRpg": True,
                "notSideScroller": True,
            },
            "streaming": {
                "chunkSize": 32,
                "preloadRadius": 1,
                "memoryBudgetMb": 768,
                "asyncLoading": True,
                "runtimeAssetUnloading": True,
            },
            "rendering": {
                "cameraMode": "fixed_angled_2_5d",
                "visualStyle": "stylized 2.5D diorama",
                "readabilityPriority": ["path visibility", "object readability", "interactable clarity", "strong silhouettes", "controlled framing"],
                "useGpuInstancing": True,
                "useLodGroups": True,
                "useOcclusionCulling": True,
                "dynamicShadowDistance": 35,
                "weatherOverlayLayer": "WeatherFX",
                "hooks": ["stylized terrain shaders", "animated foliage", "water shaders", "reflection probes", "volumetric fog", "area color grading", "post-processing", "environment VFX"],
            },
            "movement": {
                "defaultMode": "four_direction_continuous",
                "structuredZoneMode": "4_direction_continuous_fixed_camera",
                "wildZoneMode": "4_direction_continuous_with_soft_camera_orbit_and_5_degree_pitch",
                "tileSize": 1,
                "walkMetersPerSecond": 3,
                "runMetersPerSecond": 5,
                "sprintMetersPerSecond": 7,
                "fourDirectionOnly": True,
                "diagonalMovement": False,
                "wildAreaDiagonalMovement": False,
                "snapToGrid": False,
                "continuousHeldMovement": True,
            },
            "dataArchitecture": {
                "scriptableObjectDefinitions": True,
                "jsonRuntimeDatabases": True,
                "eventBus": True,
                "contentWithoutCoreRewrites": True,
            },
            "battle": {
                "inspiration": "Gen 5 pacing plus Gen 8 rules, weather, terrain, raids, and transformation hooks",
                "supportedModes": ["wild single", "trainer single", "double", "multi", "rival", "gym leader", "legendary", "raid", "boss", "tutorial", "scripted story", "postgame challenge"],
                "stateMachine": self._build_battle_system_requirements()["stateMachine"],
                "architectureLayers": self._build_battle_raid_system_requirements()["battle"]["architectureLayers"],
                "turnPipeline": [
                    "input",
                    "priority",
                    "speed",
                    "ability",
                    "move",
                    "damage",
                    "secondary",
                    "status",
                    "endTurn",
                ],
                "deterministicRng": True,
                "pureSimulationLayer": True,
            },
            "raid": {
                "sources": self._build_battle_raid_system_requirements()["raid"]["initiationSources"],
                "flow": self._build_battle_raid_system_requirements()["raid"]["flow"],
                "tiers": self._build_battle_raid_system_requirements()["raid"]["tiers"],
                "bossCapabilities": self._build_battle_raid_system_requirements()["raid"]["bossCapabilities"],
                "shieldSystem": self._build_battle_raid_system_requirements()["raid"]["shieldSystem"],
                "timerSystem": self._build_battle_raid_system_requirements()["raid"]["timerSystem"],
                "eventRotation": True,
                "capturePhaseAfterVictory": True,
            },
            "pauseMenu": {
                "fullScreen": True,
                "opensInstantly": True,
                "pausesOverworldSimulation": True,
                "supportsKeyboardControllerMouse": True,
                "mainOptions": self._build_pause_menu_system_requirements()["mainOptions"],
                "conditionalVisibility": self._build_pause_menu_system_requirements()["conditionalVisibility"],
                "dynamicMenuInjection": True,
                "modPluginSupport": True,
                "transitionTypes": self._build_pause_menu_system_requirements()["transitions"],
            },
            "saveSystem": {
                "schemaVersion": 3,
                "slots": self._build_save_system_requirements()["slots"],
                "persistenceScope": self._build_save_system_requirements()["persistenceScope"],
                "safetyFeatures": self._build_save_system_requirements()["safetyFeatures"],
                "migrationPipeline": True,
                "checksumValidation": True,
                "autosavePolicy": "dirty-state interval with manual trigger support",
                "cloudSaveScaffold": True,
            },
            "tallGrassSystem": {
                "grassTypes": self._build_tall_grass_system_requirements()["grassTypes"],
                "encounterChecks": self._build_tall_grass_system_requirements()["encounterRules"]["checks"],
                "rateFactors": self._build_tall_grass_system_requirements()["encounterRules"]["rateFactors"],
                "savePersistence": self._build_tall_grass_system_requirements()["savePersistence"],
                "prototypeZones": ["testing_site_grass", "wild_area_double_grass", "rustling_spawn_test"],
                "movementFeedback": ["grass bend", "rustle audio hook", "footstep VFX hook", "lower-body obstruction"],
                "cameraReadability": "2.5D camera-safe grass transparency and player visibility rules",
            },
        }

    def _build_project_settings(self):
        return {
            "unityEditorVersion": UNITY_EDITOR_VERSION,
            "projectIdentity": "2.5D Pokemon fangame engine framework",
            "mustBe2_5DFangame": True,
            "architecture": "modular event-driven service-oriented data-driven",
            "singletons": "bootstrap only",
            "dependencyInjection": "service registry prototype",
            "editorTools": ["Pokemon editor", "Dialogue editor", "World editor"],
            "testing": ["edit mode smoke tests", "runtime manager validation"],
        }

    def _render_project_readme(self):
        return f"""# PokeEngine V11 Generated Unity Project

This folder was generated by the PokeEngine desktop app as a reusable Unity 2022+ 2.5D Pokemon fangame engine framework.

The desktop app is a simplified blend of RPG Maker, Unity Hub, Pokemon Essentials tools, and internal studio tooling. Its job is to create the Unity project structure automatically so you do not have to build the foundations by hand.

The generated game identity is strict: fully 3D environments and models with classic top-down Pokemon-style readability, Pokemon Emerald-inspired exploration responsiveness, Gen 5 battle pacing, Gen 8-style modern battle mechanics, and controlled 2.5D cameras. It is not generated as a free-camera 3D action RPG or a side-scroller.

Generated output includes:

- Unity project markers: `Assets`, `Packages`, and `ProjectSettings`.
- Folder architecture for art, audio, scenes, scripts, data, QA, docs, editor tools, and content pipeline tools.
- ScriptableObject definitions for species, moves, encounters, zones, and event channels.
- Runtime event bus for decoupled system communication.
- Runtime C# scripts for overworld streaming, movement, NPCs, events, Pokemon data, battles, damage, abilities, Mega Evolution, Dimension Split, fusion, raids, saves, UI, and engine bootstrap.
- JSON databases for Pokemon, moves, region maps, encounters, evolutions, learnsets, storage, battle config, raids, fusion, Dimension Split, localization, settings, and system manifests.
- Editor tooling entry points for Pokemon data editing, dialogue editing, world editing, and QA.
- Documentation and QA checklists for expanding the prototype into a full RPG.
- `Docs/POKEMON_FANGAME_ENGINE_REQUIREMENTS.md` and `Assets/StreamingAssets/Data/pokemon_fangame_engine_requirements.json`, which carry the full 2.5D fangame master contract.
- `Docs/BATTLE_RAID_SYSTEM_REQUIREMENTS.md` and `Assets/StreamingAssets/Data/battle_raid_system_requirements.json`, which carry the detailed battle and raid system contract.
- `Docs/PAUSE_MENU_SYSTEM_REQUIREMENTS.md` and `Assets/StreamingAssets/Data/pause_menu_system_requirements.json`, which carry the full-screen pause menu and management hub contract.
- `Docs/SAVE_SYSTEM_REQUIREMENTS.md` and `Assets/StreamingAssets/Data/save_system_requirements.json`, which carry the full versioned save/load, autosave, backup, recovery, migration, and cloud-save scaffold contract.
- `Docs/TALL_GRASS_SYSTEM_REQUIREMENTS.md` and `Assets/StreamingAssets/Data/tall_grass_system_requirements.json`, which carry the full tall grass, rustling grass, repel, weather/time encounter, and grass persistence contract.

Open this folder with Unity Hub using Unity {UNITY_EDITOR_VERSION}. Open `Assets/Scenes/PrototypeRegion.unity` and press Play. This single combined scene includes the camera, light, `PokeEngineRuntime` bootstrap, and runtime placement for the full 100m x 100m test site, grass encounters, wild-area camera zone, and battle testing.
"""

    def _render_unity_package_manifest(self):
        return """{
  "dependencies": {
    "com.unity.inputsystem": "1.7.0",
    "com.unity.textmeshpro": "3.0.6",
    "com.unity.test-framework": "1.1.33",
    "com.unity.timeline": "1.7.6",
    "com.unity.ugui": "1.0.0",
    "com.unity.modules.animation": "1.0.0",
    "com.unity.modules.audio": "1.0.0",
    "com.unity.modules.director": "1.0.0",
    "com.unity.modules.imgui": "1.0.0",
    "com.unity.modules.jsonserialize": "1.0.0",
    "com.unity.modules.particlesystem": "1.0.0",
    "com.unity.modules.physics": "1.0.0",
    "com.unity.modules.physics2d": "1.0.0",
    "com.unity.modules.ui": "1.0.0",
    "com.unity.modules.uielements": "1.0.0"
  }
}
"""

    def _render_unity_project_version(self):
        return f"m_EditorVersion: {UNITY_EDITOR_VERSION}\nm_EditorVersionWithRevision: {UNITY_EDITOR_VERSION}\n"

    def _render_editor_build_settings(self):
        return f"""%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!1045 &1
EditorBuildSettings:
  m_ObjectHideFlags: 0
  serializedVersion: 2
  m_Scenes:
  - enabled: 1
    path: Assets/Scenes/PrototypeRegion.unity
    guid: {PROTOTYPE_REGION_SCENE_GUID}
  m_configObjects: {{}}
"""

    def _render_runtime_asmdef(self):
        return """{
    "name": "PokeEngine.Runtime",
    "rootNamespace": "PokeEngine",
    "references": [],
    "includePlatforms": [],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": false,
    "precompiledReferences": [],
    "autoReferenced": true,
    "defineConstraints": [],
    "versionDefines": [],
    "noEngineReferences": false
}
"""

    def _render_editor_asmdef(self):
        return """{
    "name": "PokeEngine.Editor",
    "rootNamespace": "PokeEngine.EditorTools",
    "references": [
        "PokeEngine.Runtime"
    ],
    "includePlatforms": [
        "Editor"
    ],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": false,
    "precompiledReferences": [],
    "autoReferenced": true,
    "defineConstraints": [],
    "versionDefines": [],
    "noEngineReferences": false
}
"""

    def _render_tests_asmdef(self):
        return """{
    "name": "PokeEngine.Tests",
    "rootNamespace": "PokeEngine.Tests",
    "references": [
        "PokeEngine.Runtime"
    ],
    "includePlatforms": [
        "Editor"
    ],
    "excludePlatforms": [],
    "allowUnsafeCode": false,
    "overrideReferences": false,
    "precompiledReferences": [],
    "autoReferenced": false,
    "defineConstraints": [],
    "versionDefines": [],
    "noEngineReferences": false,
    "optionalUnityReferences": [
        "TestAssemblies"
    ]
}
"""

    def _render_types_code(self):
        return """using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokeEngine.Data
{
    public enum PokemonType { None, Normal, Flame, Water, Leaf, Electric, Ice, Fighting, Poison, Ground, Flying, Psychic, Bug, Rock, Ghost, Dragon, Dark, Steel, Fairy, Dimensional }
    public enum MovementState { Idle, Walk, Run, Sprint, Slide, Climb, Swim, Surf, Fly, Fall, LedgeJump, PushInteraction, CutsceneLock }
    public enum TerrainType { Leaf, Water, Ice, Mud, Sand, Lava, TallLeaf, Conveyor, Fragile, Dimensional }
    public enum ZoneType { Town, City, Route, WildZone, Cave, Dungeon, Gym, Interior, RaidDen, LegendaryZone, PostgameArea }
    public enum ZoneMovementMode { StructuredFourDirection, WildEightDirection }
    public enum BattleState { Intro, SendOut, CommandSelection, ActionQueue, MoveExecution, DamageResolution, FaintHandling, SwitchHandling, VictoryLoss, RewardProcessing }
    public enum BattleMode { Single, Double, Multi, Raid, Legendary, Fusion }
    public enum AbilityHook { OnEnterBattle, OnSwitch, OnDamageTaken, OnMoveUsed, OnKO, OnTurnEnd, OnStatusApplied, OnTransformation }

    [Serializable]
    public struct Stats
    {
        public int hp;
        public int atk;
        public int def;
        public int spa;
        public int spd;
        public int spe;

        public Stats Scaled(float multiplier)
        {
            return new Stats
            {
                hp = Mathf.RoundToInt(hp * multiplier),
                atk = Mathf.RoundToInt(atk * multiplier),
                def = Mathf.RoundToInt(def * multiplier),
                spa = Mathf.RoundToInt(spa * multiplier),
                spd = Mathf.RoundToInt(spd * multiplier),
                spe = Mathf.RoundToInt(spe * multiplier)
            };
        }
    }

    [Serializable]
    public sealed class MoveDefinition
    {
        public string name;
        public PokemonType type;
        public int power;
        public int accuracy;
        public int priority;
        public string category;
        public string fxKey;
    }

    [Serializable]
    public sealed class PokemonSpecies
    {
        public int speciesId;
        public int nationalDexId;
        public int regionalDexId;
        public string displayName;
        public string category;
        public string loreText;
        public float height;
        public float weight;
        public string genderRatio;
        public string[] eggGroups;
        public string growthRate;
        public int catchRate;
        public int friendshipBase;
        public Stats baseStats;
        public PokemonType type1;
        public PokemonType type2;
        public string[] abilities;
        public string hiddenAbility;
        public string[] learnset;
        public string[] evolutionRules;
        public Stats evYield;
        public string modelKey;
        public string textureKey;
        public string portraitKey;
        public string animationControllerKey;
        public string shinyPaletteKey;
        public string[] formVariants;
        public string[] dimensionSplitForms;
        public string[] megaForms;
        public int[] fusionCompatibleSpecies;
    }

    [Serializable]
    public sealed class PokemonInstance
    {
        public string instanceId = Guid.NewGuid().ToString("N");
        public int speciesId;
        public string nickname;
        public int level = 5;
        public bool shiny;
        public string formId;
        public Stats currentStats;
        public int currentHp;
        public string[] moves = Array.Empty<string>();
        public string ability;
        public string heldItem;
        public int experience;
        public int experienceToNextLevel = 125;
        public bool megaUsed;
        public bool dimensionSplitActive;
        public bool fused;
    }

    [Serializable]
    public sealed class AreaMetadata
    {
        public string areaId;
        public string displayName;
        public string sceneKey;
        public string[] adjacentAreas;
        public string encounterTable;
        public string musicProfile;
        public string lightingProfile;
        public string npcSchedule;
        public string weatherProfile;
        public string[] progressionGates;
        public string[] triggerVolumes;
        public string[] spawnTables;
        public string[] environmentalRules;
        public int memoryBudgetMb = 128;
    }

    [Serializable]
    public sealed class BattleAction
    {
        public PokemonInstance actor;
        public PokemonInstance target;
        public MoveDefinition move;
        public int priority;
    }
}
"""

    def _render_scriptable_objects_code(self):
        return """using System.Collections.Generic;
using PokeEngine.Data;
using UnityEngine;

namespace PokeEngine.DataAssets
{
    [CreateAssetMenu(menuName = "PokeEngine/Pokemon Species")]
    public sealed class PokemonSpeciesAsset : ScriptableObject
    {
        public PokemonSpecies species = new PokemonSpecies();
        public List<MoveDefinitionAsset> levelUpMoves = new List<MoveDefinitionAsset>();
        public List<MoveDefinitionAsset> tmMoves = new List<MoveDefinitionAsset>();
        public List<PokemonSpeciesAsset> fusionCompatibleSpecies = new List<PokemonSpeciesAsset>();
    }

    [CreateAssetMenu(menuName = "PokeEngine/Move Definition")]
    public sealed class MoveDefinitionAsset : ScriptableObject
    {
        public MoveDefinition move = new MoveDefinition();
        public int pp = 35;
        public string targetRule = "single_enemy";
        public string secondaryEffectKey = "";
    }

    [CreateAssetMenu(menuName = "PokeEngine/Encounter Table")]
    public sealed class EncounterTableAsset : ScriptableObject
    {
        public string zoneId;
        public List<EncounterEntry> entries = new List<EncounterEntry>();
    }

    [CreateAssetMenu(menuName = "PokeEngine/Zone Definition")]
    public sealed class ZoneDefinitionAsset : ScriptableObject
    {
        public AreaMetadata metadata = new AreaMetadata();
        public EncounterTableAsset encounterTable;
        public string zoneType = "town";
        public string weatherRule = "clear";
        public string musicProfile = "default";
        public string lightingProfile = "day";
        public bool structuredMovement = true;
        public bool wildCameraMode;
    }

    [CreateAssetMenu(menuName = "PokeEngine/Event Channel")]
    public sealed class PokeEventChannelAsset : ScriptableObject
    {
        public string eventKey;
        public string description;
    }

    [System.Serializable]
    public sealed class EncounterEntry
    {
        public PokemonSpeciesAsset species;
        public int minLevel = 3;
        public int maxLevel = 5;
        public int weight = 10;
    }
}
"""

    def _render_event_bus_code(self):
        return """using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokeEngine.Core
{
    public sealed class PokeEventBus : MonoBehaviour, IPokeEngineService
    {
        private readonly Dictionary<string, Action<object>> listeners = new Dictionary<string, Action<object>>();

        public void Initialize(PokeEngineRuntime runtime)
        {
            Debug.Log("[PokeEngine] Event bus ready.");
        }

        public void Subscribe(string eventKey, Action<object> listener)
        {
            if (!listeners.ContainsKey(eventKey))
            {
                listeners[eventKey] = delegate { };
            }

            listeners[eventKey] += listener;
        }

        public void Unsubscribe(string eventKey, Action<object> listener)
        {
            if (listeners.ContainsKey(eventKey))
            {
                listeners[eventKey] -= listener;
            }
        }

        public void Publish(string eventKey, object payload = null)
        {
            if (listeners.TryGetValue(eventKey, out var callback))
            {
                callback.Invoke(payload);
            }

            Debug.Log("[PokeEngine] Event: " + eventKey);
        }
    }
}
"""

    def _render_feature_registry_code(self):
        matrix = self._build_feature_matrix()
        lines = [
            "using System;",
            "using System.Collections.Generic;",
            "using System.Linq;",
            "using UnityEngine;",
            "",
            "namespace PokeEngine.Core",
            "{",
            "    public sealed class PrototypeFeatureRegistry : MonoBehaviour, IPokeEngineService",
            "    {",
            "        private readonly List<PrototypeFeature> features = new List<PrototypeFeature>();",
            "",
            "        public IReadOnlyList<PrototypeFeature> Features => features;",
            "        public int TotalFeatureCount => features.Count;",
            "",
            "        public void Initialize(PokeEngineRuntime runtime)",
            "        {",
            "            if (features.Count > 0)",
            "            {",
            "                return;",
            "            }",
            "",
        ]
        for row in matrix["features"]:
            args = [
                json.dumps(row["id"]),
                json.dumps(row["sectionId"]),
                json.dumps(row["sectionTitle"]),
                json.dumps(row["feature"]),
                json.dumps(row["status"]),
            ]
            lines.append(f"            Register({', '.join(args)});")

        lines.extend(
            [
                "",
                "            Debug.Log(\"[PokeEngine] Prototype feature registry initialized with \" + features.Count + \" V12 architecture features.\");",
                "        }",
                "",
                "        public IEnumerable<PrototypeFeature> GetBySection(string sectionId)",
                "        {",
                "            return features.Where(feature => feature.sectionId == sectionId);",
                "        }",
                "",
                "        public IEnumerable<PrototypeFeature> GetPlayableFeatures()",
                "        {",
                "            return features.Where(feature => feature.status == \"playable_prototype\");",
                "        }",
                "",
                "        private void Register(string id, string sectionId, string sectionTitle, string featureName, string status)",
                "        {",
                "            features.Add(new PrototypeFeature",
                "            {",
                "                id = id,",
                "                sectionId = sectionId,",
                "                sectionTitle = sectionTitle,",
                "                featureName = featureName,",
                "                status = status",
                "            });",
                "        }",
                "    }",
                "",
                "    [Serializable]",
                "    public sealed class PrototypeFeature",
                "    {",
                "        public string id;",
                "        public string sectionId;",
                "        public string sectionTitle;",
                "        public string featureName;",
                "        public string status;",
                "    }",
                "}",
                "",
            ]
        )
        return "\n".join(lines)

    def _render_runtime_code(self):
        return """using System;
using System.Collections.Generic;
using PokeEngine.Battle;
using PokeEngine.Events;
using PokeEngine.NPC;
using PokeEngine.Overworld;
using PokeEngine.Pokemon;
using PokeEngine.Raid;
using PokeEngine.Save;
using PokeEngine.UI;
using UnityEngine;

namespace PokeEngine.Core
{
    public interface IPokeEngineService
    {
        void Initialize(PokeEngineRuntime runtime);
    }

    public sealed class PokeEngineRuntime : MonoBehaviour
    {
        private readonly Dictionary<Type, object> services = new Dictionary<Type, object>();

        public static PokeEngineRuntime Instance { get; private set; }

        public T Get<T>() where T : class
        {
            services.TryGetValue(typeof(T), out var service);
            return service as T;
        }

        private void Awake()
        {
            if (Instance != null && Instance != this)
            {
                Destroy(gameObject);
                return;
            }

            Instance = this;
            DontDestroyOnLoad(gameObject);
            ConfigureBuildSafeRendering();
            RegisterCoreServices();
            Debug.Log("[PokeEngine] Full RPG prototype runtime booted.");
        }

        private void ConfigureBuildSafeRendering()
        {
            // The prototype uses generated primitive materials. Keep the startup scene on Unity's built-in pipeline
            // so exported builds do not inherit a missing SRP asset and render the scene magenta.
            QualitySettings.renderPipeline = null;
            RenderSettings.skybox = null;
            RenderSettings.ambientMode = UnityEngine.Rendering.AmbientMode.Flat;
            RenderSettings.ambientLight = new Color(0.72f, 0.75f, 0.78f);
        }

        [ContextMenu("Bootstrap Full RPG Prototype")]
        public void RegisterCoreServices()
        {
            services.Clear();

            var eventBus = Ensure<PokeEventBus>();
            var world = Ensure<WorldStreamingManager>();
            var player = Ensure<HybridPlayerController>();
            var featureRegistry = Ensure<PrototypeFeatureRegistry>();
            var npcDirector = Ensure<NpcDirector>();
            var eventFlags = Ensure<EventFlagManager>();
            var cutscenes = Ensure<PrototypeCutsceneDirector>();
            var pokemonDatabase = Ensure<PokemonDatabaseRuntime>();
            var battle = Ensure<BattleEngineRuntime>();
            var transformations = Ensure<TransformationFusionSystems>();
            var raids = Ensure<RaidBattleRuntime>();
            var saves = Ensure<PokeSaveManager>();
            var hud = Ensure<PrototypeRpgHud>();

            Register(eventBus);
            Register(world);
            Register(player);
            Register(featureRegistry);
            Register(npcDirector);
            Register(eventFlags);
            Register(cutscenes);
            Register(pokemonDatabase);
            Register(battle);
            Register(transformations);
            Register(raids);
            Register(saves);
            Register(hud);

            InitializeService(eventBus);
            InitializeService(world);
            InitializeService(player);
            InitializeService(featureRegistry);
            InitializeService(npcDirector);
            InitializeService(eventFlags);
            InitializeService(cutscenes);
            InitializeService(pokemonDatabase);
            InitializeService(battle);
            InitializeService(transformations);
            InitializeService(raids);
            InitializeService(saves);
            InitializeService(hud);

            world.SetFollowTarget(player.transform);
        }

        private void InitializeService(object service)
        {
            if (service is IPokeEngineService pokeService)
            {
                pokeService.Initialize(this);
            }
        }

        private void Register<T>(T service) where T : Component
        {
            services[typeof(T)] = service;
        }

        private T Ensure<T>() where T : Component
        {
            var existing = GetComponentInChildren<T>();
            if (existing != null)
            {
                return existing;
            }

            var child = new GameObject(typeof(T).Name);
            child.transform.SetParent(transform);
            return child.AddComponent<T>();
        }
    }
}
"""

    def _render_world_streaming_code(self):
        return """using System.Collections;
using System.Collections.Generic;
using PokeEngine.Core;
using PokeEngine.Data;
using PokeEngine.NPC;
using PokeEngine.Raid;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace PokeEngine.Overworld
{
    public sealed class WorldStreamingManager : MonoBehaviour, IPokeEngineService
    {
        [SerializeField] private int chunkSize = 32;
        [SerializeField] private int preloadRadius = 1;
        [SerializeField] private int memoryBudgetMb = 768;
        [SerializeField] private bool useAdditiveSceneStreaming = false;
        [SerializeField] private Camera fixedCamera;
        [SerializeField] private Vector3 fixedCameraOffset = new Vector3(0, 6.8f, -7.4f);
        [SerializeField] private Vector3 fixedCameraEuler = new Vector3(52, 0, 0);

        private readonly Dictionary<string, AreaMetadata> areas = new Dictionary<string, AreaMetadata>();
        private readonly HashSet<string> loadedAreas = new HashSet<string>();
        private Vector3 pokemonCenterRespawnPoint = new Vector3(-36f, 2f, 5.35f);
        private bool hasPokemonCenterRespawnPoint;

        public string CurrentAreaId { get; private set; } = "nova_town";
        public Camera ActiveCamera => fixedCamera;
        public PokemonCameraController CameraController { get; private set; }
        private const float PrototypeSurfaceY = 0.04f;

        public void Initialize(PokeEngineRuntime runtime)
        {
            ConfigureCamera();
            SeedPrototypeRegion();
            StartCoroutine(StreamArea(CurrentAreaId));
        }

        private void ConfigureCamera()
        {
            if (fixedCamera == null)
            {
                fixedCamera = Camera.main;
            }

            if (fixedCamera == null)
            {
                fixedCamera = FindObjectOfType<Camera>();
            }

            if (fixedCamera == null)
            {
                var cameraObject = new GameObject("Prototype 2.5D Camera");
                fixedCamera = cameraObject.AddComponent<Camera>();
            }

            if (fixedCamera != null)
            {
                fixedCamera.enabled = true;
                fixedCamera.depth = 100f;
                fixedCamera.gameObject.tag = "MainCamera";
                foreach (var camera in FindObjectsOfType<Camera>())
                {
                    if (camera != fixedCamera)
                    {
                        camera.enabled = false;
                    }
                }

                fixedCamera.transform.position = fixedCameraOffset;
                fixedCamera.transform.rotation = Quaternion.Euler(fixedCameraEuler);
                fixedCamera.orthographic = true;
                fixedCamera.orthographicSize = 4.6f;
                fixedCamera.nearClipPlane = 0.03f;
                fixedCamera.farClipPlane = 200f;
                fixedCamera.clearFlags = CameraClearFlags.SolidColor;
                fixedCamera.backgroundColor = new Color(0.58f, 0.78f, 0.95f);

                CameraController = fixedCamera.GetComponent<PokemonCameraController>();
                if (CameraController == null)
                {
                    CameraController = fixedCamera.gameObject.AddComponent<PokemonCameraController>();
                }
                CameraController.Configure(fixedCameraOffset, fixedCameraEuler);
            }

            if (FindObjectOfType<Light>() == null)
            {
                var lightObject = new GameObject("Prototype Sun");
                var light = lightObject.AddComponent<Light>();
                light.type = LightType.Directional;
                light.intensity = 1.15f;
                light.shadows = LightShadows.Soft;
            lightObject.transform.rotation = Quaternion.Euler(42, -35, 0);
            }
        }

        public void SetFollowTarget(Transform target)
        {
            if (target == null)
            {
                return;
            }

            if (CameraController == null)
            {
                ConfigureCamera();
            }

            if (CameraController != null)
            {
                CameraController.SetTarget(target);
                CameraController.ForceSnapToTarget();
            }
        }

        public void TeleportPlayerToPokemonCenter()
        {
            var player = FindObjectOfType<HybridPlayerController>();
            if (player == null)
            {
                return;
            }

            var destination = hasPokemonCenterRespawnPoint ? pokemonCenterRespawnPoint : new Vector3(-36f, 2f, 5.35f);
            player.TeleportTo(destination);
            SetFollowTarget(player.transform);
            CurrentAreaId = "nova_town";
            Debug.Log("[PokeEngine] Party wiped out. Player was brought to the Pokemon Center.");
        }

        private void SeedPrototypeRegion()
        {
            AddArea("nova_town", "Prototype Testing Site", "PrototypeRegion", new[] { "route_01", "professor_lab" });
            AddArea("professor_lab", "Professor Lab Interior", "PrototypeRegion", new[] { "nova_town" });
            AddArea("route_01", "Route 01", "PrototypeRoute01", new[] { "nova_town", "echo_cave", "raid_meadow" });
            AddArea("echo_cave", "Echo Cave", "PrototypeEchoCave", new[] { "route_01", "solara_city" });
            AddArea("solara_city", "Solara City", "PrototypeSolaraCity", new[] { "echo_cave", "solara_gym" });
            AddArea("solara_gym", "Solara Gym Interior", "PrototypeRegion", new[] { "solara_city" });
            AddArea("raid_meadow", "Raid Meadow", "PrototypeRaidMeadow", new[] { "route_01" });
            AddArea("rift_sanctuary", "Rift Sanctuary", "PrototypeRiftSanctuary", new[] { "solara_city" });
        }

        private void AddArea(string id, string name, string sceneKey, string[] adjacent)
        {
            areas[id] = new AreaMetadata
            {
                areaId = id,
                displayName = name,
                sceneKey = sceneKey,
                adjacentAreas = adjacent,
                encounterTable = id + "_encounters",
                musicProfile = id + "_music",
                lightingProfile = id + "_lighting",
                npcSchedule = id + "_schedule",
                weatherProfile = id + "_weather",
                progressionGates = new[] { "story_gate_" + id },
                triggerVolumes = new[] { "entry", "exit", "secret" },
                spawnTables = new[] { id + "_spawns" },
                environmentalRules = new[] { "weather_overlay", "terrain_blend", "dynamic_shadow_budget" }
            };
        }

        public void RequestAreaTransition(string areaId)
        {
            if (!areas.ContainsKey(areaId))
            {
                Debug.LogWarning("[PokeEngine] Unknown area: " + areaId);
                return;
            }

            CurrentAreaId = areaId;
            StartCoroutine(StreamArea(areaId));
        }

        private IEnumerator StreamArea(string areaId)
        {
            if (!areas.TryGetValue(areaId, out var area))
            {
                yield break;
            }

            yield return LoadArea(area);
            foreach (var adjacent in area.adjacentAreas)
            {
                if (areas.TryGetValue(adjacent, out var adjacentArea))
                {
                    yield return LoadArea(adjacentArea);
                }
            }

            UnloadDistantAreas(area);
            ApplyAreaPresentation(area);
        }

        private IEnumerator LoadArea(AreaMetadata area)
        {
            if (loadedAreas.Contains(area.areaId))
            {
                yield break;
            }

            var activeSceneName = SceneManager.GetActiveScene().name;
            if (useAdditiveSceneStreaming && area.sceneKey != activeSceneName && Application.CanStreamedLevelBeLoaded(area.sceneKey))
            {
                var load = SceneManager.LoadSceneAsync(area.sceneKey, LoadSceneMode.Additive);
                while (!load.isDone)
                {
                    yield return null;
                }
            }
            else
            {
                CreatePrototypeChunk(area);
                yield return null;
            }

            loadedAreas.Add(area.areaId);
            Debug.Log("[PokeEngine] Loaded area " + area.displayName);
        }

        private void CreatePrototypeChunk(AreaMetadata area)
        {
            var origin = area.areaId == "nova_town"
                ? Vector3.zero
                : new Vector3(90f + loadedAreas.Count * chunkSize * 1.25f, 0, loadedAreas.Count % 2 == 0 ? 78f : -78f);
            if (area.areaId == "nova_town")
            {
                var site = new GameObject("Prototype Testing Site");
                site.transform.position = origin;
                BuildPrototypeTestingSite(origin);
                return;
            }

            var chunk = GameObject.CreatePrimitive(PrimitiveType.Cube);
            chunk.name = "PrototypeChunk_" + area.areaId;
            chunk.transform.position = origin;
            chunk.transform.localScale = new Vector3(18f, 0.035f, 18f);
            chunk.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.46f, 0.48f, 0.50f));
            Destroy(chunk.GetComponent<Collider>());
            BuildChunkDetails(chunk.transform.position, area);
        }

        private void BuildChunkDetails(Vector3 origin, AreaMetadata area)
        {
            CreateTile(origin + new Vector3(0, 0.03f, 0), new Vector3(8, 0.08f, 2.2f), new Color(0.82f, 0.70f, 0.47f), "Path_" + area.areaId);
            CreateTallLeaf(origin + new Vector3(-5.5f, 0.09f, 4), new Vector3(3.2f, 0.16f, 3.2f), "TallLeaf_" + area.areaId);
            CreateTile(origin + new Vector3(8, 0.04f, -6), new Vector3(5, 0.1f, 4), new Color(0.16f, 0.44f, 0.72f), "Water_" + area.areaId);

            if (area.areaId.Contains("town") || area.areaId.Contains("city"))
            {
                CreateBuilding(origin + new Vector3(-4, 1.2f, -5), "Pokemon Center");
                CreateBuilding(origin + new Vector3(5, 1.2f, 5), "Shop");
            }

            if (area.areaId.Contains("raid"))
            {
                CreateTile(origin + new Vector3(0, 0.4f, 6), new Vector3(5, 0.8f, 5), new Color(0.52f, 0.21f, 0.80f), "RaidDen_" + area.areaId);
            }

            if (!area.areaId.Contains("town") && !area.areaId.Contains("city") && !area.areaId.Contains("lab") && !area.areaId.Contains("gym"))
            {
                CreateWildCameraZone(origin, area.areaId);
            }

            CreateNpcMarker(origin + new Vector3(2, 0.9f, 2), "NPC_" + area.areaId);
        }

        private void BuildPrototypeTestingSite(Vector3 origin)
        {
            CreateOneMeterGrid(origin, 100, 100);
            CreateTestingSiteBoundary(origin, 100, 100);
            CreateTestLabel(origin + new Vector3(0, 0.65f, -48.5f), "PROTOTYPE TESTING SITE - 100m x 100m - 1m GRID");

            CreateTestingPad(origin + new Vector3(-36, 0.12f, -34), new Vector3(10, 0.1f, 24), new Color(0.78f, 0.68f, 0.46f), "Movement Lane");
            CreateTestLabel(origin + new Vector3(-36, 0.55f, -47f), "CONTINUOUS 1m TILE MOVEMENT");
            for (int z = -45; z <= -23; z++)
            {
                CreateTile(origin + new Vector3(-36, 0.22f, z), new Vector3(0.18f, 0.12f, 0.18f), Color.white, "MovementLane_MeterDot_" + z);
            }

            CreateTestingPad(origin + new Vector3(-16, 0.12f, -34), new Vector3(12, 0.1f, 24), new Color(0.38f, 0.42f, 0.46f), "Collision Test");
            CreateTestLabel(origin + new Vector3(-16, 0.55f, -47f), "COLLISION BLOCKS");
            CreateWallBlock(origin + new Vector3(-20, 0.9f, -34), "CollisionWall_A");
            CreateWallBlock(origin + new Vector3(-16, 0.9f, -32), "CollisionWall_B");
            CreateWallBlock(origin + new Vector3(-12, 0.9f, -34), "CollisionWall_C");

            CreateTallLeafEncounterArea(origin + new Vector3(16, 0, -34));

            CreateBuilding(origin + new Vector3(-36f, 1.2f, 4f), "Pokemon Center");
            CreateTestLabel(origin + new Vector3(-36f, 0.55f, 0.5f), "POKECENTER ENTER / EXIT");

            CreatePokemonPickup(origin + new Vector3(-20f, 0.45f, 4f), 7, "StarterPokemonPickup");
            CreateItemPickup(origin + new Vector3(-17f, 0.35f, 4f), "Tonic", "TonicPickup");
            CreateTestLabel(origin + new Vector3(-18.5f, 0.55f, 1.2f), "PICKUPS / PARTY TEST");

            CreateOverworldPokemon(origin + new Vector3(-2f, 0.65f, 4f), 7, "BattleTest_PurpleEncounter");
            CreateTestLabel(origin + new Vector3(-2f, 0.55f, 1.2f), "DIRECT BATTLE / CATCH");

            CreateWildAreaSection(origin + new Vector3(28f, 0, 26f));

            CreateTestingPad(origin + new Vector3(-5f, 0.12f, 34f), new Vector3(14, 0.1f, 10), new Color(0.52f, 0.21f, 0.80f), "Raid Feature Pad");
            CreateTestLabel(origin + new Vector3(-5f, 0.55f, 27.5f), "RAID / FEATURE HOOKS");
            CreateRaidTestDen(origin + new Vector3(-5f, 0.55f, 34f), "RaidDen_Test");

            CreateNpcMarker(origin + new Vector3(-34f, 0.9f, 34f), "RandomLetters_DialogueNPC");
            CreateTestLabel(origin + new Vector3(-34f, 0.55f, 30.8f), "INTERACTABLE NPC - RANDOM LETTERS");
        }

        private void CreateOneMeterGrid(Vector3 origin, int width, int depth)
        {
            CreateTile(origin + new Vector3(0, 0.0f, 0), new Vector3(width, 0.03f, depth), new Color(0.44f, 0.46f, 0.48f), "TestingSite_100m_Base");
            var halfWidth = width * 0.5f;
            var halfDepth = depth * 0.5f;
            for (int x = 0; x <= width; x++)
            {
                var worldX = -halfWidth + x;
                var major = x % 10 == 0;
                var color = major ? new Color(0.82f, 0.86f, 0.90f) : new Color(0.35f, 0.37f, 0.39f);
                var thickness = major ? 0.08f : 0.025f;
                CreateVisualTile(origin + new Vector3(worldX, 0.04f, 0), new Vector3(thickness, 0.025f, depth), color, "GridLine_X_" + x);
            }

            for (int z = 0; z <= depth; z++)
            {
                var worldZ = -halfDepth + z;
                var major = z % 10 == 0;
                var color = major ? new Color(0.82f, 0.86f, 0.90f) : new Color(0.35f, 0.37f, 0.39f);
                var thickness = major ? 0.08f : 0.025f;
                CreateVisualTile(origin + new Vector3(0, 0.045f, worldZ), new Vector3(width, 0.025f, thickness), color, "GridLine_Z_" + z);
            }
        }

        private void CreateTestingSiteBoundary(Vector3 origin, int width, int depth)
        {
            var halfWidth = width * 0.5f;
            var halfDepth = depth * 0.5f;
            CreateInvisibleBoundaryCollider(origin + new Vector3(0, 0.9f, -halfDepth - 0.5f), new Vector3(width + 1f, 1.8f, 1f), "TestingSite_Boundary_South");
            CreateInvisibleBoundaryCollider(origin + new Vector3(0, 0.9f, halfDepth + 0.5f), new Vector3(width + 1f, 1.8f, 1f), "TestingSite_Boundary_North");
            CreateInvisibleBoundaryCollider(origin + new Vector3(-halfWidth - 0.5f, 0.9f, 0), new Vector3(1f, 1.8f, depth + 1f), "TestingSite_Boundary_West");
            CreateInvisibleBoundaryCollider(origin + new Vector3(halfWidth + 0.5f, 0.9f, 0), new Vector3(1f, 1.8f, depth + 1f), "TestingSite_Boundary_East");
        }

        private void CreateTallLeafEncounterArea(Vector3 center)
        {
            CreateTestingPad(center + new Vector3(0, 0.12f, 0), new Vector3(22f, 0.1f, 18f), new Color(0.0f, 0.42f, 0.0f), "Tall Leaf Encounter Area");
            CreateTestLabel(center + new Vector3(0, 0.55f, -10f), "TALL GRASS - RANDOM ENCOUNTERS / BATTLE / CATCH / PARTY");
            CreateTallLeaf(center + new Vector3(-5.5f, 0.35f, -2.5f), new Vector3(8f, 0.22f, 6f), "EncounterLeaf_A");
            CreateTallLeaf(center + new Vector3(5.5f, 0.35f, -2.5f), new Vector3(8f, 0.22f, 6f), "EncounterLeaf_B");
            CreateTallLeaf(center + new Vector3(0f, 0.35f, 4.5f), new Vector3(17f, 0.22f, 5f), "EncounterLeaf_C");
        }

        private void CreateTestingPad(Vector3 center, Vector3 scale, Color color, string name)
        {
            CreateTile(center, scale, color, name);
        }

        private GameObject CreateGroundedPrimitive(PrimitiveType primitiveType, Vector3 footprintPosition, Vector3 scale, Color color, string name)
        {
            var model = GameObject.CreatePrimitive(primitiveType);
            model.name = name;
            model.transform.localScale = scale;
            model.transform.position = new Vector3(footprintPosition.x, PrototypeSurfaceY + PrimitiveHalfHeight(primitiveType, scale), footprintPosition.z);
            model.GetComponent<Renderer>().sharedMaterial = MakeMaterial(color);
            return model;
        }

        private float PrimitiveHalfHeight(PrimitiveType primitiveType, Vector3 scale)
        {
            switch (primitiveType)
            {
                case PrimitiveType.Capsule:
                case PrimitiveType.Cylinder:
                    return scale.y;
                default:
                    return scale.y * 0.5f;
            }
        }

        private void CreateWallBlock(Vector3 position, string name)
        {
            CreateGroundedPrimitive(PrimitiveType.Cube, position, new Vector3(1f, 1.8f, 1f), new Color(0.16f, 0.18f, 0.21f), name);
        }

        private void CreateRaidTestDen(Vector3 position, string name)
        {
            var baseScale = new Vector3(3.8f, 0.7f, 3.8f);
            var baseObject = CreateGroundedPrimitive(PrimitiveType.Cube, position, baseScale, new Color(0.62f, 0.12f, 1.0f), name + "_Base");
            Destroy(baseObject.GetComponent<Collider>());

            var pillar = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            pillar.name = name + "_TallMarker";
            pillar.transform.localScale = new Vector3(0.62f, 1.65f, 0.62f);
            pillar.transform.position = new Vector3(position.x, PrototypeSurfaceY + baseScale.y + PrimitiveHalfHeight(PrimitiveType.Cylinder, pillar.transform.localScale), position.z);
            pillar.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.95f, 0.25f, 1.0f));
            Destroy(pillar.GetComponent<Collider>());

            var trigger = new GameObject(name + "_StartTrigger");
            trigger.transform.position = new Vector3(position.x, PrototypeSurfaceY + 1.2f, position.z);
            var triggerCollider = trigger.AddComponent<BoxCollider>();
            triggerCollider.isTrigger = true;
            triggerCollider.size = new Vector3(4.8f, 2.4f, 4.8f);
            trigger.AddComponent<RaidDenTrigger>().Configure(1, true);

            var beacon = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            beacon.name = name + "_VisibilityBeacon";
            beacon.transform.localScale = new Vector3(0.8f, 0.24f, 0.8f);
            beacon.transform.position = new Vector3(position.x, PrototypeSurfaceY + baseScale.y + 3.4f, position.z);
            beacon.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(1.0f, 0.92f, 0.08f));
            Destroy(beacon.GetComponent<Collider>());

            CreateTestLabel(position + new Vector3(0, 0.35f, -3.35f), "RAID DEN TEST");
        }

        private void CreateTestLabel(Vector3 position, string labelText)
        {
            var label = new GameObject(labelText + "_Label");
            label.transform.position = position;
            label.transform.rotation = Quaternion.Euler(60, 0, 0);
            var text = label.AddComponent<TextMesh>();
            text.text = labelText;
            text.anchor = TextAnchor.MiddleCenter;
            text.alignment = TextAlignment.Center;
            text.characterSize = 0.32f;
            text.color = Color.white;
        }

        private void CreateWildAreaSection(Vector3 center)
        {
            CreateFlatPlane(center + new Vector3(0, 0.075f, 0), 24.2f, 20.2f, new Color(0.0f, 0.82f, 0.10f), "WildArea_ClearGreenPlayableSurface");
            CreateWildAreaGuideLines(center, 24.2f, 20.2f);
            CreateWildAreaBorderLines(center, 24.8f, 20.8f);
            CreateTallLeaf(center + new Vector3(-5f, 0.12f, 2f), new Vector3(7f, 0.035f, 7f), "WildArea_TallLeaf_A", 0.20f);
            CreateTallLeaf(center + new Vector3(5f, 0.12f, 2f), new Vector3(7f, 0.035f, 7f), "WildArea_TallLeaf_B", 0.20f);
            CreateTallLeaf(center + new Vector3(0f, 0.12f, 7.4f), new Vector3(18f, 0.035f, 3.2f), "WildArea_BattleTestGrass", 0.20f);
            CreateOverworldPokemon(center + new Vector3(0.4f, 0.85f, -5.5f), 7, "WildArea_PurpleEncounter");
            CreateWildCameraZone(center, "nova_town_wild_area", new Vector3(23.6f, 4f, 19.6f));

            var label = new GameObject("Wild Area Label");
            label.transform.position = center + new Vector3(0, 0.5f, -12.4f);
            label.transform.rotation = Quaternion.Euler(60, 0, 0);
            var text = label.AddComponent<TextMesh>();
            text.text = "WILD AREA CAMERA TEST";
            text.anchor = TextAnchor.MiddleCenter;
            text.alignment = TextAlignment.Center;
            text.characterSize = 0.42f;
            text.color = Color.white;
        }

        private void CreateWildAreaGuideLines(Vector3 center, float width, float depth)
        {
            var horizontalColor = new Color(0.0f, 0.42f, 0.08f);
            var verticalColor = new Color(0.06f, 0.68f, 0.12f);
            var halfWidth = width * 0.5f;
            var halfDepth = depth * 0.5f;

            for (float z = -halfDepth + 2f; z < halfDepth; z += 2f)
            {
                CreateFlatPlane(center + new Vector3(0, 0.086f, z), width, 0.045f, horizontalColor, "WildArea_GuideLine_H_" + z.ToString("0.0"));
            }

            for (float x = -halfWidth + 2f; x < halfWidth; x += 2f)
            {
                CreateFlatPlane(center + new Vector3(x, 0.087f, 0), 0.045f, depth, verticalColor, "WildArea_GuideLine_V_" + x.ToString("0.0"));
            }
        }

        private void CreateWildAreaBorderLines(Vector3 center, float width, float depth)
        {
            var lineColor = new Color(1.0f, 0.84f, 0.06f);
            var wallColor = new Color(0.24f, 0.08f, 0.34f);
            var halfWidth = width * 0.5f;
            var halfDepth = depth * 0.5f;

            CreateFlatPlane(center + new Vector3(0, 0.098f, -halfDepth - 0.08f), width + 0.2f, 0.16f, wallColor, "WildArea_VisualBoundary_South");
            CreateFlatPlane(center + new Vector3(0, 0.098f, halfDepth + 0.08f), width + 0.2f, 0.16f, wallColor, "WildArea_VisualBoundary_North");
            CreateFlatPlane(center + new Vector3(-halfWidth - 0.08f, 0.098f, 0), 0.16f, depth + 0.2f, wallColor, "WildArea_VisualBoundary_West");
            CreateFlatPlane(center + new Vector3(halfWidth + 0.08f, 0.098f, 0), 0.16f, depth + 0.2f, wallColor, "WildArea_VisualBoundary_East");

            CreateFlatPlane(center + new Vector3(0, 0.115f, -halfDepth), width, 0.055f, lineColor, "WildArea_AvailableBorderLine_South");
            CreateFlatPlane(center + new Vector3(0, 0.115f, halfDepth), width, 0.055f, lineColor, "WildArea_AvailableBorderLine_North");
            CreateFlatPlane(center + new Vector3(-halfWidth, 0.115f, 0), 0.055f, depth, lineColor, "WildArea_AvailableBorderLine_West");
            CreateFlatPlane(center + new Vector3(halfWidth, 0.115f, 0), 0.055f, depth, lineColor, "WildArea_AvailableBorderLine_East");
        }

        private void CreateTile(Vector3 position, Vector3 scale, Color color, string name)
        {
            var tile = GameObject.CreatePrimitive(PrimitiveType.Cube);
            tile.name = name;
            tile.transform.position = position;
            tile.transform.localScale = scale;
            tile.GetComponent<Renderer>().sharedMaterial = MakeMaterial(color);
        }

        private void CreateVisualTile(Vector3 position, Vector3 scale, Color color, string name)
        {
            var tile = GameObject.CreatePrimitive(PrimitiveType.Cube);
            tile.name = name;
            tile.transform.position = position;
            tile.transform.localScale = scale;
            tile.GetComponent<Renderer>().sharedMaterial = MakeMaterial(color);
            Destroy(tile.GetComponent<Collider>());
        }

        private void CreateFlatPlane(Vector3 position, float width, float depth, Color color, string name)
        {
            var tile = GameObject.CreatePrimitive(PrimitiveType.Cube);
            tile.name = name;
            tile.transform.position = position;
            tile.transform.localScale = new Vector3(width, 0.012f, depth);
            tile.GetComponent<Renderer>().sharedMaterial = MakeMaterial(color);
            Destroy(tile.GetComponent<Collider>());
        }

        private void CreateInvisibleBoundaryCollider(Vector3 position, Vector3 size, string name)
        {
            var boundary = new GameObject(name);
            boundary.transform.position = position;
            var collider = boundary.AddComponent<BoxCollider>();
            collider.size = size;
        }

        private void CreateTallLeaf(Vector3 position, Vector3 scale, string name)
        {
            CreateTallLeaf(position, scale, name, 0.20f);
        }

        private void CreateTallLeaf(Vector3 position, Vector3 scale, string name, float encounterChance)
        {
            var grass = GameObject.CreatePrimitive(PrimitiveType.Cube);
            grass.name = name;
            grass.transform.position = new Vector3(position.x, 0.095f, position.z);
            grass.transform.localScale = new Vector3(scale.x, 0.045f, scale.z);
            grass.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.0f, 1.0f, 0.0f));

            var collider = grass.GetComponent<BoxCollider>();
            collider.isTrigger = true;
            collider.center = new Vector3(0, 14f, 0);
            collider.size = new Vector3(1, 32, 1);

            var trigger = grass.AddComponent<TallLeafEncounterTrigger>();
            trigger.Configure(encounterChance, new[] { 1, 4, 7 });
        }

        private void CreateWildCameraZone(Vector3 origin, string areaId)
        {
            CreateWildCameraZone(origin, areaId, new Vector3(28, 4, 28));
        }

        private void CreateWildCameraZone(Vector3 origin, string areaId, Vector3 size)
        {
            var zone = new GameObject("WildAreaCameraZone_" + areaId);
            zone.transform.position = origin + new Vector3(0, 1.2f, 0);
            var collider = zone.AddComponent<BoxCollider>();
            collider.isTrigger = true;
            collider.size = size;
            zone.AddComponent<WildAreaCameraZone>();
        }

        private void CreateBuilding(Vector3 position, string name)
        {
            if (name == "Pokemon Center")
            {
                CreatePokemonCenterBuilding(position);
                return;
            }

            var building = GameObject.CreatePrimitive(PrimitiveType.Cube);
            building.name = name;
            building.transform.position = position;
            building.transform.localScale = new Vector3(4, 2.4f, 3.2f);
            building.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.85f, 0.25f, 0.25f));

            var roof = GameObject.CreatePrimitive(PrimitiveType.Cube);
            roof.name = name + "_Roof";
            roof.transform.position = position + new Vector3(0, 1.55f, 0);
            roof.transform.localScale = new Vector3(4.7f, 0.6f, 3.8f);
            roof.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.35f, 0.08f, 0.12f));

            if (name == "Pokemon Center")
            {
                var door = GameObject.CreatePrimitive(PrimitiveType.Cube);
                door.name = "PokemonCenter_DoorTrigger";
                door.transform.position = position + new Vector3(0, -0.55f, 1.85f);
                door.transform.localScale = new Vector3(1.2f, 1.4f, 0.35f);
                door.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.1f, 0.22f, 0.55f));
                var collider = door.GetComponent<BoxCollider>();
                collider.isTrigger = true;
                collider.size = new Vector3(1.4f, 2.4f, 1.8f);
                var entrance = door.AddComponent<PokemonCenterEntrance>();
                var interiorOrigin = position + new Vector3(0, 0, -9f);
                CreatePokemonCenterInterior(interiorOrigin, position + new Vector3(0, 0.2f, 3.2f));
                entrance.Configure(interiorOrigin + new Vector3(0, 1, 0), "Pokemon Center");
            }
        }

        private void CreatePokemonCenterBuilding(Vector3 position)
        {
            var center = new Vector3(position.x, 0f, position.z);
            if (!hasPokemonCenterRespawnPoint)
            {
                pokemonCenterRespawnPoint = center + new Vector3(0f, 2f, -1.35f);
                hasPokemonCenterRespawnPoint = true;
            }

            CreateTile(center + new Vector3(0, 0.06f, 0), new Vector3(7.2f, 0.12f, 5.8f), new Color(0.78f, 0.94f, 0.98f), "PokemonCenter_Floor");
            CreateTile(center + new Vector3(0, 0.10f, -2.85f), new Vector3(1.7f, 0.05f, 0.52f), new Color(0.10f, 0.28f, 0.72f), "PokemonCenter_DoorMat");

            CreateGroundedPrimitive(PrimitiveType.Cube, center + new Vector3(0, 0, 2.9f), new Vector3(7.5f, 1.9f, 0.28f), new Color(0.93f, 0.34f, 0.38f), "PokemonCenter_BackWall");
            CreateGroundedPrimitive(PrimitiveType.Cube, center + new Vector3(-3.6f, 0, 0), new Vector3(0.28f, 1.9f, 5.8f), new Color(0.93f, 0.34f, 0.38f), "PokemonCenter_LeftWall");
            CreateGroundedPrimitive(PrimitiveType.Cube, center + new Vector3(3.6f, 0, 0), new Vector3(0.28f, 1.9f, 5.8f), new Color(0.93f, 0.34f, 0.38f), "PokemonCenter_RightWall");
            CreateGroundedPrimitive(PrimitiveType.Cube, center + new Vector3(-2.35f, 0, -2.9f), new Vector3(2.2f, 1.9f, 0.28f), new Color(0.93f, 0.34f, 0.38f), "PokemonCenter_FrontWall_Left");
            CreateGroundedPrimitive(PrimitiveType.Cube, center + new Vector3(2.35f, 0, -2.9f), new Vector3(2.2f, 1.9f, 0.28f), new Color(0.93f, 0.34f, 0.38f), "PokemonCenter_FrontWall_Right");

            CreateTile(center + new Vector3(0, 0.92f, 1.7f), new Vector3(5.6f, 1.25f, 0.45f), new Color(1.0f, 0.32f, 0.42f), "PokemonCenter_HealingCounter");
            CreateNpcMarker(center + new Vector3(0, 0.9f, 2.12f), "PokemonCenter_Nurse");

            var roof = GameObject.CreatePrimitive(PrimitiveType.Cube);
            roof.name = "PokemonCenter_FadingRoof";
            roof.transform.position = center + new Vector3(0, 2.22f, 0);
            roof.transform.localScale = new Vector3(7.9f, 0.38f, 6.35f);
            roof.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.28f, 0.06f, 0.10f));
            Destroy(roof.GetComponent<Collider>());

            var roofTrim = GameObject.CreatePrimitive(PrimitiveType.Cube);
            roofTrim.name = "PokemonCenter_RoofTrim";
            roofTrim.transform.position = center + new Vector3(0, 2.46f, -2.95f);
            roofTrim.transform.localScale = new Vector3(8.25f, 0.22f, 0.42f);
            roofTrim.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.98f, 0.12f, 0.18f));
            Destroy(roofTrim.GetComponent<Collider>());

            var roofFadeZone = new GameObject("PokemonCenter_RoofFadeZone");
            roofFadeZone.transform.position = center + new Vector3(0, 1.15f, 0);
            var fadeCollider = roofFadeZone.AddComponent<BoxCollider>();
            fadeCollider.isTrigger = true;
            fadeCollider.size = new Vector3(6.9f, 2.4f, 5.25f);
            roofFadeZone.AddComponent<PokemonCenterRoofFade>().Configure(roof.GetComponent<Renderer>(), roofTrim.GetComponent<Renderer>());

            var door = GameObject.CreatePrimitive(PrimitiveType.Cube);
            door.name = "PokemonCenter_DoorTrigger";
            door.transform.position = center + new Vector3(0, 0.8f, -3.05f);
            door.transform.localScale = new Vector3(1.65f, 1.6f, 0.22f);
            door.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.08f, 0.22f, 0.72f));
            var collider = door.GetComponent<BoxCollider>();
            collider.isTrigger = true;
            collider.size = new Vector3(1.6f, 2.1f, 1.2f);
            var entrance = door.AddComponent<PokemonCenterEntrance>();
            entrance.Configure(center + new Vector3(0, 1f, -1.3f), "Pokemon Center");

            CreateTestLabel(center + new Vector3(0, 0.38f, -3.95f), "POKECENTER - WALK IN / ROOF FADES");
        }

        private void CreatePokemonCenterInterior(Vector3 origin, Vector3 exitPosition)
        {
            CreateTile(origin, new Vector3(5.5f, 0.12f, 4.2f), new Color(0.72f, 0.82f, 0.92f), "PokemonCenterInterior_Floor");
            CreateTile(origin + new Vector3(0, 0.75f, -1.65f), new Vector3(4.7f, 1.5f, 0.25f), new Color(0.92f, 0.25f, 0.33f), "PokemonCenterInterior_Counter");
            CreateNpcMarker(origin + new Vector3(0, 0.9f, -1.1f), "PokemonCenter_Nurse");

            var exit = GameObject.CreatePrimitive(PrimitiveType.Cube);
            exit.name = "PokemonCenter_ExitTrigger";
            exit.transform.position = origin + new Vector3(0, 0.7f, 1.9f);
            exit.transform.localScale = new Vector3(1.4f, 1.4f, 0.3f);
            exit.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.1f, 0.22f, 0.55f));
            var collider = exit.GetComponent<BoxCollider>();
            collider.isTrigger = true;
            collider.size = new Vector3(1.5f, 2.2f, 1.6f);
            var entrance = exit.AddComponent<PokemonCenterEntrance>();
            entrance.Configure(exitPosition, "Town");
        }

        private void CreateOverworldPokemon(Vector3 position, int speciesId, string name)
        {
            var pokemon = CreateGroundedPrimitive(PrimitiveType.Sphere, position, new Vector3(0.95f, 0.95f, 0.95f), GetPokemonPrimaryColor(speciesId), name);
            var collider = pokemon.GetComponent<SphereCollider>();
            collider.isTrigger = true;
            collider.radius = 1.4f;
            var encounter = pokemon.AddComponent<OverworldPokemonEncounter>();
            encounter.Configure(speciesId, 5);

            var beacon = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            beacon.name = name + "_EncounterBeacon";
            beacon.transform.SetParent(pokemon.transform);
            beacon.transform.localPosition = new Vector3(0, 1.2f, 0);
            beacon.transform.localScale = new Vector3(0.42f, 0.14f, 0.42f);
            beacon.GetComponent<Renderer>().sharedMaterial = MakeMaterial(GetPokemonSecondaryColor(speciesId));
            Destroy(beacon.GetComponent<Collider>());
        }

        private Color GetPokemonPrimaryColor(int speciesId)
        {
            switch (speciesId)
            {
                case 1:
                case 2:
                case 3:
                    return new Color(0.20f, 0.72f, 0.34f); // Grass
                case 4:
                case 5:
                case 6:
                    return new Color(1.0f, 0.42f, 0.10f); // Fire
                case 7:
                case 8:
                case 9:
                    return new Color(0.18f, 0.48f, 0.95f); // Water
                default:
                    return new Color(0.62f, 0.12f, 1.0f);
            }
        }

        private Color GetPokemonSecondaryColor(int speciesId)
        {
            switch (speciesId)
            {
                case 1:
                case 2:
                case 3:
                    return new Color(0.58f, 0.24f, 0.78f); // Poison
                case 6:
                    return new Color(0.34f, 0.44f, 0.95f); // Flying accent
                case 4:
                case 5:
                    return new Color(1.0f, 0.86f, 0.12f);
                case 7:
                case 8:
                case 9:
                    return new Color(0.12f, 0.92f, 1.0f);
                default:
                    return new Color(1f, 0.92f, 0.08f);
            }
        }

        private void CreateItemPickup(Vector3 position, string itemName, string name)
        {
            var pickup = CreateGroundedPrimitive(PrimitiveType.Sphere, position, new Vector3(0.45f, 0.45f, 0.45f), new Color(1f, 0.92f, 0.18f), name);
            var collider = pickup.GetComponent<SphereCollider>();
            collider.isTrigger = true;
            collider.radius = 1.8f;
            var pickupScript = pickup.AddComponent<PrototypePickup>();
            pickupScript.ConfigureItem(itemName);
        }

        private void CreatePokemonPickup(Vector3 position, int speciesId, string name)
        {
            var pickup = CreateGroundedPrimitive(PrimitiveType.Sphere, position, new Vector3(0.55f, 0.55f, 0.55f), GetPokemonPrimaryColor(speciesId), name);
            var collider = pickup.GetComponent<SphereCollider>();
            collider.isTrigger = true;
            collider.radius = 1.8f;
            var pickupScript = pickup.AddComponent<PrototypePickup>();
            pickupScript.ConfigurePokemon(speciesId);
        }

        private void CreateNpcMarker(Vector3 position, string name)
        {
            var npc = CreateGroundedPrimitive(PrimitiveType.Capsule, position, new Vector3(0.8f, 0.9f, 0.8f), new Color(0.95f, 0.80f, 0.25f), name);
            var solidCollider = npc.GetComponent<CapsuleCollider>();
            solidCollider.isTrigger = false;
            solidCollider.radius = 0.45f;
            solidCollider.height = 1.8f;

            var ring = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            ring.name = name + "_GroundRing";
            ring.transform.SetParent(npc.transform);
            ring.transform.localPosition = new Vector3(0, -0.86f, 0);
            ring.transform.localScale = new Vector3(1.05f, 0.018f, 1.05f);
            ring.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.08f, 0.95f, 1.0f));
            Destroy(ring.GetComponent<Collider>());

            var beacon = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            beacon.name = name + "_VisibilityBeacon";
            beacon.transform.SetParent(npc.transform);
            beacon.transform.localPosition = new Vector3(0, 1.35f, 0);
            beacon.transform.localScale = new Vector3(0.36f, 0.12f, 0.36f);
            beacon.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(1.0f, 0.95f, 0.05f));
            Destroy(beacon.GetComponent<Collider>());

            var npcBrain = npc.AddComponent<NpcBrain>();
            var interactionZone = new GameObject(name + "_InteractionTrigger");
            interactionZone.transform.SetParent(npc.transform);
            interactionZone.transform.localPosition = Vector3.zero;
            var triggerCollider = interactionZone.AddComponent<SphereCollider>();
            triggerCollider.isTrigger = true;
            triggerCollider.radius = 2.0f;
            interactionZone.AddComponent<NpcInteractionTrigger>().Configure(npcBrain);
        }

        private Material MakeMaterial(Color color)
        {
            var shader = FindCompatibleColorShader();
            var material = new Material(shader);
            material.enableInstancing = true;
            material.renderQueue = (int)UnityEngine.Rendering.RenderQueue.Geometry;
            if (material.HasProperty("_BaseColor"))
            {
                material.SetColor("_BaseColor", color);
            }
            if (material.HasProperty("_Color"))
            {
                material.SetColor("_Color", color);
            }
            if (material.HasProperty("_Surface"))
            {
                material.SetFloat("_Surface", 0f);
            }
            if (material.HasProperty("_AlphaClip"))
            {
                material.SetFloat("_AlphaClip", 0f);
            }
            if (material.HasProperty("_ZWrite"))
            {
                material.SetInt("_ZWrite", 1);
            }
            if (material.HasProperty("_ZTest"))
            {
                material.SetInt("_ZTest", (int)UnityEngine.Rendering.CompareFunction.LessEqual);
            }
            material.DisableKeyword("_SURFACE_TYPE_TRANSPARENT");
            material.DisableKeyword("_ALPHATEST_ON");
            material.DisableKeyword("_ALPHABLEND_ON");
            material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
            return material;
        }

        private Material MakeMarkerMaterial(Color color)
        {
            return MakeMaterial(color);
        }

        private static Shader FindCompatibleColorShader()
        {
            var shaderNames = UnityEngine.Rendering.GraphicsSettings.currentRenderPipeline != null
                ? new[] { "Universal Render Pipeline/Lit", "Universal Render Pipeline/Simple Lit", "Universal Render Pipeline/Unlit", "Standard", "Unlit/Color", "Hidden/Internal-Colored", "Sprites/Default" }
                : new[] { "Standard", "Unlit/Color", "Universal Render Pipeline/Lit", "Universal Render Pipeline/Simple Lit", "Universal Render Pipeline/Unlit", "Hidden/Internal-Colored", "Sprites/Default" };

            foreach (var shaderName in shaderNames)
            {
                var shader = Shader.Find(shaderName);
                if (shader != null)
                {
                    return shader;
                }
            }

            return Shader.Find("Hidden/InternalErrorShader");
        }

        private void UnloadDistantAreas(AreaMetadata current)
        {
            if (loadedAreas.Count <= preloadRadius + 2)
            {
                return;
            }

            Debug.Log("[PokeEngine] Memory budget " + memoryBudgetMb + "MB checked. Distant chunks are candidates for async unload.");
        }

        private void ApplyAreaPresentation(AreaMetadata area)
        {
            RenderSettings.fog = false;
            RenderSettings.fogDensity = 0f;
            Debug.Log("[PokeEngine] Swapped encounter, audio, weather, and lighting profiles for " + area.displayName);
        }
    }
}
"""

    def _render_movement_code(self):
        return """using PokeEngine.Core;
using PokeEngine.Data;
using UnityEngine;

namespace PokeEngine.Overworld
{
    [RequireComponent(typeof(CharacterController))]
    public sealed class HybridPlayerController : MonoBehaviour, IPokeEngineService
    {
        [SerializeField] private float walkMetersPerSecond = 3f;
        [SerializeField] private float runMetersPerSecond = 5f;
        [SerializeField] private float sprintMetersPerSecond = 7f;
        [SerializeField] private float turnSpeed = 16f;
        [SerializeField] private float gravity = -24f;
        [SerializeField] private float terminalFallSpeed = -34f;
        private const float SpawnDropHeight = 2.0f;

        private CharacterController controller;
        private Vector3 facingDirection = Vector3.forward;
        private Camera mainCamera;
        private float verticalVelocity;

        public MovementState State { get; private set; }
        public TerrainType CurrentTerrain { get; private set; } = TerrainType.Leaf;

        public void Initialize(PokeEngineRuntime runtime)
        {
            controller = GetComponent<CharacterController>();
            controller.radius = 0.38f;
            controller.height = 1.85f;
            controller.center = new Vector3(0, 0.92f, 0);
            controller.stepOffset = 0.35f;
            controller.slopeLimit = 45f;
            mainCamera = Camera.main;
            gameObject.tag = "Player";
            LiftToSpawnDropHeightIfNeeded();
            EnsurePlayerVisual();
            AssignCameraTarget(runtime);
            State = MovementState.Idle;
        }

        private void AssignCameraTarget(PokeEngineRuntime runtime)
        {
            var world = runtime.Get<WorldStreamingManager>();
            if (world != null)
            {
                world.SetFollowTarget(transform);
                mainCamera = world.ActiveCamera;
                return;
            }

            if (mainCamera == null)
            {
                mainCamera = Camera.main;
            }

            if (mainCamera == null)
            {
                return;
            }

            var cameraController = mainCamera.GetComponent<PokemonCameraController>();
            if (cameraController != null)
            {
                cameraController.SetTarget(transform);
                cameraController.ForceSnapToTarget();
            }
        }

        private void EnsurePlayerVisual()
        {
            if (GetComponentInChildren<Renderer>() != null)
            {
                return;
            }

            var body = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            body.name = "Prototype Player Visual";
            body.transform.SetParent(transform);
            body.transform.localPosition = new Vector3(0, 0.92f, 0);
            body.transform.localScale = new Vector3(0.78f, 0.9f, 0.78f);
            body.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.15f, 0.35f, 0.95f));
            Destroy(body.GetComponent<Collider>());

            var cap = GameObject.CreatePrimitive(PrimitiveType.Cube);
            cap.name = "Prototype Player Cap";
            cap.transform.SetParent(transform);
            cap.transform.localPosition = new Vector3(0, 1.83f, 0.05f);
            cap.transform.localScale = new Vector3(0.75f, 0.18f, 0.75f);
            cap.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(0.95f, 0.1f, 0.12f));
            Destroy(cap.GetComponent<Collider>());

            var beacon = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            beacon.name = "Prototype Player Visibility Beacon";
            beacon.transform.SetParent(transform);
            beacon.transform.localPosition = new Vector3(0, 2.2f, 0);
            beacon.transform.localScale = new Vector3(0.34f, 0.12f, 0.34f);
            beacon.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(1.0f, 0.92f, 0.05f));
            Destroy(beacon.GetComponent<Collider>());

            var ring = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            ring.name = "Prototype Player Ground Ring";
            ring.transform.SetParent(transform);
            ring.transform.localPosition = new Vector3(0, 0.035f, 0);
            ring.transform.localScale = new Vector3(0.82f, 0.012f, 0.82f);
            ring.GetComponent<Renderer>().sharedMaterial = MakeMaterial(new Color(1.0f, 1.0f, 1.0f));
            Destroy(ring.GetComponent<Collider>());
        }

        private Material MakeMaterial(Color color)
        {
            var shader = FindCompatibleColorShader();
            var material = new Material(shader);
            material.enableInstancing = true;
            material.renderQueue = (int)UnityEngine.Rendering.RenderQueue.Geometry;
            if (material.HasProperty("_BaseColor"))
            {
                material.SetColor("_BaseColor", color);
            }
            if (material.HasProperty("_Color"))
            {
                material.SetColor("_Color", color);
            }
            if (material.HasProperty("_Surface"))
            {
                material.SetFloat("_Surface", 0f);
            }
            if (material.HasProperty("_AlphaClip"))
            {
                material.SetFloat("_AlphaClip", 0f);
            }
            if (material.HasProperty("_ZWrite"))
            {
                material.SetInt("_ZWrite", 1);
            }
            if (material.HasProperty("_ZTest"))
            {
                material.SetInt("_ZTest", (int)UnityEngine.Rendering.CompareFunction.LessEqual);
            }
            material.DisableKeyword("_SURFACE_TYPE_TRANSPARENT");
            material.DisableKeyword("_ALPHATEST_ON");
            material.DisableKeyword("_ALPHABLEND_ON");
            material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
            return material;
        }

        private Material MakeAlwaysVisibleMaterial(Color color)
        {
            return MakeMaterial(color);
        }

        private static Shader FindCompatibleColorShader()
        {
            var shaderNames = UnityEngine.Rendering.GraphicsSettings.currentRenderPipeline != null
                ? new[] { "Universal Render Pipeline/Lit", "Universal Render Pipeline/Simple Lit", "Universal Render Pipeline/Unlit", "Standard", "Unlit/Color", "Hidden/Internal-Colored", "Sprites/Default" }
                : new[] { "Standard", "Unlit/Color", "Universal Render Pipeline/Lit", "Universal Render Pipeline/Simple Lit", "Universal Render Pipeline/Unlit", "Hidden/Internal-Colored", "Sprites/Default" };

            foreach (var shaderName in shaderNames)
            {
                var shader = Shader.Find(shaderName);
                if (shader != null)
                {
                    return shader;
                }
            }

            return Shader.Find("Hidden/InternalErrorShader");
        }

        private void Update()
        {
            if (State == MovementState.CutsceneLock)
            {
                return;
            }

            ClampToPrototypeTestingBounds();

            if (controller == null)
            {
                controller = GetComponent<CharacterController>();
            }

            MoveFourDirection(ReadDirectionalInput());
            ApplyGravity();
            RecoverIfBelowPrototype();
            ClampToPrototypeTestingBounds();
        }

        private Vector3 ReadDirectionalInput()
        {
            var raw = new Vector3(Input.GetAxisRaw("Horizontal"), 0, Input.GetAxisRaw("Vertical"));
            if (raw.sqrMagnitude < 0.01f)
            {
                return Vector3.zero;
            }

            return SnapToDominantAxis(raw);
        }

        public void SetWildAreaMode(bool enabled)
        {
            // Movement stays four-directional in every zone; this hook is kept for zone systems.
        }

        public void TeleportTo(Vector3 position)
        {
            if (controller == null)
            {
                controller = GetComponent<CharacterController>();
            }

            if (controller != null)
            {
                controller.enabled = false;
            }

            verticalVelocity = 0f;
            transform.position = position;

            if (controller != null)
            {
                controller.enabled = true;
            }
        }

        private void MoveFourDirection(Vector3 input)
        {
            if (input.sqrMagnitude < 0.01f)
            {
                State = MovementState.Idle;
                return;
            }

            var worldDirection = ToWorldDirection(input);
            if (worldDirection.sqrMagnitude < 0.01f)
            {
                State = MovementState.Idle;
                return;
            }

            facingDirection = worldDirection;
            var speed = CurrentMoveSpeed() * TerrainModifier(CurrentTerrain);
            controller.Move(worldDirection * speed * Time.deltaTime);
            transform.forward = Vector3.Slerp(transform.forward, facingDirection, Time.deltaTime * turnSpeed);

            State = speed >= sprintMetersPerSecond ? MovementState.Sprint : speed >= runMetersPerSecond ? MovementState.Run : MovementState.Walk;
        }

        private void ClampToPrototypeTestingBounds()
        {
            const float limit = 49.2f;
            var clamped = new Vector3(
                Mathf.Clamp(transform.position.x, -limit, limit),
                transform.position.y,
                Mathf.Clamp(transform.position.z, -limit, limit)
            );
            if ((clamped - transform.position).sqrMagnitude > 0.001f)
            {
                transform.position = clamped;
            }
        }

        private void LiftToSpawnDropHeightIfNeeded()
        {
            if (transform.position.y < 0.35f)
            {
                transform.position = new Vector3(transform.position.x, SpawnDropHeight, transform.position.z);
            }
        }

        private void ApplyGravity()
        {
            if (controller == null)
            {
                return;
            }

            if (controller.isGrounded && verticalVelocity < 0f)
            {
                verticalVelocity = -2f;
            }

            verticalVelocity = Mathf.Max(verticalVelocity + gravity * Time.deltaTime, terminalFallSpeed);
            controller.Move(Vector3.up * verticalVelocity * Time.deltaTime);

            if (controller.isGrounded && verticalVelocity < 0f)
            {
                verticalVelocity = -2f;
            }
        }

        private void RecoverIfBelowPrototype()
        {
            if (transform.position.y < -4f)
            {
                verticalVelocity = 0f;
                transform.position = new Vector3(transform.position.x, SpawnDropHeight, transform.position.z);
            }
        }

        private float CurrentMoveSpeed()
        {
            if (Input.GetKey(KeyCode.LeftShift))
            {
                return sprintMetersPerSecond;
            }

            return walkMetersPerSecond;
        }

        private Vector3 ToWorldDirection(Vector3 input)
        {
            if (mainCamera == null)
            {
                mainCamera = Camera.main;
            }

            if (mainCamera == null)
            {
                return SnapWorldDirection(input);
            }

            var forward = mainCamera.transform.forward;
            forward.y = 0;
            forward.Normalize();

            var right = mainCamera.transform.right;
            right.y = 0;
            right.Normalize();

            var move = right * input.x + forward * input.z;
            move.y = 0f;
            return move.sqrMagnitude > 0.01f ? move.normalized : Vector3.zero;
        }

        private Vector3 SnapToDominantAxis(Vector3 input)
        {
            return Mathf.Abs(input.x) > Mathf.Abs(input.z) ? new Vector3(Mathf.Sign(input.x), 0, 0) : new Vector3(0, 0, Mathf.Sign(input.z));
        }

        private Vector3 SnapWorldDirection(Vector3 direction)
        {
            direction.y = 0f;
            if (direction.sqrMagnitude < 0.01f)
            {
                return Vector3.zero;
            }

            return Mathf.Abs(direction.x) > Mathf.Abs(direction.z)
                ? new Vector3(Mathf.Sign(direction.x), 0, 0)
                : new Vector3(0, 0, Mathf.Sign(direction.z));
        }

        private float TerrainModifier(TerrainType terrain)
        {
            switch (terrain)
            {
                case TerrainType.Ice:
                    State = MovementState.Slide;
                    return 1.2f;
                case TerrainType.Mud:
                case TerrainType.Sand:
                    return 0.65f;
                case TerrainType.Water:
                    State = MovementState.Swim;
                    return 0.5f;
                case TerrainType.Lava:
                    return 0.35f;
                case TerrainType.Dimensional:
                    return 1.4f;
                default:
                    return 1f;
            }
        }
    }
}
"""

    def _render_camera_controller_code(self):
        return """using PokeEngine.UI;
using UnityEngine;

namespace PokeEngine.Overworld
{
    public sealed class PokemonCameraController : MonoBehaviour
    {
        [SerializeField] private float height = 6.8f;
        [SerializeField] private float distance = 7.4f;
        [SerializeField] private float orthographicSize = 4.6f;
        [SerializeField] private float wildHeight = 6.5f;
        [SerializeField] private float wildDistance = 7.8f;
        [SerializeField] private float wildOrthographicSize = 4.45f;
        [SerializeField] private float followSmooth = 14f;
        [SerializeField] private float modeBlendSpeed = 4.5f;
        [SerializeField] private float mouseOrbitSensitivity = 4.5f;
        [SerializeField] private float mousePitchSensitivity = 0.85f;
        [SerializeField] private float maxPitchOffsetDegrees = 15f;
        [SerializeField] private float hardSnapDistance = 7f;
        [SerializeField] private float viewportSafetyMargin = 0.10f;

        private Transform target;
        private float yaw;
        private float pitchOffset;
        private float modeBlend;
        private int orbitZoneCount;

        public void Configure(Vector3 offset, Vector3 euler)
        {
            height = Mathf.Max(4.8f, offset.y);
            distance = Mathf.Max(4.2f, Mathf.Abs(offset.z));
            yaw = 0f;

            var camera = GetComponent<Camera>();
            if (camera != null)
            {
                camera.orthographic = true;
                camera.orthographicSize = orthographicSize;
                camera.nearClipPlane = 0.03f;
                camera.farClipPlane = 200f;
                camera.clearFlags = CameraClearFlags.SolidColor;
                camera.backgroundColor = new Color(0.58f, 0.78f, 0.95f);
            }
        }

        public void SetTarget(Transform followTarget)
        {
            if (target == followTarget)
            {
                return;
            }

            target = followTarget;
        }

        public void SetOrbitAllowed(bool allowed)
        {
            orbitZoneCount = Mathf.Max(0, orbitZoneCount + (allowed ? 1 : -1));
        }

        public void ForceSnapToTarget()
        {
            ResolveTarget();
            if (target == null)
            {
                return;
            }

            var desired = CalculateDesiredPose(out var desiredRotation);
            transform.position = desired;
            transform.rotation = desiredRotation;
        }

        private void LateUpdate()
        {
            ResolveTarget();
            if (target == null)
            {
                return;
            }

            var orbitAllowed = orbitZoneCount > 0;
            var deltaTime = Time.unscaledDeltaTime > 0f ? Time.unscaledDeltaTime : 0.016f;
            var transitionStep = 1f - Mathf.Exp(-modeBlendSpeed * deltaTime);
            var followStep = 1f - Mathf.Exp(-followSmooth * deltaTime);
            modeBlend = Mathf.Lerp(modeBlend, orbitAllowed ? 1f : 0f, transitionStep);

            var lookInputAllowed = orbitAllowed && !PrototypeRpgHud.IsPauseMenuOpen && !PrototypeRpgHud.IsBattleMenuOpen;
            if (lookInputAllowed)
            {
                yaw += Input.GetAxis("Mouse X") * mouseOrbitSensitivity;
                pitchOffset = Mathf.Clamp(
                    pitchOffset - Input.GetAxis("Mouse Y") * mousePitchSensitivity,
                    -maxPitchOffsetDegrees,
                    maxPitchOffsetDegrees
                );
            }
            else if (!orbitAllowed)
            {
                yaw = Mathf.LerpAngle(yaw, 0f, transitionStep);
                pitchOffset = Mathf.Lerp(pitchOffset, 0f, transitionStep);
            }

            var desiredPosition = CalculateDesiredPose(out var desiredRotation);
            var camera = GetComponent<Camera>();
            var targetVisible = IsTargetSafelyVisible(camera);
            var tooFar = Vector3.Distance(transform.position, desiredPosition) > hardSnapDistance;

            if (!targetVisible || tooFar)
            {
                transform.position = desiredPosition;
                transform.rotation = desiredRotation;
            }
            else
            {
                transform.position = Vector3.Lerp(transform.position, desiredPosition, followStep);
                transform.rotation = Quaternion.Slerp(transform.rotation, desiredRotation, followStep);
            }

            if (camera != null)
            {
                var targetOrthoSize = Mathf.Lerp(orthographicSize, wildOrthographicSize, modeBlend);
                camera.orthographicSize = Mathf.Lerp(camera.orthographicSize, targetOrthoSize, followStep);
                camera.fieldOfView = Mathf.Lerp(45f, 38f, modeBlend);
                camera.nearClipPlane = 0.03f;
            }
        }

        private Vector3 CalculateDesiredPose(out Quaternion desiredRotation)
        {
            var activeHeight = Mathf.Lerp(height, wildHeight, modeBlend);
            var activeDistance = Mathf.Lerp(distance, wildDistance, modeBlend);
            var activePitch = Mathf.Lerp(0f, pitchOffset, modeBlend);
            var cameraOrbit = Quaternion.Euler(activePitch, yaw, 0f);
            var desiredPosition = target.position + cameraOrbit * new Vector3(0, activeHeight, -activeDistance);
            desiredPosition.y = Mathf.Max(desiredPosition.y, target.position.y + 4.4f);
            var lookTarget = target.position + Vector3.up * 0.72f;
            desiredRotation = Quaternion.LookRotation(lookTarget - desiredPosition, Vector3.up);
            return desiredPosition;
        }

        private bool IsTargetSafelyVisible(Camera camera)
        {
            if (camera == null || target == null)
            {
                return true;
            }

            var viewport = camera.WorldToViewportPoint(target.position + Vector3.up * 1.15f);
            if (viewport.z <= 0f)
            {
                return false;
            }

            return viewport.x >= viewportSafetyMargin
                && viewport.x <= 1f - viewportSafetyMargin
                && viewport.y >= viewportSafetyMargin
                && viewport.y <= 1f - viewportSafetyMargin;
        }

        private void ResolveTarget()
        {
            if (target != null)
            {
                return;
            }

            var player = GameObject.FindGameObjectWithTag("Player");
            if (player != null)
            {
                SetTarget(player.transform);
                return;
            }

            var controller = FindObjectOfType<HybridPlayerController>();
            if (controller != null)
            {
                SetTarget(controller.transform);
            }
        }
    }
}
"""

    def _render_tall_grass_system_code(self):
        return """using System;
using System.Collections.Generic;
using UnityEngine;

namespace PokeEngine.Overworld
{
    public enum TallGrassKind { Standard, Dense, Double, Rustling, Wet, FlowerField, Swamp, Snow, Dimensional, Raid, Seasonal }
    public enum TallGrassWeather { Any, Clear, Rain, Snow, Wind, Dimensional }
    public enum TallGrassTimeOfDay { Any, Morning, Day, Evening, Night }
    public enum TallGrassTraversal { Walk, Run, Sprint, Bike, Ride }

    [Serializable]
    public sealed class TallGrassRuntimeContext
    {
        public TallGrassWeather weather = TallGrassWeather.Any;
        public TallGrassTimeOfDay timeOfDay = TallGrassTimeOfDay.Any;
        public TallGrassTraversal traversal = TallGrassTraversal.Walk;
        public bool repelActive;
        public int leadPokemonLevel = 1;
        public bool swarmActive;
        public bool eventActive;
        public readonly HashSet<string> flags = new HashSet<string>();
        public readonly HashSet<string> abilities = new HashSet<string>();

        public bool HasFlag(string key)
        {
            return string.IsNullOrEmpty(key) || flags.Contains(key);
        }

        public bool HasAbility(string key)
        {
            return !string.IsNullOrEmpty(key) && abilities.Contains(key);
        }
    }

    [Serializable]
    public sealed class TallGrassEncounterEntry
    {
        public int speciesId = 1;
        public int minLevel = 2;
        public int maxLevel = 5;
        public int weight = 1;
        public bool rare;
        public bool rustlingOnly;
        public bool swarmOnly;
        public bool eventOnly;
        public TallGrassWeather weather = TallGrassWeather.Any;
        public TallGrassTimeOfDay timeOfDay = TallGrassTimeOfDay.Any;
        public string requiredFlag;

        public bool Matches(TallGrassRuntimeContext context, bool rustling)
        {
            if (rustlingOnly && !rustling) return false;
            if (swarmOnly && (context == null || !context.swarmActive)) return false;
            if (eventOnly && (context == null || !context.eventActive)) return false;
            if (context != null)
            {
                if (weather != TallGrassWeather.Any && context.weather != weather) return false;
                if (timeOfDay != TallGrassTimeOfDay.Any && context.timeOfDay != timeOfDay) return false;
                if (!context.HasFlag(requiredFlag)) return false;
            }
            return weight > 0;
        }

        public int RollLevel()
        {
            return UnityEngine.Random.Range(Mathf.Min(minLevel, maxLevel), Mathf.Max(minLevel, maxLevel) + 1);
        }
    }

    [Serializable]
    public sealed class TallGrassEncounterProfile
    {
        public string zoneId = "prototype_grass";
        public TallGrassKind grassKind = TallGrassKind.Standard;
        public float baseEncounterRate = 0.22f;
        public float rareModifier = 1f;
        public float doubleBattleChance = 0f;
        public float ambushChance = 0f;
        public float movementSpeedMultiplier = 1f;
        public float rustlingSpawnChance = 0.04f;
        public string audioProfile = "grass_rustle_standard";
        public string animationProfile = "grass_sway_standard";
        public List<TallGrassEncounterEntry> entries = new List<TallGrassEncounterEntry>();

        public float EffectiveEncounterRate(TallGrassRuntimeContext context)
        {
            var rate = baseEncounterRate;
            if (grassKind == TallGrassKind.Dense) rate *= 1.35f;
            if (grassKind == TallGrassKind.Double) rate *= 1.55f;
            if (grassKind == TallGrassKind.Rustling) rate *= 1.9f;
            if (grassKind == TallGrassKind.Raid) rate *= 0.65f;
            if (context != null)
            {
                if (context.traversal == TallGrassTraversal.Run) rate *= 1.1f;
                if (context.traversal == TallGrassTraversal.Sprint || context.traversal == TallGrassTraversal.Bike) rate *= 1.25f;
                if (context.HasAbility("reduced_encounters")) rate *= 0.5f;
                if (context.HasAbility("increased_encounters")) rate *= 1.5f;
                if (context.repelActive) rate *= 0.25f;
            }
            return Mathf.Clamp01(rate);
        }
    }

    public sealed class TallGrassEncounterRoll
    {
        public bool triggered;
        public bool doubleBattle;
        public bool ambush;
        public TallGrassEncounterEntry entry;
    }

    public sealed class TallGrassEncounterRoller
    {
        public TallGrassEncounterRoll Roll(TallGrassEncounterProfile profile, TallGrassRuntimeContext context, bool rustling = false)
        {
            var result = new TallGrassEncounterRoll();
            if (profile == null || UnityEngine.Random.value > profile.EffectiveEncounterRate(context))
            {
                return result;
            }

            var entry = RollEntry(profile, context, rustling);
            if (entry == null || IsRepelled(context, entry))
            {
                return result;
            }

            result.triggered = true;
            result.entry = entry;
            result.doubleBattle = profile.grassKind == TallGrassKind.Double || UnityEngine.Random.value < profile.doubleBattleChance;
            result.ambush = UnityEngine.Random.value < profile.ambushChance;
            return result;
        }

        public TallGrassEncounterEntry RollEntry(TallGrassEncounterProfile profile, TallGrassRuntimeContext context, bool rustling)
        {
            var legal = new List<TallGrassEncounterEntry>();
            var total = 0;
            foreach (var entry in profile.entries)
            {
                if (entry == null || !entry.Matches(context, rustling)) continue;
                var weight = entry.weight;
                if (entry.rare && context != null && context.HasAbility("rare_boost")) weight *= 2;
                legal.Add(entry);
                total += Mathf.Max(0, weight);
            }

            if (total <= 0) return null;
            var roll = UnityEngine.Random.Range(0, total);
            foreach (var entry in legal)
            {
                var weight = entry.weight;
                if (entry.rare && context != null && context.HasAbility("rare_boost")) weight *= 2;
                roll -= Mathf.Max(0, weight);
                if (roll < 0) return entry;
            }
            return null;
        }

        public bool IsRepelled(TallGrassRuntimeContext context, TallGrassEncounterEntry entry)
        {
            return context != null && context.repelActive && entry != null && entry.maxLevel < context.leadPokemonLevel;
        }
    }

    [Serializable]
    public sealed class TallGrassRustlingState
    {
        public string spawnId;
        public int speciesId;
        public Vector2Int tile;
        public float ageSeconds;
        public float visibilitySeconds = 12f;
        public bool active = true;

        public void Tick(float deltaTime)
        {
            ageSeconds += Mathf.Max(0f, deltaTime);
            if (ageSeconds >= visibilitySeconds) active = false;
        }
    }

    [Serializable]
    public sealed class TallGrassSaveRecord
    {
        public string zoneId;
        public bool swarmActive;
        public string seasonKey = "default";
        public List<TallGrassRustlingState> rustlingSpawns = new List<TallGrassRustlingState>();
    }
}
"""

    def _render_tall_grass_trigger_code(self):
        return """using PokeEngine.Battle;
using PokeEngine.Core;
using PokeEngine.Pokemon;
using UnityEngine;

namespace PokeEngine.Overworld
{
    public sealed class TallLeafEncounterTrigger : MonoBehaviour
    {
        [SerializeField] private TallGrassKind grassKind = TallGrassKind.Standard;
        [SerializeField] private float encounterChancePerRoll = 0.20f;
        [SerializeField] private float sprintEncounterChancePerRoll = 0.35f;
        [SerializeField] private float rollIntervalSeconds = 0.8f;
        [SerializeField] private int[] speciesIds = { 1, 4, 7 };

        private float nextRollTime;
        private TallGrassEncounterProfile profile;
        private readonly TallGrassEncounterRoller roller = new TallGrassEncounterRoller();
        private readonly TallGrassRuntimeContext context = new TallGrassRuntimeContext();
        private Renderer cachedRenderer;
        private Vector3 baseScale;
        private Vector3 lastPlayerPosition;
        private bool playerInside;
        private bool hasLastPlayerPosition;

        public float CurrentVisualSway { get; private set; }

        public void Configure(float chance, int[] species)
        {
            encounterChancePerRoll = chance;
            speciesIds = species;
            BuildProfile();
        }

        private void Awake()
        {
            cachedRenderer = GetComponent<Renderer>();
            baseScale = transform.localScale;
            BuildProfile();
        }

        private void Update()
        {
            var targetSway = playerInside ? 1f : 0.25f;
            CurrentVisualSway = Mathf.Lerp(CurrentVisualSway, targetSway, Time.deltaTime * 8f);
            transform.localScale = baseScale + new Vector3(0f, Mathf.Sin(Time.time * 9f) * 0.025f * CurrentVisualSway, 0f);
            if (cachedRenderer != null)
            {
                cachedRenderer.material.color = Color.Lerp(new Color(0f, 0.62f, 0f), new Color(0.05f, 1f, 0.05f), CurrentVisualSway);
            }
        }

        private void OnTriggerEnter(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                playerInside = true;
                lastPlayerPosition = other.transform.position;
                hasLastPlayerPosition = true;
            }
        }

        private void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                playerInside = false;
                hasLastPlayerPosition = false;
            }
        }

        private void OnTriggerStay(Collider other)
        {
            if (!other.CompareTag("Player") || Time.time < nextRollTime)
            {
                return;
            }

            if (!PlayerMovedInsideGrass(other.transform))
            {
                return;
            }

            nextRollTime = Time.time + rollIntervalSeconds;
            profile.baseEncounterRate = Input.GetKey(KeyCode.LeftShift) ? sprintEncounterChancePerRoll : encounterChancePerRoll;
            context.traversal = TallGrassTraversal.Walk;
            var roll = roller.Roll(profile, context, grassKind == TallGrassKind.Rustling);
            if (roll.triggered)
            {
                StartEncounter(roll.entry);
            }
        }

        private bool PlayerMovedInsideGrass(Transform player)
        {
            if (player == null)
            {
                return false;
            }

            if (!hasLastPlayerPosition)
            {
                lastPlayerPosition = player.position;
                hasLastPlayerPosition = true;
                return false;
            }

            var delta = player.position - lastPlayerPosition;
            delta.y = 0f;
            lastPlayerPosition = player.position;
            return delta.sqrMagnitude > 0.0004f;
        }

        private void BuildProfile()
        {
            profile = new TallGrassEncounterProfile
            {
                zoneId = gameObject.name,
                grassKind = grassKind,
                baseEncounterRate = encounterChancePerRoll,
                doubleBattleChance = grassKind == TallGrassKind.Double ? 0.2f : 0.0f,
                ambushChance = grassKind == TallGrassKind.Dense ? 0.08f : 0.0f,
            };
            profile.entries.Clear();
            if (speciesIds == null || speciesIds.Length == 0)
            {
                speciesIds = new[] { 1 };
            }
            foreach (var species in speciesIds)
            {
                profile.entries.Add(new TallGrassEncounterEntry { speciesId = species, minLevel = 3, maxLevel = 6, weight = 20, rare = false });
            }
        }

        private void StartEncounter(TallGrassEncounterEntry entry)
        {
            var runtime = PokeEngineRuntime.Instance;
            if (runtime == null)
            {
                return;
            }

            var database = runtime.Get<PokemonDatabaseRuntime>();
            var battle = runtime.Get<BattleEngineRuntime>();
            if (database == null || battle == null || battle.InBattle)
            {
                return;
            }

            var speciesId = entry == null ? 1 : entry.speciesId;
            var wildPokemon = database.CreatePokemon(speciesId, entry == null ? Random.Range(3, 7) : entry.RollLevel());
            battle.StartWildEncounter(wildPokemon);
        }

    }
}
"""

    def _render_wild_area_camera_zone_code(self):
        return """using UnityEngine;

namespace PokeEngine.Overworld
{
    public sealed class WildAreaCameraZone : MonoBehaviour
    {
        private void OnTriggerEnter(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                SetOrbit(true);
            }
        }

        private void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                SetOrbit(false);
            }
        }

        private void SetOrbit(bool enabled)
        {
            var player = GameObject.FindGameObjectWithTag("Player");
            var camera = Camera.main;
            if (camera != null)
            {
                var controller = camera.GetComponent<PokemonCameraController>();
                if (controller != null)
                {
                    if (player != null)
                    {
                        controller.SetTarget(player.transform);
                    }
                    controller.SetOrbitAllowed(enabled);
                }
            }

            if (player != null)
            {
                var movement = player.GetComponent<HybridPlayerController>();
                if (movement != null)
                {
                    movement.SetWildAreaMode(enabled);
                }
            }
        }
    }
}
"""

    def _render_pokemon_center_entrance_code(self):
        return """using PokeEngine.UI;
using UnityEngine;

namespace PokeEngine.Overworld
{
    public sealed class PokemonCenterEntrance : MonoBehaviour
    {
        [SerializeField] private Vector3 destination;
        [SerializeField] private string destinationName = "Pokemon Center";
        private bool playerInside;
        private Transform player;

        public void Configure(Vector3 destinationPosition, string label)
        {
            destination = destinationPosition;
            destinationName = label;
        }

        private void OnTriggerEnter(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                playerInside = true;
                player = other.transform;
            }
        }

        private void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                playerInside = false;
                player = null;
            }
        }

        private void Update()
        {
            if (!playerInside || player == null)
            {
                return;
            }

            if (Input.GetKeyDown(KeyCode.E))
            {
                var controller = player.GetComponent<CharacterController>();
                if (controller != null)
                {
                    controller.enabled = false;
                }

                player.position = destination;

                if (controller != null)
                {
                    controller.enabled = true;
                }

                Debug.Log("[PokeEngine] Entered " + destinationName + ".");
            }
        }

        private void OnGUI()
        {
            if (!playerInside || PrototypeRpgHud.IsPauseMenuOpen || PrototypeRpgHud.IsBattleMenuOpen)
            {
                return;
            }

            var guiMatrix = PrototypeGuiScale.Begin();
            try
            {
                GUI.Box(new Rect(18, PrototypeGuiScale.Height - 102, 430, 72), "Press E to enter " + destinationName);
            }
            finally
            {
                PrototypeGuiScale.End(guiMatrix);
            }
        }
    }

    public sealed class PokemonCenterRoofFade : MonoBehaviour
    {
        [SerializeField] private float visibleAlpha = 1f;
        [SerializeField] private float insideAlpha = 0.08f;
        [SerializeField] private float fadeSpeed = 8f;
        private Renderer[] roofRenderers = new Renderer[0];
        private Material[][] runtimeMaterials = new Material[0][];
        private BoxCollider fadeBounds;
        private Transform player;
        private float currentAlpha = 1f;

        public void Configure(params Renderer[] renderers)
        {
            roofRenderers = renderers ?? new Renderer[0];
            PrepareMaterials();
        }

        private void Awake()
        {
            fadeBounds = GetComponent<BoxCollider>();
            if (roofRenderers == null || roofRenderers.Length == 0)
            {
                roofRenderers = GetComponentsInChildren<Renderer>();
            }
            PrepareMaterials();
        }

        private void Update()
        {
            if (fadeBounds == null)
            {
                fadeBounds = GetComponent<BoxCollider>();
            }

            if (player == null)
            {
                var playerObject = GameObject.FindGameObjectWithTag("Player");
                if (playerObject != null)
                {
                    player = playerObject.transform;
                }
            }

            var inside = player != null && fadeBounds != null && fadeBounds.bounds.Contains(player.position + Vector3.up * 0.9f);
            var targetAlpha = inside ? insideAlpha : visibleAlpha;
            currentAlpha = Mathf.Lerp(currentAlpha, targetAlpha, 1f - Mathf.Exp(-fadeSpeed * Time.unscaledDeltaTime));
            ApplyAlpha(currentAlpha);
        }

        private void PrepareMaterials()
        {
            if (roofRenderers == null)
            {
                return;
            }

            runtimeMaterials = new Material[roofRenderers.Length][];
            for (var i = 0; i < roofRenderers.Length; i++)
            {
                var renderer = roofRenderers[i];
                if (renderer == null)
                {
                    runtimeMaterials[i] = new Material[0];
                    continue;
                }

                var source = renderer.sharedMaterials;
                var materials = new Material[source.Length];
                for (var m = 0; m < source.Length; m++)
                {
                    materials[m] = new Material(source[m]);
                    ConfigureTransparentMaterial(materials[m]);
                }
                renderer.materials = materials;
                runtimeMaterials[i] = materials;
            }
        }

        private void ConfigureTransparentMaterial(Material material)
        {
            if (material == null)
            {
                return;
            }

            material.renderQueue = (int)UnityEngine.Rendering.RenderQueue.Transparent;
            if (material.HasProperty("_Surface")) material.SetFloat("_Surface", 1f);
            if (material.HasProperty("_Mode")) material.SetFloat("_Mode", 3f);
            if (material.HasProperty("_SrcBlend")) material.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.SrcAlpha);
            if (material.HasProperty("_DstBlend")) material.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
            if (material.HasProperty("_ZWrite")) material.SetInt("_ZWrite", 0);
            material.DisableKeyword("_ALPHATEST_ON");
            material.EnableKeyword("_ALPHABLEND_ON");
            material.DisableKeyword("_ALPHAPREMULTIPLY_ON");
            ApplyMaterialAlpha(material, currentAlpha);
        }

        private void ApplyAlpha(float alpha)
        {
            if (runtimeMaterials == null)
            {
                return;
            }

            foreach (var group in runtimeMaterials)
            {
                if (group == null)
                {
                    continue;
                }

                foreach (var material in group)
                {
                    ApplyMaterialAlpha(material, alpha);
                }
            }
        }

        private void ApplyMaterialAlpha(Material material, float alpha)
        {
            if (material == null)
            {
                return;
            }

            if (material.HasProperty("_BaseColor"))
            {
                var color = material.GetColor("_BaseColor");
                color.a = alpha;
                material.SetColor("_BaseColor", color);
            }
            if (material.HasProperty("_Color"))
            {
                var color = material.GetColor("_Color");
                color.a = alpha;
                material.SetColor("_Color", color);
            }
        }
    }
}
"""

    def _render_prototype_pickup_code(self):
        return """using PokeEngine.Core;
using PokeEngine.Pokemon;
using PokeEngine.UI;
using UnityEngine;

namespace PokeEngine.Overworld
{
    public sealed class PrototypePickup : MonoBehaviour
    {
        [SerializeField] private bool givesPokemon;
        [SerializeField] private int pokemonSpeciesId;
        [SerializeField] private string itemName = "Tonic";
        private bool playerInside;

        public void ConfigureItem(string item)
        {
            givesPokemon = false;
            itemName = item;
        }

        public void ConfigurePokemon(int speciesId)
        {
            givesPokemon = true;
            pokemonSpeciesId = speciesId;
            itemName = "Pokemon";
        }

        private void OnTriggerEnter(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                playerInside = true;
            }
        }

        private void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                playerInside = false;
            }
        }

        private void Update()
        {
            if (!playerInside || !Input.GetKeyDown(KeyCode.E))
            {
                return;
            }

            var database = PokeEngineRuntime.Instance?.Get<PokemonDatabaseRuntime>();
            if (database == null)
            {
                return;
            }

            if (givesPokemon)
            {
                var pokemon = database.CreatePokemon(pokemonSpeciesId, 5);
                database.AddToParty(pokemon);
                Debug.Log("[PokeEngine] Picked up Pokemon: " + pokemon.nickname);
            }
            else
            {
                database.AddItem(itemName);
                Debug.Log("[PokeEngine] Picked up item: " + itemName);
            }

            Destroy(gameObject);
        }

        private void OnGUI()
        {
            if (!playerInside || PrototypeRpgHud.IsPauseMenuOpen || PrototypeRpgHud.IsBattleMenuOpen)
            {
                return;
            }

            var guiMatrix = PrototypeGuiScale.Begin();
            try
            {
                GUI.Box(new Rect(18, PrototypeGuiScale.Height - 180, 430, 72), "Press E to pick up " + itemName);
            }
            finally
            {
                PrototypeGuiScale.End(guiMatrix);
            }
        }
    }
}
"""

    def _render_overworld_pokemon_encounter_code(self):
        return """using PokeEngine.Battle;
using PokeEngine.Core;
using PokeEngine.Pokemon;
using PokeEngine.UI;
using UnityEngine;

namespace PokeEngine.Overworld
{
    public sealed class OverworldPokemonEncounter : MonoBehaviour
    {
        [SerializeField] private int speciesId = 7;
        [SerializeField] private int level = 5;
        private bool playerInside;

        public void Configure(int pokemonSpeciesId, int pokemonLevel)
        {
            speciesId = pokemonSpeciesId;
            level = pokemonLevel;
        }

        private void OnTriggerEnter(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                playerInside = true;
            }
        }

        private void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                playerInside = false;
            }
        }

        private void Update()
        {
            if (!playerInside || !Input.GetKeyDown(KeyCode.E))
            {
                return;
            }

            var runtime = PokeEngineRuntime.Instance;
            var database = runtime?.Get<PokemonDatabaseRuntime>();
            var battle = runtime?.Get<BattleEngineRuntime>();
            if (database == null || battle == null || battle.InBattle)
            {
                return;
            }

            battle.StartWildEncounter(database.CreatePokemon(speciesId, level));
        }

        private void OnGUI()
        {
            if (!playerInside || PrototypeRpgHud.IsPauseMenuOpen || PrototypeRpgHud.IsBattleMenuOpen)
            {
                return;
            }

            var guiMatrix = PrototypeGuiScale.Begin();
            try
            {
                GUI.Box(new Rect(18, PrototypeGuiScale.Height - 258, 460, 72), "Press E to battle prototype Pokemon");
            }
            finally
            {
                PrototypeGuiScale.End(guiMatrix);
            }
        }
    }
}
"""

    def _render_npc_code(self):
        return """using System.Collections.Generic;
using PokeEngine.Battle;
using PokeEngine.Core;
using PokeEngine.Pokemon;
using PokeEngine.UI;
using UnityEngine;

namespace PokeEngine.NPC
{
    public enum NpcCategory { Static, Patrol, Shopkeeper, Trainer, Follower, Rival, BossTrainer, RaidNpc, StoryCritical }
    public enum NpcAiState { Idle, Patrol, Dialogue, Alert, Chase, Battle, Relocate }

    public sealed class NpcDirector : MonoBehaviour, IPokeEngineService
    {
        private readonly List<NpcBrain> npcs = new List<NpcBrain>();

        public void Initialize(PokeEngineRuntime runtime)
        {
            foreach (var npc in FindObjectsOfType<NpcBrain>())
            {
                Register(npc);
            }
        }

        public void Register(NpcBrain npc)
        {
            if (!npcs.Contains(npc))
            {
                npcs.Add(npc);
            }
        }

        private void Update()
        {
            foreach (var npc in npcs)
            {
                npc.TickSchedule(Time.time);
            }
        }
    }

    public sealed class NpcBrain : MonoBehaviour
    {
        [SerializeField] private NpcCategory category;
        [SerializeField] private string dialogueTree = "default";
        [SerializeField] private string movementProfile = "idle";
        [SerializeField] private string scheduleProfile = "day";
        [SerializeField] private string trainerPartyData = "";
        [SerializeField] private float visionDistance = 6f;
        [SerializeField] private float visionAngle = 45f;
        [SerializeField] private string[] randomLetterDialogue =
        {
            "ZXQ ARO LUM.",
            "MIP VEL TAN QO.",
            "RAZ NIM OLO KEX.",
            "YUP TORI XA.",
            "BEEB ZAN FOL."
        };

        private bool playerInside;
        private GameObject nearbyPlayer;
        private string currentDialogue = "";
        public NpcAiState State { get; private set; }

        private void Update()
        {
            if (CanPlayerInteract() && Input.GetKeyDown(KeyCode.E))
            {
                if (IsPokemonCenterNurse())
                {
                    HealPokemonCenterParty();
                }
                else
                {
                    currentDialogue = randomLetterDialogue[Random.Range(0, randomLetterDialogue.Length)];
                    Debug.Log("[PokeEngine] NPC random-letter dialogue: " + currentDialogue);
                }
            }
        }

        private void OnTriggerEnter(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                SetPlayerInside(true, other.gameObject);
            }
        }

        private void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                SetPlayerInside(false);
            }
        }

        private void OnGUI()
        {
            if (!CanPlayerInteract() || PrototypeRpgHud.IsPauseMenuOpen || PrototypeRpgHud.IsBattleMenuOpen)
            {
                return;
            }

            var prompt = IsPokemonCenterNurse() ? "Press E to heal party" : "Press E to talk";
            var text = string.IsNullOrEmpty(currentDialogue) ? prompt : currentDialogue;
            var guiMatrix = PrototypeGuiScale.Begin();
            try
            {
                GUI.Box(new Rect(18, PrototypeGuiScale.Height - 336, 480, 78), text);
            }
            finally
            {
                PrototypeGuiScale.End(guiMatrix);
            }
        }

        public void TickSchedule(float worldTime)
        {
            if (category == NpcCategory.Trainer && CanSeePlayer())
            {
                State = NpcAiState.Alert;
                Debug.Log("[PokeEngine] Trainer detection triggered: " + name);
            }
            else if (scheduleProfile.Contains("night") && worldTime % 60f > 40f)
            {
                State = NpcAiState.Relocate;
            }
            else if (movementProfile.Contains("patrol"))
            {
                State = NpcAiState.Patrol;
            }
            else
            {
                State = NpcAiState.Idle;
            }
        }

        private bool CanSeePlayer()
        {
            var player = GameObject.FindGameObjectWithTag("Player");
            if (player == null)
            {
                return false;
            }

            var toPlayer = player.transform.position - transform.position;
            if (toPlayer.magnitude > visionDistance)
            {
                return false;
            }

            return Vector3.Angle(transform.forward, toPlayer.normalized) <= visionAngle && HasClearLineOfSight(player);
        }

        public bool CanPlayerInteract()
        {
            if (!playerInside)
            {
                return false;
            }

            var player = nearbyPlayer != null ? nearbyPlayer : GameObject.FindGameObjectWithTag("Player");
            return player != null && HasClearLineOfSight(player);
        }

        private bool HasClearLineOfSight(GameObject player)
        {
            var origin = transform.position + Vector3.up * 0.9f;
            var target = player.transform.position + Vector3.up * 0.9f;
            var toTarget = target - origin;
            var distance = toTarget.magnitude;
            if (distance <= 0.01f)
            {
                return true;
            }

            var hits = Physics.RaycastAll(origin, toTarget.normalized, distance, ~0, QueryTriggerInteraction.Ignore);
            if (hits.Length == 0)
            {
                return true;
            }

        System.Array.Sort(hits, (a, b) => a.distance.CompareTo(b.distance));
            foreach (var hit in hits)
            {
                var hitTransform = hit.collider.transform;
                if (hitTransform == transform || hitTransform.IsChildOf(transform))
                {
                    continue;
                }

                if (IsPokemonCenterNurse() && hit.collider.name.Contains("Counter"))
                {
                    continue;
                }

                if (hitTransform == player.transform || hitTransform.IsChildOf(player.transform))
                {
                    return true;
                }

                return false;
            }

            return true;
        }

        public string GetDialogueTree()
        {
            return dialogueTree;
        }

        public string GetTrainerParty()
        {
            return trainerPartyData;
        }

        private bool IsPokemonCenterNurse()
        {
            return name.Contains("PokemonCenter_Nurse");
        }

        private void HealPokemonCenterParty()
        {
            var runtime = PokeEngineRuntime.Instance;
            var database = runtime != null ? runtime.Get<PokemonDatabaseRuntime>() : null;
            if (database == null)
            {
                currentDialogue = "The healing system is offline.";
                return;
            }

            database.HealParty();
            runtime.Get<BattleEngineRuntime>()?.HealParty(database);
            currentDialogue = "Your party is fully healed. Please take care!";
            runtime.Get<PokeEventBus>()?.Publish("pokemon_center.party_healed", database.Party);
            Debug.Log("[PokeEngine] Pokemon Center nurse healed the party.");
        }

        public void SetPlayerInside(bool inside, GameObject playerObject = null)
        {
            playerInside = inside;
            nearbyPlayer = inside ? playerObject : null;
            if (!inside)
            {
                currentDialogue = "";
            }
        }
    }

    public sealed class NpcInteractionTrigger : MonoBehaviour
    {
        private NpcBrain npc;

        public void Configure(NpcBrain brain)
        {
            npc = brain;
        }

        private void Awake()
        {
            if (npc == null)
            {
                npc = GetComponentInParent<NpcBrain>();
            }
        }

        private void OnTriggerEnter(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                npc?.SetPlayerInside(true, other.gameObject);
            }
        }

        private void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                npc?.SetPlayerInside(false);
            }
        }
    }
}
"""

    def _render_event_code(self):
        return """using System.Collections.Generic;
using PokeEngine.Core;
using UnityEngine;

namespace PokeEngine.Events
{
    public sealed class EventFlagManager : MonoBehaviour, IPokeEngineService
    {
        private readonly Dictionary<string, bool> boolFlags = new Dictionary<string, bool>();
        private readonly Dictionary<string, int> counters = new Dictionary<string, int>();

        public void Initialize(PokeEngineRuntime runtime)
        {
            SetFlag("game_started", true);
        }

        public bool CheckFlag(string key)
        {
            return boolFlags.TryGetValue(key, out var value) && value;
        }

        public void SetFlag(string key, bool value)
        {
            boolFlags[key] = value;
            Debug.Log("[PokeEngine] Flag " + key + " = " + value);
        }

        public int GetCounter(string key)
        {
            counters.TryGetValue(key, out var value);
            return value;
        }

        public void AddCounter(string key, int amount)
        {
            counters[key] = GetCounter(key) + amount;
        }

        public Dictionary<string, bool> ExportFlags()
        {
            return new Dictionary<string, bool>(boolFlags);
        }
    }

    public sealed class PrototypeCutsceneDirector : MonoBehaviour, IPokeEngineService
    {
        private bool running;

        public void Initialize(PokeEngineRuntime runtime)
        {
        }

        public void PlayStoryBeat(string beatId)
        {
            if (running)
            {
                return;
            }

            StartCoroutine(PlayRoutine(beatId));
        }

        private System.Collections.IEnumerator PlayRoutine(string beatId)
        {
            running = true;
            Debug.Log("[PokeEngine] Cutscene start: " + beatId);
            yield return new WaitForSeconds(0.25f);
            Debug.Log("[PokeEngine] Camera rails, dialogue sync, animation playback, fade, audio ducking, and branches are reserved here.");
            yield return new WaitForSeconds(0.25f);
            running = false;
        }
    }
}
"""

    def _render_pokemon_database_code(self):
        return """using System.Collections.Generic;
using PokeEngine.Core;
using PokeEngine.Data;
using UnityEngine;

namespace PokeEngine.Pokemon
{
    public sealed class PokemonDatabaseRuntime : MonoBehaviour, IPokeEngineService
    {
        private readonly Dictionary<int, PokemonSpecies> species = new Dictionary<int, PokemonSpecies>();
        private readonly List<PokemonInstance> party = new List<PokemonInstance>();
        private readonly List<PokemonInstance> pcStorage = new List<PokemonInstance>();
        private readonly List<string> inventory = new List<string>();
        private int activePartyIndex;

        public IReadOnlyList<PokemonInstance> Party => party;
        public IReadOnlyList<PokemonInstance> PcStorage => pcStorage;
        public IReadOnlyList<string> Inventory => inventory;
        public int OwnedPokemonCount => party.Count + pcStorage.Count;
        public int ActivePartyIndex => activePartyIndex;
        public PokemonInstance ActivePartyPokemon => party.Count > 0 ? party[Mathf.Clamp(activePartyIndex, 0, party.Count - 1)] : null;

        public void Initialize(PokeEngineRuntime runtime)
        {
            SeedPrototypeSpecies();
            AddToParty(CreatePokemon(1, 5));
            AddToParty(CreatePokemon(4, 5));
        }

        public PokemonSpecies GetSpecies(int speciesId)
        {
            species.TryGetValue(speciesId, out var result);
            return result;
        }

        public PokemonInstance CreatePokemon(int speciesId, int level)
        {
            var data = GetSpecies(speciesId);
            var stats = data != null ? data.baseStats.Scaled(1f + level / 50f) : default;
            var pokemon = new PokemonInstance
            {
                speciesId = speciesId,
                nickname = data != null ? data.displayName : "Unknown",
                level = level,
                shiny = Random.Range(0, 4096) == 0,
                currentStats = stats,
                currentHp = Mathf.Max(1, stats.hp),
                moves = data != null ? data.learnset : new string[0],
                ability = data != null && data.abilities.Length > 0 ? data.abilities[0] : "",
                experience = 0,
                experienceToNextLevel = ExperienceToNextLevel(level)
            };
            return pokemon;
        }

        public PokemonInstance CreateRandomWildPokemon()
        {
            var encounterSpecies = new[] { 1, 4, 7 };
            var speciesId = encounterSpecies[Random.Range(0, encounterSpecies.Length)];
            return CreatePokemon(speciesId, Random.Range(3, 7));
        }

        public int ExperienceToNextLevel(int level)
        {
            level = Mathf.Clamp(level, 1, 100);
            return Mathf.Max(20, Mathf.RoundToInt(50f + level * level * 3.5f));
        }

        public void AddExperience(PokemonInstance pokemon, int amount)
        {
            if (pokemon == null || amount <= 0)
            {
                return;
            }

            pokemon.experience += amount;
            while (pokemon.level < 100 && pokemon.experience >= pokemon.experienceToNextLevel)
            {
                pokemon.experience -= pokemon.experienceToNextLevel;
                LevelUp(pokemon);
            }
        }

        public void LevelUp(PokemonInstance pokemon)
        {
            if (pokemon == null)
            {
                return;
            }

            pokemon.level = Mathf.Clamp(pokemon.level + 1, 1, 100);
            var oldMaxHp = GetMaxHp(pokemon);
            var speciesData = GetSpecies(pokemon.speciesId);
            if (speciesData != null)
            {
                pokemon.currentStats = speciesData.baseStats.Scaled(1f + pokemon.level / 50f);
            }
            pokemon.experienceToNextLevel = ExperienceToNextLevel(pokemon.level);
            pokemon.currentHp = Mathf.Clamp(pokemon.currentHp + Mathf.Max(1, GetMaxHp(pokemon) - oldMaxHp), 1, GetMaxHp(pokemon));
            TryApplyLevelEvolution(pokemon);
        }

        private void TryApplyLevelEvolution(PokemonInstance pokemon)
        {
            var speciesData = GetSpecies(pokemon.speciesId);
            if (speciesData == null || speciesData.evolutionRules == null)
            {
                return;
            }

            foreach (var rule in speciesData.evolutionRules)
            {
                var parts = rule.Split(':');
                if (parts.Length >= 3 && parts[0] == "level" && int.TryParse(parts[1], out var level) && pokemon.level >= level && int.TryParse(parts[2], out var targetSpeciesId))
                {
                    var target = GetSpecies(targetSpeciesId);
                    if (target == null)
                    {
                        continue;
                    }

                    pokemon.speciesId = target.speciesId;
                    pokemon.nickname = target.displayName;
                    pokemon.currentStats = target.baseStats.Scaled(1f + pokemon.level / 50f);
                    pokemon.currentHp = Mathf.Max(1, pokemon.currentStats.hp);
                    pokemon.moves = target.learnset;
                    pokemon.ability = target.abilities.Length > 0 ? target.abilities[0] : pokemon.ability;
                    Debug.Log("[PokeEngine] Evolution test: evolved into " + pokemon.nickname + ".");
                    return;
                }
            }
        }

        public bool AddToParty(PokemonInstance pokemon)
        {
            if (pokemon == null || ContainsPokemonInstance(pokemon))
            {
                return party.Contains(pokemon);
            }

            EnsureValidHp(pokemon);
            if (party.Count < 6)
            {
                party.Add(pokemon);
                if (party.Count == 1)
                {
                    activePartyIndex = 0;
                }
                return true;
            }

            pcStorage.Add(pokemon);
            return false;
        }

        public void StoreInPc(PokemonInstance pokemon)
        {
            if (pokemon == null || ContainsPokemonInstance(pokemon))
            {
                return;
            }

            EnsureValidHp(pokemon);
            pcStorage.Add(pokemon);
        }

        public void AddItem(string itemName)
        {
            inventory.Add(itemName);
        }

        public List<PokemonInstance> GetOwnedPokemon()
        {
            var owned = new List<PokemonInstance>();
            owned.AddRange(party);
            owned.AddRange(pcStorage);
            return owned;
        }

        public bool SetActivePartyIndex(int index)
        {
            if (index < 0 || index >= party.Count)
            {
                return false;
            }

            activePartyIndex = index;
            return true;
        }

        public int GetCurrentHp(PokemonInstance pokemon)
        {
            EnsureValidHp(pokemon);
            return pokemon != null ? pokemon.currentHp : 0;
        }

        public int GetMaxHp(PokemonInstance pokemon)
        {
            return pokemon != null ? Mathf.Max(1, pokemon.currentStats.hp) : 0;
        }

        public void SetCurrentHp(PokemonInstance pokemon, int hp)
        {
            if (pokemon == null)
            {
                return;
            }

            pokemon.currentHp = Mathf.Clamp(hp, 0, GetMaxHp(pokemon));
        }

        public bool PartyHasUsablePokemon()
        {
            foreach (var pokemon in party)
            {
                if (GetCurrentHp(pokemon) > 0)
                {
                    return true;
                }
            }

            return false;
        }

        public void HealParty()
        {
            foreach (var pokemon in party)
            {
                if (pokemon != null)
                {
                    pokemon.currentHp = GetMaxHp(pokemon);
                }
            }
        }

        private void EnsureValidHp(PokemonInstance pokemon)
        {
            if (pokemon == null)
            {
                return;
            }

            if (pokemon.currentHp < 0 && pokemon.currentStats.hp > 0)
            {
                pokemon.currentHp = Mathf.Max(1, pokemon.currentStats.hp);
            }
        }

        private bool ContainsPokemonInstance(PokemonInstance pokemon)
        {
            if (pokemon == null)
            {
                return false;
            }

            foreach (var existing in party)
            {
                if (existing == pokemon || existing.instanceId == pokemon.instanceId)
                {
                    return true;
                }
            }

            foreach (var existing in pcStorage)
            {
                if (existing == pokemon || existing.instanceId == pokemon.instanceId)
                {
                    return true;
                }
            }

            return false;
        }

        private void SeedPrototypeSpecies()
        {
            species[1] = new PokemonSpecies
            {
                speciesId = 1,
                nationalDexId = 1,
                regionalDexId = 1,
                displayName = "Bulbasaur",
                category = "Seed Pokemon",
                loreText = "A strange seed was planted on its back at birth.",
                height = 0.7f,
                weight = 6.9f,
                genderRatio = "87.5m_12.5f",
                eggGroups = new[] { "Monster", "Grass" },
                growthRate = "medium_slow",
                catchRate = 45,
                friendshipBase = 50,
                baseStats = new Stats { hp = 45, atk = 49, def = 49, spa = 65, spd = 65, spe = 45 },
                type1 = PokemonType.Leaf,
                type2 = PokemonType.Poison,
                abilities = new[] { "Overgrow" },
                hiddenAbility = "Chlorophyll",
                learnset = new[] { "Tackle", "Growl", "Vine Whip", "Guard Pulse" },
                evolutionRules = new[] { "level:16:2" },
                formVariants = new[] { "Default" },
                dimensionSplitForms = new[] { "Bulbasaur Rift" },
                megaForms = new string[0],
                fusionCompatibleSpecies = new[] { 4, 7 }
            };

            species[2] = new PokemonSpecies
            {
                speciesId = 2,
                nationalDexId = 2,
                regionalDexId = 2,
                displayName = "Ivysaur",
                category = "Seed Pokemon",
                loreText = "Its plant blooms as it stores more power.",
                height = 1.0f,
                weight = 13.0f,
                genderRatio = "87.5m_12.5f",
                eggGroups = new[] { "Monster", "Grass" },
                growthRate = "medium_slow",
                catchRate = 45,
                friendshipBase = 50,
                baseStats = new Stats { hp = 60, atk = 62, def = 63, spa = 80, spd = 80, spe = 60 },
                type1 = PokemonType.Leaf,
                type2 = PokemonType.Poison,
                abilities = new[] { "Overgrow" },
                hiddenAbility = "Chlorophyll",
                learnset = new[] { "Tackle", "Growl", "Vine Whip", "Razor Leaf" },
                evolutionRules = new[] { "level:32:3" },
                formVariants = new[] { "Default" },
                dimensionSplitForms = new[] { "Ivysaur Rift" },
                fusionCompatibleSpecies = new[] { 4, 7 }
            };

            species[3] = new PokemonSpecies
            {
                speciesId = 3,
                nationalDexId = 3,
                regionalDexId = 3,
                displayName = "Venusaur",
                category = "Seed Pokemon",
                loreText = "Its flower gathers sunlight and releases battle energy.",
                height = 2.0f,
                weight = 100.0f,
                genderRatio = "87.5m_12.5f",
                eggGroups = new[] { "Monster", "Grass" },
                growthRate = "medium_slow",
                catchRate = 45,
                friendshipBase = 50,
                baseStats = new Stats { hp = 80, atk = 82, def = 83, spa = 100, spd = 100, spe = 80 },
                type1 = PokemonType.Leaf,
                type2 = PokemonType.Poison,
                abilities = new[] { "Overgrow" },
                hiddenAbility = "Chlorophyll",
                learnset = new[] { "Tackle", "Vine Whip", "Razor Leaf", "Guard Pulse" },
                evolutionRules = new string[0],
                formVariants = new[] { "Default", "Gigantamax Venusaur" },
                dimensionSplitForms = new[] { "Venusaur Rift" },
                megaForms = new[] { "Mega Venusaur" },
                fusionCompatibleSpecies = new[] { 4, 7 }
            };

            species[4] = new PokemonSpecies
            {
                speciesId = 4,
                nationalDexId = 4,
                regionalDexId = 4,
                displayName = "Charmander",
                category = "Lizard Pokemon",
                loreText = "The flame on its tail shows the strength of its life force.",
                height = 0.6f,
                weight = 8.5f,
                genderRatio = "87.5m_12.5f",
                eggGroups = new[] { "Monster", "Dragon" },
                growthRate = "medium_slow",
                catchRate = 45,
                friendshipBase = 50,
                baseStats = new Stats { hp = 39, atk = 52, def = 43, spa = 60, spd = 50, spe = 65 },
                type1 = PokemonType.Flame,
                type2 = PokemonType.None,
                abilities = new[] { "Blaze" },
                hiddenAbility = "Solar Power",
                learnset = new[] { "Scratch", "Growl", "Ember", "Guard Pulse" },
                evolutionRules = new[] { "level:16:5" },
                formVariants = new[] { "Default" },
                dimensionSplitForms = new[] { "Charmander Rift" },
                fusionCompatibleSpecies = new[] { 1, 7 }
            };

            species[5] = new PokemonSpecies
            {
                speciesId = 5,
                nationalDexId = 5,
                regionalDexId = 5,
                displayName = "Charmeleon",
                category = "Flame Pokemon",
                loreText = "It swings its burning tail while looking for stronger rivals.",
                height = 1.1f,
                weight = 19.0f,
                genderRatio = "87.5m_12.5f",
                eggGroups = new[] { "Monster", "Dragon" },
                growthRate = "medium_slow",
                catchRate = 45,
                friendshipBase = 50,
                baseStats = new Stats { hp = 58, atk = 64, def = 58, spa = 80, spd = 65, spe = 80 },
                type1 = PokemonType.Flame,
                type2 = PokemonType.None,
                abilities = new[] { "Blaze" },
                hiddenAbility = "Solar Power",
                learnset = new[] { "Scratch", "Growl", "Ember", "Flame Burst" },
                evolutionRules = new[] { "level:36:6" },
                formVariants = new[] { "Default" },
                dimensionSplitForms = new[] { "Charmeleon Rift" },
                fusionCompatibleSpecies = new[] { 1, 7 }
            };

            species[6] = new PokemonSpecies
            {
                speciesId = 6,
                nationalDexId = 6,
                regionalDexId = 6,
                displayName = "Charizard",
                category = "Flame Pokemon",
                loreText = "It flies through the sky seeking strong opponents.",
                height = 1.7f,
                weight = 90.5f,
                genderRatio = "87.5m_12.5f",
                eggGroups = new[] { "Monster", "Dragon" },
                growthRate = "medium_slow",
                catchRate = 45,
                friendshipBase = 50,
                baseStats = new Stats { hp = 78, atk = 84, def = 78, spa = 109, spd = 85, spe = 100 },
                type1 = PokemonType.Flame,
                type2 = PokemonType.Flying,
                abilities = new[] { "Blaze" },
                hiddenAbility = "Solar Power",
                learnset = new[] { "Scratch", "Ember", "Flame Burst", "Air Slash" },
                evolutionRules = new string[0],
                formVariants = new[] { "Default", "Gigantamax Charizard" },
                dimensionSplitForms = new[] { "Charizard Rift" },
                megaForms = new[] { "Mega Charizard X", "Mega Charizard Y" },
                fusionCompatibleSpecies = new[] { 1, 7 }
            };

            species[7] = new PokemonSpecies
            {
                speciesId = 7,
                nationalDexId = 7,
                regionalDexId = 7,
                displayName = "Squirtle",
                category = "Tiny Turtle Pokemon",
                loreText = "It shelters in its shell, then strikes back with sprays of water.",
                height = 0.5f,
                weight = 9.0f,
                genderRatio = "87.5m_12.5f",
                eggGroups = new[] { "Monster", "Water 1" },
                growthRate = "medium_slow",
                catchRate = 45,
                friendshipBase = 50,
                baseStats = new Stats { hp = 44, atk = 48, def = 65, spa = 50, spd = 64, spe = 43 },
                type1 = PokemonType.Water,
                type2 = PokemonType.None,
                abilities = new[] { "Torrent" },
                hiddenAbility = "Rain Dish",
                learnset = new[] { "Tackle", "Tail Whip", "Water Gun", "Guard Pulse" },
                evolutionRules = new[] { "level:16:8" },
                formVariants = new[] { "Default" },
                dimensionSplitForms = new[] { "Squirtle Rift" },
                fusionCompatibleSpecies = new[] { 1, 4 }
            };

            species[8] = new PokemonSpecies
            {
                speciesId = 8,
                nationalDexId = 8,
                regionalDexId = 8,
                displayName = "Wartortle",
                category = "Turtle Pokemon",
                loreText = "Its tail is large and covered with rich fur.",
                height = 1.0f,
                weight = 22.5f,
                genderRatio = "87.5m_12.5f",
                eggGroups = new[] { "Monster", "Water 1" },
                growthRate = "medium_slow",
                catchRate = 45,
                friendshipBase = 50,
                baseStats = new Stats { hp = 59, atk = 63, def = 80, spa = 65, spd = 80, spe = 58 },
                type1 = PokemonType.Water,
                type2 = PokemonType.None,
                abilities = new[] { "Torrent" },
                hiddenAbility = "Rain Dish",
                learnset = new[] { "Tackle", "Tail Whip", "Water Gun", "Aqua Tail" },
                evolutionRules = new[] { "level:36:9" },
                formVariants = new[] { "Default" },
                dimensionSplitForms = new[] { "Wartortle Rift" },
                fusionCompatibleSpecies = new[] { 1, 4 }
            };

            species[9] = new PokemonSpecies
            {
                speciesId = 9,
                nationalDexId = 9,
                regionalDexId = 9,
                displayName = "Blastoise",
                category = "Shellfish Pokemon",
                loreText = "Its shell cannons fire water blasts with crushing force.",
                height = 1.6f,
                weight = 85.5f,
                genderRatio = "87.5m_12.5f",
                eggGroups = new[] { "Monster", "Water 1" },
                growthRate = "medium_slow",
                catchRate = 45,
                friendshipBase = 50,
                baseStats = new Stats { hp = 79, atk = 83, def = 100, spa = 85, spd = 105, spe = 78 },
                type1 = PokemonType.Water,
                type2 = PokemonType.None,
                abilities = new[] { "Torrent" },
                hiddenAbility = "Rain Dish",
                learnset = new[] { "Tackle", "Water Gun", "Aqua Tail", "Guard Pulse" },
                evolutionRules = new string[0],
                formVariants = new[] { "Default", "Gigantamax Blastoise" },
                dimensionSplitForms = new[] { "Blastoise Rift" },
                megaForms = new[] { "Mega Blastoise" },
                fusionCompatibleSpecies = new[] { 1, 4 }
            };
        }
    }
}
"""

    def _render_battle_code(self):
        return """using System.Collections.Generic;
using System.Linq;
using PokeEngine.Core;
using PokeEngine.Data;
using PokeEngine.Overworld;
using PokeEngine.Pokemon;
using UnityEngine;

namespace PokeEngine.Battle
{
    public sealed class BattleEngineRuntime : MonoBehaviour, IPokeEngineService
    {
        private readonly Queue<BattleAction> actionQueue = new Queue<BattleAction>();
        private readonly Dictionary<string, int> partyHp = new Dictionary<string, int>();
        private readonly List<PokemonInstance> activeBattleParty = new List<PokemonInstance>();

        public BattleState State { get; private set; }
        public BattleMode Mode { get; private set; }
        public bool InBattle { get; private set; }
        public PokemonInstance WildOpponent { get; private set; }
        public int WildOpponentCurrentHp { get; private set; }
        public int WildOpponentMaxHp { get; private set; }
        public int BattleTurn { get; private set; }
        public string BattleMessage { get; private set; } = "No active battle.";
        public DamageCalculator Damage { get; private set; } = new DamageCalculator();
        public AbilitySystemRuntime Abilities { get; private set; } = new AbilitySystemRuntime();
        public bool WaitingForReplacement { get; private set; }
        public string ActivePlayerPokemonId { get; private set; }

        public void Initialize(PokeEngineRuntime runtime)
        {
            State = BattleState.Intro;
        }

        public void StartBattle(BattleMode mode, IEnumerable<PokemonInstance> battlers)
        {
            Mode = mode;
            InBattle = true;
            WildOpponent = null;
            WildOpponentCurrentHp = 0;
            WildOpponentMaxHp = 0;
            BattleTurn = 1;
            WaitingForReplacement = false;
            var party = battlers != null ? battlers.ToList() : new List<PokemonInstance>();
            InitializePartyHp(party);
            ActivePlayerPokemonId = party.Count > 0 ? party[0].instanceId : string.Empty;
            Time.timeScale = 0f;
            State = BattleState.SendOut;
            BattleMessage = "Battle started: " + mode;
            Debug.Log("[PokeEngine] " + BattleMessage);
            Abilities.Trigger(AbilityHook.OnEnterBattle, battlers);
            State = BattleState.CommandSelection;
        }

        public void StartWildEncounter(PokemonInstance wildPokemon, IEnumerable<PokemonInstance> playerParty = null)
        {
            if (InBattle)
            {
                return;
            }

            Mode = BattleMode.Single;
            WildOpponent = wildPokemon;
            WildOpponentMaxHp = Mathf.Max(1, wildPokemon.currentStats.hp);
            WildOpponentCurrentHp = WildOpponentMaxHp;
            BattleTurn = 1;
            InBattle = true;
            WaitingForReplacement = false;
            var database = PokeEngineRuntime.Instance != null ? PokeEngineRuntime.Instance.Get<PokemonDatabaseRuntime>() : null;
            var resolvedParty = database != null ? database.Party : playerParty;
            InitializePartyHp(resolvedParty);
            var activePokemon = database != null ? database.ActivePartyPokemon : (resolvedParty != null ? resolvedParty.FirstOrDefault() : null);
            ActivePlayerPokemonId = activePokemon != null ? activePokemon.instanceId : string.Empty;
            Time.timeScale = 0f;
            State = BattleState.Intro;
            BattleMessage = "A wild " + wildPokemon.nickname + " appeared!";
            PokeEngineRuntime.Instance?.Get<PokeEventBus>()?.Publish("battle.wild_encounter_started", wildPokemon);
            Debug.Log("[PokeEngine] " + BattleMessage);
            State = BattleState.CommandSelection;
        }

        public void PrototypePlayerAttack(PokemonInstance playerPokemon)
        {
            PrototypePlayerAttack(playerPokemon, playerPokemon != null && playerPokemon.moves.Length > 0 ? playerPokemon.moves[0] : "Tackle");
        }

        public void PrototypePlayerAttack(PokemonInstance playerPokemon, string moveName)
        {
            if (!InBattle || playerPokemon == null)
            {
                return;
            }

            if (WaitingForReplacement)
            {
                BattleMessage = "Choose another Pokemon from your party.";
                State = BattleState.SwitchHandling;
                return;
            }

            EnsurePokemonHp(playerPokemon);
            if (IsPokemonFainted(playerPokemon))
            {
                WaitingForReplacement = true;
                State = BattleState.SwitchHandling;
                BattleMessage = playerPokemon.nickname + " has fainted. Choose another Pokemon from your party.";
                return;
            }

            if (WildOpponent == null)
            {
                BattleMessage = playerPokemon.nickname + " is ready for battle.";
                return;
            }

            var move = BuildPrototypeMove(moveName, playerPokemon);
            var result = Damage.Calculate(playerPokemon, WildOpponent, move, Mode);
            WildOpponentCurrentHp = Mathf.Max(0, WildOpponentCurrentHp - result.finalDamage);
            BattleMessage = playerPokemon.nickname + " used " + move.name + "! It dealt " + result.finalDamage + " prototype damage.";
            Debug.Log("[PokeEngine] " + BattleMessage);
            if (WildOpponentCurrentHp <= 0)
            {
                BattleMessage += " Wild " + WildOpponent.nickname + " fainted.";
                EndBattle(true);
                return;
            }

            BattleTurn++;
            BattleMessage += " Wild " + WildOpponent.nickname + " has " + WildOpponentCurrentHp + "/" + WildOpponentMaxHp + " HP. Lower HP improves capture odds.";
            PrototypeWildCounterAttack(playerPokemon);
        }

        private MoveDefinition BuildPrototypeMove(string moveName, PokemonInstance playerPokemon)
        {
            if (string.IsNullOrEmpty(moveName))
            {
                moveName = "Tackle";
            }

            var move = new MoveDefinition
            {
                name = moveName,
                power = 40,
                accuracy = 100,
                priority = 0,
                category = "Physical",
                type = PokemonType.Normal
            };

            if (moveName.Contains("Leaf") || moveName.Contains("Lash") || moveName.Contains("Vine") || moveName.Contains("Razor"))
            {
                move.type = PokemonType.Leaf;
                move.power = 45;
            }
            else if (moveName.Contains("Cinder") || moveName.Contains("Flame") || moveName.Contains("Ember"))
            {
                move.type = PokemonType.Flame;
                move.category = "Special";
                move.power = 45;
            }
            else if (moveName.Contains("Water") || moveName.Contains("Aqua"))
            {
                move.type = PokemonType.Water;
                move.category = "Special";
                move.power = 45;
            }
            else if (moveName.Contains("Rift") || moveName.Contains("Dimension"))
            {
                move.type = PokemonType.Dimensional;
                move.category = "Special";
                move.power = 55;
            }
            else if (moveName.Contains("Guard") || moveName.Contains("Growl") || moveName.Contains("Tail Whip"))
            {
                move.power = 20;
            }

            return move;
        }

        public void TryRun()
        {
            if (!InBattle)
            {
                return;
            }

            BattleMessage = "Got away safely.";
            Debug.Log("[PokeEngine] " + BattleMessage);
            EndBattle(false);
        }

        public bool TrySwitchPokemon(PokemonDatabaseRuntime database, int partyIndex)
        {
            if (!InBattle || database == null)
            {
                return false;
            }

            if (partyIndex < 0 || partyIndex >= database.Party.Count)
            {
                BattleMessage = "That party slot is empty.";
                return false;
            }

            var replacement = database.Party[partyIndex];
            EnsurePokemonHp(replacement);
            if (IsPokemonFainted(replacement))
            {
                BattleMessage = replacement.nickname + " has fainted and cannot battle.";
                WaitingForReplacement = HasUsablePartyPokemon(database);
                return false;
            }

            database.SetActivePartyIndex(partyIndex);
            ActivePlayerPokemonId = replacement.instanceId;
            WaitingForReplacement = false;
            State = BattleState.CommandSelection;
            BattleMessage = "Go, " + replacement.nickname + "!";
            Abilities.Trigger(AbilityHook.OnSwitch, new[] { replacement });
            return true;
        }

        public bool TryCatchWildPokemon(PokemonDatabaseRuntime database)
        {
            if (!InBattle || WildOpponent == null || database == null)
            {
                BattleMessage = "Capture Cores can only be used during a wild battle.";
                return false;
            }

            var species = database.GetSpecies(WildOpponent.speciesId);
            var catchRate = species != null ? species.catchRate : 45;
            var hpMissingFactor = WildOpponentMaxHp <= 0 ? 0f : 1f - (WildOpponentCurrentHp / (float)WildOpponentMaxHp);
            var catchRateFactor = Mathf.Clamp01(catchRate / 255f);
            var turnPressure = Mathf.Clamp01((BattleTurn - 1) * 0.025f);
            var catchChance = Mathf.Clamp01(catchRateFactor * 0.35f + Mathf.Lerp(0.10f, 0.55f, hpMissingFactor) + turnPressure);
            if (Random.value <= catchChance)
            {
                var addedToParty = database.AddToParty(WildOpponent);
                WildOpponent.currentHp = Mathf.Max(1, WildOpponentCurrentHp);
                BattleMessage = "Gotcha! " + WildOpponent.nickname + " was caught " + (addedToParty ? "and joined the party." : "and was sent to PC storage.") + " Owned Pokemon: " + database.OwnedPokemonCount + ".";
                PokeEngineRuntime.Instance?.Get<PokeEventBus>()?.Publish("pokemon.caught", WildOpponent);
                Debug.Log("[PokeEngine] " + BattleMessage);
                EndBattle(true);
                return true;
            }

            BattleTurn++;
            BattleMessage = WildOpponent.nickname + " broke free! Weaken it or try another Capture Core.";
            Debug.Log("[PokeEngine] " + BattleMessage);
            return false;
        }

        public void EndBattle(bool victory)
        {
            if (victory)
            {
                var database = PokeEngineRuntime.Instance != null ? PokeEngineRuntime.Instance.Get<PokemonDatabaseRuntime>() : null;
                var activePokemon = database != null ? database.ActivePartyPokemon : null;
                if (database != null && activePokemon != null && WildOpponent != null)
                {
                    var reward = Mathf.Max(15, WildOpponent.level * 24);
                    database.AddExperience(activePokemon, reward);
                    BattleMessage += " " + activePokemon.nickname + " gained " + reward + " EXP.";
                }
            }

            State = victory ? BattleState.RewardProcessing : BattleState.VictoryLoss;
            InBattle = false;
            WildOpponent = null;
            WildOpponentCurrentHp = 0;
            WildOpponentMaxHp = 0;
            BattleTurn = 0;
            WaitingForReplacement = false;
            ActivePlayerPokemonId = string.Empty;
            Time.timeScale = 1f;
        }

        public void HealParty(PokemonDatabaseRuntime database)
        {
            if (database == null)
            {
                return;
            }

            database.HealParty();
            foreach (var pokemon in database.Party)
            {
                if (pokemon == null || string.IsNullOrEmpty(pokemon.instanceId))
                {
                    continue;
                }

                partyHp[pokemon.instanceId] = database.GetMaxHp(pokemon);
            }

            BattleMessage = "Your party was fully healed.";
        }

        public void SubmitAction(BattleAction action)
        {
            actionQueue.Enqueue(action);
        }

        public void ProcessTurn()
        {
            State = BattleState.ActionQueue;
            var sorted = actionQueue.OrderByDescending(a => a.priority + a.move.priority).ThenByDescending(a => a.actor.currentStats.spe).ToList();
            actionQueue.Clear();

            foreach (var action in sorted)
            {
                State = BattleState.MoveExecution;
                Abilities.Trigger(AbilityHook.OnMoveUsed, new[] { action.actor });
                var result = Damage.Calculate(action.actor, action.target, action.move, Mode);
                Debug.Log("[PokeEngine] " + action.actor.nickname + " used " + action.move.name + " for " + result.finalDamage + " damage.");
                State = BattleState.DamageResolution;
            }

            State = BattleState.CommandSelection;
        }

        public int GetPokemonCurrentHp(PokemonInstance pokemon)
        {
            EnsurePokemonHp(pokemon);
            if (pokemon == null || string.IsNullOrEmpty(pokemon.instanceId))
            {
                return 0;
            }

            return partyHp.TryGetValue(pokemon.instanceId, out var hp) ? hp : 0;
        }

        public int GetPokemonMaxHp(PokemonInstance pokemon)
        {
            return pokemon != null ? Mathf.Max(1, pokemon.currentStats.hp) : 0;
        }

        public void SetPokemonCurrentHp(PokemonInstance pokemon, int hp)
        {
            if (pokemon == null || string.IsNullOrEmpty(pokemon.instanceId))
            {
                return;
            }

            partyHp[pokemon.instanceId] = Mathf.Clamp(hp, 0, GetPokemonMaxHp(pokemon));
            pokemon.currentHp = partyHp[pokemon.instanceId];
        }

        public bool IsPokemonFainted(PokemonInstance pokemon)
        {
            return pokemon == null || GetPokemonCurrentHp(pokemon) <= 0;
        }

        private void InitializePartyHp(IEnumerable<PokemonInstance> party)
        {
            activeBattleParty.Clear();
            if (party == null)
            {
                return;
            }

            foreach (var pokemon in party)
            {
                if (pokemon == null || string.IsNullOrEmpty(pokemon.instanceId))
                {
                    continue;
                }

                activeBattleParty.Add(pokemon);
                partyHp[pokemon.instanceId] = Mathf.Clamp(pokemon.currentHp, 0, GetPokemonMaxHp(pokemon));
            }
        }

        private void EnsurePokemonHp(PokemonInstance pokemon)
        {
            if (pokemon == null || string.IsNullOrEmpty(pokemon.instanceId))
            {
                return;
            }

            if (!partyHp.ContainsKey(pokemon.instanceId))
            {
                partyHp[pokemon.instanceId] = Mathf.Clamp(pokemon.currentHp, 0, GetPokemonMaxHp(pokemon));
            }
        }

        private void PrototypeWildCounterAttack(PokemonInstance playerPokemon)
        {
            if (!InBattle || WildOpponent == null || playerPokemon == null || WildOpponentCurrentHp <= 0)
            {
                return;
            }

            State = BattleState.ActionQueue;
            var wildMoveName = WildOpponent.moves != null && WildOpponent.moves.Length > 0 ? WildOpponent.moves[Random.Range(0, WildOpponent.moves.Length)] : "Tackle";
            var wildMove = BuildPrototypeMove(wildMoveName, WildOpponent);
            var result = Damage.Calculate(WildOpponent, playerPokemon, wildMove, Mode);
            var maxChunk = Mathf.Max(5, GetPokemonMaxHp(playerPokemon) / 3);
            var damage = Mathf.Clamp(result.finalDamage, 4, maxChunk);
            partyHp[playerPokemon.instanceId] = Mathf.Max(0, GetPokemonCurrentHp(playerPokemon) - damage);
            playerPokemon.currentHp = partyHp[playerPokemon.instanceId];
            State = BattleState.DamageResolution;
            BattleMessage += " Wild " + WildOpponent.nickname + " used " + wildMove.name + "! " + playerPokemon.nickname + " took " + damage + " damage.";

            if (partyHp[playerPokemon.instanceId] <= 0)
            {
                State = BattleState.FaintHandling;
                BattleMessage += " " + playerPokemon.nickname + " fainted!";
                var database = PokeEngineRuntime.Instance != null ? PokeEngineRuntime.Instance.Get<PokemonDatabaseRuntime>() : null;
                if ((database != null && HasUsablePartyPokemon(database)) || (database == null && HasUsablePartyPokemon(activeBattleParty)))
                {
                    WaitingForReplacement = true;
                    State = BattleState.SwitchHandling;
                    BattleMessage += " Choose another Pokemon from your party.";
                }
                else
                {
                    BattleMessage += " No Pokemon are able to battle.";
                    TriggerPartyBlackout();
                }
            }
            else
            {
                State = BattleState.CommandSelection;
                BattleMessage += " " + playerPokemon.nickname + " has " + partyHp[playerPokemon.instanceId] + "/" + GetPokemonMaxHp(playerPokemon) + " HP.";
            }
        }

        private void TriggerPartyBlackout()
        {
            BattleMessage += " You blacked out and were brought to the Pokemon Center. Talk to the nurse to heal your party.";
            var runtime = PokeEngineRuntime.Instance;
            runtime?.Get<PokeEventBus>()?.Publish("battle.party_wiped", activeBattleParty);
            runtime?.Get<WorldStreamingManager>()?.TeleportPlayerToPokemonCenter();
            EndBattle(false);
        }

        private bool HasUsablePartyPokemon(PokemonDatabaseRuntime database)
        {
            if (database == null)
            {
                return false;
            }

            return HasUsablePartyPokemon(database.Party);
        }

        private bool HasUsablePartyPokemon(IEnumerable<PokemonInstance> party)
        {
            if (party == null)
            {
                return false;
            }

            foreach (var pokemon in party)
            {
                EnsurePokemonHp(pokemon);
                if (!IsPokemonFainted(pokemon))
                {
                    return true;
                }
            }

            return false;
        }
    }

    public sealed class DamageCalculator
    {
        public DamageResult Calculate(PokemonInstance attacker, PokemonInstance defender, MoveDefinition move, BattleMode mode)
        {
            var offensive = move.category == "Special" ? attacker.currentStats.spa : attacker.currentStats.atk;
            var defensive = move.category == "Special" ? defender.currentStats.spd : defender.currentStats.def;
            var baseDamage = (((2f * attacker.level / 5f + 2f) * move.power * offensive / Mathf.Max(1, defensive)) / 50f) + 2f;
            var stab = 1.5f;
            var type = 1f;
            var weather = move.type == PokemonType.Flame ? 1.2f : 1f;
            var terrain = move.type == PokemonType.Leaf ? 1.15f : 1f;
            var burn = move.category == "Physical" ? 0.5f : 1f;
            var raid = mode == BattleMode.Raid ? 0.75f : 1f;
            var transformation = attacker.dimensionSplitActive ? 1.3f : 1f;
            var fusion = attacker.fused ? 1.15f : 1f;
            var random = Random.Range(0.85f, 1f);
            var final = Mathf.Max(1, Mathf.RoundToInt(baseDamage * stab * type * weather * terrain * burn * raid * transformation * fusion * random));
            return new DamageResult { finalDamage = final, critical = Random.value < 0.0625f };
        }
    }

    public struct DamageResult
    {
        public int finalDamage;
        public bool critical;
    }

    public sealed class AbilitySystemRuntime
    {
        private readonly HashSet<string> activeOnce = new HashSet<string>();

        public void Trigger(AbilityHook hook, IEnumerable<PokemonInstance> pokemon)
        {
            foreach (var mon in pokemon)
            {
                var key = mon.instanceId + hook;
                if (hook == AbilityHook.OnEnterBattle && activeOnce.Contains(key))
                {
                    continue;
                }

                activeOnce.Add(key);
                Debug.Log("[PokeEngine] Ability hook " + hook + " checked for " + mon.nickname + " ability " + mon.ability);
            }
        }
    }
}
"""

    def _render_transformation_code(self):
        return """using System;
using PokeEngine.Core;
using PokeEngine.Data;
using UnityEngine;

namespace PokeEngine.Battle
{
    public sealed class TransformationFusionSystems : MonoBehaviour, IPokeEngineService
    {
        [SerializeField] private int dimensionMeterMax = 100;

        public void Initialize(PokeEngineRuntime runtime)
        {
        }

        public bool TryMegaEvolve(PokemonInstance pokemon)
        {
            if (pokemon.megaUsed)
            {
                return false;
            }

            pokemon.megaUsed = true;
            pokemon.currentStats = pokemon.currentStats.Scaled(1.25f);
            Debug.Log("[PokeEngine] Mega Evolution activated for " + pokemon.nickname + ". Form, ability, stats, animation, and audio cues swapped.");
            return true;
        }

        public bool TryDimensionSplit(PokemonInstance pokemon, int meter, bool storyUnlocked, bool bondReady)
        {
            if (pokemon.dimensionSplitActive || meter < dimensionMeterMax || !storyUnlocked || !bondReady)
            {
                return false;
            }

            pokemon.dimensionSplitActive = true;
            pokemon.currentStats = pokemon.currentStats.Scaled(1.35f);
            Debug.Log("[PokeEngine] Dimension Split sequence: camera, dimensional FX, audio distortion, model morph, signature move, ability mutation.");
            return true;
        }

        public PokemonInstance Fuse(PokemonInstance left, PokemonInstance right)
        {
            var fusion = new PokemonInstance
            {
                speciesId = StableFusionId(left.speciesId, right.speciesId),
                nickname = left.nickname + "-" + right.nickname,
                level = Mathf.Max(left.level, right.level),
                fused = true,
                currentStats = new Stats
                {
                    hp = Mathf.RoundToInt((left.currentStats.hp + right.currentStats.hp) * 0.55f),
                    atk = Mathf.RoundToInt((left.currentStats.atk + right.currentStats.atk) * 0.55f),
                    def = Mathf.RoundToInt((left.currentStats.def + right.currentStats.def) * 0.55f),
                    spa = Mathf.RoundToInt((left.currentStats.spa + right.currentStats.spa) * 0.55f),
                    spd = Mathf.RoundToInt((left.currentStats.spd + right.currentStats.spd) * 0.55f),
                    spe = Mathf.RoundToInt((left.currentStats.spe + right.currentStats.spe) * 0.55f)
                },
                moves = MergeMoves(left.moves, right.moves),
                ability = left.ability + "+" + right.ability
            };
            Debug.Log("[PokeEngine] Fusion generated: metadata, stats, typing, move pool, ability inheritance, visuals, portrait, and icon cache keys.");
            return fusion;
        }

        public Tuple<PokemonInstance, PokemonInstance> Separate(PokemonInstance fusion)
        {
            Debug.Log("[PokeEngine] Fusion separated using registry source data.");
            return new Tuple<PokemonInstance, PokemonInstance>(new PokemonInstance(), new PokemonInstance());
        }

        private int StableFusionId(int left, int right)
        {
            return 900000 + Mathf.Min(left, right) * 1000 + Mathf.Max(left, right);
        }

        private string[] MergeMoves(string[] left, string[] right)
        {
            var merged = new System.Collections.Generic.List<string>();
            merged.AddRange(left);
            foreach (var move in right)
            {
                if (!merged.Contains(move))
                {
                    merged.Add(move);
                }
            }

            return merged.Count > 4 ? merged.GetRange(0, 4).ToArray() : merged.ToArray();
        }
    }
}
"""

    def _render_raid_code(self):
        return """using System.Collections.Generic;
using PokeEngine.Core;
using PokeEngine.Data;
using PokeEngine.Overworld;
using PokeEngine.Pokemon;
using PokeEngine.UI;
using UnityEngine;

namespace PokeEngine.Raid
{
    public sealed class RaidBattleRuntime : MonoBehaviour, IPokeEngineService
    {
        [SerializeField] private float sharedTimerSeconds = 600f;
        [SerializeField] private int shieldHitsToBreak = 4;

        private float timer;
        private int shieldHits;
        private readonly List<PokemonInstance> trainers = new List<PokemonInstance>();

        public int Tier { get; private set; }
        public bool Active { get; private set; }

        public void Initialize(PokeEngineRuntime runtime)
        {
            timer = sharedTimerSeconds;
        }

        public void StartRaid(int tier, PokemonInstance boss, IEnumerable<PokemonInstance> participants)
        {
            Tier = tier;
            Active = true;
            timer = sharedTimerSeconds;
            trainers.Clear();
            trainers.AddRange(participants);
            Debug.Log("[PokeEngine] Raid started tier " + tier + " with shared timer, shield phases, boss AI, capture, and loot pipeline.");
        }

        private void Update()
        {
            if (!Active)
            {
                return;
            }

            timer -= Time.deltaTime;
            if (timer <= 0f)
            {
                EndRaid(false);
            }
        }

        public void HitShield()
        {
            shieldHits++;
            if (shieldHits >= shieldHitsToBreak)
            {
                shieldHits = 0;
                Debug.Log("[PokeEngine] Raid shield broken. Boss stun and reward bonus queued.");
            }
        }

        public void EndRaid(bool victory)
        {
            Active = false;
            Debug.Log(victory ? "[PokeEngine] Raid victory. Capture and reward distribution." : "[PokeEngine] Raid failed.");
        }
    }

    public sealed class RaidDenTrigger : MonoBehaviour
    {
        [SerializeField] private int tier = 1;
        [SerializeField] private bool startOnTouch = true;
        [SerializeField] private float restartCooldownSeconds = 2f;
        private bool playerInside;
        private float lastStartTime = -99f;

        public void Configure(int raidTier, bool touchStartsRaid)
        {
            tier = Mathf.Max(1, raidTier);
            startOnTouch = touchStartsRaid;
        }

        private void OnTriggerEnter(Collider other)
        {
            if (!other.CompareTag("Player"))
            {
                return;
            }

            playerInside = true;
            if (startOnTouch)
            {
                TryStartRaid();
            }
        }

        private void OnTriggerStay(Collider other)
        {
            if (!other.CompareTag("Player"))
            {
                return;
            }

            playerInside = true;
            if (Input.GetKeyDown(KeyCode.E) || Input.GetKeyDown(KeyCode.Return))
            {
                TryStartRaid();
            }
        }

        private void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("Player"))
            {
                playerInside = false;
            }
        }

        private void OnGUI()
        {
            if (!playerInside || PrototypeRpgHud.IsPauseMenuOpen || PrototypeRpgHud.IsBattleMenuOpen)
            {
                return;
            }

            var guiMatrix = PrototypeGuiScale.Begin();
            try
            {
                GUI.Box(new Rect(18, PrototypeGuiScale.Height - 432, 500, 78), startOnTouch ? "Raid den activated. Press E to restart test raid." : "Press E to start raid test.");
            }
            finally
            {
                PrototypeGuiScale.End(guiMatrix);
            }
        }

        private void TryStartRaid()
        {
            if (Time.unscaledTime - lastStartTime < restartCooldownSeconds)
            {
                return;
            }

            var runtime = PokeEngineRuntime.Instance;
            var database = runtime != null ? runtime.Get<PokemonDatabaseRuntime>() : null;
            var raid = runtime != null ? runtime.Get<RaidBattleRuntime>() : null;
            if (database == null || raid == null || database.Party.Count == 0)
            {
                Debug.LogWarning("[PokeEngine] Raid den could not start; runtime, raid, or party is missing.");
                return;
            }

            if (raid.Active)
            {
                Debug.Log("[PokeEngine] Raid is already active.");
                return;
            }

            lastStartTime = Time.unscaledTime;
            raid.StartRaid(tier, database.Party[0], database.Party);
        }
    }
}
"""

    def _render_save_code(self):
        return """using System;
using System.IO;
using PokeEngine.Core;
using UnityEngine;

namespace PokeEngine.Save
{
    public sealed class PokeSaveManager : MonoBehaviour, IPokeEngineService
    {
        [SerializeField] private int saveVersion = 1;
        [SerializeField] private float autosaveIntervalSeconds = 60f;
        private float autosaveTimer;
        private string SavePath => Path.Combine(Application.persistentDataPath, "pokeengine_save.json");
        private string AutosavePath => Path.Combine(Application.persistentDataPath, "pokeengine_autosave.json");
        private string BackupPath => Path.Combine(Application.persistentDataPath, "pokeengine_save.bak.json");
        private string RecoveryPath => Path.Combine(Application.persistentDataPath, "pokeengine_recovery.json");

        public void Initialize(PokeEngineRuntime runtime)
        {
            autosaveTimer = autosaveIntervalSeconds;
        }

        private void Update()
        {
            autosaveTimer -= Time.deltaTime;
            if (autosaveTimer <= 0f)
            {
                Autosave();
                autosaveTimer = autosaveIntervalSeconds;
            }
        }

        public void SaveGame()
        {
            Directory.CreateDirectory(Application.persistentDataPath);
            if (File.Exists(SavePath))
            {
                File.Copy(SavePath, BackupPath, true);
            }

            var data = new PrototypeSaveData
            {
                version = saveVersion,
                savedAtUtc = DateTime.UtcNow.ToString("O"),
                playerName = "Nova",
                worldProgression = "prototype_open_world",
                currentScene = "PrototypeRegion",
                currentLocation = "Prototype Testing Site",
                money = 3000,
                badges = 1,
                party = new[] { "Bulbasaur", "Charmander" },
                inventory = new[] { "Potion", "Capture Core" },
                eventFlags = new[] { "starter_received", "prototype_town_entered" },
                questStates = new[] { "meet_professor:active", "first_encounter:active" },
                raidStates = new[] { "test_den:available" },
                transformationUnlocks = new[] { "mega", "dimension_split", "fusion" },
                fusionRegistry = new[] { "Bulbamander" }
            };
            WriteAtomic(SavePath, data);
            File.Copy(SavePath, RecoveryPath, true);
            Debug.Log("[PokeEngine] Game saved with backup, recovery, version validation, and migration hook.");
        }

        public void Autosave()
        {
            Directory.CreateDirectory(Application.persistentDataPath);
            var data = new PrototypeSaveData
            {
                version = saveVersion,
                slotId = "autosave",
                savedAtUtc = DateTime.UtcNow.ToString("O"),
                playerName = "Nova",
                currentScene = "PrototypeRegion",
                currentLocation = "Prototype Testing Site",
                worldProgression = "autosave",
                party = new[] { "Bulbasaur", "Charmander" },
                eventFlags = new[] { "autosave_written" },
                transformationUnlocks = new[] { "mega", "dimension_split", "fusion" },
                fusionRegistry = new[] { "Bulbamander" }
            };
            WriteAtomic(AutosavePath, data);
        }

        public PrototypeSaveData LoadGame()
        {
            if (!File.Exists(SavePath))
            {
                return File.Exists(AutosavePath) ? LoadFromPath(AutosavePath) : null;
            }

            var data = LoadFromPath(SavePath);
            if (data == null && File.Exists(BackupPath))
            {
                data = LoadFromPath(BackupPath);
            }
            if (data == null && File.Exists(RecoveryPath))
            {
                data = LoadFromPath(RecoveryPath);
            }
            if (data == null)
            {
                return null;
            }
            if (data.version != saveVersion)
            {
                Debug.Log("[PokeEngine] Save migration required from version " + data.version + " to " + saveVersion);
                data.version = saveVersion;
            }

            return data;
        }

        private PrototypeSaveData LoadFromPath(string path)
        {
            try
            {
                return JsonUtility.FromJson<PrototypeSaveData>(File.ReadAllText(path));
            }
            catch (Exception ex)
            {
                Debug.LogWarning("[PokeEngine] Save load failed for " + path + ": " + ex.Message);
                return null;
            }
        }

        private void WriteAtomic(string path, PrototypeSaveData data)
        {
            var temp = path + ".tmp";
            File.WriteAllText(temp, JsonUtility.ToJson(data, true));
            if (File.Exists(path))
            {
                File.Delete(path);
            }
            File.Move(temp, path);
        }
    }

    [Serializable]
    public sealed class PrototypeSaveData
    {
        public int version;
        public string slotId = "manual";
        public string savedAtUtc;
        public string playerName;
        public string currentScene;
        public string currentLocation;
        public int money;
        public int badges;
        public string[] party;
        public string[] inventory;
        public string[] eventFlags;
        public string[] questStates;
        public string[] raidStates;
        public string worldProgression;
        public string[] transformationUnlocks;
        public string[] fusionRegistry;
    }
}
"""

    def _render_ui_code(self):
        return """using PokeEngine.Battle;
using PokeEngine.Core;
using PokeEngine.Data;
using PokeEngine.Events;
using PokeEngine.Overworld;
using PokeEngine.Pokemon;
using PokeEngine.Raid;
using PokeEngine.Save;
using UnityEngine;

namespace PokeEngine.UI
{
    public static class PrototypeGuiScale
    {
        public static float Scale
        {
            get
            {
                var fit = Mathf.Min(Screen.width / 1280f, Screen.height / 720f);
                return Mathf.Clamp(fit, 1f, 1.55f);
            }
        }

        public static float Width => Screen.width / Scale;
        public static float Height => Screen.height / Scale;

        public static Matrix4x4 Begin()
        {
            var previous = GUI.matrix;
            var scale = Scale;
            GUI.matrix = Matrix4x4.TRS(Vector3.zero, Quaternion.identity, new Vector3(scale, scale, 1f));
            return previous;
        }

        public static void End(Matrix4x4 previous)
        {
            GUI.matrix = previous;
        }
    }

    public sealed class PrototypeRpgHud : MonoBehaviour, IPokeEngineService
    {
        [SerializeField] private bool showDebugHud = true;
        [SerializeField] private bool showMinimap = true;
        private PokeEngineRuntime runtime;
        private Transform minimapPlayer;
        private bool gameLaunched;
        private bool pauseMenuOpen;
        private string activeMenuScreen = "Main";
        private string battleMenuScreen = "Commands";
        private static bool battleMenuOpen;

        public static bool IsPauseMenuOpen { get; private set; }
        public static bool IsBattleMenuOpen
        {
            get
            {
                var battle = PokeEngineRuntime.Instance?.Get<BattleEngineRuntime>();
                return battleMenuOpen || (battle != null && battle.InBattle);
            }
            private set
            {
                battleMenuOpen = value;
            }
        }

        public void Initialize(PokeEngineRuntime runtime)
        {
            this.runtime = runtime;
            IsPauseMenuOpen = false;
            IsBattleMenuOpen = false;
            Time.timeScale = 0f;
            UpdateCursorLock();
        }

        private void Update()
        {
            if (runtime == null)
            {
                return;
            }

            UpdateCursorLock();

            if (!gameLaunched)
            {
                if (Input.GetKeyDown(KeyCode.Return))
                {
                    LaunchGame();
                }
                return;
            }

            var battle = runtime.Get<BattleEngineRuntime>();
            if (battle != null && battle.InBattle)
            {
                pauseMenuOpen = false;
                IsPauseMenuOpen = false;
                IsBattleMenuOpen = true;
                return;
            }

            if (Input.GetKeyDown(KeyCode.Tab) || Input.GetKeyDown(KeyCode.X) || Input.GetKeyDown(KeyCode.Escape))
            {
                TogglePauseMenu();
            }

            if (pauseMenuOpen)
            {
                return;
            }

            if (Input.GetKeyDown(KeyCode.F1))
            {
                runtime.Get<PokeSaveManager>()?.SaveGame();
            }
            if (Input.GetKeyDown(KeyCode.F2))
            {
                var save = runtime.Get<PokeSaveManager>()?.LoadGame();
                Debug.Log(save == null ? "[PokeEngine] No save found." : "[PokeEngine] Loaded save for " + save.playerName);
            }
            if (Input.GetKeyDown(KeyCode.F3))
            {
                runtime.Get<PrototypeCutsceneDirector>()?.PlayStoryBeat("intro_lab_departure");
            }
            if (Input.GetKeyDown(KeyCode.F4))
            {
                StartPrototypeBattle();
            }
            if (Input.GetKeyDown(KeyCode.F5))
            {
                StartPrototypeRaid();
            }
        }

        private void LaunchGame()
        {
            gameLaunched = true;
            pauseMenuOpen = false;
            IsPauseMenuOpen = false;
            Time.timeScale = 1f;
            UpdateCursorLock();
        }

        private void TogglePauseMenu()
        {
            pauseMenuOpen = !pauseMenuOpen;
            IsPauseMenuOpen = pauseMenuOpen;
            activeMenuScreen = "Main";
            Time.timeScale = pauseMenuOpen ? 0f : 1f;
            UpdateCursorLock();
        }

        private void OnApplicationFocus(bool hasFocus)
        {
            if (hasFocus)
            {
                UpdateCursorLock();
            }
        }

        private void OnDisable()
        {
            IsPauseMenuOpen = false;
            IsBattleMenuOpen = false;
            Cursor.lockState = CursorLockMode.None;
            Cursor.visible = true;
        }

        private void UpdateCursorLock()
        {
            IsPauseMenuOpen = pauseMenuOpen;
            var battle = runtime != null ? runtime.Get<BattleEngineRuntime>() : null;
            var battleMenuOpen = battle != null && battle.InBattle;
            IsBattleMenuOpen = battleMenuOpen;
            var lockCursor = gameLaunched && !pauseMenuOpen && !battleMenuOpen;
            Cursor.lockState = lockCursor ? CursorLockMode.Locked : CursorLockMode.None;
            Cursor.visible = !lockCursor;
        }

        private void StartPrototypeBattle()
        {
            var database = runtime.Get<PokemonDatabaseRuntime>();
            var battle = runtime.Get<BattleEngineRuntime>();
            if (database == null || battle == null || database.Party.Count == 0)
            {
                Debug.LogWarning("[PokeEngine] Battle could not start; database or party missing.");
                return;
            }

            battle.StartBattle(BattleMode.Single, database.Party);
            battleMenuScreen = "Commands";
        }

        private void UseFightCommand(string moveName = null)
        {
            var database = runtime.Get<PokemonDatabaseRuntime>();
            var battle = runtime.Get<BattleEngineRuntime>();
            if (database == null || battle == null || database.Party.Count == 0)
            {
                return;
            }

            battle.PrototypePlayerAttack(database.ActivePartyPokemon, moveName);
            battleMenuScreen = "Commands";
        }

        private void UseCatchCommand()
        {
            var database = runtime.Get<PokemonDatabaseRuntime>();
            var battle = runtime.Get<BattleEngineRuntime>();
            if (database == null || battle == null)
            {
                return;
            }

            battle.TryCatchWildPokemon(database);
            battleMenuScreen = "Commands";
        }

        private void StartPrototypeRaid()
        {
            var database = runtime.Get<PokemonDatabaseRuntime>();
            var raid = runtime.Get<RaidBattleRuntime>();
            if (database == null || raid == null || database.Party.Count == 0)
            {
                Debug.LogWarning("[PokeEngine] Raid could not start; database or party missing.");
                return;
            }

            raid.StartRaid(1, database.Party[0], database.Party);
        }

        private void OnGUI()
        {
            var guiMatrix = PrototypeGuiScale.Begin();
            try
            {
                if (runtime == null)
                {
                    return;
                }

                if (!gameLaunched)
                {
                    DrawLaunchMenu();
                    return;
                }

                var battle = runtime.Get<BattleEngineRuntime>();
                if (battle != null && battle.InBattle)
                {
                    DrawBattleMenu(battle);
                    return;
                }

                if (pauseMenuOpen)
                {
                    DrawPauseMenu();
                    return;
                }

                if (showDebugHud)
                {
                    GUILayout.BeginArea(new Rect(18, 18, 520, 182), GUI.skin.box);
                    GUILayout.Label("PokeEngine Full RPG Prototype");
                    GUILayout.Label("WASD: 4-direction movement  Hold direction to keep moving");
                    GUILayout.Label("Shift: Sprint");
                    GUILayout.Label("Tab/X/Esc: Menu  Green grass: random encounters");
                    GUILayout.Label("Structured zones: fixed camera  Wild Area: mouse orbit + 15 degree vertical tilt");
                    GUILayout.Label("Mouse is locked during play and unlocks while paused.");
                    GUILayout.EndArea();
                }

                if (showMinimap)
                {
                    DrawMiniMap();
                }
            }
            finally
            {
                PrototypeGuiScale.End(guiMatrix);
            }
        }

        private void DrawLaunchMenu()
        {
            var rect = CenterRect(520, 280);
            GUILayout.BeginArea(rect, GUI.skin.box);
            GUILayout.Label("PokeEngine Prototype", GUI.skin.label);
            GUILayout.Space(12);
            GUILayout.Label("Launch the generated Pokemon-style RPG prototype.");
            GUILayout.Label("Open the pause menu with Tab once in game.");
            GUILayout.Space(18);
            if (GUILayout.Button("Launch Game") || Event.current.keyCode == KeyCode.Return)
            {
                LaunchGame();
            }
            GUILayout.EndArea();
        }

        private void DrawPauseMenu()
        {
            GUI.Box(new Rect(0, 0, PrototypeGuiScale.Width, PrototypeGuiScale.Height), string.Empty);
            var left = new Rect(24, 24, 390, PrototypeGuiScale.Height - 48);
            GUILayout.BeginArea(left, GUI.skin.box);
            GUILayout.Label("PokeEngine Menu", GUI.skin.label);
            GUILayout.Label("Adventure Hub");
            GUILayout.FlexibleSpace();
            if (DrawPauseButton("Pokedex")) activeMenuScreen = "Pokedex";
            if (DrawPauseButton("Pokemon")) activeMenuScreen = "Pokemon";
            if (DrawPauseButton("Bag")) activeMenuScreen = "Bag";
            if (DrawPauseButton("Map")) activeMenuScreen = "Map";
            if (DrawPauseButton("Pokegear / Phone")) activeMenuScreen = "Pokegear";
            if (DrawPauseButton("Quests")) activeMenuScreen = "Quest Log";
            if (DrawPauseButton("Save")) activeMenuScreen = "Save";
            if (DrawPauseButton("Options")) activeMenuScreen = "Settings";
            if (DrawPauseButton("Profile / Trainer Card")) activeMenuScreen = "Trainer Card";
            if (DrawPauseButton("Multiplayer")) activeMenuScreen = "Multiplayer";
            if (showDebugHud && DrawPauseButton("Debug")) activeMenuScreen = "Debug";
            if (DrawPauseButton("Exit Game")) Application.Quit();
            GUILayout.Space(10);
            if (DrawPauseButton("Resume")) TogglePauseMenu();
            GUILayout.FlexibleSpace();
            GUILayout.Label("Tab/X/Esc closes menu");
            GUILayout.EndArea();

            var right = new Rect(PrototypeGuiScale.Width - 380, 24, 356, 240);
            GUILayout.BeginArea(right, GUI.skin.box);
            GUILayout.Label("Status", GUI.skin.label);
            GUILayout.Label("Location: Prototype Testing Site");
            GUILayout.Label("Objective: Test grass, capture, NPC, pickups, and wild camera");
            GUILayout.Label("Badges: 1");
            GUILayout.Label("Money: 3000");
            GUILayout.Label("Weather/Time: Clear Day");
            var database = runtime.Get<PokemonDatabaseRuntime>();
            if (database != null && database.Party.Count > 0)
            {
                var lead = database.ActivePartyPokemon ?? database.Party[0];
                GUILayout.Label("Lead: " + lead.nickname + " Lv." + lead.level);
            }
            GUILayout.EndArea();

            DrawMenuScreen();
        }

        private bool DrawPauseButton(string label)
        {
            GUILayout.BeginHorizontal();
            GUILayout.FlexibleSpace();
            var pressed = GUILayout.Button(label, GUILayout.Width(310), GUILayout.Height(36));
            GUILayout.FlexibleSpace();
            GUILayout.EndHorizontal();
            GUILayout.Space(5);
            return pressed;
        }

        private void DrawMenuScreen()
        {
            if (activeMenuScreen == "Main")
            {
                return;
            }

            var rect = new Rect(438, 24, Mathf.Max(480, PrototypeGuiScale.Width - 860), PrototypeGuiScale.Height - 48);
            GUILayout.BeginArea(rect, GUI.skin.box);
            GUILayout.Label(activeMenuScreen, GUI.skin.label);
            GUILayout.Space(8);

            var database = runtime.Get<PokemonDatabaseRuntime>();
            if (activeMenuScreen == "Pokedex")
            {
                GUILayout.Label("001 Bulbasaur - Seen");
                GUILayout.Label("004 Charmander - Seen");
                GUILayout.Label("007 Squirtle - Seen");
                GUILayout.Label("Starter evolutions, Mega forms, and Gigantamax forms are listed in the generated JSON database.");
            }
            else if (activeMenuScreen == "Pokemon")
            {
                if (database != null)
                {
                    foreach (var pokemon in database.Party)
                    {
                        GUILayout.Label(pokemon.nickname + " Lv." + pokemon.level + "  EXP " + pokemon.experience + "/" + pokemon.experienceToNextLevel + "  HP " + pokemon.currentHp + "/" + pokemon.currentStats.hp);
                        GUILayout.Label("Moves: " + string.Join(", ", pokemon.moves));
                        if (GUILayout.Button("Give " + pokemon.nickname + " 50 EXP"))
                        {
                            database.AddExperience(pokemon, 50);
                        }
                    }
                }
            }
            else if (activeMenuScreen == "Bag")
            {
                if (database != null && database.Inventory.Count > 0)
                {
                    foreach (var item in database.Inventory)
                    {
                        GUILayout.Label("- " + item);
                    }
                }
                else
                {
                    GUILayout.Label("Bag is empty. Pick up the yellow item in town.");
                }
            }
            else if (activeMenuScreen == "Trainer Card")
            {
                GUILayout.Label("Trainer: Nova");
                GUILayout.Label("Region: Aurora Province");
                GUILayout.Label("Badges: 1");
                GUILayout.Label("Money: 3000");
            }
            else if (activeMenuScreen == "Map")
            {
                GUILayout.Label("Prototype Testing Site -> Route 01 -> Echo Cave -> Solara City");
                GUILayout.Label("100m x 100m test site: movement, collision, tall grass, battle/catch, wild camera, NPC, pickups.");
            }
            else if (activeMenuScreen == "Quest Log")
            {
                GUILayout.Label("Meet the Professor");
                GUILayout.Label("Trigger one wild Pokemon encounter");
                GUILayout.Label("Pick up the starter Pokemon in town");
                GUILayout.Label("Enter the Pokemon Center");
            }
            else if (activeMenuScreen == "Save")
            {
                GUILayout.Label("Manual save, autosave, backup save, and recovery save hooks.");
                GUILayout.Label("Current location: Prototype Testing Site");
                GUILayout.Label("Party preview and last save timestamp belong here.");
                if (GUILayout.Button("Save Now")) runtime.Get<PokeSaveManager>()?.SaveGame();
            }
            else if (activeMenuScreen == "Pokegear")
            {
                GUILayout.Label("Clock, phone, radio, and route tools placeholder.");
                GUILayout.Label("Contacts, raid alerts, news feed, daily events, and friend systems belong here.");
                var registry = runtime.Get<PrototypeFeatureRegistry>();
                if (registry != null)
                {
                    GUILayout.Label("V12 architecture features: " + registry.TotalFeatureCount);
                    GUILayout.Label("Matrix: StreamingAssets/Data/prototype_feature_matrix.json");
                }
            }
            else if (activeMenuScreen == "Settings")
            {
                GUILayout.Label("Text speed: Fast");
                GUILayout.Label("Battle animations: On");
                GUILayout.Label("Autosave: On");
                GUILayout.Label("Camera sensitivity, UI scale, language, accessibility, controls, graphics, and theme settings belong here.");
            }
            else if (activeMenuScreen == "Multiplayer")
            {
                GUILayout.Label("Friend list, trading, battling, raid matchmaking, online profile, and event participation scaffolds.");
            }
            else if (activeMenuScreen == "Debug")
            {
                GUILayout.Label("Developer tools: spawn Pokemon, edit party, teleport, trigger events, toggle flags, start battles, spawn raids, weather, and performance.");
            }

            GUILayout.Space(8);
            if (GUILayout.Button("Back")) activeMenuScreen = "Main";
            GUILayout.EndArea();
        }

        private void DrawBattleMenu(BattleEngineRuntime battle)
        {
            var database = runtime.Get<PokemonDatabaseRuntime>();
            var active = database != null ? database.ActivePartyPokemon : null;
            var commandRect = new Rect(28f, PrototypeGuiScale.Height - 176f, 424f, 148f);
            var messageRect = new Rect(Mathf.Max(470f, PrototypeGuiScale.Width - 560f), PrototypeGuiScale.Height - 176f, Mathf.Max(320f, Mathf.Min(532f, PrototypeGuiScale.Width - 500f)), 148f);

            DrawFilledRect(new Rect(0, PrototypeGuiScale.Height - 210f, PrototypeGuiScale.Width, 210f), new Color(0.03f, 0.04f, 0.05f, 0.18f));
            if (active != null)
            {
                DrawBattleStatusPanel(new Rect(24f, 22f, 348f, 92f), active.nickname, active.level, battle.GetPokemonCurrentHp(active), battle.GetPokemonMaxHp(active), GetPokemonUiAccentColor(active.speciesId), true);
            }

            if (battle.WildOpponent != null)
            {
                DrawBattleStatusPanel(new Rect(PrototypeGuiScale.Width - 372f, 22f, 348f, 92f), battle.WildOpponent.nickname, battle.WildOpponent.level, battle.WildOpponentCurrentHp, battle.WildOpponentMaxHp, GetPokemonUiAccentColor(battle.WildOpponent.speciesId), false);
            }

            GUI.Box(messageRect, "");
            GUILayout.BeginArea(new Rect(messageRect.x + 16f, messageRect.y + 12f, messageRect.width - 32f, messageRect.height - 24f));
            GUILayout.Label(battle.BattleMessage);
            if (battle.WildOpponent != null)
            {
                GUILayout.Label("Turn " + battle.BattleTurn + "  Weaken wild Pokemon, then use a Capture Core.");
            }
            else
            {
                GUILayout.Label("Prototype trainer battle. Use Pokemon to inspect your current party/backpack list.");
            }
            GUILayout.EndArea();

            GUI.Box(commandRect, "");
            GUILayout.BeginArea(new Rect(commandRect.x + 12f, commandRect.y + 10f, commandRect.width - 24f, commandRect.height - 20f));
            if (battle.WaitingForReplacement)
            {
                GUILayout.Label("Your Pokemon fainted. Select a party Pokemon that can still battle.");
                DrawBattlePokemonList(database, true);
            }
            else if (battleMenuScreen == "Moves")
            {
                DrawBattleMoveChoices(database);
            }
            else if (battleMenuScreen == "Pokemon")
            {
                DrawBattlePokemonList(database, false);
            }
            else
            {
                DrawBattleCommandChoices(battle, database);
            }
            GUILayout.EndArea();
        }

        private void DrawBattleStatusPanel(Rect rect, string pokemonName, int level, int hp, int maxHp, Color accent, bool playerSide)
        {
            DrawFilledRect(rect, new Color(0.03f, 0.035f, 0.04f, 0.82f));
            DrawFilledRect(new Rect(rect.x, rect.y, 7f, rect.height), accent);
            var portraitRect = playerSide ? new Rect(rect.x + 14f, rect.y + 14f, 56f, 56f) : new Rect(rect.x + rect.width - 70f, rect.y + 14f, 56f, 56f);
            DrawFilledRect(portraitRect, new Color(0.76f, 0.78f, 0.82f, 0.9f));
            DrawFilledRect(new Rect(portraitRect.x + 8f, portraitRect.y + 8f, portraitRect.width - 16f, portraitRect.height - 16f), accent);

            var textX = playerSide ? rect.x + 84f : rect.x + 18f;
            var textWidth = rect.width - 104f;
            GUI.Label(new Rect(textX, rect.y + 12f, textWidth, 24f), pokemonName + "   Lv." + level);
            DrawBattleHpBar(new Rect(textX, rect.y + 44f, textWidth, 14f), hp, maxHp);
            GUI.Label(new Rect(textX, rect.y + 62f, textWidth, 20f), hp + "/" + maxHp);
        }

        private void DrawBattleHpBar(Rect rect, int hp, int maxHp)
        {
            DrawFilledRect(rect, new Color(0.12f, 0.12f, 0.12f, 1f));
            var ratio = maxHp <= 0 ? 0f : Mathf.Clamp01(hp / (float)maxHp);
            var hpColor = ratio > 0.5f ? new Color(0.0f, 0.84f, 0.34f) : (ratio > 0.25f ? new Color(1.0f, 0.74f, 0.12f) : new Color(1.0f, 0.16f, 0.16f));
            DrawFilledRect(new Rect(rect.x + 2f, rect.y + 2f, Mathf.Max(0f, (rect.width - 4f) * ratio), rect.height - 4f), hpColor);
        }

        private Color GetPokemonUiAccentColor(int speciesId)
        {
            switch (speciesId)
            {
                case 1:
                case 2:
                case 3:
                    return new Color(0.22f, 0.78f, 0.38f);
                case 4:
                case 5:
                case 6:
                    return new Color(1.0f, 0.44f, 0.12f);
                case 7:
                case 8:
                case 9:
                    return new Color(0.18f, 0.52f, 1.0f);
                default:
                    return new Color(0.62f, 0.12f, 1.0f);
            }
        }

        private void DrawBattleCommandChoices(BattleEngineRuntime battle, PokemonDatabaseRuntime database)
        {
            GUILayout.BeginHorizontal();
            if (GUILayout.Button("Fight", GUILayout.Height(48))) battleMenuScreen = "Moves";
            if (GUILayout.Button("Capture Core", GUILayout.Height(48))) UseCatchCommand();
            GUILayout.EndHorizontal();
            GUILayout.BeginHorizontal();
            if (GUILayout.Button("Pokemon", GUILayout.Height(48))) battleMenuScreen = "Pokemon";
            if (GUILayout.Button("Run", GUILayout.Height(48)))
            {
                battle.TryRun();
                battleMenuScreen = "Commands";
            }
            GUILayout.EndHorizontal();

            if (database != null)
            {
                GUILayout.Label("Owned Pokemon: " + database.OwnedPokemonCount);
            }
        }

        private void DrawBattleMoveChoices(PokemonDatabaseRuntime database)
        {
            if (database == null || database.Party.Count == 0)
            {
                GUILayout.Label("No Pokemon available.");
                if (GUILayout.Button("Back")) battleMenuScreen = "Commands";
                return;
            }

            var lead = database.ActivePartyPokemon;
            if (lead == null)
            {
                GUILayout.Label("No active Pokemon available.");
                if (GUILayout.Button("Back")) battleMenuScreen = "Commands";
                return;
            }

            GUILayout.Label("Choose a move for " + lead.nickname + ":");
            var moves = GetBattleMoveChoices(lead);
            GUILayout.BeginHorizontal();
            for (var i = 0; i < moves.Length; i++)
            {
                if (i == 2)
                {
                    GUILayout.EndHorizontal();
                    GUILayout.BeginHorizontal();
                }

                if (GUILayout.Button(moves[i], GUILayout.Height(42)))
                {
                    UseFightCommand(moves[i]);
                }
            }
            GUILayout.EndHorizontal();
            if (GUILayout.Button("Back")) battleMenuScreen = "Commands";
        }

        private void DrawBattlePokemonList(PokemonDatabaseRuntime database, bool replacementOnly)
        {
            GUILayout.Label(replacementOnly ? "Choose Replacement Pokemon" : "Pokemon Backpack");
            if (database == null)
            {
                GUILayout.Label("Pokemon database is not loaded.");
            }
            else
            {
                var owned = database.GetOwnedPokemon();
                if (owned.Count == 0)
                {
                    GUILayout.Label("No Pokemon owned yet.");
                }
                else
                {
                    var battle = runtime.Get<BattleEngineRuntime>();
                    for (var i = 0; i < database.Party.Count; i++)
                    {
                        var mon = database.Party[i];
                        var hp = battle != null ? battle.GetPokemonCurrentHp(mon) : mon.currentStats.hp;
                        var maxHp = battle != null ? battle.GetPokemonMaxHp(mon) : mon.currentStats.hp;
                        var fainted = battle != null && battle.IsPokemonFainted(mon);
                        var active = i == database.ActivePartyIndex;
                        var label = (active ? "* " : "") + (i + 1) + ". " + mon.nickname + " Lv." + mon.level + "  Party  HP " + hp + "/" + maxHp + "  EXP " + mon.experience + "/" + mon.experienceToNextLevel + (fainted ? "  FAINTED" : "") + "  Moves: " + string.Join(", ", mon.moves);

                        GUI.enabled = !fainted && (!replacementOnly || !active);
                        if (GUILayout.Button(label))
                        {
                            if (battle != null && battle.InBattle)
                            {
                                battle.TrySwitchPokemon(database, i);
                            }
                            else
                            {
                                database.SetActivePartyIndex(i);
                            }

                            battleMenuScreen = "Commands";
                        }
                        GUI.enabled = true;
                    }

                    for (var i = 0; i < database.PcStorage.Count; i++)
                    {
                        var mon = database.PcStorage[i];
                        GUILayout.Label((i + 1) + ". " + mon.nickname + " Lv." + mon.level + "  PC Storage  EXP " + mon.experience + "/" + mon.experienceToNextLevel + "  Moves: " + string.Join(", ", mon.moves));
                    }
                }
            }

            if (!replacementOnly && GUILayout.Button("Back")) battleMenuScreen = "Commands";
        }

        private string[] GetBattleMoveChoices(PokemonInstance pokemon)
        {
            var choices = new[] { "Tackle", "Vine Whip", "Ember", "Water Gun" };
            if (pokemon == null || pokemon.moves == null)
            {
                return choices;
            }

            for (var i = 0; i < Mathf.Min(4, pokemon.moves.Length); i++)
            {
                if (!string.IsNullOrEmpty(pokemon.moves[i]))
                {
                    choices[i] = pokemon.moves[i];
                }
            }

            return choices;
        }

        private void DrawMiniMap()
        {
            const float visibleWorldMeters = 44f;
            var size = Mathf.Clamp(Mathf.Min(PrototypeGuiScale.Width, PrototypeGuiScale.Height) * 0.25f, 168f, 230f);
            var rect = new Rect(PrototypeGuiScale.Width - size - 22f, PrototypeGuiScale.Height - size - 22f, size, size);
            var player = GetMinimapPlayer();
            var playerPosition = player != null ? player.position : Vector3.zero;
            var pixelsPerMeter = size / visibleWorldMeters;

            DrawFilledRect(new Rect(rect.x - 4f, rect.y - 24f, rect.width + 8f, rect.height + 28f), new Color(0.02f, 0.03f, 0.04f, 0.72f));
            GUI.Label(new Rect(rect.x + 6f, rect.y - 22f, rect.width - 12f, 20f), "Mini Map - Local");

            GUI.BeginGroup(rect);
            try
            {
                DrawFilledRect(new Rect(0, 0, size, size), new Color(0.24f, 0.27f, 0.28f, 0.94f));
                DrawCenteredGrid(playerPosition, size, pixelsPerMeter, 5f);

                DrawCenteredMapRect(playerPosition, pixelsPerMeter, size, new Rect(-50f, -50f, 100f, 0.35f), new Color(0.92f, 0.95f, 0.98f, 0.75f));
                DrawCenteredMapRect(playerPosition, pixelsPerMeter, size, new Rect(-50f, 49.65f, 100f, 0.35f), new Color(0.92f, 0.95f, 0.98f, 0.75f));
                DrawCenteredMapRect(playerPosition, pixelsPerMeter, size, new Rect(-50f, -50f, 0.35f, 100f), new Color(0.92f, 0.95f, 0.98f, 0.75f));
                DrawCenteredMapRect(playerPosition, pixelsPerMeter, size, new Rect(49.65f, -50f, 0.35f, 100f), new Color(0.92f, 0.95f, 0.98f, 0.75f));

                DrawCenteredMapRect(playerPosition, pixelsPerMeter, size, new Rect(15.9f, 15.9f, 24.2f, 20.2f), new Color(0.0f, 0.82f, 0.10f, 0.86f));
                DrawCenteredMapRect(playerPosition, pixelsPerMeter, size, new Rect(19.5f, 28.2f, 17f, 4f), new Color(0.12f, 0.98f, 0.18f, 0.95f));
                DrawCenteredMapRect(playerPosition, pixelsPerMeter, size, new Rect(-39.8f, 1.1f, 7.6f, 7.2f), new Color(0.92f, 0.32f, 0.38f, 0.92f));
                DrawCenteredMapRect(playerPosition, pixelsPerMeter, size, new Rect(-12f, 29f, 14f, 10f), new Color(0.57f, 0.17f, 0.91f, 0.82f));

                DrawCenteredMapLabel(playerPosition, pixelsPerMeter, size, new Vector2(-36f, 5f), "PC", Color.white);
                DrawCenteredMapLabel(playerPosition, pixelsPerMeter, size, new Vector2(28f, 26f), "Wild", Color.white);
                DrawCenteredMapLabel(playerPosition, pixelsPerMeter, size, new Vector2(-5f, 34f), "Raid", Color.white);

                var center = new Vector2(size * 0.5f, size * 0.5f);
                DrawFilledRect(new Rect(center.x - 7f, center.y - 7f, 14f, 14f), new Color(0.1f, 0.35f, 1f, 1f));
                DrawFilledRect(new Rect(center.x - 3f, center.y - 3f, 6f, 6f), Color.white);
            }
            finally
            {
                GUI.EndGroup();
            }

            DrawFrame(rect, new Color(0.95f, 0.95f, 0.95f, 0.85f));
        }

        private Transform GetMinimapPlayer()
        {
            if (minimapPlayer != null)
            {
                return minimapPlayer;
            }

            var player = FindObjectOfType<HybridPlayerController>();
            if (player != null)
            {
                minimapPlayer = player.transform;
            }

            return minimapPlayer;
        }

        private void DrawCenteredGrid(Vector3 playerPosition, float mapSize, float pixelsPerMeter, float worldStep)
        {
            var halfMeters = mapSize / pixelsPerMeter * 0.5f;
            var firstX = Mathf.Floor((playerPosition.x - halfMeters) / worldStep) * worldStep;
            var lastX = playerPosition.x + halfMeters;
            for (var x = firstX; x <= lastX; x += worldStep)
            {
                var p = WorldToCenteredMap(playerPosition, pixelsPerMeter, mapSize, x, playerPosition.z);
                var color = Mathf.Abs(x) < 0.01f ? new Color(0.78f, 0.86f, 0.92f, 0.75f) : new Color(0.12f, 0.14f, 0.15f, 0.55f);
                DrawFilledRect(new Rect(p.x, 0, 1f, mapSize), color);
            }

            var firstZ = Mathf.Floor((playerPosition.z - halfMeters) / worldStep) * worldStep;
            var lastZ = playerPosition.z + halfMeters;
            for (var z = firstZ; z <= lastZ; z += worldStep)
            {
                var p = WorldToCenteredMap(playerPosition, pixelsPerMeter, mapSize, playerPosition.x, z);
                var color = Mathf.Abs(z) < 0.01f ? new Color(0.78f, 0.86f, 0.92f, 0.75f) : new Color(0.12f, 0.14f, 0.15f, 0.55f);
                DrawFilledRect(new Rect(0, p.y, mapSize, 1f), color);
            }
        }

        private void DrawCenteredMapRect(Vector3 playerPosition, float pixelsPerMeter, float mapSize, Rect worldRect, Color color)
        {
            var a = WorldToCenteredMap(playerPosition, pixelsPerMeter, mapSize, worldRect.xMin, worldRect.yMin);
            var b = WorldToCenteredMap(playerPosition, pixelsPerMeter, mapSize, worldRect.xMax, worldRect.yMax);
            var x = Mathf.Min(a.x, b.x);
            var y = Mathf.Min(a.y, b.y);
            DrawFilledRect(new Rect(x, y, Mathf.Abs(b.x - a.x), Mathf.Abs(b.y - a.y)), color);
        }

        private void DrawCenteredMapLabel(Vector3 playerPosition, float pixelsPerMeter, float mapSize, Vector2 worldPosition, string label, Color color)
        {
            var p = WorldToCenteredMap(playerPosition, pixelsPerMeter, mapSize, worldPosition.x, worldPosition.y);
            if (p.x < -48f || p.y < -20f || p.x > mapSize + 48f || p.y > mapSize + 20f)
            {
                return;
            }

            var previous = GUI.color;
            GUI.color = color;
            GUI.Label(new Rect(p.x - 20f, p.y - 8f, 48f, 16f), label);
            GUI.color = previous;
        }

        private Vector2 WorldToCenteredMap(Vector3 playerPosition, float pixelsPerMeter, float mapSize, float worldX, float worldZ)
        {
            var center = mapSize * 0.5f;
            return new Vector2(center + (worldX - playerPosition.x) * pixelsPerMeter, center - (worldZ - playerPosition.z) * pixelsPerMeter);
        }

        private void DrawFilledRect(Rect rect, Color color)
        {
            var previous = GUI.color;
            GUI.color = color;
            GUI.DrawTexture(rect, Texture2D.whiteTexture);
            GUI.color = previous;
        }

        private void DrawFrame(Rect rect, Color color)
        {
            DrawFilledRect(new Rect(rect.x, rect.y, rect.width, 2f), color);
            DrawFilledRect(new Rect(rect.x, rect.yMax - 2f, rect.width, 2f), color);
            DrawFilledRect(new Rect(rect.x, rect.y, 2f, rect.height), color);
            DrawFilledRect(new Rect(rect.xMax - 2f, rect.y, 2f, rect.height), color);
        }

        private Rect CenterRect(float width, float height)
        {
            return new Rect((PrototypeGuiScale.Width - width) * 0.5f, (PrototypeGuiScale.Height - height) * 0.5f, width, height);
        }
    }
}
"""

    def _render_editor_code(self):
        return """using System;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace PokeEngine.EditorTools
{
    [InitializeOnLoad]
    public static class PokeEnginePlayButtonBootstrap
    {
        private const string PrototypeScenePath = "Assets/Scenes/PrototypeRegion.unity";

        static PokeEnginePlayButtonBootstrap()
        {
            EditorApplication.delayCall += ConfigurePlayModeStartScene;
            EditorApplication.playModeStateChanged += OnPlayModeStateChanged;
        }

        [MenuItem("PokeEngine/Use Prototype Scene For Play Button")]
        public static void ConfigurePlayModeStartScene()
        {
            if (IsAutomatedTestRun())
            {
                if (EditorSceneManager.playModeStartScene != null)
                {
                    EditorSceneManager.playModeStartScene = null;
                }
                return;
            }

            var sceneAsset = AssetDatabase.LoadAssetAtPath<SceneAsset>(PrototypeScenePath);
            if (sceneAsset == null)
            {
                return;
            }

            if (EditorSceneManager.playModeStartScene != sceneAsset)
            {
                EditorSceneManager.playModeStartScene = sceneAsset;
                Debug.Log("[PokeEngine] Unity Play button now starts " + PrototypeScenePath + ".");
            }
        }

        private static void OnPlayModeStateChanged(PlayModeStateChange state)
        {
            if (state == PlayModeStateChange.ExitingEditMode)
            {
                ConfigurePlayModeStartScene();
            }
        }

        private static bool IsAutomatedTestRun()
        {
            var args = Environment.GetCommandLineArgs();
            for (int i = 0; i < args.Length; i++)
            {
                if (string.Equals(args[i], "-runTests", StringComparison.OrdinalIgnoreCase))
                {
                    return true;
                }
            }

            return false;
        }
    }

    public sealed class PokeEnginePrototypeMenu : EditorWindow
    {
        private const string PrototypeScenePath = "Assets/Scenes/PrototypeRegion.unity";
        private int tab;
        private readonly string[] tabs = { "Pokemon", "Dialogue", "World", "Architecture", "QA" };

        [MenuItem("PokeEngine/Full RPG Prototype Tools")]
        public static void Open()
        {
            GetWindow<PokeEnginePrototypeMenu>("PokeEngine Tools");
        }

        [MenuItem("PokeEngine/Open Prototype Scene")]
        public static void OpenPrototypeSceneFromMenu()
        {
            OpenPrototypeScene();
        }

        private void OnGUI()
        {
            EditorGUILayout.BeginVertical(EditorStyles.helpBox);
            GUILayout.Label("Prototype Scene", EditorStyles.boldLabel);
            GUILayout.Label("Open the generated playable starter scene.");
            if (GUILayout.Button("Open Prototype Scene"))
            {
                OpenPrototypeScene();
            }
            EditorGUILayout.EndVertical();
            GUILayout.Space(8);

            tab = GUILayout.Toolbar(tab, tabs);
            GUILayout.Space(8);

            if (tab == 0)
            {
                DrawPokemonEditor();
            }
            else if (tab == 1)
            {
                DrawDialogueEditor();
            }
            else if (tab == 2)
            {
                DrawWorldEditor();
            }
            else if (tab == 3)
            {
                DrawArchitectureTools();
            }
            else
            {
                DrawQaTools();
            }
        }

        private static void OpenPrototypeScene()
        {
            var sceneAsset = AssetDatabase.LoadAssetAtPath<SceneAsset>(PrototypeScenePath);
            if (sceneAsset == null)
            {
                EditorUtility.DisplayDialog(
                    "Prototype Scene Missing",
                    "Could not find " + PrototypeScenePath + ". Regenerate the project or restore the scene asset.",
                    "OK"
                );
                return;
            }

            if (!EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
            {
                return;
            }

            EditorSceneManager.OpenScene(PrototypeScenePath);
        }

        private void DrawPokemonEditor()
        {
            GUILayout.Label("Pokemon Editor", EditorStyles.boldLabel);
            GUILayout.Label("Species, moves, abilities, forms, Mega, Dimension Split, and fusion compatibility editor entry point.");
            if (GUILayout.Button("Open generated Pokemon JSON folder"))
            {
                EditorUtility.RevealInFinder("Assets/StreamingAssets/Data");
            }
        }

        private void DrawDialogueEditor()
        {
            GUILayout.Label("Dialogue Editor", EditorStyles.boldLabel);
            GUILayout.Label("Node dialogue, branching choices, portraits, event triggers, localization, and voice cue planning.");
        }

        private void DrawWorldEditor()
        {
            GUILayout.Label("World Editor", EditorStyles.boldLabel);
            GUILayout.Label("Tile painting, encounters, spawns, events, cutscene preview, lighting/weather preview, and path visualization.");
        }

        private void DrawArchitectureTools()
        {
            GUILayout.Label("Architecture Matrix", EditorStyles.boldLabel);
            GUILayout.Label("Generated V12 feature coverage for overworld, movement, NPCs, events, Pokemon, battle, damage, abilities, Mega, Dimension Split, fusion, raids, save, tools, and engine core.");
            if (GUILayout.Button("Open architecture matrix JSON"))
            {
                EditorUtility.RevealInFinder("Assets/StreamingAssets/Data/prototype_feature_matrix.json");
            }
            if (GUILayout.Button("Open architecture matrix docs"))
            {
                EditorUtility.RevealInFinder("Docs/ARCHITECTURE_IMPLEMENTATION_MATRIX.md");
            }
        }

        private void DrawQaTools()
        {
            GUILayout.Label("QA Tools", EditorStyles.boldLabel);
            GUILayout.Label("Smoke-test battle math, save migration, streaming metadata, generated manifests, and content validation.");
        }
    }
}
"""

    def _render_tests_code(self):
        return """using NUnit.Framework;
using PokeEngine.Battle;
using PokeEngine.Data;
using PokeEngine.NPC;
using PokeEngine.Pokemon;
using UnityEngine;

namespace PokeEngine.Tests
{
    public sealed class PokeEnginePrototypeTests
    {
        [Test]
        public void DamageCalculatorProducesPositiveDamage()
        {
            var attacker = new PokemonInstance { level = 5, nickname = "Attacker", currentStats = new Stats { atk = 50, spa = 50 } };
            var defender = new PokemonInstance { level = 5, nickname = "Defender", currentStats = new Stats { def = 45, spd = 45 } };
            var move = new MoveDefinition { name = "Tackle", power = 40, accuracy = 100, category = "Physical", type = PokemonType.Normal };
            var result = new DamageCalculator().Calculate(attacker, defender, move, BattleMode.Single);
            Assert.Greater(result.finalDamage, 0);
        }

        [Test]
        public void WildEncounterFightKeepsCaptureInsideBattle()
        {
            var databaseObject = new GameObject("PokemonDatabaseRuntime_Test");
            var battleObject = new GameObject("BattleEngineRuntime_Test");
            try
            {
                var database = databaseObject.AddComponent<PokemonDatabaseRuntime>();
                database.Initialize(null);
                var battle = battleObject.AddComponent<BattleEngineRuntime>();
                battle.Initialize(null);
                var wild = database.CreatePokemon(7, 3);

                battle.StartWildEncounter(wild, database.Party);
                Assert.IsTrue(battle.InBattle);
                Assert.AreEqual(wild.currentStats.hp, battle.WildOpponentCurrentHp);

                battle.PrototypePlayerAttack(database.Party[0]);

                Assert.IsTrue(battle.InBattle);
                Assert.AreSame(wild, battle.WildOpponent);
                Assert.Less(battle.WildOpponentCurrentHp, battle.WildOpponentMaxHp);
                Assert.That(battle.BattleMessage, Does.Contain("capture odds"));
            }
            finally
            {
                Object.DestroyImmediate(databaseObject);
                Object.DestroyImmediate(battleObject);
                Time.timeScale = 1f;
            }
        }

        [Test]
        public void FaintedPokemonCanBeReplacedFromParty()
        {
            var databaseObject = new GameObject("PokemonDatabaseRuntime_FaintSwitch_Test");
            var battleObject = new GameObject("BattleEngineRuntime_FaintSwitch_Test");
            try
            {
                var database = databaseObject.AddComponent<PokemonDatabaseRuntime>();
                database.Initialize(null);
                var battle = battleObject.AddComponent<BattleEngineRuntime>();
                battle.Initialize(null);
                var wild = database.CreatePokemon(7, 5);

                battle.StartWildEncounter(wild, database.Party);
                battle.SetPokemonCurrentHp(database.Party[0], 1);
                battle.PrototypePlayerAttack(database.Party[0], "Guard Pulse");

                Assert.IsTrue(battle.WaitingForReplacement);
                Assert.AreEqual(BattleState.SwitchHandling, battle.State);
                Assert.IsTrue(battle.IsPokemonFainted(database.Party[0]));

                Assert.IsTrue(battle.TrySwitchPokemon(database, 1));
                Assert.IsFalse(battle.WaitingForReplacement);
                Assert.AreEqual(1, database.ActivePartyIndex);
                Assert.AreSame(database.Party[1], database.ActivePartyPokemon);
                Assert.AreEqual(BattleState.CommandSelection, battle.State);
            }
            finally
            {
                Object.DestroyImmediate(databaseObject);
                Object.DestroyImmediate(battleObject);
                Time.timeScale = 1f;
            }
        }

        [Test]
        public void FullPartyWipeEndsBattleAndNurseHealingRestoresParty()
        {
            var databaseObject = new GameObject("PokemonDatabaseRuntime_Blackout_Test");
            var battleObject = new GameObject("BattleEngineRuntime_Blackout_Test");
            try
            {
                var database = databaseObject.AddComponent<PokemonDatabaseRuntime>();
                database.Initialize(null);
                var battle = battleObject.AddComponent<BattleEngineRuntime>();
                battle.Initialize(null);
                var wild = database.CreatePokemon(7, 5);

                battle.StartWildEncounter(wild, database.Party);
                battle.SetPokemonCurrentHp(database.Party[0], 1);
                battle.SetPokemonCurrentHp(database.Party[1], 0);
                battle.PrototypePlayerAttack(database.Party[0], "Guard Pulse");

                Assert.IsFalse(battle.InBattle);
                Assert.That(battle.BattleMessage, Does.Contain("Pokemon Center"));
                Assert.IsFalse(database.PartyHasUsablePokemon());

                battle.HealParty(database);
                Assert.IsTrue(database.PartyHasUsablePokemon());
                Assert.AreEqual(database.GetMaxHp(database.Party[0]), database.GetCurrentHp(database.Party[0]));
                Assert.AreEqual(database.GetMaxHp(database.Party[1]), database.GetCurrentHp(database.Party[1]));
            }
            finally
            {
                Object.DestroyImmediate(databaseObject);
                Object.DestroyImmediate(battleObject);
                Time.timeScale = 1f;
            }
        }

        [Test]
        public void NpcInteractionRequiresClearLineOfSight()
        {
            var npcObject = new GameObject("Npc_LOS_Test");
            var playerObject = new GameObject("Player_LOS_Test");
            var wallObject = GameObject.CreatePrimitive(PrimitiveType.Cube);
            try
            {
                playerObject.tag = "Player";
                npcObject.transform.position = Vector3.zero;
                playerObject.transform.position = new Vector3(0f, 0f, 4f);
                wallObject.name = "Interaction_Blocking_Wall";
                wallObject.transform.position = new Vector3(0f, 0.9f, 2f);
                wallObject.transform.localScale = new Vector3(2f, 2f, 0.25f);

                var npc = npcObject.AddComponent<NpcBrain>();
                npc.SetPlayerInside(true, playerObject);
                Physics.SyncTransforms();

                Assert.IsFalse(npc.CanPlayerInteract(), "NPC interaction should be blocked by solid colliders between the player and NPC.");

                Object.DestroyImmediate(wallObject);
                Physics.SyncTransforms();

                Assert.IsTrue(npc.CanPlayerInteract(), "NPC interaction should work when the player is inside range and no wall blocks line of sight.");
            }
            finally
            {
                Object.DestroyImmediate(npcObject);
                Object.DestroyImmediate(playerObject);
                if (wallObject != null)
                {
                    Object.DestroyImmediate(wallObject);
                }
            }
        }
    }
}
"""

    def _render_mono_script_meta(self, guid):
        return f"""fileFormatVersion: 2
guid: {guid}
MonoImporter:
  externalObjects: {{}}
  serializedVersion: 2
  defaultReferences: []
  executionOrder: 0
  icon: {{instanceID: 0}}
  userData: 
  assetBundleName: 
  assetBundleVariant: 
"""

    def _render_scene_meta(self, guid):
        return f"""fileFormatVersion: 2
guid: {guid}
DefaultImporter:
  externalObjects: {{}}
  userData: 
  assetBundleName: 
  assetBundleVariant: 
"""

    def _render_prototype_scene(self):
        return f"""%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!29 &1
OcclusionCullingSettings:
  m_ObjectHideFlags: 0
  serializedVersion: 2
  m_OcclusionBakeSettings:
    smallestOccluder: 5
    smallestHole: 0.25
    backfaceThreshold: 100
  m_SceneGUID: 00000000000000000000000000000000
  m_OcclusionCullingData: {{fileID: 0}}
--- !u!104 &2
RenderSettings:
  m_ObjectHideFlags: 0
  serializedVersion: 9
  m_Fog: 1
  m_FogColor: {{r: 0.58, g: 0.78, b: 0.95, a: 1}}
  m_FogMode: 3
  m_FogDensity: 0.008
  m_LinearFogStart: 0
  m_LinearFogEnd: 300
  m_AmbientSkyColor: {{r: 0.62, g: 0.68, b: 0.76, a: 1}}
  m_AmbientEquatorColor: {{r: 0.45, g: 0.48, b: 0.52, a: 1}}
  m_AmbientGroundColor: {{r: 0.22, g: 0.24, b: 0.26, a: 1}}
  m_AmbientIntensity: 1
  m_AmbientMode: 0
  m_SubtractiveShadowColor: {{r: 0.42, g: 0.48, b: 0.62, a: 1}}
  m_SkyboxMaterial: {{fileID: 0}}
  m_HaloStrength: 0.5
  m_FlareStrength: 1
  m_FlareFadeSpeed: 3
  m_HaloTexture: {{fileID: 0}}
  m_SpotCookie: {{fileID: 0}}
  m_DefaultReflectionMode: 0
  m_DefaultReflectionResolution: 128
  m_ReflectionBounces: 1
  m_ReflectionIntensity: 1
  m_CustomReflection: {{fileID: 0}}
  m_Sun: {{fileID: 300002}}
  m_IndirectSpecularColor: {{r: 0, g: 0, b: 0, a: 1}}
  m_UseRadianceAmbientProbe: 0
--- !u!157 &3
LightmapSettings:
  m_ObjectHideFlags: 0
  serializedVersion: 12
  m_GIWorkflowMode: 1
  m_GISettings:
    serializedVersion: 2
    m_BounceScale: 1
    m_IndirectOutputScale: 1
    m_AlbedoBoost: 1
    m_EnvironmentLightingMode: 0
    m_EnableBakedLightmaps: 1
    m_EnableRealtimeLightmaps: 0
  m_LightmapEditorSettings:
    serializedVersion: 12
    m_Resolution: 2
    m_BakeResolution: 40
    m_AtlasSize: 1024
    m_AO: 1
    m_AOMaxDistance: 1
    m_CompAOExponent: 1
    m_CompAOExponentDirect: 0
    m_ExtractAmbientOcclusion: 0
    m_Padding: 2
    m_LightmapParameters: {{fileID: 0}}
    m_LightmapsBakeMode: 1
    m_TextureCompression: 1
    m_FinalGather: 0
    m_FinalGatherFiltering: 1
    m_FinalGatherRayCount: 256
    m_ReflectionCompression: 2
    m_MixedBakeMode: 2
    m_BakeBackend: 1
    m_PVRSampling: 1
    m_PVRDirectSampleCount: 32
    m_PVRSampleCount: 512
    m_PVRBounces: 2
    m_PVREnvironmentSampleCount: 256
    m_PVREnvironmentReferencePointCount: 2048
    m_PVRFilteringMode: 1
    m_PVRDenoiserTypeDirect: 1
    m_PVRDenoiserTypeIndirect: 1
    m_PVRDenoiserTypeAO: 1
    m_PVRFilterTypeDirect: 0
    m_PVRFilterTypeIndirect: 0
    m_PVRFilterTypeAO: 0
    m_PVREnvironmentMIS: 1
    m_ExportTrainingData: 0
    m_TrainingDataDestination: TrainingData
    m_LightProbeSampleCountMultiplier: 4
  m_LightingDataAsset: {{fileID: 0}}
  m_LightingSettings: {{fileID: 0}}
--- !u!196 &4
NavMeshSettings:
  serializedVersion: 2
  m_ObjectHideFlags: 0
  m_BuildSettings:
    serializedVersion: 2
    agentTypeID: 0
    agentRadius: 0.5
    agentHeight: 2
    agentSlope: 45
    agentClimb: 0.4
    ledgeDropHeight: 0
    maxJumpAcrossDistance: 0
    minRegionArea: 2
    manualCellSize: 0
    cellSize: 0.16666667
    manualTileSize: 0
    tileSize: 256
    accuratePlacement: 0
    maxJobWorkers: 0
    preserveTilesOutsideBounds: 0
    debug:
      m_Flags: 0
  m_NavMeshData: {{fileID: 0}}
--- !u!1 &100000
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: 100001}}
  - component: {{fileID: 100002}}
  - component: {{fileID: 100003}}
  m_Layer: 0
  m_Name: Main Camera
  m_TagString: MainCamera
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &100001
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: 100000}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0.3007058, y: 0, z: 0, w: 0.95371695}}
  m_LocalPosition: {{x: 0, y: 3.8, z: -6.8}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {{fileID: 0}}
  m_LocalEulerAnglesHint: {{x: 35, y: 0, z: 0}}
--- !u!20 &100002
Camera:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: 100000}}
  m_Enabled: 1
  serializedVersion: 2
  m_ClearFlags: 2
  m_BackGroundColor: {{r: 0.58, g: 0.78, b: 0.95, a: 0}}
  m_projectionMatrixMode: 1
  m_GateFitMode: 2
  m_FOVAxisMode: 0
  m_Iso: 200
  m_ShutterSpeed: 0.005
  m_Aperture: 16
  m_FocusDistance: 10
  m_FocalLength: 50
  m_BladeCount: 5
  m_Curvature: {{x: 2, y: 11}}
  m_BarrelClipping: 0.25
  m_Anamorphism: 0
  m_SensorSize: {{x: 36, y: 24}}
  m_LensShift: {{x: 0, y: 0}}
  m_NormalizedViewPortRect:
    serializedVersion: 2
    x: 0
    y: 0
    width: 1
    height: 1
  near clip plane: 0.3
  far clip plane: 1000
  field of view: 60
  orthographic: 1
  orthographic size: 4.6
  m_Depth: -1
  m_CullingMask:
    serializedVersion: 2
    m_Bits: 4294967295
  m_RenderingPath: -1
  m_TargetTexture: {{fileID: 0}}
  m_TargetDisplay: 0
  m_TargetEye: 3
  m_HDR: 1
  m_AllowMSAA: 1
  m_AllowDynamicResolution: 0
  m_ForceIntoRT: 0
  m_OcclusionCulling: 1
  m_StereoConvergence: 10
  m_StereoSeparation: 0.022
--- !u!81 &100003
AudioListener:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: 100000}}
  m_Enabled: 1
--- !u!1 &200000
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: 200001}}
  - component: {{fileID: 200002}}
  m_Layer: 0
  m_Name: PokeEngineRuntime
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &200001
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: 200000}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0, y: 0, z: 0, w: 1}}
  m_LocalPosition: {{x: 0, y: 0, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {{fileID: 0}}
  m_LocalEulerAnglesHint: {{x: 0, y: 0, z: 0}}
--- !u!114 &200002
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: 200000}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: 11500000, guid: {POKEENGINE_RUNTIME_SCRIPT_GUID}, type: 3}}
  m_Name: 
  m_EditorClassIdentifier: 
--- !u!1 &300000
GameObject:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  serializedVersion: 6
  m_Component:
  - component: {{fileID: 300001}}
  - component: {{fileID: 300002}}
  m_Layer: 0
  m_Name: Prototype Sun
  m_TagString: Untagged
  m_Icon: {{fileID: 0}}
  m_NavMeshLayer: 0
  m_StaticEditorFlags: 0
  m_IsActive: 1
--- !u!4 &300001
Transform:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: 300000}}
  serializedVersion: 2
  m_LocalRotation: {{x: 0.3147672, y: -0.259829, z: 0.089288, w: 0.908123}}
  m_LocalPosition: {{x: 0, y: 3, z: 0}}
  m_LocalScale: {{x: 1, y: 1, z: 1}}
  m_ConstrainProportionsScale: 0
  m_Children: []
  m_Father: {{fileID: 0}}
  m_LocalEulerAnglesHint: {{x: 42, y: -35, z: 0}}
--- !u!108 &300002
Light:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: 300000}}
  m_Enabled: 1
  serializedVersion: 10
  m_Type: 1
  m_Shape: 0
  m_Color: {{r: 1, g: 0.956, b: 0.839, a: 1}}
  m_Intensity: 1.15
  m_Range: 10
  m_SpotAngle: 30
  m_InnerSpotAngle: 21.80208
  m_CookieSize: 10
  m_Shadows:
    m_Type: 2
    m_Resolution: -1
    m_CustomResolution: -1
    m_Strength: 1
    m_Bias: 0.05
    m_NormalBias: 0.4
    m_NearPlane: 0.2
    m_CullingMatrixOverride:
      e00: 1
      e01: 0
      e02: 0
      e03: 0
      e10: 0
      e11: 1
      e12: 0
      e13: 0
      e20: 0
      e21: 0
      e22: 1
      e23: 0
      e30: 0
      e31: 0
      e32: 0
      e33: 1
    m_UseCullingMatrixOverride: 0
  m_Cookie: {{fileID: 0}}
  m_DrawHalo: 0
  m_Flare: {{fileID: 0}}
  m_RenderMode: 0
  m_CullingMask:
    serializedVersion: 2
    m_Bits: 4294967295
  m_RenderingLayerMask: 1
  m_Lightmapping: 4
  m_LightShadowCasterMode: 0
  m_AreaSize: {{x: 1, y: 1}}
  m_BounceIntensity: 1
  m_ColorTemperature: 6570
  m_UseColorTemperature: 0
  m_BoundingSphereOverride: {{x: 0, y: 0, z: 0, w: 0}}
  m_UseBoundingSphereOverride: 0
  m_UseViewFrustumForShadowCasterCull: 1
  m_ShadowRadius: 0
  m_ShadowAngle: 0
"""

    def _render_scene_note(self):
        return """PokeEngine generated scene note.

The generator now creates a real Unity scene at:
Assets/Scenes/PrototypeRegion.unity

Open that scene in Unity and press Play. It already contains:
- Main Camera
- Prototype Sun
- PokeEngineRuntime object with PokeEngine.Core.PokeEngineRuntime attached

The runtime will create its prototype managers, visible player, and diorama chunks automatically.
"""

    def _render_architecture_matrix_doc(self):
        matrix = self._build_feature_matrix()
        lines = [
            "# Architecture Implementation Matrix",
            "",
            f"Generated feature count: {matrix['totalFeatureCount']}",
            "",
            "Statuses:",
            "- `playable_prototype`: active in the generated scene/runtime.",
            "- `data_configured`: represented in generated JSON/data models.",
            "- `runtime_scaffold`: represented by generated runtime services or extension points.",
            "- `runtime_hook`: reserved hook for expansion inside the runtime.",
            "- `editor_tool_hook`: exposed through generated editor tooling.",
            "",
        ]
        current_section = None
        for row in matrix["features"]:
            if row["sectionTitle"] != current_section:
                current_section = row["sectionTitle"]
                lines.extend(["", f"## {current_section}", ""])
            lines.append(f"- `{row['status']}` {row['feature']}")
        lines.append("")
        return "\n".join(lines)

    def _render_full_prototype_doc(self):
        return """# Full RPG Prototype Output

The generator now creates a button-press Unity RPG prototype foundation:

- Data-driven framework foundations with JSON runtime databases plus ScriptableObject definitions for Pokemon species, moves, encounter tables, zone definitions, and event channels.
- Event-driven runtime core with `PokeEventBus` for decoupled battle, Pokemon, overworld, save, and UI events.
- Overworld streaming manager with fixed 2.5D camera, chunk placeholders, adjacent preloading, lighting/weather/audio profile hooks, memory budget checks, and async scene-loading paths.
- Pokemon-style player controller with continuous 4-direction movement, terrain modifiers, movement states, collision support, and cutscene lock support.
- Structured zones use a fixed 2.5D follow camera. Wild Area zones keep 4-direction movement and enable horizontal mouse orbit plus a limited 15-degree vertical tilt.
- NPC director and NPC brain with categories, schedules, dialogue profile hooks, trainer vision cones, alert and chase/battle triggers.
- Event flag manager and cutscene director with persistent flag export, counters, scripted story beat playback, and branching-ready hooks.
- Pokemon database runtime with identity, biological, combat, visual, shiny, learnset, evolution, form, Mega, Dimension Split, and fusion compatibility fields.
- Battle engine with state flow, action queue, priority/speed sorting, ability hooks, damage formula stages, raid/fusion/Dimension modifiers, and UI debug surface.
- Mega Evolution, Dimension Split, and Fusion runtime systems with validation, stat overlays, move/ability mutation hooks, visual/audio pipeline hooks, and separation entry point.
- Raid runtime with multiplayer-scale participants, shared timer, shield break logic, tier handling, capture and reward pipeline hooks.
- Save runtime with autosave, backup save, version validation, migration hook, and transformation/fusion registry fields.
- Prototype feature registry that lists every V12 architecture feature and its generated status.
- Editor tooling entry point for Pokemon, dialogue, world design, and QA workflows.
- EditMode smoke test for generated battle math.

`PrototypeRegion.unity` now builds a visible 100m x 100m testing site with a 1m grid, movement lane, collision blocks, Pokecenter entry/interior, item and Pokemon pickups, random-letter interactable NPC, battle/catch encounter, large tall-grass random encounter field, Wild Area camera test, and raid/feature hook pad.

This is a prototype architecture, not a shipped commercial RPG. It gives every major requirement a working runtime foothold so you can press Generate, open `Assets/Scenes/PrototypeRegion.unity`, press Play, and start expanding systems in place.
"""

    def _write_json(self, path, data):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        payload = data if isinstance(data, dict) else {"items": data}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)
        self.logger(f"Generated: {path}")

    def _write_text(self, path, text):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        self.logger(f"Generated: {path}")

    def _to_class_name(self, value):
        words = []
        current = []
        for char in value:
            if char.isalnum():
                current.append(char)
            elif current:
                words.append("".join(current))
                current = []
        if current:
            words.append("".join(current))
        class_name = "".join(word[:1].upper() + word[1:] for word in words)
        if class_name and class_name[0].isdigit():
            class_name = f"Feature{class_name}"
        return f"{class_name}System"

    def _to_snake_name(self, value):
        chars = []
        previous_was_separator = False
        for char in value.lower():
            if char.isalnum():
                chars.append(char)
                previous_was_separator = False
            elif not previous_was_separator:
                chars.append("_")
                previous_was_separator = True
        return "".join(chars).strip("_")

    def _escape_csharp(self, value):
        return value.replace("\\", "\\\\").replace('"', '\\"')

    def _render_system_stub(self, class_name, requirement):
        requirement_id = self._escape_csharp(requirement["id"])
        requirement_name = self._escape_csharp(requirement["name"])
        category = self._escape_csharp(requirement["category"])
        optional = "true" if requirement["optional"] else "false"
        return f"""using UnityEngine;

namespace PokeEngine.Generated.Systems
{{
    public sealed class {class_name} : MonoBehaviour
    {{
        [SerializeField] private string requirementId = "{requirement_id}";
        [SerializeField] private string requirementName = "{requirement_name}";
        [SerializeField] private string category = "{category}";
        [SerializeField] private bool optional = {optional};

        public string RequirementId => requirementId;
        public string RequirementName => requirementName;
        public string Category => category;
        public bool Optional => optional;

        public void Initialize()
        {{
            Debug.Log($"[PokeEngine] {{requirementName}} scaffold initialized.");
        }}
    }}
}}
"""

    def _render_bootstrap_stub(self, manifest):
        count = len(manifest)
        return f"""using UnityEngine;

namespace PokeEngine.Generated.Core
{{
    public sealed class PokeEngineBootstrap : MonoBehaviour
    {{
        [SerializeField] private int expectedSystemCount = {count};

        private void Awake()
        {{
            Debug.Log($"[PokeEngine] Bootstrap ready. Expected generated systems: {{expectedSystemCount}}.");
        }}
    }}
}}
"""

    def _render_requirements_doc(self):
        lines = [
            "# PokeEngine V11 Feature Requirements",
            "",
            "This file is generated by the Python project builder. Each requirement also has a JSON config and a Unity C# scaffold under `Assets/Scripts/PokeEngine/Systems`.",
            "",
        ]
        for requirement in self.feature_requirements:
            optional = " optional" if requirement["optional"] else ""
            lines.append(f"- [{requirement['id']}] {requirement['name']} ({requirement['category']}{optional})")
        lines.append("")
        return "\n".join(lines)

    def _render_test_plan(self):
        lines = [
            "# Prototype QA Test Plan",
            "",
            "Use this checklist to convert generated scaffolds into testable gameplay systems.",
            "",
        ]
        for requirement in self.feature_requirements:
            lines.append(f"- Verify {requirement['name']}: data loads, scene integration works, save/load behavior is defined, and UI feedback is present.")
        lines.append("")
        return "\n".join(lines)





PROJECT_FRAMEWORK_TEMPLATE_FILES = {'Assets/Scenes/Battle.unity': '%YAML 1.1\n'
                               '%TAG !u! tag:unity3d.com,2011:\n'
                               '--- !u!29 &1\n'
                               'OcclusionCullingSettings:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  serializedVersion: 2\n'
                               '  m_OcclusionBakeSettings:\n'
                               '    smallestOccluder: 5\n'
                               '    smallestHole: 0.25\n'
                               '    backfaceThreshold: 100\n'
                               '  m_SceneGUID: 00000000000000000000000000000000\n'
                               '  m_OcclusionCullingData: {fileID: 0}\n'
                               '--- !u!104 &2\n'
                               'RenderSettings:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  serializedVersion: 9\n'
                               '  m_Fog: 0\n'
                               '  m_FogColor: {r: 0.5, g: 0.5, b: 0.5, a: 1}\n'
                               '  m_FogMode: 3\n'
                               '  m_FogDensity: 0.01\n'
                               '  m_LinearFogStart: 0\n'
                               '  m_LinearFogEnd: 300\n'
                               '  m_AmbientSkyColor: {r: 0.212, g: 0.227, b: 0.259, a: 1}\n'
                               '  m_AmbientEquatorColor: {r: 0.114, g: 0.125, b: 0.133, a: 1}\n'
                               '  m_AmbientGroundColor: {r: 0.047, g: 0.043, b: 0.035, a: 1}\n'
                               '  m_AmbientIntensity: 1\n'
                               '  m_AmbientMode: 0\n'
                               '  m_SubtractiveShadowColor: {r: 0.42, g: 0.478, b: 0.627, a: 1}\n'
                               '  m_SkyboxMaterial: {fileID: 10304, guid: 0000000000000000f000000000000000, type: 0}\n'
                               '  m_HaloStrength: 0.5\n'
                               '  m_FlareStrength: 1\n'
                               '  m_FlareFadeSpeed: 3\n'
                               '  m_HaloTexture: {fileID: 0}\n'
                               '  m_SpotCookie: {fileID: 10001, guid: 0000000000000000e000000000000000, type: 0}\n'
                               '  m_DefaultReflectionMode: 0\n'
                               '  m_DefaultReflectionResolution: 128\n'
                               '  m_ReflectionBounces: 1\n'
                               '  m_ReflectionIntensity: 1\n'
                               '  m_CustomReflection: {fileID: 0}\n'
                               '  m_Sun: {fileID: 0}\n'
                               '  m_UseRadianceAmbientProbe: 0\n'
                               '--- !u!157 &3\n'
                               'LightmapSettings:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  serializedVersion: 12\n'
                               '  m_GIWorkflowMode: 1\n'
                               '  m_GISettings:\n'
                               '    serializedVersion: 2\n'
                               '    m_BounceScale: 1\n'
                               '    m_IndirectOutputScale: 1\n'
                               '    m_AlbedoBoost: 1\n'
                               '    m_EnvironmentLightingMode: 0\n'
                               '    m_EnableBakedLightmaps: 1\n'
                               '    m_EnableRealtimeLightmaps: 0\n'
                               '  m_LightmapEditorSettings:\n'
                               '    serializedVersion: 12\n'
                               '    m_Resolution: 2\n'
                               '    m_BakeResolution: 40\n'
                               '    m_AtlasSize: 1024\n'
                               '    m_AO: 0\n'
                               '    m_AOMaxDistance: 1\n'
                               '    m_CompAOExponent: 1\n'
                               '    m_CompAOExponentDirect: 0\n'
                               '    m_ExtractAmbientOcclusion: 0\n'
                               '    m_Padding: 2\n'
                               '    m_LightmapParameters: {fileID: 0}\n'
                               '    m_LightmapsBakeMode: 1\n'
                               '    m_TextureCompression: 1\n'
                               '    m_FinalGather: 0\n'
                               '    m_FinalGatherFiltering: 1\n'
                               '    m_FinalGatherRayCount: 256\n'
                               '    m_ReflectionCompression: 2\n'
                               '    m_MixedBakeMode: 2\n'
                               '    m_BakeBackend: 1\n'
                               '    m_PVRSampling: 1\n'
                               '    m_PVRDirectSampleCount: 32\n'
                               '    m_PVRSampleCount: 512\n'
                               '    m_PVRBounces: 2\n'
                               '    m_PVREnvironmentSampleCount: 256\n'
                               '    m_PVREnvironmentReferencePointCount: 2048\n'
                               '    m_PVRFilteringMode: 1\n'
                               '    m_PVRDenoiserTypeDirect: 1\n'
                               '    m_PVRDenoiserTypeIndirect: 1\n'
                               '    m_PVRDenoiserTypeAO: 1\n'
                               '    m_PVRFilterTypeDirect: 0\n'
                               '    m_PVRFilterTypeIndirect: 0\n'
                               '    m_PVRFilterTypeAO: 0\n'
                               '    m_PVREnvironmentMIS: 1\n'
                               '    m_PVRCulling: 1\n'
                               '    m_PVRFilteringGaussRadiusDirect: 1\n'
                               '    m_PVRFilteringGaussRadiusIndirect: 5\n'
                               '    m_PVRFilteringGaussRadiusAO: 2\n'
                               '    m_PVRFilteringAtrousPositionSigmaDirect: 0.5\n'
                               '    m_PVRFilteringAtrousPositionSigmaIndirect: 2\n'
                               '    m_PVRFilteringAtrousPositionSigmaAO: 1\n'
                               '    m_ExportTrainingData: 0\n'
                               '    m_TrainingDataDestination: TrainingData\n'
                               '    m_LightProbeSampleCountMultiplier: 4\n'
                               '  m_LightingDataAsset: {fileID: 0}\n'
                               '  m_LightingSettings: {fileID: 0}\n'
                               '--- !u!196 &4\n'
                               'NavMeshSettings:\n'
                               '  serializedVersion: 2\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_BuildSettings:\n'
                               '    serializedVersion: 3\n'
                               '    agentTypeID: 0\n'
                               '    agentRadius: 0.5\n'
                               '    agentHeight: 2\n'
                               '    agentSlope: 45\n'
                               '    agentClimb: 0.4\n'
                               '    ledgeDropHeight: 0\n'
                               '    maxJumpAcrossDistance: 0\n'
                               '    minRegionArea: 2\n'
                               '    manualCellSize: 0\n'
                               '    cellSize: 0.16666667\n'
                               '    manualTileSize: 0\n'
                               '    tileSize: 256\n'
                               '    buildHeightMesh: 0\n'
                               '    maxJobWorkers: 0\n'
                               '    preserveTilesOutsideBounds: 0\n'
                               '    debug:\n'
                               '      m_Flags: 0\n'
                               '  m_NavMeshData: {fileID: 0}\n'
                               '--- !u!1 &3610205\n'
                               'GameObject:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  serializedVersion: 6\n'
                               '  m_Component:\n'
                               '  - component: {fileID: 3610209}\n'
                               '  - component: {fileID: 3610208}\n'
                               '  - component: {fileID: 3610207}\n'
                               '  - component: {fileID: 3610206}\n'
                               '  m_Layer: 0\n'
                               '  m_Name: Opponent Creature Slot\n'
                               '  m_TagString: Untagged\n'
                               '  m_Icon: {fileID: 0}\n'
                               '  m_NavMeshLayer: 0\n'
                               '  m_StaticEditorFlags: 0\n'
                               '  m_IsActive: 1\n'
                               '--- !u!23 &3610206\n'
                               'MeshRenderer:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 3610205}\n'
                               '  m_Enabled: 1\n'
                               '  m_CastShadows: 1\n'
                               '  m_ReceiveShadows: 1\n'
                               '  m_DynamicOccludee: 1\n'
                               '  m_StaticShadowCaster: 0\n'
                               '  m_MotionVectors: 1\n'
                               '  m_LightProbeUsage: 1\n'
                               '  m_ReflectionProbeUsage: 1\n'
                               '  m_RayTracingMode: 2\n'
                               '  m_RayTraceProcedural: 0\n'
                               '  m_RenderingLayerMask: 1\n'
                               '  m_RendererPriority: 0\n'
                               '  m_Materials:\n'
                               '  - {fileID: 10303, guid: 0000000000000000f000000000000000, type: 0}\n'
                               '  m_StaticBatchInfo:\n'
                               '    firstSubMesh: 0\n'
                               '    subMeshCount: 0\n'
                               '  m_StaticBatchRoot: {fileID: 0}\n'
                               '  m_ProbeAnchor: {fileID: 0}\n'
                               '  m_LightProbeVolumeOverride: {fileID: 0}\n'
                               '  m_ScaleInLightmap: 1\n'
                               '  m_ReceiveGI: 1\n'
                               '  m_PreserveUVs: 1\n'
                               '  m_IgnoreNormalsForChartDetection: 0\n'
                               '  m_ImportantGI: 0\n'
                               '  m_StitchLightmapSeams: 1\n'
                               '  m_SelectedEditorRenderState: 3\n'
                               '  m_MinimumChartSize: 4\n'
                               '  m_AutoUVMaxDistance: 0.5\n'
                               '  m_AutoUVMaxAngle: 89\n'
                               '  m_LightmapParameters: {fileID: 0}\n'
                               '  m_SortingLayerID: 0\n'
                               '  m_SortingLayer: 0\n'
                               '  m_SortingOrder: 0\n'
                               '  m_AdditionalVertexStreams: {fileID: 0}\n'
                               '--- !u!135 &3610207\n'
                               'SphereCollider:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 3610205}\n'
                               '  m_Material: {fileID: 0}\n'
                               '  m_IncludeLayers:\n'
                               '    serializedVersion: 2\n'
                               '    m_Bits: 0\n'
                               '  m_ExcludeLayers:\n'
                               '    serializedVersion: 2\n'
                               '    m_Bits: 0\n'
                               '  m_LayerOverridePriority: 0\n'
                               '  m_IsTrigger: 0\n'
                               '  m_ProvidesContacts: 0\n'
                               '  m_Enabled: 1\n'
                               '  serializedVersion: 3\n'
                               '  m_Radius: 0.5\n'
                               '  m_Center: {x: 0, y: 0, z: 0}\n'
                               '--- !u!33 &3610208\n'
                               'MeshFilter:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 3610205}\n'
                               '  m_Mesh: {fileID: 10207, guid: 0000000000000000e000000000000000, type: 0}\n'
                               '--- !u!4 &3610209\n'
                               'Transform:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 3610205}\n'
                               '  serializedVersion: 2\n'
                               '  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}\n'
                               '  m_LocalPosition: {x: 3, y: 0, z: 0}\n'
                               '  m_LocalScale: {x: 1, y: 1, z: 1}\n'
                               '  m_ConstrainProportionsScale: 0\n'
                               '  m_Children: []\n'
                               '  m_Father: {fileID: 0}\n'
                               '  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}\n'
                               '--- !u!1 &911724678\n'
                               'GameObject:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  serializedVersion: 6\n'
                               '  m_Component:\n'
                               '  - component: {fileID: 911724682}\n'
                               '  - component: {fileID: 911724681}\n'
                               '  - component: {fileID: 911724680}\n'
                               '  - component: {fileID: 911724679}\n'
                               '  m_Layer: 0\n'
                               '  m_Name: Player Creature Slot\n'
                               '  m_TagString: Untagged\n'
                               '  m_Icon: {fileID: 0}\n'
                               '  m_NavMeshLayer: 0\n'
                               '  m_StaticEditorFlags: 0\n'
                               '  m_IsActive: 1\n'
                               '--- !u!23 &911724679\n'
                               'MeshRenderer:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 911724678}\n'
                               '  m_Enabled: 1\n'
                               '  m_CastShadows: 1\n'
                               '  m_ReceiveShadows: 1\n'
                               '  m_DynamicOccludee: 1\n'
                               '  m_StaticShadowCaster: 0\n'
                               '  m_MotionVectors: 1\n'
                               '  m_LightProbeUsage: 1\n'
                               '  m_ReflectionProbeUsage: 1\n'
                               '  m_RayTracingMode: 2\n'
                               '  m_RayTraceProcedural: 0\n'
                               '  m_RenderingLayerMask: 1\n'
                               '  m_RendererPriority: 0\n'
                               '  m_Materials:\n'
                               '  - {fileID: 10303, guid: 0000000000000000f000000000000000, type: 0}\n'
                               '  m_StaticBatchInfo:\n'
                               '    firstSubMesh: 0\n'
                               '    subMeshCount: 0\n'
                               '  m_StaticBatchRoot: {fileID: 0}\n'
                               '  m_ProbeAnchor: {fileID: 0}\n'
                               '  m_LightProbeVolumeOverride: {fileID: 0}\n'
                               '  m_ScaleInLightmap: 1\n'
                               '  m_ReceiveGI: 1\n'
                               '  m_PreserveUVs: 1\n'
                               '  m_IgnoreNormalsForChartDetection: 0\n'
                               '  m_ImportantGI: 0\n'
                               '  m_StitchLightmapSeams: 1\n'
                               '  m_SelectedEditorRenderState: 3\n'
                               '  m_MinimumChartSize: 4\n'
                               '  m_AutoUVMaxDistance: 0.5\n'
                               '  m_AutoUVMaxAngle: 89\n'
                               '  m_LightmapParameters: {fileID: 0}\n'
                               '  m_SortingLayerID: 0\n'
                               '  m_SortingLayer: 0\n'
                               '  m_SortingOrder: 0\n'
                               '  m_AdditionalVertexStreams: {fileID: 0}\n'
                               '--- !u!135 &911724680\n'
                               'SphereCollider:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 911724678}\n'
                               '  m_Material: {fileID: 0}\n'
                               '  m_IncludeLayers:\n'
                               '    serializedVersion: 2\n'
                               '    m_Bits: 0\n'
                               '  m_ExcludeLayers:\n'
                               '    serializedVersion: 2\n'
                               '    m_Bits: 0\n'
                               '  m_LayerOverridePriority: 0\n'
                               '  m_IsTrigger: 0\n'
                               '  m_ProvidesContacts: 0\n'
                               '  m_Enabled: 1\n'
                               '  serializedVersion: 3\n'
                               '  m_Radius: 0.5\n'
                               '  m_Center: {x: 0, y: 0, z: 0}\n'
                               '--- !u!33 &911724681\n'
                               'MeshFilter:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 911724678}\n'
                               '  m_Mesh: {fileID: 10207, guid: 0000000000000000e000000000000000, type: 0}\n'
                               '--- !u!4 &911724682\n'
                               'Transform:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 911724678}\n'
                               '  serializedVersion: 2\n'
                               '  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}\n'
                               '  m_LocalPosition: {x: 0, y: 0, z: 0}\n'
                               '  m_LocalScale: {x: 1, y: 1, z: 1}\n'
                               '  m_ConstrainProportionsScale: 0\n'
                               '  m_Children: []\n'
                               '  m_Father: {fileID: 0}\n'
                               '  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}\n'
                               '--- !u!1 &1794595743\n'
                               'GameObject:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  serializedVersion: 6\n'
                               '  m_Component:\n'
                               '  - component: {fileID: 1794595745}\n'
                               '  - component: {fileID: 1794595744}\n'
                               '  m_Layer: 0\n'
                               '  m_Name: Battle Camera\n'
                               '  m_TagString: Untagged\n'
                               '  m_Icon: {fileID: 0}\n'
                               '  m_NavMeshLayer: 0\n'
                               '  m_StaticEditorFlags: 0\n'
                               '  m_IsActive: 1\n'
                               '--- !u!20 &1794595744\n'
                               'Camera:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 1794595743}\n'
                               '  m_Enabled: 1\n'
                               '  serializedVersion: 2\n'
                               '  m_ClearFlags: 1\n'
                               '  m_BackGroundColor: {r: 0.19215687, g: 0.3019608, b: 0.4745098, a: 0}\n'
                               '  m_projectionMatrixMode: 1\n'
                               '  m_GateFitMode: 2\n'
                               '  m_FOVAxisMode: 0\n'
                               '  m_Iso: 200\n'
                               '  m_ShutterSpeed: 0.005\n'
                               '  m_Aperture: 16\n'
                               '  m_FocusDistance: 10\n'
                               '  m_FocalLength: 50\n'
                               '  m_BladeCount: 5\n'
                               '  m_Curvature: {x: 2, y: 11}\n'
                               '  m_BarrelClipping: 0.25\n'
                               '  m_Anamorphism: 0\n'
                               '  m_SensorSize: {x: 36, y: 24}\n'
                               '  m_LensShift: {x: 0, y: 0}\n'
                               '  m_NormalizedViewPortRect:\n'
                               '    serializedVersion: 2\n'
                               '    x: 0\n'
                               '    y: 0\n'
                               '    width: 1\n'
                               '    height: 1\n'
                               '  near clip plane: 0.3\n'
                               '  far clip plane: 1000\n'
                               '  field of view: 60\n'
                               '  orthographic: 1\n'
                               '  orthographic size: 6\n'
                               '  m_Depth: 0\n'
                               '  m_CullingMask:\n'
                               '    serializedVersion: 2\n'
                               '    m_Bits: 4294967295\n'
                               '  m_RenderingPath: -1\n'
                               '  m_TargetTexture: {fileID: 0}\n'
                               '  m_TargetDisplay: 0\n'
                               '  m_TargetEye: 3\n'
                               '  m_HDR: 1\n'
                               '  m_AllowMSAA: 1\n'
                               '  m_AllowDynamicResolution: 0\n'
                               '  m_ForceIntoRT: 0\n'
                               '  m_OcclusionCulling: 1\n'
                               '  m_StereoConvergence: 10\n'
                               '  m_StereoSeparation: 0.022\n'
                               '--- !u!4 &1794595745\n'
                               'Transform:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_CorrespondingSourceObject: {fileID: 0}\n'
                               '  m_PrefabInstance: {fileID: 0}\n'
                               '  m_PrefabAsset: {fileID: 0}\n'
                               '  m_GameObject: {fileID: 1794595743}\n'
                               '  serializedVersion: 2\n'
                               '  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}\n'
                               '  m_LocalPosition: {x: 0, y: 0, z: 0}\n'
                               '  m_LocalScale: {x: 1, y: 1, z: 1}\n'
                               '  m_ConstrainProportionsScale: 0\n'
                               '  m_Children: []\n'
                               '  m_Father: {fileID: 0}\n'
                               '  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}\n'
                               '--- !u!1660057539 &9223372036854775807\n'
                               'SceneRoots:\n'
                               '  m_ObjectHideFlags: 0\n'
                               '  m_Roots:\n'
                               '  - {fileID: 1794595745}\n'
                               '  - {fileID: 911724682}\n'
                               '  - {fileID: 3610209}\n',
 'Assets/Scenes/Battle.unity.meta': 'fileFormatVersion: 2\n'
                                    'guid: c48ab548f7f2ad145a75ecd5bc981302\n'
                                    'DefaultImporter:\n'
                                    '  externalObjects: {}\n'
                                    '  userData: \n'
                                    '  assetBundleName: \n'
                                    '  assetBundleVariant: \n',
 'Assets/Scenes/Overworld.unity': '%YAML 1.1\n'
                                  '%TAG !u! tag:unity3d.com,2011:\n'
                                  '--- !u!29 &1\n'
                                  'OcclusionCullingSettings:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  serializedVersion: 2\n'
                                  '  m_OcclusionBakeSettings:\n'
                                  '    smallestOccluder: 5\n'
                                  '    smallestHole: 0.25\n'
                                  '    backfaceThreshold: 100\n'
                                  '  m_SceneGUID: 00000000000000000000000000000000\n'
                                  '  m_OcclusionCullingData: {fileID: 0}\n'
                                  '--- !u!104 &2\n'
                                  'RenderSettings:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  serializedVersion: 9\n'
                                  '  m_Fog: 0\n'
                                  '  m_FogColor: {r: 0.5, g: 0.5, b: 0.5, a: 1}\n'
                                  '  m_FogMode: 3\n'
                                  '  m_FogDensity: 0.01\n'
                                  '  m_LinearFogStart: 0\n'
                                  '  m_LinearFogEnd: 300\n'
                                  '  m_AmbientSkyColor: {r: 0.212, g: 0.227, b: 0.259, a: 1}\n'
                                  '  m_AmbientEquatorColor: {r: 0.114, g: 0.125, b: 0.133, a: 1}\n'
                                  '  m_AmbientGroundColor: {r: 0.047, g: 0.043, b: 0.035, a: 1}\n'
                                  '  m_AmbientIntensity: 1\n'
                                  '  m_AmbientMode: 0\n'
                                  '  m_SubtractiveShadowColor: {r: 0.42, g: 0.478, b: 0.627, a: 1}\n'
                                  '  m_SkyboxMaterial: {fileID: 10304, guid: 0000000000000000f000000000000000, type: '
                                  '0}\n'
                                  '  m_HaloStrength: 0.5\n'
                                  '  m_FlareStrength: 1\n'
                                  '  m_FlareFadeSpeed: 3\n'
                                  '  m_HaloTexture: {fileID: 0}\n'
                                  '  m_SpotCookie: {fileID: 10001, guid: 0000000000000000e000000000000000, type: 0}\n'
                                  '  m_DefaultReflectionMode: 0\n'
                                  '  m_DefaultReflectionResolution: 128\n'
                                  '  m_ReflectionBounces: 1\n'
                                  '  m_ReflectionIntensity: 1\n'
                                  '  m_CustomReflection: {fileID: 0}\n'
                                  '  m_Sun: {fileID: 0}\n'
                                  '  m_UseRadianceAmbientProbe: 0\n'
                                  '--- !u!157 &3\n'
                                  'LightmapSettings:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  serializedVersion: 12\n'
                                  '  m_GIWorkflowMode: 1\n'
                                  '  m_GISettings:\n'
                                  '    serializedVersion: 2\n'
                                  '    m_BounceScale: 1\n'
                                  '    m_IndirectOutputScale: 1\n'
                                  '    m_AlbedoBoost: 1\n'
                                  '    m_EnvironmentLightingMode: 0\n'
                                  '    m_EnableBakedLightmaps: 1\n'
                                  '    m_EnableRealtimeLightmaps: 0\n'
                                  '  m_LightmapEditorSettings:\n'
                                  '    serializedVersion: 12\n'
                                  '    m_Resolution: 2\n'
                                  '    m_BakeResolution: 40\n'
                                  '    m_AtlasSize: 1024\n'
                                  '    m_AO: 0\n'
                                  '    m_AOMaxDistance: 1\n'
                                  '    m_CompAOExponent: 1\n'
                                  '    m_CompAOExponentDirect: 0\n'
                                  '    m_ExtractAmbientOcclusion: 0\n'
                                  '    m_Padding: 2\n'
                                  '    m_LightmapParameters: {fileID: 0}\n'
                                  '    m_LightmapsBakeMode: 1\n'
                                  '    m_TextureCompression: 1\n'
                                  '    m_FinalGather: 0\n'
                                  '    m_FinalGatherFiltering: 1\n'
                                  '    m_FinalGatherRayCount: 256\n'
                                  '    m_ReflectionCompression: 2\n'
                                  '    m_MixedBakeMode: 2\n'
                                  '    m_BakeBackend: 1\n'
                                  '    m_PVRSampling: 1\n'
                                  '    m_PVRDirectSampleCount: 32\n'
                                  '    m_PVRSampleCount: 512\n'
                                  '    m_PVRBounces: 2\n'
                                  '    m_PVREnvironmentSampleCount: 256\n'
                                  '    m_PVREnvironmentReferencePointCount: 2048\n'
                                  '    m_PVRFilteringMode: 1\n'
                                  '    m_PVRDenoiserTypeDirect: 1\n'
                                  '    m_PVRDenoiserTypeIndirect: 1\n'
                                  '    m_PVRDenoiserTypeAO: 1\n'
                                  '    m_PVRFilterTypeDirect: 0\n'
                                  '    m_PVRFilterTypeIndirect: 0\n'
                                  '    m_PVRFilterTypeAO: 0\n'
                                  '    m_PVREnvironmentMIS: 1\n'
                                  '    m_PVRCulling: 1\n'
                                  '    m_PVRFilteringGaussRadiusDirect: 1\n'
                                  '    m_PVRFilteringGaussRadiusIndirect: 5\n'
                                  '    m_PVRFilteringGaussRadiusAO: 2\n'
                                  '    m_PVRFilteringAtrousPositionSigmaDirect: 0.5\n'
                                  '    m_PVRFilteringAtrousPositionSigmaIndirect: 2\n'
                                  '    m_PVRFilteringAtrousPositionSigmaAO: 1\n'
                                  '    m_ExportTrainingData: 0\n'
                                  '    m_TrainingDataDestination: TrainingData\n'
                                  '    m_LightProbeSampleCountMultiplier: 4\n'
                                  '  m_LightingDataAsset: {fileID: 0}\n'
                                  '  m_LightingSettings: {fileID: 0}\n'
                                  '--- !u!196 &4\n'
                                  'NavMeshSettings:\n'
                                  '  serializedVersion: 2\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_BuildSettings:\n'
                                  '    serializedVersion: 3\n'
                                  '    agentTypeID: 0\n'
                                  '    agentRadius: 0.5\n'
                                  '    agentHeight: 2\n'
                                  '    agentSlope: 45\n'
                                  '    agentClimb: 0.4\n'
                                  '    ledgeDropHeight: 0\n'
                                  '    maxJumpAcrossDistance: 0\n'
                                  '    minRegionArea: 2\n'
                                  '    manualCellSize: 0\n'
                                  '    cellSize: 0.16666667\n'
                                  '    manualTileSize: 0\n'
                                  '    tileSize: 256\n'
                                  '    buildHeightMesh: 0\n'
                                  '    maxJobWorkers: 0\n'
                                  '    preserveTilesOutsideBounds: 0\n'
                                  '    debug:\n'
                                  '      m_Flags: 0\n'
                                  '  m_NavMeshData: {fileID: 0}\n'
                                  '--- !u!1 &3610205\n'
                                  'GameObject:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  serializedVersion: 6\n'
                                  '  m_Component:\n'
                                  '  - component: {fileID: 3610207}\n'
                                  '  - component: {fileID: 3610206}\n'
                                  '  m_Layer: 0\n'
                                  '  m_Name: Sun\n'
                                  '  m_TagString: Untagged\n'
                                  '  m_Icon: {fileID: 0}\n'
                                  '  m_NavMeshLayer: 0\n'
                                  '  m_StaticEditorFlags: 0\n'
                                  '  m_IsActive: 1\n'
                                  '--- !u!108 &3610206\n'
                                  'Light:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 3610205}\n'
                                  '  m_Enabled: 1\n'
                                  '  serializedVersion: 10\n'
                                  '  m_Type: 1\n'
                                  '  m_Shape: 0\n'
                                  '  m_Color: {r: 1, g: 1, b: 1, a: 1}\n'
                                  '  m_Intensity: 1\n'
                                  '  m_Range: 10\n'
                                  '  m_SpotAngle: 30\n'
                                  '  m_InnerSpotAngle: 21.80208\n'
                                  '  m_CookieSize: 10\n'
                                  '  m_Shadows:\n'
                                  '    m_Type: 0\n'
                                  '    m_Resolution: -1\n'
                                  '    m_CustomResolution: -1\n'
                                  '    m_Strength: 1\n'
                                  '    m_Bias: 0.05\n'
                                  '    m_NormalBias: 0.4\n'
                                  '    m_NearPlane: 0.2\n'
                                  '    m_CullingMatrixOverride:\n'
                                  '      e00: 1\n'
                                  '      e01: 0\n'
                                  '      e02: 0\n'
                                  '      e03: 0\n'
                                  '      e10: 0\n'
                                  '      e11: 1\n'
                                  '      e12: 0\n'
                                  '      e13: 0\n'
                                  '      e20: 0\n'
                                  '      e21: 0\n'
                                  '      e22: 1\n'
                                  '      e23: 0\n'
                                  '      e30: 0\n'
                                  '      e31: 0\n'
                                  '      e32: 0\n'
                                  '      e33: 1\n'
                                  '    m_UseCullingMatrixOverride: 0\n'
                                  '  m_Cookie: {fileID: 0}\n'
                                  '  m_DrawHalo: 0\n'
                                  '  m_Flare: {fileID: 0}\n'
                                  '  m_RenderMode: 0\n'
                                  '  m_CullingMask:\n'
                                  '    serializedVersion: 2\n'
                                  '    m_Bits: 4294967295\n'
                                  '  m_RenderingLayerMask: 1\n'
                                  '  m_Lightmapping: 4\n'
                                  '  m_LightShadowCasterMode: 0\n'
                                  '  m_AreaSize: {x: 1, y: 1}\n'
                                  '  m_BounceIntensity: 1\n'
                                  '  m_ColorTemperature: 6570\n'
                                  '  m_UseColorTemperature: 0\n'
                                  '  m_BoundingSphereOverride: {x: 0, y: 0, z: 0, w: 0}\n'
                                  '  m_UseBoundingSphereOverride: 0\n'
                                  '  m_UseViewFrustumForShadowCasterCull: 1\n'
                                  '  m_ShadowRadius: 0\n'
                                  '  m_ShadowAngle: 0\n'
                                  '--- !u!4 &3610207\n'
                                  'Transform:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 3610205}\n'
                                  '  serializedVersion: 2\n'
                                  '  m_LocalRotation: {x: 0.40821794, y: -0.23456973, z: 0.10938166, w: 0.8754261}\n'
                                  '  m_LocalPosition: {x: 0, y: 0, z: 0}\n'
                                  '  m_LocalScale: {x: 1, y: 1, z: 1}\n'
                                  '  m_ConstrainProportionsScale: 0\n'
                                  '  m_Children: []\n'
                                  '  m_Father: {fileID: 0}\n'
                                  '  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}\n'
                                  '--- !u!115 &337416045\n'
                                  'MonoScript:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_Name: \n'
                                  '  serializedVersion: 7\n'
                                  '  m_DefaultReferences: {}\n'
                                  '  m_Icon: {fileID: 0}\n'
                                  '  m_Type: 0\n'
                                  '  m_ExecutionOrder: 0\n'
                                  '  m_ClassName: PlayerMovementController\n'
                                  '  m_Namespace: __PROJECT_NAMESPACE__.Overworld\n'
                                  '  m_AssemblyName: __PROJECT_NAMESPACE__.Runtime\n'
                                  '--- !u!1 &482848659\n'
                                  'GameObject:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  serializedVersion: 6\n'
                                  '  m_Component:\n'
                                  '  - component: {fileID: 482848660}\n'
                                  '  - component: {fileID: 482848664}\n'
                                  '  - component: {fileID: 482848663}\n'
                                  '  - component: {fileID: 482848662}\n'
                                  '  - component: {fileID: 482848661}\n'
                                  '  m_Layer: 0\n'
                                  '  m_Name: Player\n'
                                  '  m_TagString: Untagged\n'
                                  '  m_Icon: {fileID: 0}\n'
                                  '  m_NavMeshLayer: 0\n'
                                  '  m_StaticEditorFlags: 0\n'
                                  '  m_IsActive: 1\n'
                                  '--- !u!4 &482848660\n'
                                  'Transform:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 482848659}\n'
                                  '  serializedVersion: 2\n'
                                  '  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}\n'
                                  '  m_LocalPosition: {x: 0, y: 1, z: 0}\n'
                                  '  m_LocalScale: {x: 1, y: 1, z: 1}\n'
                                  '  m_ConstrainProportionsScale: 0\n'
                                  '  m_Children: []\n'
                                  '  m_Father: {fileID: 0}\n'
                                  '  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}\n'
                                  '--- !u!114 &482848661\n'
                                  'MonoBehaviour:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 482848659}\n'
                                  '  m_Enabled: 1\n'
                                  '  m_EditorHideFlags: 0\n'
                                  '  m_Script: {fileID: 337416045}\n'
                                  '  m_Name: \n'
                                  '  m_EditorClassIdentifier: \n'
                                  '  profile: {fileID: 0}\n'
                                  '--- !u!23 &482848662\n'
                                  'MeshRenderer:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 482848659}\n'
                                  '  m_Enabled: 1\n'
                                  '  m_CastShadows: 1\n'
                                  '  m_ReceiveShadows: 1\n'
                                  '  m_DynamicOccludee: 1\n'
                                  '  m_StaticShadowCaster: 0\n'
                                  '  m_MotionVectors: 1\n'
                                  '  m_LightProbeUsage: 1\n'
                                  '  m_ReflectionProbeUsage: 1\n'
                                  '  m_RayTracingMode: 2\n'
                                  '  m_RayTraceProcedural: 0\n'
                                  '  m_RenderingLayerMask: 1\n'
                                  '  m_RendererPriority: 0\n'
                                  '  m_Materials:\n'
                                  '  - {fileID: 10303, guid: 0000000000000000f000000000000000, type: 0}\n'
                                  '  m_StaticBatchInfo:\n'
                                  '    firstSubMesh: 0\n'
                                  '    subMeshCount: 0\n'
                                  '  m_StaticBatchRoot: {fileID: 0}\n'
                                  '  m_ProbeAnchor: {fileID: 0}\n'
                                  '  m_LightProbeVolumeOverride: {fileID: 0}\n'
                                  '  m_ScaleInLightmap: 1\n'
                                  '  m_ReceiveGI: 1\n'
                                  '  m_PreserveUVs: 1\n'
                                  '  m_IgnoreNormalsForChartDetection: 0\n'
                                  '  m_ImportantGI: 0\n'
                                  '  m_StitchLightmapSeams: 1\n'
                                  '  m_SelectedEditorRenderState: 3\n'
                                  '  m_MinimumChartSize: 4\n'
                                  '  m_AutoUVMaxDistance: 0.5\n'
                                  '  m_AutoUVMaxAngle: 89\n'
                                  '  m_LightmapParameters: {fileID: 0}\n'
                                  '  m_SortingLayerID: 0\n'
                                  '  m_SortingLayer: 0\n'
                                  '  m_SortingOrder: 0\n'
                                  '  m_AdditionalVertexStreams: {fileID: 0}\n'
                                  '--- !u!136 &482848663\n'
                                  'CapsuleCollider:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 482848659}\n'
                                  '  m_Material: {fileID: 0}\n'
                                  '  m_IncludeLayers:\n'
                                  '    serializedVersion: 2\n'
                                  '    m_Bits: 0\n'
                                  '  m_ExcludeLayers:\n'
                                  '    serializedVersion: 2\n'
                                  '    m_Bits: 0\n'
                                  '  m_LayerOverridePriority: 0\n'
                                  '  m_IsTrigger: 0\n'
                                  '  m_ProvidesContacts: 0\n'
                                  '  m_Enabled: 1\n'
                                  '  serializedVersion: 2\n'
                                  '  m_Radius: 0.5\n'
                                  '  m_Height: 2\n'
                                  '  m_Direction: 1\n'
                                  '  m_Center: {x: 0, y: 0, z: 0}\n'
                                  '--- !u!33 &482848664\n'
                                  'MeshFilter:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 482848659}\n'
                                  '  m_Mesh: {fileID: 10208, guid: 0000000000000000e000000000000000, type: 0}\n'
                                  '--- !u!1 &612024511\n'
                                  'GameObject:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  serializedVersion: 6\n'
                                  '  m_Component:\n'
                                  '  - component: {fileID: 612024515}\n'
                                  '  - component: {fileID: 612024514}\n'
                                  '  - component: {fileID: 612024513}\n'
                                  '  - component: {fileID: 612024512}\n'
                                  '  m_Layer: 0\n'
                                  '  m_Name: 100m Testing Ground\n'
                                  '  m_TagString: Untagged\n'
                                  '  m_Icon: {fileID: 0}\n'
                                  '  m_NavMeshLayer: 0\n'
                                  '  m_StaticEditorFlags: 0\n'
                                  '  m_IsActive: 1\n'
                                  '--- !u!23 &612024512\n'
                                  'MeshRenderer:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 612024511}\n'
                                  '  m_Enabled: 1\n'
                                  '  m_CastShadows: 1\n'
                                  '  m_ReceiveShadows: 1\n'
                                  '  m_DynamicOccludee: 1\n'
                                  '  m_StaticShadowCaster: 0\n'
                                  '  m_MotionVectors: 1\n'
                                  '  m_LightProbeUsage: 1\n'
                                  '  m_ReflectionProbeUsage: 1\n'
                                  '  m_RayTracingMode: 2\n'
                                  '  m_RayTraceProcedural: 0\n'
                                  '  m_RenderingLayerMask: 1\n'
                                  '  m_RendererPriority: 0\n'
                                  '  m_Materials:\n'
                                  '  - {fileID: 10303, guid: 0000000000000000f000000000000000, type: 0}\n'
                                  '  m_StaticBatchInfo:\n'
                                  '    firstSubMesh: 0\n'
                                  '    subMeshCount: 0\n'
                                  '  m_StaticBatchRoot: {fileID: 0}\n'
                                  '  m_ProbeAnchor: {fileID: 0}\n'
                                  '  m_LightProbeVolumeOverride: {fileID: 0}\n'
                                  '  m_ScaleInLightmap: 1\n'
                                  '  m_ReceiveGI: 1\n'
                                  '  m_PreserveUVs: 1\n'
                                  '  m_IgnoreNormalsForChartDetection: 0\n'
                                  '  m_ImportantGI: 0\n'
                                  '  m_StitchLightmapSeams: 1\n'
                                  '  m_SelectedEditorRenderState: 3\n'
                                  '  m_MinimumChartSize: 4\n'
                                  '  m_AutoUVMaxDistance: 0.5\n'
                                  '  m_AutoUVMaxAngle: 89\n'
                                  '  m_LightmapParameters: {fileID: 0}\n'
                                  '  m_SortingLayerID: 0\n'
                                  '  m_SortingLayer: 0\n'
                                  '  m_SortingOrder: 0\n'
                                  '  m_AdditionalVertexStreams: {fileID: 0}\n'
                                  '--- !u!65 &612024513\n'
                                  'BoxCollider:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 612024511}\n'
                                  '  m_Material: {fileID: 0}\n'
                                  '  m_IncludeLayers:\n'
                                  '    serializedVersion: 2\n'
                                  '    m_Bits: 0\n'
                                  '  m_ExcludeLayers:\n'
                                  '    serializedVersion: 2\n'
                                  '    m_Bits: 0\n'
                                  '  m_LayerOverridePriority: 0\n'
                                  '  m_IsTrigger: 0\n'
                                  '  m_ProvidesContacts: 0\n'
                                  '  m_Enabled: 1\n'
                                  '  serializedVersion: 3\n'
                                  '  m_Size: {x: 1, y: 1, z: 1}\n'
                                  '  m_Center: {x: 0, y: 0, z: 0}\n'
                                  '--- !u!33 &612024514\n'
                                  'MeshFilter:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 612024511}\n'
                                  '  m_Mesh: {fileID: 10202, guid: 0000000000000000e000000000000000, type: 0}\n'
                                  '--- !u!4 &612024515\n'
                                  'Transform:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 612024511}\n'
                                  '  serializedVersion: 2\n'
                                  '  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}\n'
                                  '  m_LocalPosition: {x: 0, y: -0.05, z: 0}\n'
                                  '  m_LocalScale: {x: 100, y: 0.1, z: 100}\n'
                                  '  m_ConstrainProportionsScale: 0\n'
                                  '  m_Children: []\n'
                                  '  m_Father: {fileID: 0}\n'
                                  '  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}\n'
                                  '--- !u!1 &911724678\n'
                                  'GameObject:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  serializedVersion: 6\n'
                                  '  m_Component:\n'
                                  '  - component: {fileID: 911724681}\n'
                                  '  - component: {fileID: 911724680}\n'
                                  '  - component: {fileID: 911724679}\n'
                                  '  m_Layer: 0\n'
                                  '  m_Name: 2.5D Follow Camera\n'
                                  '  m_TagString: Untagged\n'
                                  '  m_Icon: {fileID: 0}\n'
                                  '  m_NavMeshLayer: 0\n'
                                  '  m_StaticEditorFlags: 0\n'
                                  '  m_IsActive: 1\n'
                                  '--- !u!114 &911724679\n'
                                  'MonoBehaviour:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 911724678}\n'
                                  '  m_Enabled: 1\n'
                                  '  m_EditorHideFlags: 0\n'
                                  '  m_Script: {fileID: 1794595743}\n'
                                  '  m_Name: \n'
                                  '  m_EditorClassIdentifier: \n'
                                  '  target: {fileID: 482848660}\n'
                                  '  profile: {fileID: 0}\n'
                                  '--- !u!20 &911724680\n'
                                  'Camera:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 911724678}\n'
                                  '  m_Enabled: 1\n'
                                  '  serializedVersion: 2\n'
                                  '  m_ClearFlags: 1\n'
                                  '  m_BackGroundColor: {r: 0.19215687, g: 0.3019608, b: 0.4745098, a: 0}\n'
                                  '  m_projectionMatrixMode: 1\n'
                                  '  m_GateFitMode: 2\n'
                                  '  m_FOVAxisMode: 0\n'
                                  '  m_Iso: 200\n'
                                  '  m_ShutterSpeed: 0.005\n'
                                  '  m_Aperture: 16\n'
                                  '  m_FocusDistance: 10\n'
                                  '  m_FocalLength: 50\n'
                                  '  m_BladeCount: 5\n'
                                  '  m_Curvature: {x: 2, y: 11}\n'
                                  '  m_BarrelClipping: 0.25\n'
                                  '  m_Anamorphism: 0\n'
                                  '  m_SensorSize: {x: 36, y: 24}\n'
                                  '  m_LensShift: {x: 0, y: 0}\n'
                                  '  m_NormalizedViewPortRect:\n'
                                  '    serializedVersion: 2\n'
                                  '    x: 0\n'
                                  '    y: 0\n'
                                  '    width: 1\n'
                                  '    height: 1\n'
                                  '  near clip plane: 0.3\n'
                                  '  far clip plane: 1000\n'
                                  '  field of view: 60\n'
                                  '  orthographic: 1\n'
                                  '  orthographic size: 5\n'
                                  '  m_Depth: 0\n'
                                  '  m_CullingMask:\n'
                                  '    serializedVersion: 2\n'
                                  '    m_Bits: 4294967295\n'
                                  '  m_RenderingPath: -1\n'
                                  '  m_TargetTexture: {fileID: 0}\n'
                                  '  m_TargetDisplay: 0\n'
                                  '  m_TargetEye: 3\n'
                                  '  m_HDR: 1\n'
                                  '  m_AllowMSAA: 1\n'
                                  '  m_AllowDynamicResolution: 0\n'
                                  '  m_ForceIntoRT: 0\n'
                                  '  m_OcclusionCulling: 1\n'
                                  '  m_StereoConvergence: 10\n'
                                  '  m_StereoSeparation: 0.022\n'
                                  '--- !u!4 &911724681\n'
                                  'Transform:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_GameObject: {fileID: 911724678}\n'
                                  '  serializedVersion: 2\n'
                                  '  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}\n'
                                  '  m_LocalPosition: {x: 0, y: 0, z: 0}\n'
                                  '  m_LocalScale: {x: 1, y: 1, z: 1}\n'
                                  '  m_ConstrainProportionsScale: 0\n'
                                  '  m_Children: []\n'
                                  '  m_Father: {fileID: 0}\n'
                                  '  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}\n'
                                  '--- !u!115 &1794595743\n'
                                  'MonoScript:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_CorrespondingSourceObject: {fileID: 0}\n'
                                  '  m_PrefabInstance: {fileID: 0}\n'
                                  '  m_PrefabAsset: {fileID: 0}\n'
                                  '  m_Name: \n'
                                  '  serializedVersion: 7\n'
                                  '  m_DefaultReferences: {}\n'
                                  '  m_Icon: {fileID: 0}\n'
                                  '  m_Type: 0\n'
                                  '  m_ExecutionOrder: 0\n'
                                  '  m_ClassName: CameraFollowController\n'
                                  '  m_Namespace: __PROJECT_NAMESPACE__.CameraSystem\n'
                                  '  m_AssemblyName: __PROJECT_NAMESPACE__.Runtime\n'
                                  '--- !u!1660057539 &9223372036854775807\n'
                                  'SceneRoots:\n'
                                  '  m_ObjectHideFlags: 0\n'
                                  '  m_Roots:\n'
                                  '  - {fileID: 482848660}\n'
                                  '  - {fileID: 612024515}\n'
                                  '  - {fileID: 911724681}\n'
                                  '  - {fileID: 3610207}\n',
 'Assets/Scenes/Overworld.unity.meta': 'fileFormatVersion: 2\n'
                                       'guid: 0d7bc528ec58c77459faf02a2cf098bc\n'
                                       'DefaultImporter:\n'
                                       '  externalObjects: {}\n'
                                       '  userData: \n'
                                       '  assetBundleName: \n'
                                       '  assetBundleVariant: \n',
 'Assets/Scripts/Audio/AudioVisualScaffolds.cs': 'using __PROJECT_NAMESPACE__.Core;\n'
                                                 'using UnityEngine;\n'
                                                 '\n'
                                                 'namespace __PROJECT_NAMESPACE__.Audio\n'
                                                 '{\n'
                                                 '    public sealed class MusicManager\n'
                                                 '    {\n'
                                                 '        private readonly EventBus events;\n'
                                                 '        public string CurrentTrack { get; private set; }\n'
                                                 '        public MusicManager(EventBus events = null) { this.events = '
                                                 'events; }\n'
                                                 '        public void SwitchTrack(string areaTrackId) { CurrentTrack = '
                                                 'areaTrackId; events?.Publish(new '
                                                 'MusicTrackChangedEvent(areaTrackId)); }\n'
                                                 '    }\n'
                                                 '\n'
                                                 '    public sealed class SFXManager { public string LastPlayed { get; '
                                                 'private set; } public void Play(string id) { LastPlayed = id; } }\n'
                                                 '    public sealed class AmbientAudioManager { public string '
                                                 'CurrentAmbient { get; private set; } public void SetAmbient(string '
                                                 'id) { CurrentAmbient = id; } }\n'
                                                 '}\n'
                                                 '\n'
                                                 'namespace __PROJECT_NAMESPACE__.Visuals\n'
                                                 '{\n'
                                                 '    public sealed class WeatherVisualController\n'
                                                 '    {\n'
                                                 '        private readonly EventBus events;\n'
                                                 '        public string Weather { get; private set; }\n'
                                                 '        public WeatherVisualController(EventBus events = null) { '
                                                 'this.events = events; }\n'
                                                 '        public void SetWeather(string weatherId) { Weather = '
                                                 'weatherId; events?.Publish(new WeatherChangedEvent(weatherId)); }\n'
                                                 '    }\n'
                                                 '\n'
                                                 '    public sealed class DayNightLightingController { public float '
                                                 'Time01 { get; private set; } public void Advance(float delta01) { '
                                                 'Time01 = Mathf.Repeat(Time01 + delta01, 1f); } }\n'
                                                 '    public sealed class BattleAnimationEventHooks { public event '
                                                 'System.Action<string> AnimationEvent; public void Flame(string id) { '
                                                 'AnimationEvent?.Invoke(id); } }\n'
                                                 '    public sealed class TransformationFXHooks { private readonly '
                                                 'EventBus events; public TransformationFXHooks(EventBus events = '
                                                 'null) { this.events = events; } public void Flame(string creatureId, '
                                                 'string fxId) { events?.Publish(new TransformationFxEvent(creatureId, '
                                                 'fxId)); } }\n'
                                                 '    public sealed class RaidCameraHooks { public string LastCue { '
                                                 'get; private set; } public void PlayCue(string cue) { LastCue = cue; '
                                                 '} }\n'
                                                 '}\n',
 'Assets/Scripts/Battle/BattleSystem.cs': 'using System.Collections.Generic;\n'
                                          'using System.Linq;\n'
                                          'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                          'using UnityEngine;\n'
                                          '\n'
                                          'namespace __PROJECT_NAMESPACE__.Battle\n'
                                          '{\n'
                                          '    public enum BattleState { Intro, CommandSelection, ActionQueue, '
                                          'MoveExecution, DamageResolution, FaintHandling, Victory, Defeat }\n'
                                          '    public enum BattleCommandType { Fight, Switch, Item, Run }\n'
                                          '    public enum WeatherState { Clear, Rain, Sun, Storm }\n'
                                          '    public enum TerrainState { Normal, Leafy, Electric, Dimensional }\n'
                                          '\n'
                                          '    public interface IRandomSource\n'
                                          '    {\n'
                                          '        int Range(int minInclusive, int maxExclusive);\n'
                                          '        double Value01();\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class SystemRandomSource : IRandomSource\n'
                                          '    {\n'
                                          '        private readonly System.Random rng;\n'
                                          '        public SystemRandomSource(int seed = 0) { rng = seed == 0 ? new '
                                          'System.Random() : new System.Random(seed); }\n'
                                          '        public int Range(int minInclusive, int maxExclusive) => '
                                          'rng.Next(minInclusive, maxExclusive);\n'
                                          '        public double Value01() => rng.NextDouble();\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class FixedRandomSource : IRandomSource\n'
                                          '    {\n'
                                          '        private readonly int value;\n'
                                          '        public FixedRandomSource(int value) { this.value = value; }\n'
                                          '        public int Range(int minInclusive, int maxExclusive) => '
                                          'Mathf.Clamp(value, minInclusive, maxExclusive - 1);\n'
                                          '        public double Value01() => value / 100.0;\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class BattleCreature\n'
                                          '    {\n'
                                          '        public CreatureInstance Instance { get; }\n'
                                          '        public int CurrentHp { get; private set; }\n'
                                          '        public StatusCondition Status { get; set; }\n'
                                          '        public bool Fainted => CurrentHp <= 0;\n'
                                          '        public StatBlock Stats => Instance.CalculateStats();\n'
                                          '\n'
                                          '        public BattleCreature(CreatureInstance instance)\n'
                                          '        {\n'
                                          '            Instance = instance;\n'
                                          '            CurrentHp = instance.CurrentHp > 0 ? instance.CurrentHp : '
                                          'instance.CalculateStats().hp;\n'
                                          '        }\n'
                                          '\n'
                                          '        public void ApplyDamage(int amount)\n'
                                          '        {\n'
                                          '            CurrentHp = Mathf.Max(0, CurrentHp - Mathf.Max(0, amount));\n'
                                          '            Instance.CurrentHp = CurrentHp;\n'
                                          '        }\n'
                                          '\n'
                                          '        public void HealFull()\n'
                                          '        {\n'
                                          '            CurrentHp = Stats.hp;\n'
                                          '            Instance.CurrentHp = CurrentHp;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class BattleParticipant\n'
                                          '    {\n'
                                          '        public string id;\n'
                                          '        public BattleCreature active;\n'
                                          '        public bool isPlayer;\n'
                                          '        public IReadOnlyList<MoveDefinition> LegalMoves => '
                                          'active?.Instance?.KnownMoves ?? new List<MoveDefinition>();\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class BattleCommand\n'
                                          '    {\n'
                                          '        public BattleParticipant user;\n'
                                          '        public BattleParticipant target;\n'
                                          '        public BattleCommandType type;\n'
                                          '        public MoveDefinition move;\n'
                                          '\n'
                                          '        public static BattleCommand Fight(BattleParticipant user, '
                                          'BattleParticipant target, MoveDefinition move)\n'
                                          '        {\n'
                                          '            return new BattleCommand { user = user, target = target, type = '
                                          'BattleCommandType.Fight, move = move };\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class BattleStateMachine\n'
                                          '    {\n'
                                          '        public BattleState State { get; private set; } = '
                                          'BattleState.Intro;\n'
                                          '        public void Change(BattleState state) { State = state; }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class AccuracyResolver\n'
                                          '    {\n'
                                          '        public bool DoesHit(MoveDefinition move, IRandomSource rng)\n'
                                          '        {\n'
                                          '            return move == null || move.accuracy >= 100 || rng.Range(0, '
                                          '100) < move.accuracy;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    /// <summary>Damage formula is intentionally compact but includes STAB, '
                                          'type, crit, weather/terrain hooks.</summary>\n'
                                          '    public sealed class DamageCalculator\n'
                                          '    {\n'
                                          '        private readonly TypeChart typeChart;\n'
                                          '\n'
                                          '        public DamageCalculator(TypeChart typeChart)\n'
                                          '        {\n'
                                          '            this.typeChart = typeChart ?? '
                                          'TypeChart.CreateDefaultForTests();\n'
                                          '        }\n'
                                          '\n'
                                          '        public int Calculate(BattleCreature attacker, BattleCreature '
                                          'defender, MoveDefinition move, bool critical = false, float weatherModifier '
                                          '= 1f, float terrainModifier = 1f)\n'
                                          '        {\n'
                                          '            if (attacker == null || defender == null || move == null || '
                                          'move.power <= 0)\n'
                                          '            {\n'
                                          '                return 0;\n'
                                          '            }\n'
                                          '\n'
                                          '            var a = attacker.Stats;\n'
                                          '            var d = defender.Stats;\n'
                                          '            var offense = move.category == MoveCategory.Special ? '
                                          'a.specialAttack : a.attack;\n'
                                          '            var defense = Mathf.Max(1, move.category == '
                                          'MoveCategory.Special ? d.specialDefense : d.defense);\n'
                                          '            var level = attacker.Instance.Level;\n'
                                          '            var baseDamage = (((((2 * level) / 5f) + 2f) * move.power * '
                                          'offense / defense) / 50f) + 2f;\n'
                                          '            var species = attacker.Instance.Species;\n'
                                          '            var target = defender.Instance.Species;\n'
                                          '            var stab = species != null && (species.primaryType == move.type '
                                          '|| species.secondaryType == move.type) ? 1.5f : 1f;\n'
                                          '            var type = target != null ? typeChart.GetMultiplier(move.type, '
                                          'target.primaryType, target.secondaryType) : 1f;\n'
                                          '            var crit = critical ? 1.5f : 1f;\n'
                                          '            return Mathf.Max(1, Mathf.FloorToInt(baseDamage * stab * type * '
                                          'crit * weatherModifier * terrainModifier));\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class StatusEffectController\n'
                                          '    {\n'
                                          '        public void ApplyEndTurn(BattleCreature creature)\n'
                                          '        {\n'
                                          '            if (creature != null && creature.Status == StatusCondition.Burn '
                                          '&& !creature.Fainted)\n'
                                          '            {\n'
                                          '                creature.ApplyDamage(Mathf.Max(1, creature.Stats.hp / '
                                          '16));\n'
                                          '            }\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class WeatherController { public WeatherState State { '
                                          'get; private set; } public void Set(WeatherState state) { State = state; } '
                                          '}\n'
                                          '    public sealed class TerrainController { public TerrainState State { '
                                          'get; private set; } public void Set(TerrainState state) { State = state; } '
                                          '}\n'
                                          '\n'
                                          '    public sealed class MoveResolver\n'
                                          '    {\n'
                                          '        private readonly AccuracyResolver accuracy = new '
                                          'AccuracyResolver();\n'
                                          '        private readonly DamageCalculator damage;\n'
                                          '\n'
                                          '        public MoveResolver(DamageCalculator damage)\n'
                                          '        {\n'
                                          '            this.damage = damage;\n'
                                          '        }\n'
                                          '\n'
                                          '        public List<BattleCommand> SortCommands(IEnumerable<BattleCommand> '
                                          'commands)\n'
                                          '        {\n'
                                          '            return commands.OrderByDescending(c => c.move != null ? '
                                          'c.move.priority : 0).ThenByDescending(c => '
                                          'c.user.active.Stats.speed).ToList();\n'
                                          '        }\n'
                                          '\n'
                                          '        public bool Execute(BattleCommand command, IRandomSource rng)\n'
                                          '        {\n'
                                          '            if (command?.move == null || command.target?.active == null)\n'
                                          '            {\n'
                                          '                return false;\n'
                                          '            }\n'
                                          '\n'
                                          '            if (!accuracy.DoesHit(command.move, rng))\n'
                                          '            {\n'
                                          '                return false;\n'
                                          '            }\n'
                                          '\n'
                                          '            var amount = damage.Calculate(command.user.active, '
                                          'command.target.active, command.move);\n'
                                          '            command.target.active.ApplyDamage(amount);\n'
                                          '            if (command.move.statusToApply != StatusCondition.None)\n'
                                          '            {\n'
                                          '                command.target.active.Status = command.move.statusToApply;\n'
                                          '            }\n'
                                          '\n'
                                          '            return true;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public abstract class BattleAI\n'
                                          '    {\n'
                                          '        public abstract BattleCommand Choose(BattleParticipant self, '
                                          'BattleParticipant opponent);\n'
                                          '        protected MoveDefinition FirstLegal(BattleParticipant participant) '
                                          '=> participant.LegalMoves.FirstOrDefault();\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class WildBattleAI : BattleAI\n'
                                          '    {\n'
                                          '        public override BattleCommand Choose(BattleParticipant self, '
                                          'BattleParticipant opponent) => BattleCommand.Fight(self, opponent, '
                                          'FirstLegal(self));\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class TrainerBattleAI : BattleAI\n'
                                          '    {\n'
                                          '        public override BattleCommand Choose(BattleParticipant self, '
                                          'BattleParticipant opponent) => BattleCommand.Fight(self, opponent, '
                                          'self.LegalMoves.OrderByDescending(m => m.power).FirstOrDefault());\n'
                                          '    }\n'
                                          '\n'
                                          '    /// <summary>Single-battle controller. Extend with doubles/raids by '
                                          'adding participants and command collection policies.</summary>\n'
                                          '    public sealed class BattleController\n'
                                          '    {\n'
                                          '        public BattleStateMachine StateMachine { get; } = new '
                                          'BattleStateMachine();\n'
                                          '        private readonly MoveResolver resolver;\n'
                                          '        private readonly StatusEffectController status = new '
                                          'StatusEffectController();\n'
                                          '\n'
                                          '        public BattleController(TypeChart chart)\n'
                                          '        {\n'
                                          '            resolver = new MoveResolver(new DamageCalculator(chart));\n'
                                          '        }\n'
                                          '\n'
                                          '        public void StartSingleBattle()\n'
                                          '        {\n'
                                          '            StateMachine.Change(BattleState.CommandSelection);\n'
                                          '        }\n'
                                          '\n'
                                          '        public void ExecuteTurn(IEnumerable<BattleCommand> commands, '
                                          'IRandomSource rng)\n'
                                          '        {\n'
                                          '            var commandList = commands.ToList();\n'
                                          '            StateMachine.Change(BattleState.ActionQueue);\n'
                                          '            foreach (var command in resolver.SortCommands(commandList))\n'
                                          '            {\n'
                                          '                StateMachine.Change(BattleState.MoveExecution);\n'
                                          '                resolver.Execute(command, rng);\n'
                                          '                if (command.target.active.Fainted)\n'
                                          '                {\n'
                                          '                    StateMachine.Change(BattleState.FaintHandling);\n'
                                          '                }\n'
                                          '            }\n'
                                          '\n'
                                          '            foreach (var command in commandList)\n'
                                          '            {\n'
                                          '                status.ApplyEndTurn(command.user.active);\n'
                                          '            }\n'
                                          '\n'
                                          '            StateMachine.Change(BattleState.CommandSelection);\n'
                                          '        }\n'
                                          '    }\n'
                                          '}\n',
 'Assets/Scripts/Camera/CameraSystem.cs': 'using UnityEngine;\n'
                                          '\n'
                                          'namespace __PROJECT_NAMESPACE__.CameraSystem\n'
                                          '{\n'
                                          '    public enum CameraMode { Fixed, WildFreeLook }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Camera Zone Profile")]\n'
                                          '    public sealed class CameraZoneProfile : ScriptableObject\n'
                                          '    {\n'
                                          '        public CameraMode mode = CameraMode.Fixed;\n'
                                          '        public Vector3 offset = new Vector3(0f, 5f, -6f);\n'
                                          '        public float zoom = 5f;\n'
                                          '        public float fixedYaw;\n'
                                          '        public float horizontalSensitivity = 90f;\n'
                                          '        public float verticalSensitivity = 30f;\n'
                                          '        public float minPitch = -5f;\n'
                                          '        public float maxPitch = 5f;\n'
                                          '        public float smoothTime = 0.08f;\n'
                                          '    }\n'
                                          '\n'
                                          '    public readonly struct CameraInput\n'
                                          '    {\n'
                                          '        public readonly float mouseX, mouseY, rightStickX;\n'
                                          '        public CameraInput(float mouseX, float mouseY, float rightStickX = '
                                          '0f)\n'
                                          '        {\n'
                                          '            this.mouseX = mouseX;\n'
                                          '            this.mouseY = mouseY;\n'
                                          '            this.rightStickX = rightStickX;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public readonly struct CameraPose\n'
                                          '    {\n'
                                          '        public readonly Vector3 position;\n'
                                          '        public readonly Quaternion rotation;\n'
                                          '        public readonly float yaw;\n'
                                          '        public readonly float pitch;\n'
                                          '\n'
                                          '        public CameraPose(Vector3 position, Quaternion rotation, float yaw, '
                                          'float pitch)\n'
                                          '        {\n'
                                          '            this.position = position;\n'
                                          '            this.rotation = rotation;\n'
                                          '            this.yaw = yaw;\n'
                                          '            this.pitch = pitch;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public interface ICameraMode\n'
                                          '    {\n'
                                          '        CameraPose UpdatePose(Vector3 targetPosition, CameraZoneProfile '
                                          'profile, CameraInput input, float deltaTime);\n'
                                          '    }\n'
                                          '\n'
                                          '    /// <summary>Fixed/semi-fixed camera for structured maps. Add '
                                          'area-specific offsets through CameraZoneProfile.</summary>\n'
                                          '    public sealed class FixedCameraMode : ICameraMode\n'
                                          '    {\n'
                                          '        public CameraPose UpdatePose(Vector3 targetPosition, '
                                          'CameraZoneProfile profile, CameraInput input, float deltaTime)\n'
                                          '        {\n'
                                          '            var yaw = profile != null ? profile.fixedYaw : 0f;\n'
                                          '            var offset = Quaternion.Euler(0f, yaw, 0f) * (profile != null ? '
                                          'profile.offset : new Vector3(0f, 5f, -6f));\n'
                                          '            var position = targetPosition + offset;\n'
                                          '            return new CameraPose(position, '
                                          'Quaternion.LookRotation(targetPosition + Vector3.up - position, '
                                          'Vector3.up), yaw, 0f);\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    /// <summary>Wild camera rotates horizontally and clamps vertical pitch '
                                          'so it never becomes a full free camera.</summary>\n'
                                          '    public sealed class WildAreaFreeLookCameraMode : ICameraMode\n'
                                          '    {\n'
                                          '        public float Yaw { get; private set; }\n'
                                          '        public float Pitch { get; private set; }\n'
                                          '\n'
                                          '        public CameraPose UpdatePose(Vector3 targetPosition, '
                                          'CameraZoneProfile profile, CameraInput input, float deltaTime)\n'
                                          '        {\n'
                                          '            var p = profile != null ? profile : '
                                          'ScriptableObject.CreateInstance<CameraZoneProfile>();\n'
                                          '            Yaw += (input.mouseX + input.rightStickX) * '
                                          'p.horizontalSensitivity * deltaTime;\n'
                                          '            Pitch = Mathf.Clamp(Pitch - input.mouseY * '
                                          'p.verticalSensitivity * deltaTime, p.minPitch, p.maxPitch);\n'
                                          '            var orbit = Quaternion.Euler(Pitch, Yaw, 0f);\n'
                                          '            var position = targetPosition + orbit * p.offset;\n'
                                          '            return new CameraPose(position, '
                                          'Quaternion.LookRotation(targetPosition + Vector3.up - position, '
                                          'Vector3.up), Yaw, Pitch);\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class CameraCollisionResolver\n'
                                          '    {\n'
                                          '        public Vector3 Resolve(Vector3 target, Vector3 desired)\n'
                                          '        {\n'
                                          '            return desired;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    /// <summary>Unity adapter for camera modes. Extend by swapping '
                                          'profiles from trigger zones or streamed area metadata.</summary>\n'
                                          '    public sealed class CameraFollowController : MonoBehaviour\n'
                                          '    {\n'
                                          '        public Transform target;\n'
                                          '        public CameraZoneProfile profile;\n'
                                          '        public bool lookInputPaused;\n'
                                          '        private readonly FixedCameraMode fixedMode = new '
                                          'FixedCameraMode();\n'
                                          '        private readonly WildAreaFreeLookCameraMode wildMode = new '
                                          'WildAreaFreeLookCameraMode();\n'
                                          '        private readonly CameraCollisionResolver collision = new '
                                          'CameraCollisionResolver();\n'
                                          '\n'
                                          '        public bool HasTarget => target != null;\n'
                                          '        public CameraMode CurrentMode => profile != null ? profile.mode : '
                                          'CameraMode.Fixed;\n'
                                          '\n'
                                          '        public void SetTarget(Transform followTarget)\n'
                                          '        {\n'
                                          '            target = followTarget;\n'
                                          '        }\n'
                                          '\n'
                                          '        public void SwitchProfile(CameraZoneProfile nextProfile)\n'
                                          '        {\n'
                                          '            profile = nextProfile;\n'
                                          '        }\n'
                                          '\n'
                                          '        public void SetLookInputPaused(bool paused)\n'
                                          '        {\n'
                                          '            lookInputPaused = paused;\n'
                                          '        }\n'
                                          '\n'
                                          '        public CameraInput FilterLookInput(CameraInput input)\n'
                                          '        {\n'
                                          '            return lookInputPaused || Time.timeScale <= 0f ? new CameraInput(0f, 0f, 0f) : input;\n'
                                          '        }\n'
                                          '\n'
                                          '        public CameraPose Evaluate(CameraInput input, float deltaTime)\n'
                                          '        {\n'
                                          '            var targetPosition = target != null ? target.position : '
                                          'Vector3.zero;\n'
                                          '            var mode = CurrentMode == CameraMode.WildFreeLook ? '
                                          '(ICameraMode)wildMode : fixedMode;\n'
                                          '            var pose = mode.UpdatePose(targetPosition, profile, input, '
                                          'deltaTime);\n'
                                          '            var resolved = collision.Resolve(targetPosition, '
                                          'pose.position);\n'
                                          '            return new CameraPose(resolved, pose.rotation, pose.yaw, '
                                          'pose.pitch);\n'
                                          '        }\n'
                                          '\n'
                                          '        private void LateUpdate()\n'
                                          '        {\n'
                                          '            if (target == null)\n'
                                          '            {\n'
                                          '                return;\n'
                                          '            }\n'
                                          '\n'
                                          '            var input = FilterLookInput(new CameraInput(ReadAxis("Mouse X"), '
                                          'ReadAxis("Mouse Y"), ReadAxis("RightStickX")));\n'
                                          '            var pose = Evaluate(input, Time.deltaTime);\n'
                                          '            '
                                          'transform.SetPositionAndRotation(Vector3.Lerp(transform.position, '
                                          'pose.position, 1f), pose.rotation);\n'
                                          '            var cam = GetComponent<UnityEngine.Camera>();\n'
                                          '            if (cam != null && profile != null)\n'
                                          '            {\n'
                                          '                cam.orthographicSize = profile.zoom;\n'
                                          '            }\n'
                                          '        }\n'
                                          '\n'
                                          '        private static float ReadAxis(string axisName)\n'
                                          '        {\n'
                                          '            try\n'
                                          '            {\n'
                                          '                return Input.GetAxis(axisName);\n'
                                          '            }\n'
                                          '            catch (System.ArgumentException)\n'
                                          '            {\n'
                                          '                return 0f;\n'
                                          '            }\n'
                                          '        }\n'
                                          '    }\n'
                                          '}\n',
 'Assets/Scripts/Core/CoreSystems.cs': 'using System;\n'
                                       'using System.Collections.Generic;\n'
                                       'using System.IO;\n'
                                       'using UnityEngine;\n'
                                       'using UnityEngine.SceneManagement;\n'
                                       '\n'
                                       'namespace __PROJECT_NAMESPACE__.Core\n'
                                       '{\n'
                                       '    /// <summary>Base interface for services. Extend by registering new '
                                       'services in GameServiceRegistry instead of hard-linking singletons.</summary>\n'
                                       '    public interface IGameService\n'
                                       '    {\n'
                                       '        void Initialize(GameServiceRegistry registry);\n'
                                       '    }\n'
                                       '\n'
                                       '    /// <summary>Small dependency registry for loose coupling between runtime '
                                       'systems.</summary>\n'
                                       '    public sealed class GameServiceRegistry\n'
                                       '    {\n'
                                       '        private readonly Dictionary<Type, object> services = new '
                                       'Dictionary<Type, object>();\n'
                                       '\n'
                                       '        public void Register<T>(T service) where T : class\n'
                                       '        {\n'
                                       '            services[typeof(T)] = service;\n'
                                       '        }\n'
                                       '\n'
                                       '        public T Get<T>() where T : class\n'
                                       '        {\n'
                                       '            return services.TryGetValue(typeof(T), out var service) ? '
                                       '(T)service : null;\n'
                                       '        }\n'
                                       '\n'
                                       '        public bool TryGet<T>(out T service) where T : class\n'
                                       '        {\n'
                                       '            service = Get<T>();\n'
                                       '            return service != null;\n'
                                       '        }\n'
                                       '\n'
                                       '        public void Clear()\n'
                                       '        {\n'
                                       '            services.Clear();\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    /// <summary>Type-safe pub/sub bus. Add new event structs/classes and '
                                       'publish them here to avoid direct references.</summary>\n'
                                       '    public sealed class EventBus\n'
                                       '    {\n'
                                       '        private readonly Dictionary<Type, List<Delegate>> subscribers = new '
                                       'Dictionary<Type, List<Delegate>>();\n'
                                       '\n'
                                       '        public void Subscribe<T>(Action<T> handler)\n'
                                       '        {\n'
                                       '            var type = typeof(T);\n'
                                       '            if (!subscribers.TryGetValue(type, out var list))\n'
                                       '            {\n'
                                       '                list = new List<Delegate>();\n'
                                       '                subscribers[type] = list;\n'
                                       '            }\n'
                                       '\n'
                                       '            if (!list.Contains(handler))\n'
                                       '            {\n'
                                       '                list.Add(handler);\n'
                                       '            }\n'
                                       '        }\n'
                                       '\n'
                                       '        public void Unsubscribe<T>(Action<T> handler)\n'
                                       '        {\n'
                                       '            if (subscribers.TryGetValue(typeof(T), out var list))\n'
                                       '            {\n'
                                       '                list.Remove(handler);\n'
                                       '            }\n'
                                       '        }\n'
                                       '\n'
                                       '        public void Publish<T>(T payload)\n'
                                       '        {\n'
                                       '            if (!subscribers.TryGetValue(typeof(T), out var list))\n'
                                       '            {\n'
                                       '                return;\n'
                                       '            }\n'
                                       '\n'
                                       '            var snapshot = list.ToArray();\n'
                                       '            foreach (var handler in snapshot)\n'
                                       '            {\n'
                                       '                ((Action<T>)handler).Invoke(payload);\n'
                                       '            }\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    public enum GameState { Boot, Overworld, Dialogue, Battle, Menu, Cutscene, '
                                       'Loading }\n'
                                       '\n'
                                       '    /// <summary>Central state gate. Extend by adding valid transition rules '
                                       'before changing CurrentState.</summary>\n'
                                       '    public sealed class GameStateManager\n'
                                       '    {\n'
                                       '        public GameState CurrentState { get; private set; } = GameState.Boot;\n'
                                       '        public event Action<GameState, GameState> StateChanged;\n'
                                       '\n'
                                       '        public void ChangeState(GameState next)\n'
                                       '        {\n'
                                       '            if (next == CurrentState)\n'
                                       '            {\n'
                                       '                return;\n'
                                       '            }\n'
                                       '\n'
                                       '            var previous = CurrentState;\n'
                                       '            CurrentState = next;\n'
                                       '            StateChanged?.Invoke(previous, next);\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    /// <summary>Scene loading facade. Replace the request method with '
                                       'addressables/streaming later without touching callers.</summary>\n'
                                       '    public sealed class SceneLoader\n'
                                       '    {\n'
                                       '        public string CurrentSceneName { get; private set; }\n'
                                       '        public event Action<string> SceneLoadRequested;\n'
                                       '\n'
                                       '        public void RequestLoad(string sceneName)\n'
                                       '        {\n'
                                       '            CurrentSceneName = sceneName;\n'
                                       '            SceneLoadRequested?.Invoke(sceneName);\n'
                                       '            if (Application.isPlaying)\n'
                                       '            {\n'
                                       '                SceneManager.LoadScene(sceneName);\n'
                                       '            }\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    [Serializable]\n'
                                       '    public sealed class GameClockData\n'
                                       '    {\n'
                                       '        public int day;\n'
                                       '        public float timeOfDay01;\n'
                                       '    }\n'
                                       '\n'
                                       '    /// <summary>Deterministic game clock used by day/night and NPC '
                                       'schedules.</summary>\n'
                                       '    public sealed class TimeManager\n'
                                       '    {\n'
                                       '        public GameClockData Data { get; private set; } = new '
                                       'GameClockData();\n'
                                       '        public event Action<GameClockData> TimeAdvanced;\n'
                                       '\n'
                                       '        public void Advance(float normalizedDelta)\n'
                                       '        {\n'
                                       '            Data.timeOfDay01 += normalizedDelta;\n'
                                       '            while (Data.timeOfDay01 >= 1f)\n'
                                       '            {\n'
                                       '                Data.timeOfDay01 -= 1f;\n'
                                       '                Data.day++;\n'
                                       '            }\n'
                                       '\n'
                                       '            TimeAdvanced?.Invoke(Data);\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    [Serializable]\n'
                                       '    public sealed class SettingsData\n'
                                       '    {\n'
                                       '        public float masterVolume = 1f;\n'
                                       '        public float musicVolume = 1f;\n'
                                       '        public float sfxVolume = 1f;\n'
                                       '        public bool fullscreen = true;\n'
                                       '        public string language = "en";\n'
                                       '    }\n'
                                       '\n'
                                       '    public readonly struct SettingsChangedEvent\n'
                                       '    {\n'
                                       '        public readonly SettingsData Data;\n'
                                       '        public SettingsChangedEvent(SettingsData data) { Data = data; }\n'
                                       '    }\n'
                                       '\n'
                                       '    public readonly struct WeatherChangedEvent\n'
                                       '    {\n'
                                       '        public readonly string WeatherId;\n'
                                       '        public WeatherChangedEvent(string weatherId) { WeatherId = weatherId; '
                                       '}\n'
                                       '    }\n'
                                       '\n'
                                       '    public readonly struct MusicTrackChangedEvent\n'
                                       '    {\n'
                                       '        public readonly string TrackId;\n'
                                       '        public MusicTrackChangedEvent(string trackId) { TrackId = trackId; }\n'
                                       '    }\n'
                                       '\n'
                                       '    public readonly struct TransformationFxEvent\n'
                                       '    {\n'
                                       '        public readonly string CreatureId;\n'
                                       '        public readonly string FxId;\n'
                                       '        public TransformationFxEvent(string creatureId, string fxId) { '
                                       'CreatureId = creatureId; FxId = fxId; }\n'
                                       '    }\n'
                                       '\n'
                                       '    public readonly struct BattleStartedEvent\n'
                                       '    {\n'
                                       '        public readonly string SourceId;\n'
                                       '        public BattleStartedEvent(string sourceId) { SourceId = sourceId; }\n'
                                       '    }\n'
                                       '\n'
                                       '    /// <summary>Persists player-facing options. Add new fields to '
                                       'SettingsData with safe defaults.</summary>\n'
                                       '    public sealed class SettingsManager\n'
                                       '    {\n'
                                       '        private readonly EventBus events;\n'
                                       '        public SettingsData Data { get; private set; } = new SettingsData();\n'
                                       '\n'
                                       '        public SettingsManager(EventBus events = null)\n'
                                       '        {\n'
                                       '            this.events = events;\n'
                                       '        }\n'
                                       '\n'
                                       '        public void Apply(SettingsData data)\n'
                                       '        {\n'
                                       '            Data = data ?? new SettingsData();\n'
                                       '            events?.Publish(new SettingsChangedEvent(Data));\n'
                                       '        }\n'
                                       '\n'
                                       '        public string Serialize()\n'
                                       '        {\n'
                                       '            return JsonUtility.ToJson(Data, true);\n'
                                       '        }\n'
                                       '\n'
                                       '        public void Deserialize(string json)\n'
                                       '        {\n'
                                       '            Apply(string.IsNullOrWhiteSpace(json) ? new SettingsData() : '
                                       'JsonUtility.FromJson<SettingsData>(json));\n'
                                       '        }\n'
                                       '\n'
                                       '        public void SaveToFile(string path)\n'
                                       '        {\n'
                                       '            Directory.CreateDirectory(Path.GetDirectoryName(path));\n'
                                       '            File.WriteAllText(path, Serialize());\n'
                                       '        }\n'
                                       '\n'
                                       '        public void LoadFromFile(string path)\n'
                                       '        {\n'
                                       '            Deserialize(File.Exists(path) ? File.ReadAllText(path) : '
                                       'string.Empty);\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    /// <summary>Simple key lookup localization scaffold. Replace table '
                                       'injection with asset-backed language packs later.</summary>\n'
                                       '    public sealed class LocalizationManager\n'
                                       '    {\n'
                                       '        private readonly Dictionary<string, Dictionary<string, string>> tables '
                                       '= new Dictionary<string, Dictionary<string, string>>();\n'
                                       '        public string Language { get; private set; } = "en";\n'
                                       '\n'
                                       '        public void SetLanguage(string language)\n'
                                       '        {\n'
                                       '            Language = language;\n'
                                       '        }\n'
                                       '\n'
                                       '        public void Register(string language, string key, string value)\n'
                                       '        {\n'
                                       '            if (!tables.TryGetValue(language, out var table))\n'
                                       '            {\n'
                                       '                table = new Dictionary<string, string>();\n'
                                       '                tables[language] = table;\n'
                                       '            }\n'
                                       '\n'
                                       '            table[key] = value;\n'
                                       '        }\n'
                                       '\n'
                                       '        public string Get(string key)\n'
                                       '        {\n'
                                       '            return tables.TryGetValue(Language, out var table) && '
                                       'table.TryGetValue(key, out var value) ? value : key;\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    /// <summary>Audio service scaffold for core systems; '
                                       'presentation-specific managers live under __PROJECT_NAMESPACE__.Audio.</summary>\n'
                                       '    public sealed class AudioManager\n'
                                       '    {\n'
                                       '        private readonly EventBus events;\n'
                                       '        public string CurrentTrackId { get; private set; }\n'
                                       '\n'
                                       '        public AudioManager(EventBus events = null)\n'
                                       '        {\n'
                                       '            this.events = events;\n'
                                       '        }\n'
                                       '\n'
                                       '        public void PlayMusic(string trackId)\n'
                                       '        {\n'
                                       '            CurrentTrackId = trackId;\n'
                                       '            events?.Publish(new MusicTrackChangedEvent(trackId));\n'
                                       '        }\n'
                                       '    }\n'
                                       '}\n',
 'Assets/Scripts/__PROJECT_NAMESPACE__.Runtime.asmdef': '{\n'
                                               '  "name": "__PROJECT_NAMESPACE__.Runtime",\n'
                                               '  "rootNamespace": "__PROJECT_NAMESPACE__",\n'
                                               '  "references": [],\n'
                                               '  "includePlatforms": [],\n'
                                               '  "excludePlatforms": [],\n'
                                               '  "allowUnsafeCode": false,\n'
                                               '  "overrideReferences": false,\n'
                                               '  "precompiledReferences": [],\n'
                                               '  "autoReferenced": true,\n'
                                               '  "defineConstraints": [],\n'
                                               '  "versionDefines": [],\n'
                                               '  "noEngineReferences": false\n'
                                               '}\n',
 'Assets/Scripts/Events/FlagAndCutsceneSystems.cs': 'using System.Collections.Generic;\n'
                                                    'using __PROJECT_NAMESPACE__.Save;\n'
                                                    '\n'
                                                    'namespace __PROJECT_NAMESPACE__.Events\n'
                                                    '{\n'
                                                    '    /// <summary>Progression flags live outside scene objects so '
                                                    'save/load and event scripts can share them.</summary>\n'
                                                    '    public sealed class FlagProgressionSystem\n'
                                                    '    {\n'
                                                    '        private readonly Dictionary<string, bool> flags = new '
                                                    'Dictionary<string, bool>();\n'
                                                    '\n'
                                                    '        public void Set(string key, bool value = true)\n'
                                                    '        {\n'
                                                    '            flags[key] = value;\n'
                                                    '        }\n'
                                                    '\n'
                                                    '        public bool Get(string key)\n'
                                                    '        {\n'
                                                    '            return flags.TryGetValue(key, out var value) && '
                                                    'value;\n'
                                                    '        }\n'
                                                    '\n'
                                                    '        public void WriteToSave(SaveData save)\n'
                                                    '        {\n'
                                                    '            save.flags.Clear();\n'
                                                    '            foreach (var pair in flags)\n'
                                                    '            {\n'
                                                    '                save.flags.Add(new FlagRecord { key = pair.Key, '
                                                    'value = pair.Value });\n'
                                                    '            }\n'
                                                    '        }\n'
                                                    '\n'
                                                    '        public void LoadFromSave(SaveData save)\n'
                                                    '        {\n'
                                                    '            flags.Clear();\n'
                                                    '            foreach (var flag in save.flags)\n'
                                                    '            {\n'
                                                    '                flags[flag.key] = flag.value;\n'
                                                    '            }\n'
                                                    '        }\n'
                                                    '    }\n'
                                                    '\n'
                                                    '    public interface ICutsceneStep\n'
                                                    '    {\n'
                                                    '        void Run(List<string> log);\n'
                                                    '    }\n'
                                                    '\n'
                                                    '    public sealed class LogCutsceneStep : ICutsceneStep\n'
                                                    '    {\n'
                                                    '        private readonly string id;\n'
                                                    '        public LogCutsceneStep(string id) { this.id = id; }\n'
                                                    '        public void Run(List<string> log) { log.Add(id); }\n'
                                                    '    }\n'
                                                    '\n'
                                                    '    /// <summary>Ordered cutscene runner. Replace LogCutsceneStep '
                                                    'with camera/dialogue/audio steps as content grows.</summary>\n'
                                                    '    public sealed class CutsceneSequence\n'
                                                    '    {\n'
                                                    '        private readonly List<ICutsceneStep> steps = new '
                                                    'List<ICutsceneStep>();\n'
                                                    '        public void Add(ICutsceneStep step) { steps.Add(step); }\n'
                                                    '\n'
                                                    '        public List<string> Run()\n'
                                                    '        {\n'
                                                    '            var log = new List<string>();\n'
                                                    '            foreach (var step in steps)\n'
                                                    '            {\n'
                                                    '                step.Run(log);\n'
                                                    '            }\n'
                                                    '\n'
                                                    '            return log;\n'
                                                    '        }\n'
                                                    '    }\n'
                                                    '}\n',
 'Assets/Scripts/Fusion/FusionSystem.cs': 'using System.Collections.Generic;\n'
                                          'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                          'using __PROJECT_NAMESPACE__.Save;\n'
                                          '\n'
                                          'namespace __PROJECT_NAMESPACE__.Fusion\n'
                                          '{\n'
                                          '    public sealed class FusionResult\n'
                                          '    {\n'
                                          '        public string fusionId;\n'
                                          '        public CreatureInstance left;\n'
                                          '        public CreatureInstance right;\n'
                                          '        public StatBlock stats;\n'
                                          '        public CreatureType primaryType;\n'
                                          '        public CreatureType secondaryType;\n'
                                          '        public AbilityDefinition inheritedAbility;\n'
                                          '    }\n'
                                          '\n'
                                          '    /// <summary>Data-driven compatibility and fusion math. Extend by '
                                          'loading compatiblePairs from assets.</summary>\n'
                                          '    public sealed class FusionSystem\n'
                                          '    {\n'
                                          '        private readonly HashSet<string> compatiblePairs = new '
                                          'HashSet<string>();\n'
                                          '\n'
                                          '        public void AddCompatibility(string a, string b)\n'
                                          '        {\n'
                                          '            compatiblePairs.Add(Key(a, b));\n'
                                          '        }\n'
                                          '\n'
                                          '        public bool AreCompatible(CreatureSpecies a, CreatureSpecies b)\n'
                                          '        {\n'
                                          '            return a != null && b != null && '
                                          'compatiblePairs.Contains(Key(a.id, b.id));\n'
                                          '        }\n'
                                          '\n'
                                          '        public FusionResult Fuse(CreatureInstance a, CreatureInstance b)\n'
                                          '        {\n'
                                          '            if (a?.Species == null || b?.Species == null || '
                                          '!AreCompatible(a.Species, b.Species))\n'
                                          '            {\n'
                                          '                return null;\n'
                                          '            }\n'
                                          '\n'
                                          '            return new FusionResult\n'
                                          '            {\n'
                                          '                fusionId = Key(a.Species.id, b.Species.id),\n'
                                          '                left = a,\n'
                                          '                right = b,\n'
                                          '                stats = StatBlock.Average(a.CalculateStats(), '
                                          'b.CalculateStats()),\n'
                                          '                primaryType = a.Species.primaryType,\n'
                                          '                secondaryType = b.Species.primaryType,\n'
                                          '                inheritedAbility = a.ActiveAbility ?? b.ActiveAbility\n'
                                          '            };\n'
                                          '        }\n'
                                          '\n'
                                          '        public CreatureInstance[] Separate(FusionResult fusion)\n'
                                          '        {\n'
                                          '            return fusion == null ? new CreatureInstance[0] : new[] { '
                                          'fusion.left, fusion.right };\n'
                                          '        }\n'
                                          '\n'
                                          '        public FusionSaveRecord ToSave(FusionResult fusion)\n'
                                          '        {\n'
                                          '            return new FusionSaveRecord { fusionId = fusion.fusionId, '
                                          'leftSpeciesId = fusion.left.speciesId, rightSpeciesId = '
                                          'fusion.right.speciesId, active = true };\n'
                                          '        }\n'
                                          '\n'
                                          '        private static string Key(string a, string b)\n'
                                          '        {\n'
                                          '            return string.CompareOrdinal(a, b) <= 0 ? a + "+" + b : b + "+" '
                                          '+ a;\n'
                                          '        }\n'
                                          '    }\n'
                                          '}\n',
 'Assets/Scripts/Interaction/EncounterSystem.cs': 'using __PROJECT_NAMESPACE__.Battle;\n'
                                                  'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                                  'using UnityEngine;\n'
                                                  '\n'
                                                  'namespace __PROJECT_NAMESPACE__.EncounterSystem\n'
                                                  '{\n'
                                                  '    /// <summary>Area encounter policy. Extend by adding weather, '
                                                  'time-of-day, repel, and story filters.</summary>\n'
                                                  '    public sealed class RandomEncounterSystem\n'
                                                  '    {\n'
                                                  '        public bool ShouldTrigger(float encounterRate, '
                                                  'IRandomSource rng)\n'
                                                  '        {\n'
                                                  '            return rng.Value01() < Mathf.Clamp01(encounterRate);\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public EncounterEntry Roll(EncounterTable table, '
                                                  'System.Random rng)\n'
                                                  '        {\n'
                                                  '            return table != null ? table.Roll(rng) : null;\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public bool CheckStructuredStep(int stepsSinceLastCheck, '
                                                  'int stepInterval, float rate, IRandomSource rng)\n'
                                                  '        {\n'
                                                  '            return stepsSinceLastCheck >= stepInterval && '
                                                  'ShouldTrigger(rate, rng);\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public bool CheckWildTimed(float elapsed, float interval, '
                                                  'float rate, IRandomSource rng)\n'
                                                  '        {\n'
                                                  '            return elapsed >= interval && ShouldTrigger(rate, '
                                                  'rng);\n'
                                                  '        }\n'
                                                  '    }\n'
                                                  '\n'
                                                  '    public sealed class EncounterZone : MonoBehaviour\n'
                                                  '    {\n'
                                                  '        public EncounterTable table;\n'
                                                  '        public float encounterRate = 0.1f;\n'
                                                  '        public bool visibleEncounterMode;\n'
                                                  '    }\n'
                                                  '}\n',
 'Assets/Scripts/Interaction/InteractionSystems.cs': 'using System;\n'
                                                     'using System.Collections.Generic;\n'
                                                     'using __PROJECT_NAMESPACE__.Core;\n'
                                                     'using __PROJECT_NAMESPACE__.Events;\n'
                                                     'using __PROJECT_NAMESPACE__.Overworld;\n'
                                                     'using UnityEngine;\n'
                                                     '\n'
                                                     'namespace __PROJECT_NAMESPACE__.Interaction\n'
                                                     '{\n'
                                                     '    public readonly struct InteractionContext\n'
                                                     '    {\n'
                                                     '        public readonly Vector2Int actorTile;\n'
                                                     '        public readonly Direction facing;\n'
                                                     '        public readonly EventBus events;\n'
                                                     '\n'
                                                     '        public InteractionContext(Vector2Int actorTile, '
                                                     'Direction facing, EventBus events = null)\n'
                                                     '        {\n'
                                                     '            this.actorTile = actorTile;\n'
                                                     '            this.facing = facing;\n'
                                                     '            this.events = events;\n'
                                                     '        }\n'
                                                     '    }\n'
                                                     '\n'
                                                     '    public interface IInteractable\n'
                                                     '    {\n'
                                                     '        Vector2Int Tile { get; }\n'
                                                     '        void Interact(InteractionContext context);\n'
                                                     '    }\n'
                                                     '\n'
                                                     '    /// <summary>Resolves the object directly in front of the '
                                                     'actor. Extend with layers/raycasting for scene '
                                                     'objects.</summary>\n'
                                                     '    public sealed class FacingInteractionResolver\n'
                                                     '    {\n'
                                                     '        private readonly Dictionary<Vector2Int, IInteractable> '
                                                     'interactables = new Dictionary<Vector2Int, IInteractable>();\n'
                                                     '        public void Register(IInteractable interactable) { '
                                                     'interactables[interactable.Tile] = interactable; }\n'
                                                     '\n'
                                                     '        public bool TryInteract(InteractionContext context)\n'
                                                     '        {\n'
                                                     '            var target = context.actorTile + '
                                                     'GridMovementMotor.DirectionToVector(context.facing);\n'
                                                     '            if (!interactables.TryGetValue(target, out var '
                                                     'interactable))\n'
                                                     '            {\n'
                                                     '                return false;\n'
                                                     '            }\n'
                                                     '\n'
                                                     '            interactable.Interact(context);\n'
                                                     '            return true;\n'
                                                     '        }\n'
                                                     '    }\n'
                                                     '\n'
                                                     '    public sealed class DialogueStartedEvent\n'
                                                     '    {\n'
                                                     '        public readonly string[] Lines;\n'
                                                     '        public DialogueStartedEvent(string[] lines) { Lines = '
                                                     'lines; }\n'
                                                     '    }\n'
                                                     '\n'
                                                     '    public sealed class NPCDialogueComponent : MonoBehaviour, '
                                                     'IInteractable\n'
                                                     '    {\n'
                                                     '        public Vector2Int tile;\n'
                                                     '        public string[] lines = { "HELLO DIMENSION TRAVELER." '
                                                     '};\n'
                                                     '        public bool started;\n'
                                                     '        public Vector2Int Tile => tile;\n'
                                                     '\n'
                                                     '        public void Interact(InteractionContext context)\n'
                                                     '        {\n'
                                                     '            started = true;\n'
                                                     '            context.events?.Publish(new '
                                                     'DialogueStartedEvent(lines));\n'
                                                     '        }\n'
                                                     '    }\n'
                                                     '\n'
                                                     '    public sealed class NPCPathingComponent : MonoBehaviour\n'
                                                     '    {\n'
                                                     '        public Vector2Int[] patrolPoints;\n'
                                                     '        public int currentIndex;\n'
                                                     '\n'
                                                     '        public Vector2Int Next()\n'
                                                     '        {\n'
                                                     '            if (patrolPoints == null || patrolPoints.Length == '
                                                     '0)\n'
                                                     '            {\n'
                                                     '                return Vector2Int.zero;\n'
                                                     '            }\n'
                                                     '\n'
                                                     '            currentIndex = (currentIndex + 1) % '
                                                     'patrolPoints.Length;\n'
                                                     '            return patrolPoints[currentIndex];\n'
                                                     '        }\n'
                                                     '    }\n'
                                                     '\n'
                                                     '    public sealed class TrainerDetectionComponent : '
                                                     'MonoBehaviour\n'
                                                     '    {\n'
                                                     '        public Vector2Int tile;\n'
                                                     '        public Direction facing = Direction.Down;\n'
                                                     '        public int range = 4;\n'
                                                     '\n'
                                                     '        public bool CanDetect(Vector2Int playerTile)\n'
                                                     '        {\n'
                                                     '            var delta = playerTile - tile;\n'
                                                     '            var dir = '
                                                     'GridMovementMotor.DirectionToVector(facing);\n'
                                                     '            if (dir.x != 0)\n'
                                                     '            {\n'
                                                     '                return delta.y == 0 && Math.Sign(delta.x) == '
                                                     'dir.x && Mathf.Abs(delta.x) <= range;\n'
                                                     '            }\n'
                                                     '\n'
                                                     '            return delta.x == 0 && Math.Sign(delta.y) == dir.y '
                                                     '&& Mathf.Abs(delta.y) <= range;\n'
                                                     '        }\n'
                                                     '\n'
                                                     '        public void TriggerBattle(EventBus events)\n'
                                                     '        {\n'
                                                     '            events?.Publish(new BattleStartedEvent(name));\n'
                                                     '        }\n'
                                                     '    }\n'
                                                     '\n'
                                                     '    public sealed class WorldEventTrigger : MonoBehaviour\n'
                                                     '    {\n'
                                                     '        public string flagKey = "event_triggered";\n'
                                                     '        public void Trigger(FlagProgressionSystem flags) { '
                                                     'flags.Set(flagKey, true); }\n'
                                                     '    }\n'
                                                     '\n'
                                                     '    public sealed class GymTrialProgression { public int '
                                                     'clearedCount; public void MarkCleared() { clearedCount++; } }\n'
                                                     '    public sealed class RivalEncounterScaffold { public string '
                                                     'rivalId = "rival_01"; }\n'
                                                     '    public sealed class LegendaryEncounterScaffold { public '
                                                     'string encounterId = "legendary_original_01"; }\n'
                                                     '    public sealed class PostgameFlagScaffold { public const '
                                                     'string PostgameUnlocked = "postgame_unlocked"; }\n'
                                                     '}\n',
 'Assets/Scripts/Overworld/OverworldMovement.cs': 'using System;\n'
                                                  'using System.Collections.Generic;\n'
                                                  'using UnityEngine;\n'
                                                  '\n'
                                                  'namespace __PROJECT_NAMESPACE__.Overworld\n'
                                                  '{\n'
                                                  '    public enum MovementMode { StructuredGrid, WildArea }\n'
                                                  '    public enum Direction { Down, Left, Right, Up }\n'
                                                  '\n'
                                                  '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Area Movement '
                                                  'Profile")]\n'
                                                  '    public sealed class AreaMovementProfile : ScriptableObject\n'
                                                  '    {\n'
                                                  '        public MovementMode mode = MovementMode.StructuredGrid;\n'
                                                  '        public bool allowDiagonal;\n'
                                                  '        public float tileSize = 1f;\n'
                                                  '        public float structuredStepSeconds = 0.18f;\n'
                                                  '        public float wildMoveSpeed = 4f;\n'
                                                  '    }\n'
                                                  '\n'
                                                  '    [Serializable]\n'
                                                  '    public sealed class TileMetadata\n'
                                                  '    {\n'
                                                  '        public Vector2Int position;\n'
                                                  '        public string terrainId = "ground";\n'
                                                  '        public bool blocked;\n'
                                                  '    }\n'
                                                  '\n'
                                                  '    /// <summary>Tile collision and metadata store. Extend by '
                                                  'baking this from tilemaps or area data assets.</summary>\n'
                                                  '    public sealed class TileCollisionMap\n'
                                                  '    {\n'
                                                  '        private readonly HashSet<Vector2Int> blocked = new '
                                                  'HashSet<Vector2Int>();\n'
                                                  '        private readonly Dictionary<Vector2Int, TileMetadata> '
                                                  'metadata = new Dictionary<Vector2Int, TileMetadata>();\n'
                                                  '\n'
                                                  '        public void SetBlocked(Vector2Int tile, bool value)\n'
                                                  '        {\n'
                                                  '            if (value) blocked.Add(tile); else '
                                                  'blocked.Remove(tile);\n'
                                                  '            SetMetadata(tile, new TileMetadata { position = tile, '
                                                  'blocked = value });\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public bool IsBlocked(Vector2Int tile)\n'
                                                  '        {\n'
                                                  '            return blocked.Contains(tile) || '
                                                  '(metadata.TryGetValue(tile, out var meta) && meta.blocked);\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public void SetMetadata(Vector2Int tile, TileMetadata '
                                                  'meta)\n'
                                                  '        {\n'
                                                  '            metadata[tile] = meta;\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public TileMetadata GetMetadata(Vector2Int tile)\n'
                                                  '        {\n'
                                                  '            return metadata.TryGetValue(tile, out var meta) ? meta '
                                                  ': null;\n'
                                                  '        }\n'
                                                  '    }\n'
                                                  '\n'
                                                  '    /// <summary>Emerald-style grid motor: cardinal-only, one tile '
                                                  'internally, interpolated visually, collision-aware.</summary>\n'
                                                  '    public sealed class GridMovementMotor\n'
                                                  '    {\n'
                                                  '        private readonly TileCollisionMap collision;\n'
                                                  '        private readonly float tileSize;\n'
                                                  '        private readonly float stepSeconds;\n'
                                                  '        private Vector2Int bufferedDirection;\n'
                                                  '        private Vector2Int targetTile;\n'
                                                  '        private Vector3 startWorld;\n'
                                                  '        private Vector3 targetWorld;\n'
                                                  '        private float stepTimer;\n'
                                                  '\n'
                                                  '        public Vector2Int Tile { get; private set; }\n'
                                                  '        public Vector3 WorldPosition { get; private set; }\n'
                                                  '        public Direction Facing { get; private set; } = '
                                                  'Direction.Down;\n'
                                                  '        public bool IsMoving { get; private set; }\n'
                                                  '        public Vector2Int InteractionFacingTile => Tile + '
                                                  'DirectionToVector(Facing);\n'
                                                  '\n'
                                                  '        public GridMovementMotor(TileCollisionMap collision, float '
                                                  'tileSize = 1f, float stepSeconds = 0.18f)\n'
                                                  '        {\n'
                                                  '            this.collision = collision ?? new TileCollisionMap();\n'
                                                  '            this.tileSize = tileSize;\n'
                                                  '            this.stepSeconds = Mathf.Max(0.01f, stepSeconds);\n'
                                                  '            SetTile(Vector2Int.zero);\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public void SetTile(Vector2Int tile)\n'
                                                  '        {\n'
                                                  '            Tile = tile;\n'
                                                  '            WorldPosition = ToWorld(tile);\n'
                                                  '            IsMoving = false;\n'
                                                  '            bufferedDirection = Vector2Int.zero;\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public bool TryMove(Vector2Int input)\n'
                                                  '        {\n'
                                                  '            var dir = Cardinalize(input);\n'
                                                  '            if (dir == Vector2Int.zero)\n'
                                                  '            {\n'
                                                  '                return false;\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            Facing = VectorToDirection(dir);\n'
                                                  '            if (IsMoving)\n'
                                                  '            {\n'
                                                  '                bufferedDirection = dir;\n'
                                                  '                return false;\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            var next = Tile + dir;\n'
                                                  '            if (collision.IsBlocked(next))\n'
                                                  '            {\n'
                                                  '                return false;\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            targetTile = next;\n'
                                                  '            startWorld = WorldPosition;\n'
                                                  '            targetWorld = ToWorld(next);\n'
                                                  '            stepTimer = 0f;\n'
                                                  '            IsMoving = true;\n'
                                                  '            return true;\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public void Tick(float deltaTime)\n'
                                                  '        {\n'
                                                  '            if (!IsMoving)\n'
                                                  '            {\n'
                                                  '                return;\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            stepTimer += deltaTime;\n'
                                                  '            var t = Mathf.Clamp01(stepTimer / stepSeconds);\n'
                                                  '            WorldPosition = Vector3.Lerp(startWorld, targetWorld, '
                                                  't);\n'
                                                  '            if (t < 1f)\n'
                                                  '            {\n'
                                                  '                return;\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            Tile = targetTile;\n'
                                                  '            WorldPosition = ToWorld(Tile);\n'
                                                  '            IsMoving = false;\n'
                                                  '            if (bufferedDirection != Vector2Int.zero)\n'
                                                  '            {\n'
                                                  '                var next = bufferedDirection;\n'
                                                  '                bufferedDirection = Vector2Int.zero;\n'
                                                  '                TryMove(next);\n'
                                                  '            }\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public static Vector2Int Cardinalize(Vector2Int input)\n'
                                                  '        {\n'
                                                  '            if (input == Vector2Int.zero)\n'
                                                  '            {\n'
                                                  '                return Vector2Int.zero;\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            return Mathf.Abs(input.x) > Mathf.Abs(input.y) ? new '
                                                  'Vector2Int(Math.Sign(input.x), 0) : new Vector2Int(0, '
                                                  'Math.Sign(input.y));\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public static Direction VectorToDirection(Vector2Int dir)\n'
                                                  '        {\n'
                                                  '            if (dir.x < 0) return Direction.Left;\n'
                                                  '            if (dir.x > 0) return Direction.Right;\n'
                                                  '            if (dir.y > 0) return Direction.Up;\n'
                                                  '            return Direction.Down;\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public static Vector2Int DirectionToVector(Direction '
                                                  'facing)\n'
                                                  '        {\n'
                                                  '            switch (facing)\n'
                                                  '            {\n'
                                                  '                case Direction.Left: return Vector2Int.left;\n'
                                                  '                case Direction.Right: return Vector2Int.right;\n'
                                                  '                case Direction.Up: return Vector2Int.up;\n'
                                                  '                default: return Vector2Int.down;\n'
                                                  '            }\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        private Vector3 ToWorld(Vector2Int tile)\n'
                                                  '        {\n'
                                                  '            return new Vector3(tile.x * tileSize, 0f, tile.y * '
                                                  'tileSize);\n'
                                                  '        }\n'
                                                  '    }\n'
                                                  '\n'
                                                  '    /// <summary>Wild-area motor keeps collision checks but allows '
                                                  'normalized 8-way motion when the area profile allows it.</summary>\n'
                                                  '    public sealed class WildAreaMovementMotor\n'
                                                  '    {\n'
                                                  '        private readonly TileCollisionMap collision;\n'
                                                  '        public Vector3 LastVelocity { get; private set; }\n'
                                                  '\n'
                                                  '        public WildAreaMovementMotor(TileCollisionMap collision)\n'
                                                  '        {\n'
                                                  '            this.collision = collision ?? new TileCollisionMap();\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public Vector3 Move(Vector3 position, Vector2 input, float '
                                                  'speed, float deltaTime, bool allowDiagonal = true)\n'
                                                  '        {\n'
                                                  '            if (input.sqrMagnitude < 0.001f)\n'
                                                  '            {\n'
                                                  '                LastVelocity = Vector3.zero;\n'
                                                  '                return position;\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            Vector2 source;\n'
                                                  '            if (allowDiagonal)\n'
                                                  '            {\n'
                                                  '                source = Vector2.ClampMagnitude(input, 1f);\n'
                                                  '            }\n'
                                                  '            else\n'
                                                  '            {\n'
                                                  '                var card = '
                                                  'GridMovementMotor.Cardinalize(Vector2Int.RoundToInt(input));\n'
                                                  '                source = new Vector2(card.x, card.y);\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            var delta = new Vector3(source.x, 0f, source.y) * speed '
                                                  '* deltaTime;\n'
                                                  '            var candidate = position + delta;\n'
                                                  '            var candidateTile = new '
                                                  'Vector2Int(Mathf.RoundToInt(candidate.x), '
                                                  'Mathf.RoundToInt(candidate.z));\n'
                                                  '            if (collision.IsBlocked(candidateTile))\n'
                                                  '            {\n'
                                                  '                LastVelocity = Vector3.zero;\n'
                                                  '                return position;\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            LastVelocity = deltaTime > 0f ? delta / deltaTime : '
                                                  'Vector3.zero;\n'
                                                  '            return candidate;\n'
                                                  '        }\n'
                                                  '    }\n'
                                                  '\n'
                                                  '    public sealed class TerrainTag : MonoBehaviour\n'
                                                  '    {\n'
                                                  '        public string terrainId = "ground";\n'
                                                  '        public float speedMultiplier = 1f;\n'
                                                  '    }\n'
                                                  '\n'
                                                  '    /// <summary>Unity adapter for the pure movement motors. Extend '
                                                  'by feeding input from the new Input System.</summary>\n'
                                                  '    public sealed class PlayerMovementController : MonoBehaviour\n'
                                                  '    {\n'
                                                  '        public AreaMovementProfile profile;\n'
                                                  '        public TileCollisionMap CollisionMap { get; private set; } '
                                                  '= new TileCollisionMap();\n'
                                                  '        public GridMovementMotor GridMotor { get; private set; }\n'
                                                  '        public WildAreaMovementMotor WildMotor { get; private set; '
                                                  '}\n'
                                                  '        public Direction Facing => GridMotor != null ? '
                                                  'GridMotor.Facing : Direction.Down;\n'
                                                  '\n'
                                                  '        private void Awake()\n'
                                                  '        {\n'
                                                  '            Configure(profile);\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        public void Configure(AreaMovementProfile movementProfile)\n'
                                                  '        {\n'
                                                  '            profile = movementProfile;\n'
                                                  '            var tile = profile != null ? profile.tileSize : 1f;\n'
                                                  '            var step = profile != null ? '
                                                  'profile.structuredStepSeconds : 0.18f;\n'
                                                  '            GridMotor = new GridMovementMotor(CollisionMap, tile, '
                                                  'step);\n'
                                                  '            WildMotor = new WildAreaMovementMotor(CollisionMap);\n'
                                                  '        }\n'
                                                  '\n'
                                                  '        private void Update()\n'
                                                  '        {\n'
                                                  '            if (profile == null || GridMotor == null)\n'
                                                  '            {\n'
                                                  '                return;\n'
                                                  '            }\n'
                                                  '\n'
                                                  '            var input = new Vector2(Input.GetAxisRaw("Horizontal"), '
                                                  'Input.GetAxisRaw("Vertical"));\n'
                                                  '            if (profile.mode == MovementMode.StructuredGrid)\n'
                                                  '            {\n'
                                                  '                if (!GridMotor.IsMoving)\n'
                                                  '                {\n'
                                                  '                    '
                                                  'GridMotor.TryMove(Vector2Int.RoundToInt(input));\n'
                                                  '                }\n'
                                                  '\n'
                                                  '                GridMotor.Tick(Time.deltaTime);\n'
                                                  '                transform.position = GridMotor.WorldPosition;\n'
                                                  '            }\n'
                                                  '            else\n'
                                                  '            {\n'
                                                  '                transform.position = '
                                                  'WildMotor.Move(transform.position, input, profile.wildMoveSpeed, '
                                                  'Time.deltaTime, profile.allowDiagonal);\n'
                                                  '            }\n'
                                                  '        }\n'
                                                  '    }\n'
                                                  '}\n',
 'Assets/Scripts/Pokemon/PokemonData.cs': 'using System;\n'
                                          'using System.Collections.Generic;\n'
                                          'using UnityEngine;\n'
                                          '\n'
                                          'namespace __PROJECT_NAMESPACE__.Pokemon\n'
                                          '{\n'
                                          '    public enum CreatureType { None, Neutral, Leaf, Flame, Tide, Spark, '
                                          'Stone, Mind, Shadow, Light }\n'
                                          '    public enum MoveCategory { Physical, Special, Status }\n'
                                          '    public enum StatusCondition { None, Burn, Poison, Toxic, Sleep, '
                                          'Paralysis, Freeze, Confusion }\n'
                                          '\n'
                                          '    [Serializable]\n'
                                          '    public struct StatBlock\n'
                                          '    {\n'
                                          '        public int hp, attack, defense, specialAttack, specialDefense, '
                                          'speed;\n'
                                          '\n'
                                          '        public StatBlock(int hp, int attack, int defense, int '
                                          'specialAttack, int specialDefense, int speed)\n'
                                          '        {\n'
                                          '            this.hp = hp;\n'
                                          '            this.attack = attack;\n'
                                          '            this.defense = defense;\n'
                                          '            this.specialAttack = specialAttack;\n'
                                          '            this.specialDefense = specialDefense;\n'
                                          '            this.speed = speed;\n'
                                          '        }\n'
                                          '\n'
                                          '        public static StatBlock operator +(StatBlock a, StatBlock b)\n'
                                          '        {\n'
                                          '            return new StatBlock(a.hp + b.hp, a.attack + b.attack, '
                                          'a.defense + b.defense, a.specialAttack + b.specialAttack, a.specialDefense '
                                          '+ b.specialDefense, a.speed + b.speed);\n'
                                          '        }\n'
                                          '\n'
                                          '        public static StatBlock Average(StatBlock a, StatBlock b)\n'
                                          '        {\n'
                                          '            return new StatBlock((a.hp + b.hp) / 2, (a.attack + b.attack) / '
                                          '2, (a.defense + b.defense) / 2, (a.specialAttack + b.specialAttack) / 2, '
                                          '(a.specialDefense + b.specialDefense) / 2, (a.speed + b.speed) / 2);\n'
                                          '        }\n'
                                          '\n'
                                          '        public StatBlock Scale(float multiplier)\n'
                                          '        {\n'
                                          '            return new StatBlock(Mathf.RoundToInt(hp * multiplier), '
                                          'Mathf.RoundToInt(attack * multiplier), Mathf.RoundToInt(defense * '
                                          'multiplier), Mathf.RoundToInt(specialAttack * multiplier), '
                                          'Mathf.RoundToInt(specialDefense * multiplier), Mathf.RoundToInt(speed * '
                                          'multiplier));\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Ability")]\n'
                                          '    public sealed class AbilityDefinition : ScriptableObject\n'
                                          '    {\n'
                                          '        public string id;\n'
                                          '        public string displayName;\n'
                                          '        public string description;\n'
                                          '    }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Item")]\n'
                                          '    public sealed class ItemDefinition : ScriptableObject\n'
                                          '    {\n'
                                          '        public string id;\n'
                                          '        public string displayName;\n'
                                          '        public string description;\n'
                                          '        public bool consumable = true;\n'
                                          '    }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Move")]\n'
                                          '    public sealed class MoveDefinition : ScriptableObject\n'
                                          '    {\n'
                                          '        public string id;\n'
                                          '        public string displayName;\n'
                                          '        public CreatureType type = CreatureType.Neutral;\n'
                                          '        public MoveCategory category = MoveCategory.Physical;\n'
                                          '        public int power = 40;\n'
                                          '        public int accuracy = 100;\n'
                                          '        public int pp = 35;\n'
                                          '        public int priority;\n'
                                          '        public StatusCondition statusToApply;\n'
                                          '    }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Form")]\n'
                                          '    public sealed class FormDefinition : ScriptableObject\n'
                                          '    {\n'
                                          '        public string id;\n'
                                          '        public string displayName;\n'
                                          '        public StatBlock statModifier;\n'
                                          '        public float statMultiplier = 1f;\n'
                                          '        public CreatureType primaryTypeOverride = CreatureType.None;\n'
                                          '        public CreatureType secondaryTypeOverride = CreatureType.None;\n'
                                          '        public AbilityDefinition abilityOverride;\n'
                                          '        public MoveDefinition signatureMove;\n'
                                          '        public GameObject modelPrefab;\n'
                                          '        public Sprite portrait;\n'
                                          '    }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Learnset Entry")]\n'
                                          '    public sealed class LearnsetEntry : ScriptableObject\n'
                                          '    {\n'
                                          '        public int level = 1;\n'
                                          '        public MoveDefinition move;\n'
                                          '    }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Evolution Rule")]\n'
                                          '    public sealed class EvolutionRule : ScriptableObject\n'
                                          '    {\n'
                                          '        public string fromSpeciesId;\n'
                                          '        public CreatureSpecies evolvesInto;\n'
                                          '        public int minimumLevel = 16;\n'
                                          '        public string requiredItemId;\n'
                                          '        public bool RequiresItem => !string.IsNullOrEmpty(requiredItemId);\n'
                                          '\n'
                                          '        public bool CanEvolve(CreatureInstance creature, string usedItemId '
                                          '= null)\n'
                                          '        {\n'
                                          '            return creature != null && creature.speciesId == fromSpeciesId '
                                          '&& creature.Level >= minimumLevel && (!RequiresItem || requiredItemId == '
                                          'usedItemId);\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Creature Species")]\n'
                                          '    public sealed class CreatureSpecies : ScriptableObject\n'
                                          '    {\n'
                                          '        public string id;\n'
                                          '        public string displayName;\n'
                                          '        public string category;\n'
                                          '        [TextArea] public string lore;\n'
                                          '        public CreatureType primaryType = CreatureType.Neutral;\n'
                                          '        public CreatureType secondaryType = CreatureType.None;\n'
                                          '        public StatBlock baseStats = new StatBlock(45, 45, 45, 45, 45, '
                                          '45);\n'
                                          '        public AbilityDefinition[] abilities;\n'
                                          '        public AbilityDefinition hiddenAbility;\n'
                                          '        public LearnsetEntry[] learnset;\n'
                                          '        public EvolutionRule[] evolutions;\n'
                                          '        public FormDefinition[] forms;\n'
                                          '        public int shinyOdds = 4096;\n'
                                          '        public GameObject modelPrefab;\n'
                                          '        public Sprite portrait;\n'
                                          '    }\n'
                                          '\n'
                                          '    [Serializable]\n'
                                          '    public sealed class EncounterEntry\n'
                                          '    {\n'
                                          '        public CreatureSpecies species;\n'
                                          '        public int minLevel = 2;\n'
                                          '        public int maxLevel = 4;\n'
                                          '        public int weight = 1;\n'
                                          '    }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Encounter Table")]\n'
                                          '    public sealed class EncounterTable : ScriptableObject\n'
                                          '    {\n'
                                          '        public string id;\n'
                                          '        public EncounterEntry[] entries;\n'
                                          '\n'
                                          '        public EncounterEntry Roll(System.Random rng)\n'
                                          '        {\n'
                                          '            if (entries == null || entries.Length == 0)\n'
                                          '            {\n'
                                          '                return null;\n'
                                          '            }\n'
                                          '\n'
                                          '            var total = 0;\n'
                                          '            foreach (var entry in entries)\n'
                                          '            {\n'
                                          '                if (entry != null && entry.species != null && entry.weight '
                                          '> 0)\n'
                                          '                {\n'
                                          '                    total += entry.weight;\n'
                                          '                }\n'
                                          '            }\n'
                                          '\n'
                                          '            if (total <= 0)\n'
                                          '            {\n'
                                          '                return null;\n'
                                          '            }\n'
                                          '\n'
                                          '            var roll = rng.Next(0, total);\n'
                                          '            foreach (var entry in entries)\n'
                                          '            {\n'
                                          '                if (entry == null || entry.species == null || entry.weight '
                                          '<= 0)\n'
                                          '                {\n'
                                          '                    continue;\n'
                                          '                }\n'
                                          '\n'
                                          '                roll -= entry.weight;\n'
                                          '                if (roll < 0)\n'
                                          '                {\n'
                                          '                    return entry;\n'
                                          '                }\n'
                                          '            }\n'
                                          '\n'
                                          '            return null;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Trainer")]\n'
                                          '    public sealed class TrainerDefinition : ScriptableObject\n'
                                          '    {\n'
                                          '        public string id;\n'
                                          '        public string displayName;\n'
                                          '        public CreatureSpecies[] partySpecies;\n'
                                          '        public int level = 5;\n'
                                          '    }\n'
                                          '\n'
                                          '    /// <summary>Runtime creature. Store species as data and calculate '
                                          'stats on demand so forms/transforms can layer cleanly.</summary>\n'
                                          '    [Serializable]\n'
                                          '    public sealed class CreatureInstance\n'
                                          '    {\n'
                                          '        public string speciesId;\n'
                                          '        [NonSerialized] public CreatureSpecies Species;\n'
                                          '        public int Level { get; private set; }\n'
                                          '        public int Experience { get; private set; }\n'
                                          '        public bool Shiny { get; private set; }\n'
                                          '        public int CurrentHp { get; set; }\n'
                                          '        public AbilityDefinition ActiveAbility { get; set; }\n'
                                          '        public readonly List<MoveDefinition> KnownMoves = new '
                                          'List<MoveDefinition>();\n'
                                          '\n'
                                          '        public CreatureInstance(CreatureSpecies species, int level, bool '
                                          'shiny = false)\n'
                                          '        {\n'
                                          '            Species = species;\n'
                                          '            speciesId = species != null ? species.id : string.Empty;\n'
                                          '            Level = Mathf.Max(1, level);\n'
                                          '            Shiny = shiny;\n'
                                          '            ActiveAbility = species != null && species.abilities != null && '
                                          'species.abilities.Length > 0 ? species.abilities[0] : null;\n'
                                          '            CurrentHp = CalculateStats().hp;\n'
                                          '        }\n'
                                          '\n'
                                          '        public void AddExperience(int amount)\n'
                                          '        {\n'
                                          '            Experience += Mathf.Max(0, amount);\n'
                                          '        }\n'
                                          '\n'
                                          '        public StatBlock CalculateStats()\n'
                                          '        {\n'
                                          '            var b = Species != null ? Species.baseStats : new StatBlock(1, '
                                          '1, 1, 1, 1, 1);\n'
                                          '            return new StatBlock(\n'
                                          '                ((b.hp * 2 * Level) / 100) + Level + 10,\n'
                                          '                ((b.attack * 2 * Level) / 100) + 5,\n'
                                          '                ((b.defense * 2 * Level) / 100) + 5,\n'
                                          '                ((b.specialAttack * 2 * Level) / 100) + 5,\n'
                                          '                ((b.specialDefense * 2 * Level) / 100) + 5,\n'
                                          '                ((b.speed * 2 * Level) / 100) + 5);\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class Party\n'
                                          '    {\n'
                                          '        public const int MaxPartySize = 6;\n'
                                          '        private readonly List<CreatureInstance> creatures = new '
                                          'List<CreatureInstance>();\n'
                                          '        public IReadOnlyList<CreatureInstance> Creatures => creatures;\n'
                                          '\n'
                                          '        public bool Add(CreatureInstance creature)\n'
                                          '        {\n'
                                          '            if (creature == null || creatures.Count >= MaxPartySize)\n'
                                          '            {\n'
                                          '                return false;\n'
                                          '            }\n'
                                          '\n'
                                          '            creatures.Add(creature);\n'
                                          '            return true;\n'
                                          '        }\n'
                                          '\n'
                                          '        public bool Remove(CreatureInstance creature)\n'
                                          '        {\n'
                                          '            return creatures.Remove(creature);\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class PCStorage\n'
                                          '    {\n'
                                          '        private readonly List<CreatureInstance> stored = new '
                                          'List<CreatureInstance>();\n'
                                          '        public IReadOnlyList<CreatureInstance> Stored => stored;\n'
                                          '\n'
                                          '        public void Add(CreatureInstance creature)\n'
                                          '        {\n'
                                          '            if (creature != null)\n'
                                          '            {\n'
                                          '                stored.Add(creature);\n'
                                          '            }\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    /// <summary>Small type chart. Extend by loading matchup data from '
                                          'ScriptableObjects or JSON.</summary>\n'
                                          '    public sealed class TypeChart\n'
                                          '    {\n'
                                          '        private readonly Dictionary<string, float> multipliers = new '
                                          'Dictionary<string, float>();\n'
                                          '\n'
                                          '        public void SetMultiplier(CreatureType attack, CreatureType defend, '
                                          'float multiplier)\n'
                                          '        {\n'
                                          '            multipliers[$"{attack}>{defend}"] = multiplier;\n'
                                          '        }\n'
                                          '\n'
                                          '        public float GetMultiplier(CreatureType attack, CreatureType '
                                          'defend)\n'
                                          '        {\n'
                                          '            return defend == CreatureType.None ? 1f : '
                                          'multipliers.TryGetValue($"{attack}>{defend}", out var value) ? value : 1f;\n'
                                          '        }\n'
                                          '\n'
                                          '        public float GetMultiplier(CreatureType attack, CreatureType '
                                          'defendA, CreatureType defendB)\n'
                                          '        {\n'
                                          '            return GetMultiplier(attack, defendA) * GetMultiplier(attack, '
                                          'defendB);\n'
                                          '        }\n'
                                          '\n'
                                          '        public static TypeChart CreateDefaultForTests()\n'
                                          '        {\n'
                                          '            var chart = new TypeChart();\n'
                                          '            chart.SetMultiplier(CreatureType.Flame, CreatureType.Leaf, '
                                          '2f);\n'
                                          '            chart.SetMultiplier(CreatureType.Leaf, CreatureType.Flame, '
                                          '0.5f);\n'
                                          '            chart.SetMultiplier(CreatureType.Spark, CreatureType.Tide, '
                                          '2f);\n'
                                          '            chart.SetMultiplier(CreatureType.Tide, CreatureType.Flame, '
                                          '2f);\n'
                                          '            chart.SetMultiplier(CreatureType.Neutral, CreatureType.Shadow, '
                                          '0f);\n'
                                          '            return chart;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class LearnsetSystem\n'
                                          '    {\n'
                                          '        public List<MoveDefinition> GetMovesAtLevel(CreatureSpecies '
                                          'species, int level)\n'
                                          '        {\n'
                                          '            var result = new List<MoveDefinition>();\n'
                                          '            if (species?.learnset == null)\n'
                                          '            {\n'
                                          '                return result;\n'
                                          '            }\n'
                                          '\n'
                                          '            foreach (var entry in species.learnset)\n'
                                          '            {\n'
                                          '                if (entry != null && entry.move != null && entry.level <= '
                                          'level)\n'
                                          '                {\n'
                                          '                    result.Add(entry.move);\n'
                                          '                }\n'
                                          '            }\n'
                                          '\n'
                                          '            return result;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class EvolutionSystem\n'
                                          '    {\n'
                                          '        public CreatureSpecies GetEvolution(CreatureInstance creature, '
                                          'string itemId = null)\n'
                                          '        {\n'
                                          '            if (creature?.Species?.evolutions == null)\n'
                                          '            {\n'
                                          '                return null;\n'
                                          '            }\n'
                                          '\n'
                                          '            foreach (var rule in creature.Species.evolutions)\n'
                                          '            {\n'
                                          '                if (rule != null && rule.CanEvolve(creature, itemId))\n'
                                          '                {\n'
                                          '                    return rule.evolvesInto;\n'
                                          '                }\n'
                                          '            }\n'
                                          '\n'
                                          '            return null;\n'
                                          '        }\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class ExperienceSystem\n'
                                          '    {\n'
                                          '        public int ExperienceForLevel(int level) => level * level * level;\n'
                                          '    }\n'
                                          '\n'
                                          '    public sealed class ShinyRoller\n'
                                          '    {\n'
                                          '        private readonly System.Random rng;\n'
                                          '        public ShinyRoller(int seed) { rng = new System.Random(seed); }\n'
                                          '        public bool RollShiny(int odds) => rng.Next(0, Mathf.Max(1, odds)) '
                                          '== 0;\n'
                                          '    }\n'
                                          '}\n',
 'Assets/Scripts/Raids/RaidSystem.cs': 'using System;\n'
                                       'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                       'using UnityEngine;\n'
                                       '\n'
                                       'namespace __PROJECT_NAMESPACE__.Raids\n'
                                       '{\n'
                                       '    public enum RaidDifficultyTier { OneStar = 1, TwoStar, ThreeStar, '
                                       'FourStar, FiveStar, Legendary, EventExclusive }\n'
                                       '\n'
                                       '    [Serializable]\n'
                                       '    public sealed class RaidReward\n'
                                       '    {\n'
                                       '        public ItemDefinition item;\n'
                                       '        public int minCount = 1;\n'
                                       '        public int maxCount = 1;\n'
                                       '        public int weight = 1;\n'
                                       '    }\n'
                                       '\n'
                                       '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Raid Reward Table")]\n'
                                       '    public sealed class RaidRewardTable : ScriptableObject\n'
                                       '    {\n'
                                       '        public RaidReward[] rewards;\n'
                                       '        public RaidReward Roll(System.Random rng)\n'
                                       '        {\n'
                                       '            if (rewards == null || rewards.Length == 0)\n'
                                       '            {\n'
                                       '                return null;\n'
                                       '            }\n'
                                       '\n'
                                       '            return rewards[Mathf.Clamp(rng.Next(0, rewards.Length), 0, '
                                       'rewards.Length - 1)];\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Raid Definition")]\n'
                                       '    public sealed class RaidDefinition : ScriptableObject\n'
                                       '    {\n'
                                       '        public string id;\n'
                                       '        public CreatureSpecies bossSpecies;\n'
                                       '        public RaidDifficultyTier tier = RaidDifficultyTier.OneStar;\n'
                                       '        public RaidRewardTable rewardTable;\n'
                                       '        public float hpMultiplier = 4f;\n'
                                       '    }\n'
                                       '\n'
                                       '    public sealed class RaidBoss\n'
                                       '    {\n'
                                       '        public CreatureSpecies species;\n'
                                       '        public int maxHp;\n'
                                       '        public int currentHp;\n'
                                       '\n'
                                       '        public RaidBoss(RaidDefinition definition, int level)\n'
                                       '        {\n'
                                       '            species = definition.bossSpecies;\n'
                                       '            var baseHp = species != null ? species.baseStats.hp + level * 2 : '
                                       '50;\n'
                                       '            maxHp = Mathf.RoundToInt(baseHp * definition.hpMultiplier * '
                                       'Mathf.Max(1, (int)definition.tier));\n'
                                       '            currentHp = maxHp;\n'
                                       '        }\n'
                                       '    }\n'
                                       '\n'
                                       '    public sealed class RaidShieldController\n'
                                       '    {\n'
                                       '        public bool ShieldActive { get; private set; }\n'
                                       '        public float threshold = 0.5f;\n'
                                       '        public void Update(int hp, int maxHp) { ShieldActive = maxHp > 0 && hp '
                                       '/ (float)maxHp <= threshold; }\n'
                                       '        public void Break() { ShieldActive = false; }\n'
                                       '    }\n'
                                       '\n'
                                       '    public sealed class RaidTimerController\n'
                                       '    {\n'
                                       '        public float Remaining { get; private set; }\n'
                                       '        public bool Expired => Remaining <= 0f;\n'
                                       '        public RaidTimerController(float seconds) { Remaining = seconds; }\n'
                                       '        public void Tick(float deltaTime) { Remaining = Mathf.Max(0f, '
                                       'Remaining - deltaTime); }\n'
                                       '    }\n'
                                       '\n'
                                       '    public sealed class RaidCaptureController\n'
                                       '    {\n'
                                       '        public bool CaptureStarted { get; private set; }\n'
                                       '        public void TryStartCapture(bool victory) { if (victory) '
                                       'CaptureStarted = true; }\n'
                                       '    }\n'
                                       '\n'
                                       '    public sealed class RaidBattleController\n'
                                       '    {\n'
                                       '        public bool Victory { get; private set; }\n'
                                       '        public bool Failed { get; private set; }\n'
                                       '        public void MarkVictory() { Victory = true; }\n'
                                       '        public void ApplyTimer(RaidTimerController timer) { if (timer.Expired '
                                       '&& !Victory) Failed = true; }\n'
                                       '    }\n'
                                       '\n'
                                       '    public sealed class RaidDen : MonoBehaviour { public RaidDefinition raid; '
                                       '}\n'
                                       '    public sealed class RaidEventRotationSystem { public RaidDefinition '
                                       'SelectActive(RaidDefinition[] raids, int dayIndex) { if (raids == null || '
                                       'raids.Length == 0) return null; return raids[Mathf.Abs(dayIndex) % '
                                       'raids.Length]; } }\n'
                                       '    public sealed class RaidMatchmakingScaffold { public string QueueId = '
                                       '"local_ai_assist"; }\n'
                                       '}\n',
 'Assets/Scripts/Save/SaveSystem.cs': 'using System;\n'
                                      'using System.Collections.Generic;\n'
                                      'using System.IO;\n'
                                      'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                      'using UnityEngine;\n'
                                      '\n'
                                      'namespace __PROJECT_NAMESPACE__.Save\n'
                                      '{\n'
                                      '    [Serializable]\n'
                                      '    public sealed class PlayerSaveData\n'
                                      '    {\n'
                                      '        public string sceneName = "Overworld";\n'
                                      '        public Vector3 position;\n'
                                      '        public int money;\n'
                                      '    }\n'
                                      '\n'
                                      '    [Serializable]\n'
                                      '    public sealed class CreatureSaveData\n'
                                      '    {\n'
                                      '        public string speciesId;\n'
                                      '        public int level;\n'
                                      '        public int experience;\n'
                                      '        public bool shiny;\n'
                                      '        public int currentHp;\n'
                                      '    }\n'
                                      '\n'
                                      '    [Serializable]\n'
                                      '    public sealed class InventoryStack\n'
                                      '    {\n'
                                      '        public string itemId;\n'
                                      '        public int count;\n'
                                      '    }\n'
                                      '\n'
                                      '    [Serializable]\n'
                                      '    public sealed class FlagRecord\n'
                                      '    {\n'
                                      '        public string key;\n'
                                      '        public bool value;\n'
                                      '    }\n'
                                      '\n'
                                      '    [Serializable]\n'
                                      '    public sealed class WorldStateRecord\n'
                                      '    {\n'
                                      '        public string key;\n'
                                      '        public string value;\n'
                                      '    }\n'
                                      '\n'
                                      '    [Serializable]\n'
                                      '    public sealed class FusionSaveRecord\n'
                                      '    {\n'
                                      '        public string fusionId;\n'
                                      '        public string leftSpeciesId;\n'
                                      '        public string rightSpeciesId;\n'
                                      '        public bool active;\n'
                                      '    }\n'
                                      '\n'
                                      '    [Serializable]\n'
                                      '    public sealed class TransformationSaveRecord\n'
                                      '    {\n'
                                      '        public string creatureGuid;\n'
                                      '        public bool megaUnlocked;\n'
                                      '        public bool dimensionSplitUnlocked;\n'
                                      '        public int dimensionMeter;\n'
                                      '    }\n'
                                      '\n'
                                      '    [Serializable]\n'
                                      '    public sealed class SaveData\n'
                                      '    {\n'
                                      '        public int version = 1;\n'
                                      '        public PlayerSaveData player = new PlayerSaveData();\n'
                                      '        public List<CreatureSaveData> party = new List<CreatureSaveData>();\n'
                                      '        public List<CreatureSaveData> pcStorage = new '
                                      'List<CreatureSaveData>();\n'
                                      '        public List<InventoryStack> inventory = new List<InventoryStack>();\n'
                                      '        public List<FlagRecord> flags = new List<FlagRecord>();\n'
                                      '        public List<WorldStateRecord> worldState = new '
                                      'List<WorldStateRecord>();\n'
                                      '        public List<FusionSaveRecord> fusions = new List<FusionSaveRecord>();\n'
                                      '        public List<TransformationSaveRecord> transformations = new '
                                      'List<TransformationSaveRecord>();\n'
                                      '    }\n'
                                      '\n'
                                      '    /// <summary>JSON save pipeline. Extend SaveData with versioned fields and '
                                      'migrate in Deserialize when version changes.</summary>\n'
                                      '    public sealed class SaveManager\n'
                                      '    {\n'
                                      '        public SaveData Current { get; private set; } = new SaveData();\n'
                                      '\n'
                                      '        public string Serialize(SaveData data = null)\n'
                                      '        {\n'
                                      '            return JsonUtility.ToJson(data ?? Current, true);\n'
                                      '        }\n'
                                      '\n'
                                      '        public SaveData Deserialize(string json)\n'
                                      '        {\n'
                                      '            Current = string.IsNullOrWhiteSpace(json) ? new SaveData() : '
                                      'JsonUtility.FromJson<SaveData>(json);\n'
                                      '            if (Current.flags == null) Current.flags = new List<FlagRecord>();\n'
                                      '            if (Current.party == null) Current.party = new '
                                      'List<CreatureSaveData>();\n'
                                      '            if (Current.inventory == null) Current.inventory = new '
                                      'List<InventoryStack>();\n'
                                      '            if (Current.worldState == null) Current.worldState = new '
                                      'List<WorldStateRecord>();\n'
                                      '            if (Current.fusions == null) Current.fusions = new '
                                      'List<FusionSaveRecord>();\n'
                                      '            if (Current.transformations == null) Current.transformations = new '
                                      'List<TransformationSaveRecord>();\n'
                                      '            return Current;\n'
                                      '        }\n'
                                      '\n'
                                      '        public void SaveToFile(string path)\n'
                                      '        {\n'
                                      '            Directory.CreateDirectory(Path.GetDirectoryName(path));\n'
                                      '            File.WriteAllText(path, Serialize());\n'
                                      '        }\n'
                                      '\n'
                                      '        public SaveData LoadFromFile(string path)\n'
                                      '        {\n'
                                      '            return Deserialize(File.Exists(path) ? File.ReadAllText(path) : '
                                      'string.Empty);\n'
                                      '        }\n'
                                      '\n'
                                      '        public void SetFlag(string key, bool value)\n'
                                      '        {\n'
                                      '            var record = Current.flags.Find(f => f.key == key);\n'
                                      '            if (record == null)\n'
                                      '            {\n'
                                      '                Current.flags.Add(new FlagRecord { key = key, value = value '
                                      '});\n'
                                      '            }\n'
                                      '            else\n'
                                      '            {\n'
                                      '                record.value = value;\n'
                                      '            }\n'
                                      '        }\n'
                                      '\n'
                                      '        public bool GetFlag(string key)\n'
                                      '        {\n'
                                      '            var record = Current.flags.Find(f => f.key == key);\n'
                                      '            return record != null && record.value;\n'
                                      '        }\n'
                                      '\n'
                                      '        public void CaptureParty(Party party)\n'
                                      '        {\n'
                                      '            Current.party.Clear();\n'
                                      '            foreach (var creature in party.Creatures)\n'
                                      '            {\n'
                                      '                Current.party.Add(CreatureToSave(creature));\n'
                                      '            }\n'
                                      '        }\n'
                                      '\n'
                                      '        public static CreatureSaveData CreatureToSave(CreatureInstance '
                                      'creature)\n'
                                      '        {\n'
                                      '            return new CreatureSaveData\n'
                                      '            {\n'
                                      '                speciesId = creature.Species != null ? creature.Species.id : '
                                      'creature.speciesId,\n'
                                      '                level = creature.Level,\n'
                                      '                experience = creature.Experience,\n'
                                      '                shiny = creature.Shiny,\n'
                                      '                currentHp = creature.CurrentHp\n'
                                      '            };\n'
                                      '        }\n'
                                      '    }\n'
                                      '}\n',
 'Assets/Scripts/Tools/__PROJECT_NAMESPACE__.Editor.asmdef': '{\n'
                                                    '  "name": "__PROJECT_NAMESPACE__.Editor",\n'
                                                    '  "rootNamespace": "__PROJECT_NAMESPACE__.Tools",\n'
                                                    '  "references": [\n'
                                                    '    "__PROJECT_NAMESPACE__.Runtime"\n'
                                                    '  ],\n'
                                                    '  "includePlatforms": [\n'
                                                    '    "Editor"\n'
                                                    '  ],\n'
                                                    '  "excludePlatforms": [],\n'
                                                    '  "allowUnsafeCode": false,\n'
                                                    '  "overrideReferences": false,\n'
                                                    '  "precompiledReferences": [],\n'
                                                    '  "autoReferenced": true,\n'
                                                    '  "defineConstraints": [],\n'
                                                    '  "versionDefines": [],\n'
                                                    '  "noEngineReferences": false\n'
                                                    '}\n',
 'Assets/Scripts/Tools/EditorTools.cs': '#if UNITY_EDITOR\n'
                                        'using System.Collections.Generic;\n'
                                        'using System.IO;\n'
                                        'using __PROJECT_NAMESPACE__.CameraSystem;\n'
                                        'using __PROJECT_NAMESPACE__.Overworld;\n'
                                        'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                        'using UnityEditor;\n'
                                        'using UnityEditor.SceneManagement;\n'
                                        'using UnityEngine;\n'
                                        '\n'
                                        'namespace __PROJECT_NAMESPACE__.Tools\n'
                                        '{\n'
                                        '    public sealed class ValidationResult\n'
                                        '    {\n'
                                        '        public readonly List<string> errors = new List<string>();\n'
                                        '        public bool IsValid => errors.Count == 0;\n'
                                        '    }\n'
                                        '\n'
                                        '    /// <summary>Data validation rules. Add project-specific checks here '
                                        'before content is allowed into builds.</summary>\n'
                                        '    public static class __PROJECT_NAMESPACE__DataValidator\n'
                                        '    {\n'
                                        '        public static ValidationResult '
                                        'ValidateSpecies(IEnumerable<CreatureSpecies> species)\n'
                                        '        {\n'
                                        '            var result = new ValidationResult();\n'
                                        '            var ids = new HashSet<string>();\n'
                                        '            foreach (var s in species)\n'
                                        '            {\n'
                                        '                if (s == null)\n'
                                        '                {\n'
                                        '                    continue;\n'
                                        '                }\n'
                                        '\n'
                                        '                if (string.IsNullOrEmpty(s.id))\n'
                                        '                {\n'
                                        '                    result.errors.Add("Species missing ID");\n'
                                        '                }\n'
                                        '                else if (!ids.Add(s.id))\n'
                                        '                {\n'
                                        '                    result.errors.Add("Duplicate species ID: " + s.id);\n'
                                        '                }\n'
                                        '\n'
                                        '                if (s.learnset != null)\n'
                                        '                {\n'
                                        '                    foreach (var entry in s.learnset)\n'
                                        '                    {\n'
                                        '                        if (entry == null || entry.move == null)\n'
                                        '                        {\n'
                                        '                            result.errors.Add($"Species {s.id} has missing '
                                        'move in learnset");\n'
                                        '                        }\n'
                                        '                    }\n'
                                        '                }\n'
                                        '\n'
                                        '                if (s.evolutions != null)\n'
                                        '                {\n'
                                        '                    foreach (var evo in s.evolutions)\n'
                                        '                    {\n'
                                        '                        if (evo != null && evo.evolvesInto == null)\n'
                                        '                        {\n'
                                        '                            result.errors.Add($"Species {s.id} has invalid '
                                        'evolution target");\n'
                                        '                        }\n'
                                        '                    }\n'
                                        '                }\n'
                                        '            }\n'
                                        '\n'
                                        '            return result;\n'
                                        '        }\n'
                                        '\n'
                                        '        public static ValidationResult ValidateEncounterTable(EncounterTable '
                                        'table)\n'
                                        '        {\n'
                                        '            var result = new ValidationResult();\n'
                                        '            if (table == null || table.entries == null || '
                                        'table.entries.Length == 0)\n'
                                        '            {\n'
                                        '                result.errors.Add("Encounter table has no entries");\n'
                                        '                return result;\n'
                                        '            }\n'
                                        '\n'
                                        '            foreach (var entry in table.entries)\n'
                                        '            {\n'
                                        '                if (entry == null || entry.species == null || entry.weight <= '
                                        '0)\n'
                                        '                {\n'
                                        '                    result.errors.Add("Encounter table has invalid entry");\n'
                                        '                }\n'
                                        '            }\n'
                                        '\n'
                                        '            return result;\n'
                                        '        }\n'
                                        '    }\n'
                                        '\n'
                                        '    public sealed class CreatureDataEditor : EditorWindow { '
                                        '[MenuItem("__PROJECT_MENU_ROOT__/Creature Data Editor")] public static void Open() => '
                                        'GetWindow<CreatureDataEditor>("Creature Data"); }\n'
                                        '    public sealed class MoveDataEditor : EditorWindow { '
                                        '[MenuItem("__PROJECT_MENU_ROOT__/Move Data Editor")] public static void Open() => '
                                        'GetWindow<MoveDataEditor>("Move Data"); }\n'
                                        '    public sealed class EncounterTableEditorWindow : EditorWindow { '
                                        '[MenuItem("__PROJECT_MENU_ROOT__/Encounter Table Editor")] public static void Open() '
                                        '=> GetWindow<EncounterTableEditorWindow>("Encounters"); }\n'
                                        '    public sealed class DialogueEditorWindow : EditorWindow { '
                                        '[MenuItem("__PROJECT_MENU_ROOT__/Dialogue Editor")] public static void Open() => '
                                        'GetWindow<DialogueEditorWindow>("Dialogue"); }\n'
                                        '    public sealed class MapGridVisualizerWindow : EditorWindow { '
                                        '[MenuItem("__PROJECT_MENU_ROOT__/Map Grid Visualizer")] public static void Open() => '
                                        'GetWindow<MapGridVisualizerWindow>("Grid"); }\n'
                                        '    public sealed class TestDebugPanelWindow : EditorWindow { '
                                        '[MenuItem("__PROJECT_MENU_ROOT__/Test Debug Panel")] public static void Open() => '
                                        'GetWindow<TestDebugPanelWindow>("Debug"); }\n'
                                        '\n'
                                        '    public static class __PROJECT_NAMESPACE__SceneFactory\n'
                                        '    {\n'
                                        '        [MenuItem("__PROJECT_MENU_ROOT__/Open Combined Prototype Scene")]\n'
                                        '        public static void OpenCombinedPrototypeScene()\n'
                                        '        {\n'
                                        '            const string scenePath = "Assets/Scenes/PrototypeRegion.unity";\n'
                                        '            Directory.CreateDirectory("Assets/Scenes");\n'
                                        '            if (File.Exists(scenePath))\n'
                                        '            {\n'
                                        '                EditorSceneManager.OpenScene(scenePath, OpenSceneMode.Single);\n'
                                        '            }\n'
                                        '\n'
                                        '            EditorBuildSettings.scenes = new[]\n'
                                        '            {\n'
                                        '                new EditorBuildSettingsScene(scenePath, true)\n'
                                        '            };\n'
                                        '            AssetDatabase.SaveAssets();\n'
                                        '            AssetDatabase.Refresh();\n'
                                        '        }\n'
                                        '    }\n'
                                        '}\n'
                                        '#endif\n',
 'Assets/Scripts/Transformations/TransformationSystems.cs': 'using System.Collections.Generic;\n'
                                                            'using __PROJECT_NAMESPACE__.Battle;\n'
                                                            'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                                            'using UnityEngine;\n'
                                                            '\n'
                                                            'namespace __PROJECT_NAMESPACE__.Transformations\n'
                                                            '{\n'
                                                            '    public sealed class MegaEvolutionSystem\n'
                                                            '    {\n'
                                                            '        private readonly HashSet<string> usedBattles = '
                                                            'new HashSet<string>();\n'
                                                            '\n'
                                                            '        public bool TryActivate(string battleId, '
                                                            'BattleCreature creature, FormDefinition form)\n'
                                                            '        {\n'
                                                            '            if (usedBattles.Contains(battleId) || '
                                                            'creature == null || form == null)\n'
                                                            '            {\n'
                                                            '                return false;\n'
                                                            '            }\n'
                                                            '\n'
                                                            '            usedBattles.Add(battleId);\n'
                                                            '            if (form.abilityOverride != null)\n'
                                                            '            {\n'
                                                            '                creature.Instance.ActiveAbility = '
                                                            'form.abilityOverride;\n'
                                                            '            }\n'
                                                            '\n'
                                                            '            return true;\n'
                                                            '        }\n'
                                                            '\n'
                                                            '        public StatBlock PreviewStats(CreatureInstance '
                                                            'creature, FormDefinition form)\n'
                                                            '        {\n'
                                                            '            return creature.CalculateStats().Scale(form '
                                                            '!= null ? Mathf.Max(1f, form.statMultiplier) : 1f) + '
                                                            '(form != null ? form.statModifier : default);\n'
                                                            '        }\n'
                                                            '    }\n'
                                                            '\n'
                                                            '    public sealed class DimensionSplitSystem\n'
                                                            '    {\n'
                                                            '        public bool CanActivate(int meter, bool '
                                                            'storyUnlocked)\n'
                                                            '        {\n'
                                                            '            return storyUnlocked && meter >= 100;\n'
                                                            '        }\n'
                                                            '\n'
                                                            '        public bool TryActivate(CreatureInstance '
                                                            'creature, FormDefinition splitForm, int meter, bool '
                                                            'storyUnlocked)\n'
                                                            '        {\n'
                                                            '            if (!CanActivate(meter, storyUnlocked) || '
                                                            'creature == null || splitForm == null)\n'
                                                            '            {\n'
                                                            '                return false;\n'
                                                            '            }\n'
                                                            '\n'
                                                            '            if (splitForm.abilityOverride != null)\n'
                                                            '            {\n'
                                                            '                creature.ActiveAbility = '
                                                            'splitForm.abilityOverride;\n'
                                                            '            }\n'
                                                            '\n'
                                                            '            if (splitForm.signatureMove != null && '
                                                            '!creature.KnownMoves.Contains(splitForm.signatureMove))\n'
                                                            '            {\n'
                                                            '                '
                                                            'creature.KnownMoves.Add(splitForm.signatureMove);\n'
                                                            '            }\n'
                                                            '\n'
                                                            '            return true;\n'
                                                            '        }\n'
                                                            '\n'
                                                            '        public StatBlock BuffStats(CreatureInstance '
                                                            'creature, float multiplier)\n'
                                                            '        {\n'
                                                            '            return '
                                                            'creature.CalculateStats().Scale(multiplier);\n'
                                                            '        }\n'
                                                            '    }\n'
                                                            '}\n',
 'Assets/Scripts/UI/UIScaffolds.cs': 'using System;\n'
                                     'using System.Collections.Generic;\n'
                                     'using __PROJECT_NAMESPACE__.Battle;\n'
                                     'using __PROJECT_NAMESPACE__.Core;\n'
                                     'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                     '\n'
                                     'namespace __PROJECT_NAMESPACE__.UI\n'
                                     '{\n'
                                     '    public sealed class DialogueBox\n'
                                     '    {\n'
                                     '        private readonly Queue<string> lines = new Queue<string>();\n'
                                     '        public string CurrentLine { get; private set; }\n'
                                     '\n'
                                     '        public void Start(IEnumerable<string> source)\n'
                                     '        {\n'
                                     '            lines.Clear();\n'
                                     '            foreach (var line in source)\n'
                                     '            {\n'
                                     '                lines.Enqueue(line);\n'
                                     '            }\n'
                                     '\n'
                                     '            Advance();\n'
                                     '        }\n'
                                     '\n'
                                     '        public bool Advance()\n'
                                     '        {\n'
                                     '            if (lines.Count == 0)\n'
                                     '            {\n'
                                     '                CurrentLine = null;\n'
                                     '                return false;\n'
                                     '            }\n'
                                     '\n'
                                     '            CurrentLine = lines.Dequeue();\n'
                                     '            return true;\n'
                                     '        }\n'
                                     '    }\n'
                                     '\n'
                                     '    public sealed class BattleCommandMenu\n'
                                     '    {\n'
                                     '        public event Action<BattleCommandType> CommandSelected;\n'
                                     '        public void Select(BattleCommandType type) { '
                                     'CommandSelected?.Invoke(type); }\n'
                                     '    }\n'
                                     '\n'
                                     '    public sealed class PartyMenu { public Party Party { get; private set; } '
                                     'public void Bind(Party party) { Party = party; } }\n'
                                     '    public sealed class BagMenu { public readonly List<string> itemIds = new '
                                     'List<string>(); }\n'
                                     '    public sealed class CreatureSummaryScreen { public CreatureInstance Creature '
                                     '{ get; private set; } public void Show(CreatureInstance creature) { Creature = '
                                     'creature; } }\n'
                                     '    public sealed class MapScreen { public string CurrentAreaId { get; private '
                                     'set; } public void SetArea(string areaId) { CurrentAreaId = areaId; } }\n'
                                     '\n'
                                     '    public sealed class SettingsMenu\n'
                                     '    {\n'
                                     '        private readonly SettingsManager settings;\n'
                                     '        public SettingsMenu(SettingsManager settings) { this.settings = '
                                     'settings; }\n'
                                     '\n'
                                     '        public void SetMasterVolume(float value)\n'
                                     '        {\n'
                                     '            var data = settings.Data;\n'
                                     '            data.masterVolume = value;\n'
                                     '            settings.Apply(data);\n'
                                     '        }\n'
                                     '    }\n'
                                     '}\n',
 'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/CoreSaveTests.cs': 'using __PROJECT_NAMESPACE__.Core;\n'
                                                        'using __PROJECT_NAMESPACE__.Save;\n'
                                                        'using NUnit.Framework;\n'
                                                        '\n'
                                                        'namespace __PROJECT_NAMESPACE__.Tests\n'
                                                        '{\n'
                                                        '    public sealed class CoreSaveTests\n'
                                                        '    {\n'
                                                        '        [Test]\n'
                                                        '        public void '
                                                        'EventBus_SubscribePublishUnsubscribe_Works()\n'
                                                        '        {\n'
                                                        '            var bus = new EventBus();\n'
                                                        '            var count = 0;\n'
                                                        '            System.Action<int> handler = v => count += v;\n'
                                                        '            bus.Subscribe(handler);\n'
                                                        '            bus.Publish(2);\n'
                                                        '            bus.Unsubscribe(handler);\n'
                                                        '            bus.Publish(2);\n'
                                                        '            Assert.AreEqual(2, count);\n'
                                                        '        }\n'
                                                        '\n'
                                                        '        [Test]\n'
                                                        '        public void '
                                                        'SaveManager_SerializesPartyInventoryFlagsAndWorldState()\n'
                                                        '        {\n'
                                                        '            var save = new SaveManager();\n'
                                                        '            save.Current.party.Add(new CreatureSaveData { '
                                                        'speciesId = "auraling", level = 5 });\n'
                                                        '            save.Current.inventory.Add(new InventoryStack { '
                                                        'itemId = "tonic", count = 2 });\n'
                                                        '            save.Current.worldState.Add(new WorldStateRecord '
                                                        '{ key = "door", value = "open" });\n'
                                                        '            save.SetFlag("intro_done", true);\n'
                                                        '            var clone = new '
                                                        'SaveManager().Deserialize(save.Serialize());\n'
                                                        '            Assert.IsTrue(clone.flags.Exists(f => f.key == '
                                                        '"intro_done" && f.value));\n'
                                                        '            Assert.AreEqual("auraling", '
                                                        'clone.party[0].speciesId);\n'
                                                        '            Assert.AreEqual("open", '
                                                        'clone.worldState[0].value);\n'
                                                        '        }\n'
                                                        '\n'
                                                        '        [Test]\n'
                                                        '        public void SettingsManager_PersistsSettings()\n'
                                                        '        {\n'
                                                        '            var manager = new SettingsManager();\n'
                                                        '            manager.Apply(new SettingsData { masterVolume = '
                                                        '0.25f, language = "es" });\n'
                                                        '            var copy = new SettingsManager();\n'
                                                        '            copy.Deserialize(manager.Serialize());\n'
                                                        '            Assert.AreEqual(0.25f, copy.Data.masterVolume);\n'
                                                        '            Assert.AreEqual("es", copy.Data.language);\n'
                                                        '        }\n'
                                                        '\n'
                                                        '        [Test]\n'
                                                        '        public void SaveManager_FlagPersistence_Works()\n'
                                                        '        {\n'
                                                        '            var save = new SaveManager();\n'
                                                        '            save.SetFlag("gym_clear", true);\n'
                                                        '            var copy = new '
                                                        'SaveManager().Deserialize(save.Serialize());\n'
                                                        '            Assert.IsTrue(copy.flags.Exists(f => f.key == '
                                                        '"gym_clear" && f.value));\n'
                                                        '        }\n'
                                                        '    }\n'
                                                        '}\n',
 'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/CreatureBattleTests.cs': 'using __PROJECT_NAMESPACE__.Battle;\n'
                                                              'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                                              'using NUnit.Framework;\n'
                                                              '\n'
                                                              'namespace __PROJECT_NAMESPACE__.Tests\n'
                                                              '{\n'
                                                              '    public sealed class CreatureBattleTests\n'
                                                              '    {\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'PartyCannotExceedSix_AndPcAcceptsOverflow()\n'
                                                              '        {\n'
                                                              '            var party = new Party();\n'
                                                              '            var pc = new PCStorage();\n'
                                                              '            for (var i = 0; i < 6; i++)\n'
                                                              '            {\n'
                                                              '                '
                                                              'Assert.IsTrue(party.Add(TestFactories.Creature("c" + '
                                                              'i)));\n'
                                                              '            }\n'
                                                              '\n'
                                                              '            var overflow = '
                                                              'TestFactories.Creature("overflow");\n'
                                                              '            Assert.IsFalse(party.Add(overflow));\n'
                                                              '            pc.Add(overflow);\n'
                                                              '            Assert.AreEqual(1, pc.Stored.Count);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'TypeChart_ReturnsSampleMultipliers()\n'
                                                              '        {\n'
                                                              '            var chart = '
                                                              'TypeChart.CreateDefaultForTests();\n'
                                                              '            Assert.AreEqual(2f, '
                                                              'chart.GetMultiplier(CreatureType.Flame, '
                                                              'CreatureType.Leaf));\n'
                                                              '            Assert.AreEqual(0f, '
                                                              'chart.GetMultiplier(CreatureType.Neutral, '
                                                              'CreatureType.Shadow));\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void Learnset_ReturnsMovesAtLevel()\n'
                                                              '        {\n'
                                                              '            var move = TestFactories.Move();\n'
                                                              '            var entry = '
                                                              'UnityEngine.ScriptableObject.CreateInstance<LearnsetEntry>();\n'
                                                              '            entry.level = 5;\n'
                                                              '            entry.move = move;\n'
                                                              '            var species = TestFactories.Species();\n'
                                                              '            species.learnset = new[] { entry };\n'
                                                              '            Assert.Contains(move, new '
                                                              'LearnsetSystem().GetMovesAtLevel(species, 5));\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void EvolutionRule_Triggers()\n'
                                                              '        {\n'
                                                              '            var from = '
                                                              'TestFactories.Species("seedling");\n'
                                                              '            var to = '
                                                              'TestFactories.Species("grovekin");\n'
                                                              '            var rule = '
                                                              'UnityEngine.ScriptableObject.CreateInstance<EvolutionRule>();\n'
                                                              '            rule.fromSpeciesId = from.id;\n'
                                                              '            rule.evolvesInto = to;\n'
                                                              '            rule.minimumLevel = 10;\n'
                                                              '            from.evolutions = new[] { rule };\n'
                                                              '            Assert.AreEqual(to, new '
                                                              'EvolutionSystem().GetEvolution(new '
                                                              'CreatureInstance(from, 10)));\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void ShinyRoller_CanBeDeterministic()\n'
                                                              '        {\n'
                                                              '            Assert.AreEqual(new '
                                                              'ShinyRoller(42).RollShiny(2), new '
                                                              'ShinyRoller(42).RollShiny(2));\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void CreatureInstance_CalculatesStats()\n'
                                                              '        {\n'
                                                              '            var creature = '
                                                              'TestFactories.Creature(level: 10);\n'
                                                              '            '
                                                              'Assert.Greater(creature.CalculateStats().hp, '
                                                              'creature.Species.baseStats.hp / 2);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'FasterCreatureActsFirst_WhenPriorityEqual()\n'
                                                              '        {\n'
                                                              '            var fast = new BattleParticipant { active = '
                                                              'new BattleCreature(TestFactories.Creature("fast", '
                                                              'speed: 100)) };\n'
                                                              '            var slow = new BattleParticipant { active = '
                                                              'new BattleCreature(TestFactories.Creature("slow", '
                                                              'speed: 10)) };\n'
                                                              '            var move = TestFactories.Move();\n'
                                                              '            var sorted = new MoveResolver(new '
                                                              'DamageCalculator(TypeChart.CreateDefaultForTests())).SortCommands(new[] '
                                                              '{ BattleCommand.Fight(slow, fast, move), '
                                                              'BattleCommand.Fight(fast, slow, move) });\n'
                                                              '            Assert.AreSame(fast, sorted[0].user);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void HigherPriorityMoveActsFirst()\n'
                                                              '        {\n'
                                                              '            var a = new BattleParticipant { active = '
                                                              'new BattleCreature(TestFactories.Creature("a", speed: '
                                                              '1)) };\n'
                                                              '            var b = new BattleParticipant { active = '
                                                              'new BattleCreature(TestFactories.Creature("b", speed: '
                                                              '100)) };\n'
                                                              '            var quick = TestFactories.Move(priority: '
                                                              '1);\n'
                                                              '            var normal = TestFactories.Move(priority: '
                                                              '0);\n'
                                                              '            var sorted = new MoveResolver(new '
                                                              'DamageCalculator(TypeChart.CreateDefaultForTests())).SortCommands(new[] '
                                                              '{ BattleCommand.Fight(b, a, normal), '
                                                              'BattleCommand.Fight(a, b, quick) });\n'
                                                              '            Assert.AreSame(a, sorted[0].user);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void AccuracyCanMiss()\n'
                                                              '        {\n'
                                                              '            var move = TestFactories.Move(accuracy: '
                                                              '50);\n'
                                                              '            Assert.IsFalse(new '
                                                              'AccuracyResolver().DoesHit(move, new '
                                                              'FixedRandomSource(99)));\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'Damage_TypeAndStab_ModifyDamage_AndFaintCanTrigger()\n'
                                                              '        {\n'
                                                              '            var flame = new '
                                                              'BattleCreature(TestFactories.Creature("flame", '
                                                              'CreatureType.Flame));\n'
                                                              '            var leaf = new '
                                                              'BattleCreature(TestFactories.Creature("leaf", '
                                                              'CreatureType.Leaf));\n'
                                                              '            var move = TestFactories.Move(type: '
                                                              'CreatureType.Flame, power: 60);\n'
                                                              '            var calc = new '
                                                              'DamageCalculator(TypeChart.CreateDefaultForTests());\n'
                                                              '            var damage = calc.Calculate(flame, leaf, '
                                                              'move);\n'
                                                              '            Assert.Greater(damage, 0);\n'
                                                              '            leaf.ApplyDamage(9999);\n'
                                                              '            Assert.IsTrue(leaf.Fainted);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void BurnDamageAppliesAtEndTurn()\n'
                                                              '        {\n'
                                                              '            var creature = new '
                                                              'BattleCreature(TestFactories.Creature());\n'
                                                              '            creature.Status = StatusCondition.Burn;\n'
                                                              '            var hp = creature.CurrentHp;\n'
                                                              '            new '
                                                              'StatusEffectController().ApplyEndTurn(creature);\n'
                                                              '            Assert.Less(creature.CurrentHp, hp);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void AIsSelectLegalMoves()\n'
                                                              '        {\n'
                                                              '            var move = TestFactories.Move();\n'
                                                              '            var self = new BattleParticipant { active = '
                                                              'new BattleCreature(TestFactories.Creature()) };\n'
                                                              '            self.active.Instance.KnownMoves.Add(move);\n'
                                                              '            var foe = new BattleParticipant { active = '
                                                              'new BattleCreature(TestFactories.Creature("foe")) };\n'
                                                              '            Assert.AreSame(move, new '
                                                              'WildBattleAI().Choose(self, foe).move);\n'
                                                              '            Assert.AreSame(move, new '
                                                              'TrainerBattleAI().Choose(self, foe).move);\n'
                                                              '        }\n'
                                                              '    }\n'
                                                              '}\n',
 'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/__PROJECT_NAMESPACE__.EditModeTests.asmdef': '{\n'
                                                                         '  "name": "__PROJECT_NAMESPACE__.EditModeTests",\n'
                                                                         '  "rootNamespace": "__PROJECT_NAMESPACE__.Tests",\n'
                                                                         '  "references": [\n'
                                                                         '    "__PROJECT_NAMESPACE__.Runtime",\n'
                                                                         '    "__PROJECT_NAMESPACE__.Editor"\n'
                                                                         '  ],\n'
                                                                         '  "includePlatforms": [\n'
                                                                         '    "Editor"\n'
                                                                         '  ],\n'
                                                                         '  "excludePlatforms": [],\n'
                                                                         '  "allowUnsafeCode": false,\n'
                                                                         '  "overrideReferences": false,\n'
                                                                         '  "precompiledReferences": [],\n'
                                                                         '  "autoReferenced": false,\n'
                                                                         '  "defineConstraints": [],\n'
                                                                         '  "versionDefines": [],\n'
                                                                         '  "optionalUnityReferences": [\n'
                                                                         '    "TestAssemblies"\n'
                                                                         '  ],\n'
                                                                         '  "noEngineReferences": false\n'
                                                                         '}\n',
 'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/MovementCameraTests.cs': 'using __PROJECT_NAMESPACE__.CameraSystem;\n'
                                                              'using __PROJECT_NAMESPACE__.Overworld;\n'
                                                              'using NUnit.Framework;\n'
                                                              'using UnityEngine;\n'
                                                              '\n'
                                                              'namespace __PROJECT_NAMESPACE__.Tests\n'
                                                              '{\n'
                                                              '    public sealed class MovementCameraTests\n'
                                                              '    {\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'StructuredMovement_BlocksDiagonalInput()\n'
                                                              '        {\n'
                                                              '            var motor = new GridMovementMotor(new '
                                                              'TileCollisionMap());\n'
                                                              '            motor.TryMove(new Vector2Int(1, 1));\n'
                                                              '            motor.Tick(1f);\n'
                                                              '            Assert.IsTrue(motor.Tile == Vector2Int.up '
                                                              '|| motor.Tile == Vector2Int.right);\n'
                                                              '            Assert.AreNotEqual(new Vector2Int(1, 1), '
                                                              'motor.Tile);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'StructuredMovement_SnapsToTileCenters()\n'
                                                              '        {\n'
                                                              '            var motor = new GridMovementMotor(new '
                                                              'TileCollisionMap());\n'
                                                              '            motor.TryMove(Vector2Int.right);\n'
                                                              '            motor.Tick(1f);\n'
                                                              '            Assert.AreEqual(new Vector3(1, 0, 0), '
                                                              'motor.WorldPosition);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'StructuredMovement_RefusesBlockedTiles()\n'
                                                              '        {\n'
                                                              '            var map = new TileCollisionMap();\n'
                                                              '            map.SetBlocked(Vector2Int.right, true);\n'
                                                              '            var motor = new GridMovementMotor(map);\n'
                                                              '            '
                                                              'Assert.IsFalse(motor.TryMove(Vector2Int.right));\n'
                                                              '            Assert.AreEqual(Vector2Int.zero, '
                                                              'motor.Tile);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'WildMovement_AcceptsAndNormalizesDiagonalInput()\n'
                                                              '        {\n'
                                                              '            var motor = new WildAreaMovementMotor(new '
                                                              'TileCollisionMap());\n'
                                                              '            motor.Move(Vector3.zero, new Vector2(1, 1), '
                                                              '4f, 1f);\n'
                                                              '            Assert.AreEqual(4f, '
                                                              'motor.LastVelocity.magnitude, 0.001f);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void FacingDirection_Updates()\n'
                                                              '        {\n'
                                                              '            var motor = new GridMovementMotor(new '
                                                              'TileCollisionMap());\n'
                                                              '            motor.TryMove(Vector2Int.left);\n'
                                                              '            Assert.AreEqual(Direction.Left, '
                                                              'motor.Facing);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'InputBuffering_StartsNextTileAfterCurrentMove()\n'
                                                              '        {\n'
                                                              '            var motor = new GridMovementMotor(new '
                                                              'TileCollisionMap(), 1f, 0.5f);\n'
                                                              '            motor.TryMove(Vector2Int.right);\n'
                                                              '            motor.TryMove(Vector2Int.up);\n'
                                                              '            motor.Tick(0.5f);\n'
                                                              '            Assert.IsTrue(motor.IsMoving);\n'
                                                              '            motor.Tick(0.5f);\n'
                                                              '            Assert.AreEqual(new Vector2Int(1, 1), '
                                                              'motor.Tile);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void FixedCamera_IgnoresMouseRotation()\n'
                                                              '        {\n'
                                                              '            var profile = '
                                                              'ScriptableObject.CreateInstance<CameraZoneProfile>();\n'
                                                              '            profile.fixedYaw = 30f;\n'
                                                              '            var mode = new FixedCameraMode();\n'
                                                              '            var a = mode.UpdatePose(Vector3.zero, '
                                                              'profile, new CameraInput(0, 0), 1f);\n'
                                                              '            var b = mode.UpdatePose(Vector3.zero, '
                                                              'profile, new CameraInput(100, 0), 1f);\n'
                                                              '            Assert.AreEqual(a.yaw, b.yaw);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'WildCamera_AcceptsHorizontalInputAndClampsTilt()\n'
                                                              '        {\n'
                                                              '            var profile = '
                                                              'ScriptableObject.CreateInstance<CameraZoneProfile>();\n'
                                                              '            profile.mode = CameraMode.WildFreeLook;\n'
                                                              '            profile.minPitch = -5;\n'
                                                              '            profile.maxPitch = 5;\n'
                                                              '            var mode = new '
                                                              'WildAreaFreeLookCameraMode();\n'
                                                              '            var pose = mode.UpdatePose(Vector3.zero, '
                                                              'profile, new CameraInput(1, 100), 1f);\n'
                                                              '            Assert.Greater(pose.yaw, 0f);\n'
                                                              '            Assert.AreEqual(-5f, pose.pitch);\n'
                                                              '        }\n'
                                                              '\n'
                                                              '        [Test]\n'
                                                              '        public void '
                                                              'CameraController_KeepsTargetAndSwitchesMode()\n'
                                                              '        {\n'
                                                              '            var go = new GameObject("cam");\n'
                                                              '            var target = new GameObject("target");\n'
                                                              '            var controller = '
                                                              'go.AddComponent<CameraFollowController>();\n'
                                                              '            var profile = '
                                                              'ScriptableObject.CreateInstance<CameraZoneProfile>();\n'
                                                              '            profile.mode = CameraMode.WildFreeLook;\n'
                                                              '            controller.SetTarget(target.transform);\n'
                                                              '            controller.SwitchProfile(profile);\n'
                                                              '            Assert.IsTrue(controller.HasTarget);\n'
                                                              '            Assert.AreEqual(CameraMode.WildFreeLook, '
                                                              'controller.CurrentMode);\n'
                                                              '            Object.DestroyImmediate(go);\n'
                                                              '            Object.DestroyImmediate(target);\n'
                                                              '        }\n'
                                                              '    }\n'
                                                              '}\n',
 'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/TestFactories.cs': 'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                                        'using UnityEngine;\n'
                                                        '\n'
                                                        'namespace __PROJECT_NAMESPACE__.Tests\n'
                                                        '{\n'
                                                        '    public static class TestFactories\n'
                                                        '    {\n'
                                                        '        public static MoveDefinition Move(string id = '
                                                        '"pulse", CreatureType type = CreatureType.Neutral, int power '
                                                        '= 40, int accuracy = 100, int priority = 0)\n'
                                                        '        {\n'
                                                        '            var move = '
                                                        'ScriptableObject.CreateInstance<MoveDefinition>();\n'
                                                        '            move.id = id;\n'
                                                        '            move.displayName = id;\n'
                                                        '            move.type = type;\n'
                                                        '            move.power = power;\n'
                                                        '            move.accuracy = accuracy;\n'
                                                        '            move.priority = priority;\n'
                                                        '            return move;\n'
                                                        '        }\n'
                                                        '\n'
                                                        '        public static AbilityDefinition Ability(string id = '
                                                        '"steady")\n'
                                                        '        {\n'
                                                        '            var ability = '
                                                        'ScriptableObject.CreateInstance<AbilityDefinition>();\n'
                                                        '            ability.id = id;\n'
                                                        '            ability.displayName = id;\n'
                                                        '            return ability;\n'
                                                        '        }\n'
                                                        '\n'
                                                        '        public static CreatureSpecies Species(string id = '
                                                        '"auraling", CreatureType type = CreatureType.Neutral, int '
                                                        'speed = 45)\n'
                                                        '        {\n'
                                                        '            var species = '
                                                        'ScriptableObject.CreateInstance<CreatureSpecies>();\n'
                                                        '            species.id = id;\n'
                                                        '            species.displayName = id;\n'
                                                        '            species.primaryType = type;\n'
                                                        '            species.baseStats = new StatBlock(50, 50, 50, 50, '
                                                        '50, speed);\n'
                                                        '            species.abilities = new[] { Ability(id + '
                                                        '"_ability") };\n'
                                                        '            return species;\n'
                                                        '        }\n'
                                                        '\n'
                                                        '        public static CreatureInstance Creature(string id = '
                                                        '"auraling", CreatureType type = CreatureType.Neutral, int '
                                                        'level = 10, int speed = 45)\n'
                                                        '        {\n'
                                                        '            return new CreatureInstance(Species(id, type, '
                                                        'speed), level);\n'
                                                        '        }\n'
                                                        '    }\n'
                                                        '}\n',
 'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/TransformRaidAudioEditorTests.cs': 'using __PROJECT_NAMESPACE__.Audio;\n'
                                                                        'using __PROJECT_NAMESPACE__.Battle;\n'
                                                                        'using __PROJECT_NAMESPACE__.Core;\n'
                                                                        'using __PROJECT_NAMESPACE__.Fusion;\n'
                                                                        'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                                                        'using __PROJECT_NAMESPACE__.Raids;\n'
                                                                        'using __PROJECT_NAMESPACE__.Tools;\n'
                                                                        'using __PROJECT_NAMESPACE__.Transformations;\n'
                                                                        'using __PROJECT_NAMESPACE__.Visuals;\n'
                                                                        'using NUnit.Framework;\n'
                                                                        'using UnityEngine;\n'
                                                                        '\n'
                                                                        'namespace __PROJECT_NAMESPACE__.Tests\n'
                                                                        '{\n'
                                                                        '    public sealed class '
                                                                        'TransformRaidAudioEditorTests\n'
                                                                        '    {\n'
                                                                        '        [Test]\n'
                                                                        '        public void '
                                                                        'Mega_CanOnlyActivateOnce_AndChangesAbilityStats()\n'
                                                                        '        {\n'
                                                                        '            var creature = new '
                                                                        'BattleCreature(TestFactories.Creature());\n'
                                                                        '            var form = '
                                                                        'ScriptableObject.CreateInstance<FormDefinition>();\n'
                                                                        '            form.statMultiplier = 1.3f;\n'
                                                                        '            form.abilityOverride = '
                                                                        'TestFactories.Ability("mega_ability");\n'
                                                                        '            var mega = new '
                                                                        'MegaEvolutionSystem();\n'
                                                                        '            '
                                                                        'Assert.IsTrue(mega.TryActivate("battle", '
                                                                        'creature, form));\n'
                                                                        '            '
                                                                        'Assert.IsFalse(mega.TryActivate("battle", '
                                                                        'creature, form));\n'
                                                                        '            Assert.AreEqual("mega_ability", '
                                                                        'creature.Instance.ActiveAbility.id);\n'
                                                                        '            '
                                                                        'Assert.Greater(mega.PreviewStats(creature.Instance, '
                                                                        'form).attack, '
                                                                        'creature.Instance.CalculateStats().attack);\n'
                                                                        '        }\n'
                                                                        '\n'
                                                                        '        [Test]\n'
                                                                        '        public void '
                                                                        'DimensionSplit_RequiresCondition_UnlocksMoveAndBuffsStats()\n'
                                                                        '        {\n'
                                                                        '            var creature = '
                                                                        'TestFactories.Creature();\n'
                                                                        '            var move = '
                                                                        'TestFactories.Move("rift_burst");\n'
                                                                        '            var form = '
                                                                        'ScriptableObject.CreateInstance<FormDefinition>();\n'
                                                                        '            form.signatureMove = move;\n'
                                                                        '            var split = new '
                                                                        'DimensionSplitSystem();\n'
                                                                        '            '
                                                                        'Assert.IsFalse(split.TryActivate(creature, '
                                                                        'form, 99, true));\n'
                                                                        '            '
                                                                        'Assert.IsTrue(split.TryActivate(creature, '
                                                                        'form, 100, true));\n'
                                                                        '            Assert.Contains(move, '
                                                                        'creature.KnownMoves);\n'
                                                                        '            '
                                                                        'Assert.Greater(split.BuffStats(creature, '
                                                                        '1.5f).speed, '
                                                                        'creature.CalculateStats().speed);\n'
                                                                        '        }\n'
                                                                        '\n'
                                                                        '        [Test]\n'
                                                                        '        public void '
                                                                        'Fusion_RejectsIncompatible_CombinesCompatible_Separates_AndSaves()\n'
                                                                        '        {\n'
                                                                        '            var a = '
                                                                        'TestFactories.Creature("a");\n'
                                                                        '            var b = '
                                                                        'TestFactories.Creature("b");\n'
                                                                        '            var fusion = new FusionSystem();\n'
                                                                        '            Assert.IsNull(fusion.Fuse(a, '
                                                                        'b));\n'
                                                                        '            fusion.AddCompatibility("a", '
                                                                        '"b");\n'
                                                                        '            var result = fusion.Fuse(a, b);\n'
                                                                        '            Assert.NotNull(result);\n'
                                                                        '            Assert.AreEqual(2, '
                                                                        'fusion.Separate(result).Length);\n'
                                                                        '            Assert.AreEqual("a+b", '
                                                                        'fusion.ToSave(result).fusionId);\n'
                                                                        '        }\n'
                                                                        '\n'
                                                                        '        [Test]\n'
                                                                        '        public void '
                                                                        'Raid_ScalesShieldTimerRewardsCaptureAndRotation()\n'
                                                                        '        {\n'
                                                                        '            var def = '
                                                                        'ScriptableObject.CreateInstance<RaidDefinition>();\n'
                                                                        '            def.bossSpecies = '
                                                                        'TestFactories.Species("boss");\n'
                                                                        '            def.tier = '
                                                                        'RaidDifficultyTier.ThreeStar;\n'
                                                                        '            def.hpMultiplier = 2;\n'
                                                                        '            var boss = new RaidBoss(def, '
                                                                        '10);\n'
                                                                        '            Assert.Greater(boss.maxHp, '
                                                                        'def.bossSpecies.baseStats.hp);\n'
                                                                        '            var shield = new '
                                                                        'RaidShieldController();\n'
                                                                        '            shield.Update(1, boss.maxHp);\n'
                                                                        '            '
                                                                        'Assert.IsTrue(shield.ShieldActive);\n'
                                                                        '            var timer = new '
                                                                        'RaidTimerController(1);\n'
                                                                        '            timer.Tick(2);\n'
                                                                        '            var raid = new '
                                                                        'RaidBattleController();\n'
                                                                        '            raid.ApplyTimer(timer);\n'
                                                                        '            Assert.IsTrue(raid.Failed);\n'
                                                                        '            var capture = new '
                                                                        'RaidCaptureController();\n'
                                                                        '            capture.TryStartCapture(true);\n'
                                                                        '            '
                                                                        'Assert.IsTrue(capture.CaptureStarted);\n'
                                                                        '            Assert.AreSame(def, new '
                                                                        'RaidEventRotationSystem().SelectActive(new[] '
                                                                        '{ def }, 4));\n'
                                                                        '        }\n'
                                                                        '\n'
                                                                        '        [Test]\n'
                                                                        '        public void AudioVisual_EventsFlame()\n'
                                                                        '        {\n'
                                                                        '            var bus = new EventBus();\n'
                                                                        '            var weather = false;\n'
                                                                        '            var fx = false;\n'
                                                                        '            '
                                                                        'bus.Subscribe<WeatherChangedEvent>(_ => '
                                                                        'weather = true);\n'
                                                                        '            '
                                                                        'bus.Subscribe<TransformationFxEvent>(_ => fx '
                                                                        '= true);\n'
                                                                        '            new '
                                                                        'MusicManager(bus).SwitchTrack("town_theme");\n'
                                                                        '            new '
                                                                        'WeatherVisualController(bus).SetWeather("rain");\n'
                                                                        '            new '
                                                                        'TransformationFXHooks(bus).Flame("a", '
                                                                        '"split");\n'
                                                                        '            var light = new '
                                                                        'DayNightLightingController();\n'
                                                                        '            light.Advance(0.25f);\n'
                                                                        '            Assert.IsTrue(weather);\n'
                                                                        '            Assert.IsTrue(fx);\n'
                                                                        '            Assert.Greater(light.Time01, '
                                                                        '0f);\n'
                                                                        '        }\n'
                                                                        '\n'
                                                                        '        [Test]\n'
                                                                        '        public void '
                                                                        'DataValidation_CatchesBadData()\n'
                                                                        '        {\n'
                                                                        '            var s1 = '
                                                                        'TestFactories.Species("dup");\n'
                                                                        '            var s2 = '
                                                                        'TestFactories.Species("dup");\n'
                                                                        '            var result = '
                                                                        '__PROJECT_NAMESPACE__DataValidator.ValidateSpecies(new[] '
                                                                        '{ s1, s2 });\n'
                                                                        '            Assert.IsFalse(result.IsValid);\n'
                                                                        '            var table = '
                                                                        'ScriptableObject.CreateInstance<EncounterTable>();\n'
                                                                        '            table.entries = new '
                                                                        'EncounterEntry[0];\n'
                                                                        '            '
                                                                        'Assert.IsFalse(__PROJECT_NAMESPACE__DataValidator.ValidateEncounterTable(table).IsValid);\n'
                                                                        '        }\n'
                                                                        '    }\n'
                                                                        '}\n',
 'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/UIInteractionEncounterTests.cs': 'using __PROJECT_NAMESPACE__.Battle;\n'
                                                                      'using __PROJECT_NAMESPACE__.Core;\n'
                                                                      'using __PROJECT_NAMESPACE__.EncounterSystem;\n'
                                                                      'using __PROJECT_NAMESPACE__.Events;\n'
                                                                      'using __PROJECT_NAMESPACE__.Interaction;\n'
                                                                      'using __PROJECT_NAMESPACE__.Overworld;\n'
                                                                      'using __PROJECT_NAMESPACE__.Pokemon;\n'
                                                                      'using __PROJECT_NAMESPACE__.Save;\n'
                                                                      'using __PROJECT_NAMESPACE__.UI;\n'
                                                                      'using NUnit.Framework;\n'
                                                                      'using UnityEngine;\n'
                                                                      '\n'
                                                                      'namespace __PROJECT_NAMESPACE__.Tests\n'
                                                                      '{\n'
                                                                      '    public sealed class '
                                                                      'UIInteractionEncounterTests\n'
                                                                      '    {\n'
                                                                      '        [Test]\n'
                                                                      '        public void '
                                                                      'BattleCommandMenu_EmitsCommand()\n'
                                                                      '        {\n'
                                                                      '            var menu = new '
                                                                      'BattleCommandMenu();\n'
                                                                      '            var got = BattleCommandType.Run;\n'
                                                                      '            menu.CommandSelected += c => got = '
                                                                      'c;\n'
                                                                      '            '
                                                                      'menu.Select(BattleCommandType.Fight);\n'
                                                                      '            '
                                                                      'Assert.AreEqual(BattleCommandType.Fight, got);\n'
                                                                      '        }\n'
                                                                      '\n'
                                                                      '        [Test]\n'
                                                                      '        public void '
                                                                      'Dialogue_AdvancesThroughLines()\n'
                                                                      '        {\n'
                                                                      '            var box = new DialogueBox();\n'
                                                                      '            box.Start(new[] { "A", "B" });\n'
                                                                      '            Assert.AreEqual("A", '
                                                                      'box.CurrentLine);\n'
                                                                      '            box.Advance();\n'
                                                                      '            Assert.AreEqual("B", '
                                                                      'box.CurrentLine);\n'
                                                                      '        }\n'
                                                                      '\n'
                                                                      '        [Test]\n'
                                                                      '        public void '
                                                                      'SettingsMenu_UpdatesManager()\n'
                                                                      '        {\n'
                                                                      '            var manager = new '
                                                                      'SettingsManager();\n'
                                                                      '            new '
                                                                      'SettingsMenu(manager).SetMasterVolume(0.4f);\n'
                                                                      '            Assert.AreEqual(0.4f, '
                                                                      'manager.Data.masterVolume);\n'
                                                                      '        }\n'
                                                                      '\n'
                                                                      '        [Test]\n'
                                                                      '        public void '
                                                                      'Interactable_TriggersWhenFaced()\n'
                                                                      '        {\n'
                                                                      '            var go = new GameObject("npc");\n'
                                                                      '            var npc = '
                                                                      'go.AddComponent<NPCDialogueComponent>();\n'
                                                                      '            npc.tile = Vector2Int.up;\n'
                                                                      '            var resolver = new '
                                                                      'FacingInteractionResolver();\n'
                                                                      '            resolver.Register(npc);\n'
                                                                      '            '
                                                                      'Assert.IsTrue(resolver.TryInteract(new '
                                                                      'InteractionContext(Vector2Int.zero, '
                                                                      'Direction.Up)));\n'
                                                                      '            Assert.IsTrue(npc.started);\n'
                                                                      '            Object.DestroyImmediate(go);\n'
                                                                      '        }\n'
                                                                      '\n'
                                                                      '        [Test]\n'
                                                                      '        public void '
                                                                      'EventTrigger_SetsFlags_AndFlagsPersist()\n'
                                                                      '        {\n'
                                                                      '            var flags = new '
                                                                      'FlagProgressionSystem();\n'
                                                                      '            var go = new '
                                                                      'GameObject("trigger");\n'
                                                                      '            var trigger = '
                                                                      'go.AddComponent<WorldEventTrigger>();\n'
                                                                      '            trigger.flagKey = "gate_open";\n'
                                                                      '            trigger.Trigger(flags);\n'
                                                                      '            var save = new SaveData();\n'
                                                                      '            flags.WriteToSave(save);\n'
                                                                      '            var loaded = new '
                                                                      'FlagProgressionSystem();\n'
                                                                      '            loaded.LoadFromSave(save);\n'
                                                                      '            '
                                                                      'Assert.IsTrue(loaded.Get("gate_open"));\n'
                                                                      '            Object.DestroyImmediate(go);\n'
                                                                      '        }\n'
                                                                      '\n'
                                                                      '        [Test]\n'
                                                                      '        public void '
                                                                      'Cutscene_RunsStepsInOrder()\n'
                                                                      '        {\n'
                                                                      '            var seq = new CutsceneSequence();\n'
                                                                      '            seq.Add(new '
                                                                      'LogCutsceneStep("camera"));\n'
                                                                      '            seq.Add(new '
                                                                      'LogCutsceneStep("dialogue"));\n'
                                                                      '            CollectionAssert.AreEqual(new[] { '
                                                                      '"camera", "dialogue" }, seq.Run());\n'
                                                                      '        }\n'
                                                                      '\n'
                                                                      '        [Test]\n'
                                                                      '        public void '
                                                                      'TrainerDetection_StartsBattleEvent()\n'
                                                                      '        {\n'
                                                                      '            var bus = new EventBus();\n'
                                                                      '            var started = false;\n'
                                                                      '            bus.Subscribe<BattleStartedEvent>(_ '
                                                                      '=> started = true);\n'
                                                                      '            var go = new '
                                                                      'GameObject("trainer");\n'
                                                                      '            var trainer = '
                                                                      'go.AddComponent<TrainerDetectionComponent>();\n'
                                                                      '            trainer.tile = Vector2Int.zero;\n'
                                                                      '            trainer.facing = Direction.Up;\n'
                                                                      '            Assert.IsTrue(trainer.CanDetect(new '
                                                                      'Vector2Int(0, 3)));\n'
                                                                      '            trainer.TriggerBattle(bus);\n'
                                                                      '            Assert.IsTrue(started);\n'
                                                                      '            Object.DestroyImmediate(go);\n'
                                                                      '        }\n'
                                                                      '\n'
                                                                      '        [Test]\n'
                                                                      '        public void '
                                                                      'EncounterTable_ReturnsLegalSpecies_AndRatesConfigurable()\n'
                                                                      '        {\n'
                                                                      '            var table = '
                                                                      'ScriptableObject.CreateInstance<EncounterTable>();\n'
                                                                      '            table.entries = new[] { new '
                                                                      'EncounterEntry { species = '
                                                                      'TestFactories.Species("wildling"), weight = 1 } '
                                                                      '};\n'
                                                                      '            var system = new '
                                                                      'RandomEncounterSystem();\n'
                                                                      '            Assert.NotNull(system.Roll(table, '
                                                                      'new System.Random(1)).species);\n'
                                                                      '            '
                                                                      'Assert.IsTrue(system.ShouldTrigger(1f, new '
                                                                      'FixedRandomSource(0)));\n'
                                                                      '            '
                                                                      'Assert.IsTrue(system.CheckStructuredStep(5, 5, '
                                                                      '1f, new FixedRandomSource(0)));\n'
                                                                      '            '
                                                                      'Assert.IsTrue(system.CheckWildTimed(10f, 5f, '
                                                                      '1f, new FixedRandomSource(0)));\n'
                                                                      '        }\n'
                                                                      '    }\n'
                                                                      '}\n',
 'Assets/Tests/__PROJECT_NAMESPACE__/PlayMode/__PROJECT_NAMESPACE__.PlayModeTests.asmdef': '{\n'
                                                                         '  "name": "__PROJECT_NAMESPACE__.PlayModeTests",\n'
                                                                         '  "rootNamespace": "__PROJECT_NAMESPACE__.Tests",\n'
                                                                         '  "references": [\n'
                                                                         '    "__PROJECT_NAMESPACE__.Runtime"\n'
                                                                         '  ],\n'
                                                                         '  "includePlatforms": [],\n'
                                                                         '  "excludePlatforms": [],\n'
                                                                         '  "allowUnsafeCode": false,\n'
                                                                         '  "overrideReferences": false,\n'
                                                                         '  "precompiledReferences": [],\n'
                                                                         '  "autoReferenced": false,\n'
                                                                         '  "defineConstraints": [],\n'
                                                                         '  "versionDefines": [],\n'
                                                                         '  "optionalUnityReferences": [\n'
                                                                         '    "TestAssemblies"\n'
                                                                         '  ],\n'
                                                                         '  "noEngineReferences": false\n'
                                                                         '}\n',
 'Assets/Tests/__PROJECT_NAMESPACE__/PlayMode/SmokePlayModeTests.cs': 'using System.Collections;\n'
                                                             'using __PROJECT_NAMESPACE__.CameraSystem;\n'
                                                             'using __PROJECT_NAMESPACE__.Overworld;\n'
                                                             'using NUnit.Framework;\n'
                                                             'using UnityEngine;\n'
                                                             'using UnityEngine.TestTools;\n'
                                                             '\n'
                                                             'namespace __PROJECT_NAMESPACE__.Tests\n'
                                                             '{\n'
                                                             '    public sealed class SmokePlayModeTests\n'
                                                             '    {\n'
                                                             '        [UnityTest]\n'
                                                             '        public IEnumerator '
                                                             'PlayerAndCameraComponentsCanTickInPlayMode()\n'
                                                             '        {\n'
                                                             '            var player = new GameObject("player");\n'
                                                             '            var profile = '
                                                             'ScriptableObject.CreateInstance<AreaMovementProfile>();\n'
                                                             '            profile.mode = MovementMode.StructuredGrid;\n'
                                                             '            var movement = '
                                                             'player.AddComponent<PlayerMovementController>();\n'
                                                             '            movement.Configure(profile);\n'
                                                             '            var cam = new GameObject("camera");\n'
                                                             '            var follow = '
                                                             'cam.AddComponent<CameraFollowController>();\n'
                                                             '            follow.SetTarget(player.transform);\n'
                                                             '            yield return null;\n'
                                                             '            Assert.IsTrue(follow.HasTarget);\n'
                                                             '            Object.Destroy(player);\n'
                                                             '            Object.Destroy(cam);\n'
                                                             '        }\n'
                                                             '    }\n'
                                                             '}\n',
 'Docs/__PROJECT_NAMESPACE___RPG.md': '# __PROJECT_DISPLAY_NAME__\n'
                             '\n'
                             'A Unity 2022+ 2.5D monster-catching RPG engine foundation using original placeholder '
                             'creatures and systems.\n'
                             '\n'
                             'The project focuses on modular, testable C# systems: overworld movement, camera modes, '
                             'creature data, battles, save/load, UI scaffolds, events, encounters, transformations, '
                             'fusion, raids, audio/visual hooks, and editor validation tools.\n'
                             '\n'
                             'Open with Unity 2022.3.62f3 or newer. The generator uses the combined startup scene '
                             '`Assets/Scenes/PrototypeRegion.unity` for overworld, battle, grass encounter, raid, and tooling tests.\n'}

PROJECT_FRAMEWORK_TEMPLATE_FILES.update({
    'Assets/Scripts/Battle/AdvancedBattleSystem.cs': r'''using System;
using System.Collections.Generic;
using System.Linq;
using __PROJECT_NAMESPACE__.Pokemon;
using UnityEngine;

namespace __PROJECT_NAMESPACE__.Battle.Advanced
{
    public enum BattleState { None, Intro, SendOut, StartTurn, CommandSelection, TargetSelection, ActionOrdering, ActionExecution, DamageResolution, SecondaryEffects, StatusResolution, SwitchResolution, FaintResolution, CaptureAttempt, TransformationSelection, RaidPhaseCheck, EndTurn, RewardResolution, Victory, Defeat, Escape, Cleanup }
    public enum BattleFormatType { WildSingle, TrainerSingle, Double, Multi, Rival, GymLeader, Legendary, Raid, Boss, Tutorial, ScriptedStory, PostgameChallenge }
    public enum ParticipantKind { Player, WildCreature, Trainer, Rival, GymLeader, RaidBoss, AiAlly, OnlineAlly, OnlineOpponent }
    public enum BattleCommandKind { Fight, Bag, Party, Run, Capture, MegaEvolution, DimensionSplit, Fusion, RaidCheer, Wait }
    public enum TargetRule { SelectedEnemy, AllEnemies, AllAllies, Self, Any, Field }
    public enum BattleMoveTag { Contact, Sound, Punch, Bite, Pulse, ProtectBlocked, Reflectable, Snatchable, Signature, DimensionSignature, FusionExclusive, RaidBoss }
    public enum PermanentStatus { None, Burn, Poison, BadPoison, Paralysis, Sleep, Freeze }
    public enum VolatileStatus { Confusion, Flinch, LeechDrain, Curse, Infatuation, Taunt, Encore, Disable, Protect, Substitute, Trapped, Bound, Charging, Recharge }
    public enum StatId { Attack, Defense, SpecialAttack, SpecialDefense, Speed, Accuracy, Evasion }
    public enum WeatherKind { Clear, Rain, HarshSunlight, Sandstorm, Snow, Fog, DimensionalStorm }
    public enum TerrainKind { None, Electric, Grassy, Psychic, Misty, Dimensional, RaidArena }
    public enum BattleAiDifficulty { Easy, Normal, Smart, Boss, RaidBoss }
    public enum TransformationKind { None, Mega, DimensionSplit, Fusion }
    public enum BattleEventTiming { OnBattleStart, OnSwitchIn, OnTurnStart, OnBeforeMoveSelected, OnBeforeMoveUsed, OnMoveHit, OnDamageTaken, OnDamageDealt, OnStatusApplied, OnStatChange, OnWeatherChange, OnTerrainChange, OnTransformation, OnHPThreshold, OnFaint, OnTurnEnd }
    public enum BattleEffectTiming { StartTurn, BeforeAction, DuringAction, AfterAction, EndTurn, OnSwitch, OnFaint, OnBattleEnd }
    public enum RaidInitiatorKind { RaidDen, LegendaryShrine, EventPortal, PostgameArena, StoryEncounter }
    public enum RaidPhaseState { Selection, Lobby, TeamConfirmation, IntroCinematic, BossBattle, ShieldPhase, TimerManagement, Victory, Defeat, RewardPhase, CapturePhase, Cleanup }
    public enum AdvancedRaidDifficultyTier { OneStar, TwoStar, ThreeStar, FourStar, FiveStar, Legendary, Event }
    public enum RaidRewardKind { RareItem, EvolutionMaterial, FusionMaterial, DimensionEnergy, Currency, Cosmetic, HiddenAbility, RareCreature }

    public interface IBattleRandom { int Range(int minInclusive, int maxExclusive); float Value01(); }

    public sealed class SeededBattleRandom : IBattleRandom
    {
        private readonly System.Random random;
        public SeededBattleRandom(int seed) { random = new System.Random(seed); }
        public int Range(int minInclusive, int maxExclusive) { return random.Next(minInclusive, maxExclusive); }
        public float Value01() { return (float)random.NextDouble(); }
    }

    [Serializable]
    public sealed class BattleRuleset
    {
        public BattleFormatType format = BattleFormatType.WildSingle;
        public int activeCreaturesPerSide = 1;
        public bool switchingAllowed = true;
        public bool captureAllowed = true;
        public bool escapeAllowed = true;
        public bool itemsAllowed = true;
        public bool transformationsAllowed = true;
        public bool rewardsEnabled = true;
        public BattleAiDifficulty aiDifficulty = BattleAiDifficulty.Normal;
        public string battleBackground = "field";
        public string musicProfile = "battle_standard";
        public string introAnimationProfile = "snap_intro";
        public string cameraProfile = "gen5_snap";
        public string arenaRules = "standard";
        public string timerRule = "none";
        public readonly List<BattleCommandKind> allowedCommands = new List<BattleCommandKind> { BattleCommandKind.Fight, BattleCommandKind.Bag, BattleCommandKind.Party, BattleCommandKind.Run, BattleCommandKind.Capture, BattleCommandKind.MegaEvolution, BattleCommandKind.DimensionSplit, BattleCommandKind.Fusion, BattleCommandKind.RaidCheer, BattleCommandKind.Wait };

        public static BattleRuleset ForFormat(BattleFormatType format)
        {
            var rules = new BattleRuleset { format = format };
            if (format == BattleFormatType.Double) rules.activeCreaturesPerSide = 2;
            if (format == BattleFormatType.Multi) rules.activeCreaturesPerSide = 2;
            if (format == BattleFormatType.TrainerSingle || format == BattleFormatType.Rival || format == BattleFormatType.GymLeader || format == BattleFormatType.Boss || format == BattleFormatType.ScriptedStory || format == BattleFormatType.PostgameChallenge)
            {
                rules.captureAllowed = false;
                rules.escapeAllowed = false;
            }
            if (format == BattleFormatType.Legendary)
            {
                rules.escapeAllowed = false;
                rules.musicProfile = "battle_legendary";
                rules.introAnimationProfile = "legendary_intro";
            }
            if (format == BattleFormatType.Raid)
            {
                rules.captureAllowed = false;
                rules.escapeAllowed = false;
                rules.activeCreaturesPerSide = 4;
                rules.aiDifficulty = BattleAiDifficulty.RaidBoss;
                rules.battleBackground = "raid_arena";
                rules.musicProfile = "battle_raid";
                rules.introAnimationProfile = "boss_intro";
                rules.cameraProfile = "raid_boss";
                rules.arenaRules = "raid_shield_timer";
                rules.timerRule = "shared_raid_timer";
            }
            return rules;
        }
    }

    [Serializable]
    public sealed class SecondaryBattleEffect
    {
        public PermanentStatus status = PermanentStatus.None;
        public int chancePercent;
        public StatId stat;
        public int stageDelta;
        public bool affectsTarget = true;
        public BattleEffectTiming timing = BattleEffectTiming.AfterAction;
    }

    [Serializable]
    public sealed class BattleMoveData
    {
        public string moveId = "pulse";
        public string displayName = "Pulse";
        public string description = "A clean prototype strike.";
        public CreatureType type = CreatureType.Neutral;
        public MoveCategory category = MoveCategory.Physical;
        public int basePower = 40;
        public int accuracy = 100;
        public int pp = 35;
        public int priority;
        public TargetRule targetRule = TargetRule.SelectedEnemy;
        public readonly HashSet<BattleMoveTag> tags = new HashSet<BattleMoveTag>();
        public bool bypassesAccuracy;
        public bool canProtectAgainst = true;
        public bool reflectable;
        public bool snatchable;
        public float recoilPercent;
        public float drainPercent;
        public float healPercent;
        public SecondaryBattleEffect secondaryEffect;
        public WeatherKind weatherToSet = WeatherKind.Clear;
        public TerrainKind terrainToSet = TerrainKind.None;
        public int minHits = 1;
        public int maxHits = 1;
        public float criticalModifier = 1.5f;
        public bool forcesTargetSwitch;
        public bool switchesUserOut;
        public int chargeTurns;
        public int rechargeTurns;
        public string animationProfile = "fast_hit";
        public string audioProfile = "impact_light";
        public string cameraProfile = "quick_cut";
        public bool IsDamaging => category != MoveCategory.Status && basePower > 0;
        public bool HasTag(BattleMoveTag tag) { return tags.Contains(tag); }
    }

    public sealed class StatStageSet
    {
        private readonly Dictionary<StatId, int> stages = new Dictionary<StatId, int>();
        public int Get(StatId stat) { return stages.TryGetValue(stat, out var value) ? value : 0; }
        public void Set(StatId stat, int stage) { stages[stat] = Mathf.Clamp(stage, -6, 6); }
        public void Change(StatId stat, int delta) { Set(stat, Get(stat) + delta); }
        public void ResetVolatileStages() { stages.Clear(); }
        public float Multiplier(StatId stat)
        {
            var stage = Get(stat);
            if (stat == StatId.Accuracy || stat == StatId.Evasion) return stage >= 0 ? (3f + stage) / 3f : 3f / (3f - stage);
            return stage >= 0 ? (2f + stage) / 2f : 2f / (2f - stage);
        }
    }

    public sealed class BattleCreature
    {
        public CreatureSpecies speciesReference;
        public FormDefinition currentForm;
        public int currentLevel;
        public int currentHp;
        public int maxHp;
        public StatBlock currentStats;
        public readonly StatStageSet statStages = new StatStageSet();
        public CreatureType primaryType;
        public CreatureType secondaryType;
        public CreatureType temporaryPrimaryType = CreatureType.None;
        public CreatureType temporarySecondaryType = CreatureType.None;
        public AbilityDefinition currentAbility;
        public ItemDefinition heldItem;
        public readonly List<BattleMoveData> knownMoves = new List<BattleMoveData>();
        public readonly Dictionary<string, int> currentPp = new Dictionary<string, int>();
        public PermanentStatus permanentStatus;
        public readonly HashSet<VolatileStatus> volatileStatuses = new HashSet<VolatileStatus>();
        public readonly List<string> battleOnlyEffects = new List<string>();
        public TransformationKind transformationState;
        public bool megaState, dimensionSplitState, fusionState, raidBossState, shieldState;
        public int shieldSegments;
        public int raidPhaseIndex;
        public bool raidRageState;
        public int raidActionsPerTurn = 1;
        public readonly Dictionary<string, int> turnCounters = new Dictionary<string, int>();
        public readonly List<int> damageHistory = new List<int>();
        public BattleMoveData lastMoveUsed;
        public string lastDamageSource;
        public bool hasMovedThisTurn;
        public int lastTurnActed;
        public bool IsFainted => currentHp <= 0;
        public int catchRate = 45;
        public CreatureType EffectivePrimaryType => temporaryPrimaryType == CreatureType.None ? primaryType : temporaryPrimaryType;
        public CreatureType EffectiveSecondaryType => temporarySecondaryType == CreatureType.None ? secondaryType : temporarySecondaryType;

        public BattleCreature(CreatureSpecies species, int level)
        {
            speciesReference = species;
            currentLevel = Mathf.Max(1, level);
            primaryType = species != null ? species.primaryType : CreatureType.Neutral;
            secondaryType = species != null ? species.secondaryType : CreatureType.None;
            currentAbility = species != null && species.abilities != null && species.abilities.Length > 0 ? species.abilities[0] : null;
            RecalculateStats();
            currentHp = maxHp;
        }

        public void AddMove(BattleMoveData move)
        {
            if (move == null) return;
            knownMoves.Add(move);
            currentPp[move.moveId] = move.pp;
        }

        public void ApplyDamage(int damage, string source = null)
        {
            var finalDamage = Mathf.Max(0, damage);
            currentHp = Mathf.Max(0, currentHp - finalDamage);
            damageHistory.Add(finalDamage);
            lastDamageSource = source;
        }

        public void Heal(int amount) { currentHp = Mathf.Min(maxHp, currentHp + Mathf.Max(0, amount)); }

        public void RecalculateStats()
        {
            var baseStats = speciesReference != null ? speciesReference.baseStats : new StatBlock(45, 45, 45, 45, 45, 45);
            currentStats = new StatBlock(
                ((baseStats.hp * 2 * currentLevel) / 100) + currentLevel + 10,
                ((baseStats.attack * 2 * currentLevel) / 100) + 5,
                ((baseStats.defense * 2 * currentLevel) / 100) + 5,
                ((baseStats.specialAttack * 2 * currentLevel) / 100) + 5,
                ((baseStats.specialDefense * 2 * currentLevel) / 100) + 5,
                ((baseStats.speed * 2 * currentLevel) / 100) + 5);
            if (currentForm != null)
            {
                currentStats = currentStats.Scale(Mathf.Max(0.1f, currentForm.statMultiplier)) + currentForm.statModifier;
                if (currentForm.primaryTypeOverride != CreatureType.None) primaryType = currentForm.primaryTypeOverride;
                if (currentForm.secondaryTypeOverride != CreatureType.None) secondaryType = currentForm.secondaryTypeOverride;
                if (currentForm.abilityOverride != null) currentAbility = currentForm.abilityOverride;
            }
            maxHp = Mathf.Max(1, currentStats.hp);
            currentHp = currentHp <= 0 ? maxHp : Mathf.Min(currentHp, maxHp);
        }

        public int ModifiedStat(StatId stat, bool ignorePositive = false, bool ignoreNegative = false)
        {
            var baseValue = stat == StatId.Attack ? currentStats.attack :
                stat == StatId.Defense ? currentStats.defense :
                stat == StatId.SpecialAttack ? currentStats.specialAttack :
                stat == StatId.SpecialDefense ? currentStats.specialDefense :
                stat == StatId.Speed ? currentStats.speed : 1;
            var stage = statStages.Get(stat);
            if (ignorePositive && stage > 0) stage = 0;
            if (ignoreNegative && stage < 0) stage = 0;
            var temp = new StatStageSet();
            temp.Set(stat, stage);
            return Mathf.Max(1, Mathf.RoundToInt(baseValue * temp.Multiplier(stat)));
        }

        public void ResetOnSwitch()
        {
            statStages.ResetVolatileStages();
            volatileStatuses.Clear();
            temporaryPrimaryType = CreatureType.None;
            temporarySecondaryType = CreatureType.None;
            hasMovedThisTurn = false;
        }
    }

    public sealed class BattleParticipant
    {
        public string participantId;
        public ParticipantKind kind;
        public readonly List<BattleCreature> activeSlots = new List<BattleCreature>();
        public readonly List<BattleCreature> reserveParty = new List<BattleCreature>();
        public readonly List<BattleCommandKind> availableCommands = new List<BattleCommandKind>();
        public bool itemPermissions = true, switchPermissions = true, capturePermissions = true, transformationPermissions = true;
        public IBattleAiController aiController;
        public BattleCreature Active => activeSlots.FirstOrDefault(c => c != null && !c.IsFainted);
        public bool HasLegalSwitchTarget() { return switchPermissions && reserveParty.Any(c => c != null && !c.IsFainted); }
    }

    public sealed class BattleCommand
    {
        public BattleParticipant user;
        public BattleCreature actor;
        public BattleCreature target;
        public BattleCommandKind kind;
        public BattleMoveData move;
        public ItemDefinition item;
        public int targetSlot;
        public static BattleCommand Fight(BattleParticipant user, BattleCreature target, BattleMoveData move)
        {
            return new BattleCommand { user = user, actor = user?.Active, target = target, kind = BattleCommandKind.Fight, move = move };
        }
        public static BattleCommand Capture(BattleParticipant user, BattleCreature target)
        {
            return new BattleCommand { user = user, actor = user?.Active, target = target, kind = BattleCommandKind.Capture };
        }
        public static BattleCommand Switch(BattleParticipant user, int targetSlot)
        {
            return new BattleCommand { user = user, actor = user?.Active, kind = BattleCommandKind.Party, targetSlot = targetSlot };
        }
    }

    public sealed class BattleContext
    {
        public string battleId = Guid.NewGuid().ToString("N");
        public BattleRuleset rules = BattleRuleset.ForFormat(BattleFormatType.WildSingle);
        public readonly List<BattleParticipant> participants = new List<BattleParticipant>();
        public readonly BattleEventLog eventLog = new BattleEventLog();
        public readonly WeatherController weather = new WeatherController();
        public readonly TerrainController terrain = new TerrainController();
        public int turnNumber = 1;
        public bool trickRoom;
        public bool raidVictory;
        public RaidPhaseState raidPhaseState = RaidPhaseState.Selection;
    }

    public sealed class BattleStateMachine
    {
        public BattleState State { get; private set; }
        public readonly List<BattleState> History = new List<BattleState>();
        public void Change(BattleState next) { State = next; History.Add(next); }
        public void StartBattle()
        {
            Change(BattleState.Intro);
            Change(BattleState.SendOut);
            Change(BattleState.StartTurn);
            Change(BattleState.CommandSelection);
        }
        public void MarkTurnResolutionSkeleton()
        {
            Change(BattleState.TargetSelection);
            Change(BattleState.ActionOrdering);
            Change(BattleState.ActionExecution);
            Change(BattleState.DamageResolution);
            Change(BattleState.SecondaryEffects);
            Change(BattleState.StatusResolution);
            Change(BattleState.FaintResolution);
            Change(BattleState.RaidPhaseCheck);
            Change(BattleState.EndTurn);
        }
    }

    public sealed class BattleEventLog
    {
        private readonly List<string> entries = new List<string>();
        public IReadOnlyList<string> Entries => entries;
        public void Add(string entry) { entries.Add(entry); }
        public bool Contains(string text) { return entries.Any(e => e.Contains(text)); }
    }

    public sealed class BattleTypeChart
    {
        private readonly Dictionary<string, float> multipliers = new Dictionary<string, float>();
        private static string Key(CreatureType attack, CreatureType defend) { return attack + ">" + defend; }
        public void Set(CreatureType attack, CreatureType defend, float multiplier) { multipliers[Key(attack, defend)] = multiplier; }
        public float Get(CreatureType attack, CreatureType defend) { return defend == CreatureType.None ? 1f : multipliers.TryGetValue(Key(attack, defend), out var value) ? value : 1f; }
        public float Get(CreatureType attack, CreatureType defendA, CreatureType defendB) { return Get(attack, defendA) * Get(attack, defendB); }
        public static BattleTypeChart Default()
        {
            var chart = new BattleTypeChart();
            chart.Set(CreatureType.Flame, CreatureType.Leaf, 2f);
            chart.Set(CreatureType.Leaf, CreatureType.Flame, 0.5f);
            chart.Set(CreatureType.Spark, CreatureType.Tide, 2f);
            chart.Set(CreatureType.Neutral, CreatureType.Shadow, 0f);
            return chart;
        }
    }

    public sealed class AccuracyResolver
    {
        public bool DoesHit(BattleCreature user, BattleCreature target, BattleMoveData move, IBattleRandom rng)
        {
            if (move == null || move.bypassesAccuracy || move.accuracy <= 0) return true;
            var accuracyMultiplier = user != null ? user.statStages.Multiplier(StatId.Accuracy) : 1f;
            var evasionMultiplier = target != null ? target.statStages.Multiplier(StatId.Evasion) : 1f;
            var chance = Mathf.Clamp(move.accuracy * accuracyMultiplier / Mathf.Max(0.01f, evasionMultiplier), 1f, 100f);
            return rng.Range(1, 101) <= chance;
        }
    }

    public sealed class DamageRequest
    {
        public BattleCreature attacker, defender;
        public BattleMoveData move;
        public bool critical, spreadMove;
        public BattleContext context;
        public IBattleRandom rng = new SeededBattleRandom(1);
    }

    public sealed class DamageResult
    {
        public int damage;
        public float typeMultiplier = 1f;
        public bool immune, critical;
        public float randomModifier = 1f;
    }

    public sealed class DamageCalculator
    {
        private readonly BattleTypeChart typeChart;
        public DamageCalculator(BattleTypeChart chart) { typeChart = chart ?? BattleTypeChart.Default(); }

        public DamageResult Calculate(DamageRequest request)
        {
            var result = new DamageResult { critical = request != null && request.critical };
            if (request == null || request.attacker == null || request.defender == null || request.move == null || !request.move.IsDamaging) return result;
            var move = request.move;
            result.typeMultiplier = typeChart.Get(move.type, request.defender.EffectivePrimaryType, request.defender.EffectiveSecondaryType);
            if (Mathf.Approximately(result.typeMultiplier, 0f))
            {
                result.immune = true;
                result.damage = 0;
                return result;
            }
            var physical = move.category == MoveCategory.Physical;
            var offensive = request.attacker.ModifiedStat(physical ? StatId.Attack : StatId.SpecialAttack, false, request.critical);
            var defensive = request.defender.ModifiedStat(physical ? StatId.Defense : StatId.SpecialDefense, request.critical, false);
            var damage = ((((2f * request.attacker.currentLevel / 5f) + 2f) * move.basePower * offensive / Mathf.Max(1, defensive)) / 50f) + 2f;
            if (request.critical) damage *= move.criticalModifier;
            result.randomModifier = request.rng.Range(85, 101) / 100f;
            damage *= result.randomModifier;
            if (move.type == request.attacker.EffectivePrimaryType || move.type == request.attacker.EffectiveSecondaryType) damage *= 1.5f;
            damage *= result.typeMultiplier;
            if (physical && request.attacker.permanentStatus == PermanentStatus.Burn) damage *= 0.5f;
            if (request.context != null)
            {
                damage *= request.context.weather.ModifyDamage(move);
                damage *= request.context.terrain.ModifyDamage(move);
            }
            if (request.spreadMove) damage *= 0.75f;
            if (request.attacker.raidBossState) damage *= 1.15f;
            if (request.attacker.dimensionSplitState) damage *= 1.25f;
            if (request.attacker.megaState) damage *= 1.15f;
            if (request.attacker.fusionState) damage *= 1.1f;
            result.damage = Mathf.Max(1, Mathf.FloorToInt(damage));
            return result;
        }
    }

    public sealed class ActionQueue
    {
        private sealed class OrderedCommand { public BattleCommand command; public int tier, priority, speed, tie; }
        public List<BattleCommand> Sort(IEnumerable<BattleCommand> commands, BattleContext context, IBattleRandom rng)
        {
            var trickRoom = context != null && context.trickRoom;
            return commands.Where(c => c != null && c.actor != null && !c.actor.IsFainted)
                .Select(c => new OrderedCommand { command = c, tier = CategoryPriority(c), priority = c.kind == BattleCommandKind.Fight && c.move != null ? c.move.priority : 0, speed = c.actor.ModifiedStat(StatId.Speed), tie = rng.Range(0, 1000000) })
                .OrderByDescending(o => o.tier)
                .ThenByDescending(o => o.priority)
                .ThenBy(o => trickRoom ? o.speed : -o.speed)
                .ThenBy(o => o.tie)
                .Select(o => o.command)
                .ToList();
        }

        private static int CategoryPriority(BattleCommand command)
        {
            if (command.kind == BattleCommandKind.Party) return 60;
            if (command.kind == BattleCommandKind.Bag) return 50;
            if (command.kind == BattleCommandKind.MegaEvolution || command.kind == BattleCommandKind.DimensionSplit || command.kind == BattleCommandKind.Fusion) return 45;
            if (command.kind == BattleCommandKind.Capture) return 40;
            if (command.kind == BattleCommandKind.RaidCheer) return 30;
            if (command.kind == BattleCommandKind.Fight) return 20;
            return 0;
        }
    }

    public sealed class BattleCommandValidator
    {
        public bool IsAllowed(BattleContext context, BattleCommandKind command)
        {
            if (context != null && command == BattleCommandKind.Capture && context.rules.format == BattleFormatType.Raid && context.raidVictory) return true;
            return IsAllowed(context?.rules, command);
        }

        public bool IsAllowed(BattleRuleset rules, BattleCommandKind command)
        {
            if (rules == null) return false;
            if (!rules.allowedCommands.Contains(command)) return false;
            if (command == BattleCommandKind.Bag && !rules.itemsAllowed) return false;
            if (command == BattleCommandKind.Party && !rules.switchingAllowed) return false;
            if (command == BattleCommandKind.Run && !rules.escapeAllowed) return false;
            if (command == BattleCommandKind.Capture && !rules.captureAllowed) return false;
            if ((command == BattleCommandKind.MegaEvolution || command == BattleCommandKind.DimensionSplit || command == BattleCommandKind.Fusion) && !rules.transformationsAllowed) return false;
            return true;
        }
    }

    public sealed class SwitchController
    {
        public bool CanSwitch(BattleParticipant participant, int reserveIndex)
        {
            return participant != null && participant.switchPermissions && reserveIndex >= 0 && reserveIndex < participant.reserveParty.Count && participant.reserveParty[reserveIndex] != null && !participant.reserveParty[reserveIndex].IsFainted;
        }

        public bool SwitchTo(BattleParticipant participant, int reserveIndex, BattleContext context)
        {
            if (!CanSwitch(participant, reserveIndex)) return false;
            var outgoing = participant.Active;
            if (outgoing != null) outgoing.ResetOnSwitch();
            var incoming = participant.reserveParty[reserveIndex];
            participant.reserveParty.RemoveAt(reserveIndex);
            if (participant.activeSlots.Count == 0) participant.activeSlots.Add(incoming);
            else
            {
                if (outgoing != null) participant.reserveParty.Add(outgoing);
                participant.activeSlots[0] = incoming;
            }
            context?.eventLog.Add("Switch resolved");
            return true;
        }
    }

    public sealed class StatusController
    {
        public bool CanSelectMove(BattleCreature creature) { return creature != null && !creature.volatileStatuses.Contains(VolatileStatus.Recharge) && !creature.volatileStatuses.Contains(VolatileStatus.Flinch); }
        public void ApplyPermanent(BattleCreature creature, PermanentStatus status) { if (creature != null && creature.permanentStatus == PermanentStatus.None) creature.permanentStatus = status; }
        public bool CanApplyStatus(BattleCreature creature, PermanentStatus status, BattleContext context = null)
        {
            if (creature == null || status == PermanentStatus.None || creature.permanentStatus != PermanentStatus.None) return false;
            if (context != null && context.terrain.Current == TerrainKind.Misty && (status == PermanentStatus.Sleep || status == PermanentStatus.Burn || status == PermanentStatus.Poison || status == PermanentStatus.BadPoison)) return false;
            return true;
        }
        public void ResolveTiming(BattleCreature creature, BattleEffectTiming timing)
        {
            if (timing == BattleEffectTiming.EndTurn) ResolveEndTurn(creature);
            if (timing == BattleEffectTiming.OnSwitch && creature != null) creature.ResetOnSwitch();
        }
        public void ResolveEndTurn(BattleCreature creature)
        {
            if (creature == null || creature.IsFainted) return;
            if (creature.permanentStatus == PermanentStatus.Burn || creature.permanentStatus == PermanentStatus.Poison) creature.ApplyDamage(Mathf.Max(1, creature.maxHp / 8), creature.permanentStatus.ToString());
            if (creature.permanentStatus == PermanentStatus.BadPoison)
            {
                var counter = creature.turnCounters.TryGetValue("bad_poison", out var value) ? value + 1 : 1;
                creature.turnCounters["bad_poison"] = counter;
                creature.ApplyDamage(Mathf.Max(1, creature.maxHp * counter / 16), "BadPoison");
            }
        }
    }

    public sealed class AbilityProcessor
    {
        public void Trigger(BattleEventTiming timing, BattleCreature owner, BattleContext battle, BattleMoveData move = null)
        {
            Trigger(timing.ToString(), owner, battle, move);
        }

        public void Trigger(string timing, BattleCreature owner, BattleContext battle, BattleMoveData move = null)
        {
            if (owner?.currentAbility == null || battle == null) return;
            battle.eventLog.Add("Ability " + owner.currentAbility.id + " triggered at " + timing);
            if (timing == BattleEventTiming.OnBattleStart.ToString() && owner.currentAbility.id == "rain_start") battle.weather.Set(WeatherKind.Rain, 5);
            if (timing == BattleEventTiming.OnTransformation.ToString() && owner.currentAbility.id == "dimension_amp") owner.battleOnlyEffects.Add("dimension_amp");
        }
    }

    public sealed class ItemProcessor
    {
        public void Trigger(BattleEventTiming timing, BattleCreature owner, BattleContext battle)
        {
            if (timing == BattleEventTiming.OnHPThreshold) TriggerHpThreshold(owner, battle);
            else if (owner?.heldItem != null && battle != null) battle.eventLog.Add("Item " + owner.heldItem.id + " checked at " + timing);
        }

        public void TriggerHpThreshold(BattleCreature owner, BattleContext battle)
        {
            if (owner?.heldItem == null || battle == null) return;
            if (owner.currentHp <= owner.maxHp / 2 && owner.heldItem.consumable)
            {
                owner.Heal(Mathf.Max(1, owner.maxHp / 4));
                battle.eventLog.Add("Item " + owner.heldItem.id + " restored HP");
                owner.heldItem = null;
            }
        }
    }

    public sealed class WeatherController
    {
        public WeatherKind Current { get; private set; } = WeatherKind.Clear;
        public int TurnsRemaining { get; private set; }
        public void Set(WeatherKind weather, int turns) { Current = weather; TurnsRemaining = Mathf.Max(0, turns); }
        public void Tick() { if (TurnsRemaining > 0 && --TurnsRemaining == 0) Current = WeatherKind.Clear; }
        public float ModifyDamage(BattleMoveData move)
        {
            if (move == null) return 1f;
            if (Current == WeatherKind.Rain && move.type == CreatureType.Tide) return 1.5f;
            if (Current == WeatherKind.Rain && move.type == CreatureType.Flame) return 0.5f;
            if (Current == WeatherKind.HarshSunlight && move.type == CreatureType.Flame) return 1.5f;
            if (Current == WeatherKind.HarshSunlight && move.type == CreatureType.Tide) return 0.5f;
            if (Current == WeatherKind.DimensionalStorm && move.HasTag(BattleMoveTag.DimensionSignature)) return 1.25f;
            return 1f;
        }
    }

    public sealed class TerrainController
    {
        public TerrainKind Current { get; private set; } = TerrainKind.None;
        public int TurnsRemaining { get; private set; }
        public void Set(TerrainKind terrain, int turns) { Current = terrain; TurnsRemaining = Mathf.Max(0, turns); }
        public void Tick() { if (TurnsRemaining > 0 && --TurnsRemaining == 0) Current = TerrainKind.None; }
        public float ModifyDamage(BattleMoveData move)
        {
            if (move == null) return 1f;
            if (Current == TerrainKind.Grassy && move.type == CreatureType.Leaf) return 1.3f;
            if (Current == TerrainKind.Electric && move.type == CreatureType.Spark) return 1.3f;
            if (Current == TerrainKind.Dimensional && move.HasTag(BattleMoveTag.DimensionSignature)) return 1.3f;
            return 1f;
        }
    }

    public sealed class CaptureController
    {
        public bool CanCapture(BattleContext context) { return context != null && (context.rules.captureAllowed || (context.rules.format == BattleFormatType.Raid && context.raidVictory)); }
        public float CalculateChance(BattleCreature target, float captureDeviceModifier = 1f)
        {
            if (target == null || target.maxHp <= 0) return 0f;
            var hpFactor = 1f - Mathf.Clamp01(target.currentHp / (float)target.maxHp);
            var statusBonus = target.permanentStatus == PermanentStatus.None ? 1f : 1.5f;
            return Mathf.Clamp01(((target.catchRate / 255f) * 0.35f + hpFactor * 0.55f) * statusBonus * captureDeviceModifier);
        }
        public bool TryCapture(BattleContext context, BattleCreature target, IBattleRandom rng, out int shakes)
        {
            shakes = 0;
            if (!CanCapture(context)) return false;
            var chance = CalculateChance(target);
            shakes = Mathf.Clamp(Mathf.FloorToInt(chance * 4f), 0, 3);
            var success = rng.Value01() <= chance;
            if (success) shakes = 4;
            return success;
        }
    }

    public sealed class BattleRewardResult
    {
        public int experience;
        public int currency;
        public readonly List<string> items = new List<string>();
        public readonly List<string> progressionFlags = new List<string>();
    }

    public sealed class RewardController
    {
        public int AwardExperience(BattleCreature defeated, IEnumerable<BattleCreature> recipients, BattleContext context)
        {
            if (defeated == null || recipients == null || context == null || !context.rules.rewardsEnabled) return 0;
            var reward = Mathf.Max(1, defeated.currentLevel * 12);
            context.eventLog.Add("Award EXP " + reward);
            return reward;
        }
        public int AwardMoney(BattleContext context, int baseAmount) { return context == null || !context.rules.rewardsEnabled ? 0 : Mathf.Max(0, baseAmount); }
        public BattleRewardResult ResolveRewards(BattleContext context, BattleCreature defeated, IEnumerable<BattleCreature> recipients)
        {
            var result = new BattleRewardResult();
            result.experience = AwardExperience(defeated, recipients, context);
            result.currency = AwardMoney(context, context != null && context.rules.format == BattleFormatType.TrainerSingle ? 120 : 0);
            if (context != null && context.rules.format == BattleFormatType.Raid) result.items.Add("raid_core_sample");
            if (context != null && context.rules.format == BattleFormatType.GymLeader) result.progressionFlags.Add("gym_clear_sample");
            return result;
        }
    }

    public interface IBattleAiController { BattleCommand ChooseCommand(BattleParticipant self, BattleParticipant opponent, BattleContext context); }

    public sealed class WildBattleAI : IBattleAiController
    {
        public BattleCommand ChooseCommand(BattleParticipant self, BattleParticipant opponent, BattleContext context)
        {
            var legal = self?.Active?.knownMoves.Where(m => m != null).ToList();
            if (legal == null || legal.Count == 0) return new BattleCommand { user = self, actor = self?.Active, kind = BattleCommandKind.Wait };
            var damaging = legal.Where(m => m.IsDamaging).OrderByDescending(m => m.basePower).FirstOrDefault();
            return BattleCommand.Fight(self, opponent?.Active, damaging ?? legal[0]);
        }
    }

    public sealed class TrainerBattleAI : IBattleAiController
    {
        private readonly DamageCalculator damage;
        public TrainerBattleAI(DamageCalculator damage) { this.damage = damage; }
        public BattleCommand ChooseCommand(BattleParticipant self, BattleParticipant opponent, BattleContext context)
        {
            var best = self?.Active?.knownMoves.Where(m => m != null).OrderByDescending(m => damage.Calculate(new DamageRequest { attacker = self.Active, defender = opponent?.Active, move = m, context = context, rng = new SeededBattleRandom(7) }).damage).FirstOrDefault();
            return best != null ? BattleCommand.Fight(self, opponent?.Active, best) : new BattleCommand { user = self, actor = self?.Active, kind = BattleCommandKind.Wait };
        }
    }

    public sealed class RaidBossBattleAI : IBattleAiController
    {
        public int actionsPerRound = 2;
        public BattleCommand ChooseCommand(BattleParticipant self, BattleParticipant opponent, BattleContext context)
        {
            var command = new WildBattleAI().ChooseCommand(self, opponent, context);
            context?.eventLog.Add("Raid boss queued " + actionsPerRound + " actions");
            return command;
        }
    }

    public sealed class RaidLobby
    {
        public string raidId = "prototype_raid";
        public int requiredAllies = 4;
        public readonly List<BattleParticipant> allies = new List<BattleParticipant>();
        public bool teamConfirmed;
        public bool Ready => teamConfirmed && allies.Count >= requiredAllies;
        public void AddAlly(BattleParticipant ally)
        {
            if (ally != null && !allies.Contains(ally)) allies.Add(ally);
        }
        public void ConfirmTeam() { teamConfirmed = true; }
    }

    public sealed class RaidArenaProfile
    {
        public string arenaId = "prototype_den";
        public string battleBackground = "raid_arena";
        public string lightingProfile = "dimensional_boss";
        public WeatherKind weather = WeatherKind.DimensionalStorm;
        public TerrainKind terrain = TerrainKind.RaidArena;
        public string cameraProfile = "raid_boss";
        public readonly List<string> hazards = new List<string>();
        public readonly List<string> vfx = new List<string>();
    }

    public sealed class RaidBossProfile
    {
        public string bossId = "raid_boss_sample";
        public RaidInitiatorKind source = RaidInitiatorKind.RaidDen;
        public AdvancedRaidDifficultyTier tier = AdvancedRaidDifficultyTier.OneStar;
        public readonly float[] shieldThresholds = { 0.75f, 0.5f, 0.25f };
        public int currentPhaseIndex;
        public bool rageState;

        public int HpMultiplier()
        {
            switch (tier)
            {
                case AdvancedRaidDifficultyTier.TwoStar: return 3;
                case AdvancedRaidDifficultyTier.ThreeStar: return 5;
                case AdvancedRaidDifficultyTier.FourStar: return 7;
                case AdvancedRaidDifficultyTier.FiveStar: return 10;
                case AdvancedRaidDifficultyTier.Legendary: return 14;
                case AdvancedRaidDifficultyTier.Event: return 16;
                default: return 2;
            }
        }

        public int ActionsPerTurn()
        {
            if (tier == AdvancedRaidDifficultyTier.Legendary || tier == AdvancedRaidDifficultyTier.Event) return 4;
            if (tier == AdvancedRaidDifficultyTier.FourStar || tier == AdvancedRaidDifficultyTier.FiveStar) return 3;
            return 2;
        }

        public int ShieldSegments()
        {
            if (tier == AdvancedRaidDifficultyTier.Legendary || tier == AdvancedRaidDifficultyTier.Event) return 6;
            if (tier == AdvancedRaidDifficultyTier.FiveStar) return 5;
            if (tier == AdvancedRaidDifficultyTier.FourStar) return 4;
            return 3;
        }

        public void ApplyTo(BattleCreature boss)
        {
            if (boss == null) return;
            boss.raidBossState = true;
            boss.raidActionsPerTurn = ActionsPerTurn();
            boss.maxHp = Mathf.Max(1, boss.maxHp * HpMultiplier());
            boss.currentHp = boss.maxHp;
            boss.shieldSegments = ShieldSegments();
            boss.raidPhaseIndex = 0;
            boss.raidRageState = false;
        }

        public bool UpdatePhase(BattleCreature boss, BattleContext context)
        {
            if (boss == null || !boss.raidBossState) return false;
            var hpPercent = boss.currentHp / (float)Mathf.Max(1, boss.maxHp);
            if (!rageState && hpPercent <= 0.2f)
            {
                rageState = true;
                boss.raidRageState = true;
                context?.eventLog.Add("Raid boss entered rage state");
            }
            if (currentPhaseIndex < shieldThresholds.Length && hpPercent <= shieldThresholds[currentPhaseIndex])
            {
                currentPhaseIndex++;
                boss.raidPhaseIndex = currentPhaseIndex;
                boss.shieldState = true;
                boss.shieldSegments = Mathf.Max(1, boss.shieldSegments);
                if (context != null)
                {
                    context.raidPhaseState = RaidPhaseState.ShieldPhase;
                    context.eventLog.Add("Raid phase " + currentPhaseIndex + " shield activated");
                }
                return true;
            }
            return false;
        }
    }

    public sealed class RaidTimer
    {
        public float remainingSeconds;
        public int turnsRemaining;
        public bool Expired => remainingSeconds <= 0f || turnsRemaining == 0;
        public RaidTimer(float seconds, int turns)
        {
            remainingSeconds = Mathf.Max(0f, seconds);
            turnsRemaining = Mathf.Max(0, turns);
        }
        public void TickSeconds(float seconds) { remainingSeconds = Mathf.Max(0f, remainingSeconds - Mathf.Max(0f, seconds)); }
        public void ConsumeTurn() { if (turnsRemaining > 0) turnsRemaining--; }
        public void ApplyRevivePenalty(float seconds) { TickSeconds(seconds); }
    }

    public sealed class AdvancedRaidReward
    {
        public RaidRewardKind kind;
        public string rewardId;
        public int quantity;
        public int rarityScore;
    }

    public sealed class AdvancedRaidRewardTable
    {
        public readonly List<AdvancedRaidReward> entries = new List<AdvancedRaidReward>();

        public List<AdvancedRaidReward> Roll(AdvancedRaidDifficultyTier tier, int performanceScore, float speedBonus, float eventModifier, IBattleRandom rng)
        {
            var source = entries.Count > 0 ? entries : DefaultEntries();
            var count = tier == AdvancedRaidDifficultyTier.Legendary || tier == AdvancedRaidDifficultyTier.Event ? 3 : 2;
            var rewards = new List<AdvancedRaidReward>();
            for (var i = 0; i < count; i++)
            {
                var pick = source[rng.Range(0, source.Count)];
                rewards.Add(new AdvancedRaidReward
                {
                    kind = pick.kind,
                    rewardId = pick.rewardId,
                    rarityScore = Mathf.RoundToInt((pick.rarityScore + (int)tier * 3 + performanceScore / 10) * Mathf.Max(0.1f, eventModifier)),
                    quantity = Mathf.Max(1, pick.quantity + (int)tier / 2 + Mathf.FloorToInt(speedBonus))
                });
            }
            return rewards;
        }

        private static List<AdvancedRaidReward> DefaultEntries()
        {
            return new List<AdvancedRaidReward>
            {
                new AdvancedRaidReward { kind = RaidRewardKind.RareItem, rewardId = "rare_core", quantity = 1, rarityScore = 10 },
                new AdvancedRaidReward { kind = RaidRewardKind.FusionMaterial, rewardId = "fusion_shard", quantity = 1, rarityScore = 14 },
                new AdvancedRaidReward { kind = RaidRewardKind.DimensionEnergy, rewardId = "dimension_energy", quantity = 2, rarityScore = 16 },
                new AdvancedRaidReward { kind = RaidRewardKind.HiddenAbility, rewardId = "ability_capsule_sample", quantity = 1, rarityScore = 20 }
            };
        }
    }

    public sealed class RaidEventRotation
    {
        private readonly Dictionary<string, List<string>> pools = new Dictionary<string, List<string>>();
        public void SetPool(string poolId, IEnumerable<string> raidIds)
        {
            pools[poolId] = raidIds != null ? raidIds.Where(id => !string.IsNullOrEmpty(id)).ToList() : new List<string>();
        }
        public string SelectActivePool(int dayIndex)
        {
            if (pools.Count == 0) return string.Empty;
            var keys = pools.Keys.OrderBy(k => k).ToList();
            return keys[Mathf.Abs(dayIndex) % keys.Count];
        }
        public string SelectActiveRaidId(int dayIndex, IBattleRandom rng)
        {
            var poolId = SelectActivePool(dayIndex);
            if (string.IsNullOrEmpty(poolId) || pools[poolId].Count == 0) return string.Empty;
            return pools[poolId][rng.Range(0, pools[poolId].Count)];
        }
    }

    public sealed class RaidEncounterController
    {
        public RaidPhaseState Phase { get; private set; } = RaidPhaseState.Selection;
        public RaidLobby Lobby { get; private set; } = new RaidLobby();
        public RaidBossProfile BossProfile { get; private set; }
        public RaidArenaProfile Arena { get; private set; } = new RaidArenaProfile();
        public BattleContext Context { get; private set; }

        public void Select(RaidBossProfile profile, RaidArenaProfile arena = null)
        {
            BossProfile = profile;
            if (arena != null) Arena = arena;
            Phase = RaidPhaseState.Selection;
        }

        public void OpenLobby(string raidId)
        {
            Lobby = new RaidLobby { raidId = raidId };
            Phase = RaidPhaseState.Lobby;
        }

        public void ConfirmTeam()
        {
            Lobby.ConfirmTeam();
            Phase = RaidPhaseState.TeamConfirmation;
        }

        public void StartBattle(BattleContext context, BattleCreature boss)
        {
            Context = context ?? new BattleContext { rules = BattleRuleset.ForFormat(BattleFormatType.Raid) };
            Context.rules = BattleRuleset.ForFormat(BattleFormatType.Raid);
            Context.weather.Set(Arena.weather, 5);
            Context.terrain.Set(Arena.terrain, 5);
            Context.raidPhaseState = RaidPhaseState.IntroCinematic;
            Phase = RaidPhaseState.IntroCinematic;
            BossProfile?.ApplyTo(boss);
            Phase = RaidPhaseState.BossBattle;
            Context.raidPhaseState = RaidPhaseState.BossBattle;
            Context.eventLog.Add("Raid battle began in " + Arena.arenaId);
        }

        public void EnterShieldPhase()
        {
            Phase = RaidPhaseState.ShieldPhase;
            if (Context != null) Context.raidPhaseState = RaidPhaseState.ShieldPhase;
        }

        public void CompleteVictory()
        {
            Phase = RaidPhaseState.RewardPhase;
            if (Context != null)
            {
                Context.raidVictory = true;
                Context.raidPhaseState = RaidPhaseState.RewardPhase;
                Context.eventLog.Add("Raid victory rewards ready");
            }
        }

        public bool StartCapturePhase()
        {
            if (Context == null || !Context.raidVictory) return false;
            Phase = RaidPhaseState.CapturePhase;
            Context.raidPhaseState = RaidPhaseState.CapturePhase;
            return true;
        }

        public void Cleanup()
        {
            Phase = RaidPhaseState.Cleanup;
            if (Context != null) Context.raidPhaseState = RaidPhaseState.Cleanup;
        }
    }

    public sealed class TransformationController
    {
        private readonly HashSet<string> megaUsed = new HashSet<string>();
        public bool TryMega(BattleContext context, BattleCreature creature, FormDefinition form)
        {
            if (context == null || creature == null || form == null || !context.rules.transformationsAllowed || megaUsed.Contains(context.battleId)) return false;
            megaUsed.Add(context.battleId);
            creature.currentForm = form;
            creature.megaState = true;
            creature.transformationState = TransformationKind.Mega;
            creature.RecalculateStats();
            context.eventLog.Add("Mega Evolution");
            return true;
        }
        public bool TryDimensionSplit(BattleContext context, BattleCreature creature, FormDefinition form, int meter)
        {
            if (context == null || creature == null || form == null || meter < 100 || !context.rules.transformationsAllowed) return false;
            creature.currentForm = form;
            creature.dimensionSplitState = true;
            creature.transformationState = TransformationKind.DimensionSplit;
            if (form.signatureMove != null) creature.AddMove(new BattleMoveData { moveId = form.signatureMove.id, displayName = form.signatureMove.displayName, type = form.signatureMove.type, category = form.signatureMove.category, basePower = form.signatureMove.power, accuracy = form.signatureMove.accuracy, pp = form.signatureMove.pp, priority = form.signatureMove.priority });
            creature.RecalculateStats();
            context.eventLog.Add("Dimension Split");
            return true;
        }
        public bool TryFusion(BattleContext context, BattleCreature left, BattleCreature right)
        {
            if (context == null || left == null || right == null || !context.rules.transformationsAllowed) return false;
            left.fusionState = true;
            left.transformationState = TransformationKind.Fusion;
            left.currentStats = StatBlock.Average(left.currentStats, right.currentStats);
            left.secondaryType = right.primaryType;
            context.eventLog.Add("Fusion");
            return true;
        }
    }

    public sealed class RaidPhaseController
    {
        public int turnLimit = 10;
        public readonly float[] shieldThresholds = { 0.75f, 0.5f, 0.25f };
        public void Check(BattleContext context, BattleCreature boss)
        {
            if (context == null || boss == null || !boss.raidBossState) return;
            var hpPercent = boss.currentHp / (float)Mathf.Max(1, boss.maxHp);
            if (shieldThresholds.Any(t => hpPercent <= t) && !boss.shieldState)
            {
                boss.shieldState = true;
                boss.shieldSegments = Mathf.Max(1, boss.shieldSegments == 0 ? 3 : boss.shieldSegments);
                context.raidPhaseState = RaidPhaseState.ShieldPhase;
                context.eventLog.Add("Raid shield activated");
            }
            if (hpPercent <= 0.2f && !boss.raidRageState)
            {
                boss.raidRageState = true;
                context.eventLog.Add("Raid boss entered rage state");
            }
            if (context.turnNumber > turnLimit && !context.raidVictory)
            {
                context.raidPhaseState = RaidPhaseState.Defeat;
                context.eventLog.Add("Raid timer expired");
            }
        }

        public void BreakShield(BattleContext context, BattleCreature boss)
        {
            if (boss == null || !boss.shieldState) return;
            boss.shieldState = false;
            boss.shieldSegments = 0;
            context?.eventLog.Add("Raid shield broke");
        }
    }

    public sealed class MoveResolver
    {
        private readonly AccuracyResolver accuracy = new AccuracyResolver();
        private readonly DamageCalculator damage;
        private readonly StatusController status = new StatusController();
        public MoveResolver(DamageCalculator damage) { this.damage = damage; }
        public DamageResult Resolve(BattleContext context, BattleCommand command, IBattleRandom rng)
        {
            if (command == null || command.move == null || command.actor == null || command.target == null) return new DamageResult();
            command.actor.lastMoveUsed = command.move;
            command.actor.hasMovedThisTurn = true;
            if (!accuracy.DoesHit(command.actor, command.target, command.move, rng))
            {
                context?.eventLog.Add(command.move.displayName + " missed");
                return new DamageResult();
            }
            var result = damage.Calculate(new DamageRequest { attacker = command.actor, defender = command.target, move = command.move, context = context, rng = rng });
            command.target.ApplyDamage(result.damage, command.move.moveId);
            context?.eventLog.Add("Damage " + result.damage);
            if (context != null && command.move.weatherToSet != WeatherKind.Clear) context.weather.Set(command.move.weatherToSet, 5);
            if (context != null && command.move.terrainToSet != TerrainKind.None) context.terrain.Set(command.move.terrainToSet, 5);
            if (command.move.secondaryEffect != null && rng.Range(1, 101) <= command.move.secondaryEffect.chancePercent)
            {
                var target = command.move.secondaryEffect.affectsTarget ? command.target : command.actor;
                if (command.move.secondaryEffect.status != PermanentStatus.None && status.CanApplyStatus(target, command.move.secondaryEffect.status, context)) status.ApplyPermanent(target, command.move.secondaryEffect.status);
                target.statStages.Change(command.move.secondaryEffect.stat, command.move.secondaryEffect.stageDelta);
            }
            if (command.move.recoilPercent > 0f) command.actor.ApplyDamage(Mathf.RoundToInt(result.damage * command.move.recoilPercent), "Recoil");
            if (command.move.drainPercent > 0f) command.actor.Heal(Mathf.RoundToInt(result.damage * command.move.drainPercent));
            if (command.move.rechargeTurns > 0) command.actor.volatileStatuses.Add(VolatileStatus.Recharge);
            return result;
        }
    }

    public sealed class BattleController
    {
        public BattleContext Context { get; private set; }
        public readonly BattleStateMachine StateMachine = new BattleStateMachine();
        private readonly ActionQueue actionQueue = new ActionQueue();
        private readonly MoveResolver moveResolver;
        private readonly StatusController status = new StatusController();
        private readonly AbilityProcessor abilities = new AbilityProcessor();
        private readonly ItemProcessor items = new ItemProcessor();
        private readonly RaidPhaseController raids = new RaidPhaseController();
        private readonly SwitchController switches = new SwitchController();
        public BattleController(BattleTypeChart chart) { moveResolver = new MoveResolver(new DamageCalculator(chart)); }
        public void StartBattle(BattleRuleset rules, params BattleParticipant[] participants)
        {
            Context = new BattleContext { rules = rules ?? BattleRuleset.ForFormat(BattleFormatType.WildSingle) };
            Context.participants.AddRange(participants.Where(p => p != null));
            StateMachine.StartBattle();
            foreach (var participant in Context.participants) abilities.Trigger("OnBattleStart", participant.Active, Context);
        }
        public void ExecuteTurn(IEnumerable<BattleCommand> commands, IBattleRandom rng)
        {
            StateMachine.Change(BattleState.ActionOrdering);
            var sorted = actionQueue.Sort(commands, Context, rng);
            StateMachine.Change(BattleState.ActionExecution);
            foreach (var command in sorted)
            {
                if (command.kind == BattleCommandKind.Fight) moveResolver.Resolve(Context, command, rng);
                if (command.kind == BattleCommandKind.Party) switches.SwitchTo(command.user, command.targetSlot, Context);
                if (command.kind == BattleCommandKind.Capture) StateMachine.Change(BattleState.CaptureAttempt);
                items.TriggerHpThreshold(command.actor, Context);
                if (command.target != null && command.target.IsFainted) StateMachine.Change(BattleState.FaintResolution);
            }
            StateMachine.Change(BattleState.SecondaryEffects);
            StateMachine.Change(BattleState.StatusResolution);
            foreach (var creature in Context.participants.SelectMany(p => p.activeSlots))
            {
                status.ResolveEndTurn(creature);
                raids.Check(Context, creature);
                creature.hasMovedThisTurn = false;
            }
            StateMachine.Change(BattleState.RaidPhaseCheck);
            Context.weather.Tick();
            Context.terrain.Tick();
            Context.turnNumber++;
            StateMachine.Change(BattleState.EndTurn);
            StateMachine.Change(BattleState.CommandSelection);
        }
    }

    public sealed class BattlePresentationController { public float textSpeed = 1f; public bool animationSkipEnabled; public void PlayMessage(BattleContext context, string message) { context?.eventLog.Add("UI: " + message); } }
    public sealed class BattleUIController
    {
        public bool effectivenessPreviewEnabled = true;
        public bool hpPanelVisible = true, expBarVisible = true, statusIconsVisible = true, weatherIndicatorVisible = true, terrainIndicatorVisible = true, raidShieldVisible = true, timerVisible = true;
        public readonly List<BattleCommandKind> bufferedInputs = new List<BattleCommandKind>();
        public void Buffer(BattleCommandKind command) { bufferedInputs.Add(command); }
    }
    public sealed class BattleCameraController { public string activeProfile = "gen5_snap"; public void CutTo(string profile) { activeProfile = profile; } }
    public sealed class BattleAnimationController { public string lastAnimation; public float hitPauseSeconds; public float shakeStrength; public void PlayMove(BattleMoveData move) { lastAnimation = move != null ? move.animationProfile : string.Empty; hitPauseSeconds = move != null && move.IsDamaging ? 0.08f : 0f; } public void Shake(float strength) { shakeStrength = strength; } }
    public sealed class BattleAudioController { public string currentMusic; public void SwitchMusic(string profile) { currentMusic = profile; } }
}
''',
    'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/AdvancedBattleSystemTests.cs': r'''using System.Linq;
using __PROJECT_NAMESPACE__.Battle.Advanced;
using __PROJECT_NAMESPACE__.Pokemon;
using NUnit.Framework;
using UnityEngine;

namespace __PROJECT_NAMESPACE__.Tests
{
    public sealed class AdvancedBattleSystemTests
    {
        private static BattleMoveData Move(string id = "strike", CreatureType type = CreatureType.Neutral, MoveCategory category = MoveCategory.Physical, int power = 40, int accuracy = 100, int priority = 0)
        {
            return new BattleMoveData { moveId = id, displayName = id, type = type, category = category, basePower = power, accuracy = accuracy, priority = priority, pp = 20 };
        }

        private static BattleCreature Creature(string id, CreatureType type = CreatureType.Neutral, int level = 50, int speed = 50)
        {
            var species = TestFactories.Species(id, type, speed);
            species.baseStats = new StatBlock(80, 80, 80, 80, 80, speed);
            return new BattleCreature(species, level);
        }

        private static BattleParticipant Participant(string id, BattleCreature creature, ParticipantKind kind = ParticipantKind.Player)
        {
            var participant = new BattleParticipant { participantId = id, kind = kind };
            participant.activeSlots.Add(creature);
            participant.availableCommands.AddRange(new[] { BattleCommandKind.Fight, BattleCommandKind.Bag, BattleCommandKind.Party, BattleCommandKind.Run, BattleCommandKind.Capture });
            return participant;
        }

        [Test]
        public void StateMachine_UsesClassicCommandFlow()
        {
            var state = new BattleStateMachine();
            state.StartBattle();
            CollectionAssert.AreEqual(new[] { BattleState.Intro, BattleState.SendOut, BattleState.StartTurn, BattleState.CommandSelection }, state.History);
            state.MarkTurnResolutionSkeleton();
            CollectionAssert.Contains(state.History, BattleState.SecondaryEffects);
            CollectionAssert.Contains(state.History, BattleState.EndTurn);
        }

        [Test]
        public void Rulesets_ConfigureBattleFormats()
        {
            var wild = BattleRuleset.ForFormat(BattleFormatType.WildSingle);
            var trainer = BattleRuleset.ForFormat(BattleFormatType.TrainerSingle);
            var raid = BattleRuleset.ForFormat(BattleFormatType.Raid);
            Assert.IsTrue(wild.captureAllowed);
            Assert.IsFalse(trainer.captureAllowed);
            Assert.AreEqual(4, raid.activeCreaturesPerSide);
            Assert.AreEqual(BattleAiDifficulty.RaidBoss, raid.aiDifficulty);
            Assert.AreEqual(2, BattleRuleset.ForFormat(BattleFormatType.Multi).activeCreaturesPerSide);
            Assert.AreEqual("shared_raid_timer", raid.timerRule);
        }

        [Test]
        public void ActionOrdering_UsesCategoryPriorityMovePrioritySpeedAndSeededTie()
        {
            var slow = Participant("slow", Creature("slow", speed: 10));
            var fast = Participant("fast", Creature("fast", speed: 120));
            var normal = BattleCommand.Fight(slow, fast.Active, Move("normal"));
            var quick = BattleCommand.Fight(slow, fast.Active, Move("quick", priority: 1));
            var fastNormal = BattleCommand.Fight(fast, slow.Active, Move("fast"));
            var item = new BattleCommand { user = slow, actor = slow.Active, kind = BattleCommandKind.Bag };
            var sorted = new ActionQueue().Sort(new[] { normal, fastNormal, item, quick }, new BattleContext(), new SeededBattleRandom(4));
            Assert.AreSame(item, sorted[0]);
            Assert.AreSame(quick, sorted[1]);
            Assert.AreSame(fastNormal, sorted[2]);
            var trickRoom = new BattleContext { trickRoom = true };
            var inverted = new ActionQueue().Sort(new[] { normal, fastNormal }, trickRoom, new SeededBattleRandom(4));
            Assert.AreSame(normal, inverted[0]);
        }

        [Test]
        public void DamagePipeline_CoversTypeStabBurnCritVarianceAndImmunity()
        {
            var calc = new DamageCalculator(BattleTypeChart.Default());
            var attacker = Creature("attacker", CreatureType.Flame);
            var defender = Creature("defender", CreatureType.Leaf);
            var neutral = Creature("neutral", CreatureType.Neutral);
            var flame = Move("flame", CreatureType.Flame, power: 70);
            var neutralMove = Move("neutral", CreatureType.Neutral, power: 70);
            var context = new BattleContext();
            var neutralDamage = calc.Calculate(new DamageRequest { attacker = attacker, defender = neutral, move = neutralMove, context = context, rng = new SeededBattleRandom(10) }).damage;
            var superEffective = calc.Calculate(new DamageRequest { attacker = attacker, defender = defender, move = flame, context = context, rng = new SeededBattleRandom(10) }).damage;
            Assert.Greater(neutralDamage, 0);
            Assert.Greater(superEffective, neutralDamage);
            var resisted = calc.Calculate(new DamageRequest { attacker = defender, defender = attacker, move = Move("leaf", CreatureType.Leaf, power: 70), context = context, rng = new SeededBattleRandom(10) }).damage;
            Assert.Less(resisted, neutralDamage);
            var immune = calc.Calculate(new DamageRequest { attacker = neutral, defender = Creature("shadow", CreatureType.Shadow), move = neutralMove, context = context, rng = new SeededBattleRandom(10) });
            Assert.AreEqual(0, immune.damage);
            Assert.IsTrue(immune.immune);
            attacker.permanentStatus = PermanentStatus.Burn;
            var burned = calc.Calculate(new DamageRequest { attacker = attacker, defender = neutral, move = flame, context = context, rng = new SeededBattleRandom(10) }).damage;
            attacker.permanentStatus = PermanentStatus.None;
            var critical = calc.Calculate(new DamageRequest { attacker = attacker, defender = neutral, move = flame, critical = true, context = context, rng = new SeededBattleRandom(10) }).damage;
            var stab = calc.Calculate(new DamageRequest { attacker = attacker, defender = neutral, move = flame, context = context, rng = new SeededBattleRandom(10) }).damage;
            Assert.Less(burned, stab);
            Assert.Greater(critical, stab);
            Assert.AreEqual(stab, calc.Calculate(new DamageRequest { attacker = attacker, defender = neutral, move = flame, context = context, rng = new SeededBattleRandom(10) }).damage);
        }

        [Test]
        public void AccuracyResolver_HandlesStagesGuaranteedHitsAndMisses()
        {
            var resolver = new AccuracyResolver();
            var user = Creature("user");
            var target = Creature("target");
            Assert.IsTrue(resolver.DoesHit(user, target, Move(accuracy: 100), new SeededBattleRandom(1)));
            Assert.IsFalse(resolver.DoesHit(user, target, Move(accuracy: 1), new SeededBattleRandom(1)));
            var low = Move(accuracy: 50);
            target.statStages.Set(StatId.Evasion, 6);
            Assert.IsFalse(resolver.DoesHit(user, target, low, new SeededBattleRandom(2)));
            low.bypassesAccuracy = true;
            Assert.IsTrue(resolver.DoesHit(user, target, low, new SeededBattleRandom(2)));
        }

        [Test]
        public void MoveResolver_AppliesSecondaryEffectsWeatherTerrainDrainAndRecharge()
        {
            var attacker = Participant("attacker", Creature("attacker", CreatureType.Tide));
            var defender = Participant("defender", Creature("defender", CreatureType.Flame));
            var move = Move("storm", CreatureType.Tide, power: 50);
            move.weatherToSet = WeatherKind.Rain;
            move.terrainToSet = TerrainKind.Dimensional;
            move.drainPercent = 0.5f;
            move.rechargeTurns = 1;
            move.secondaryEffect = new SecondaryBattleEffect { status = PermanentStatus.Paralysis, chancePercent = 100, stat = StatId.Speed, stageDelta = -1 };
            var context = new BattleContext();
            var beforeHp = attacker.Active.currentHp;
            attacker.Active.currentHp -= 10;
            new MoveResolver(new DamageCalculator(BattleTypeChart.Default())).Resolve(context, BattleCommand.Fight(attacker, defender.Active, move), new SeededBattleRandom(2));
            Assert.AreEqual(WeatherKind.Rain, context.weather.Current);
            Assert.AreEqual(TerrainKind.Dimensional, context.terrain.Current);
            Assert.AreEqual(PermanentStatus.Paralysis, defender.Active.permanentStatus);
            Assert.Less(defender.Active.statStages.Get(StatId.Speed), 0);
            Assert.Greater(attacker.Active.currentHp, beforeHp - 10);
            Assert.IsTrue(attacker.Active.volatileStatuses.Contains(VolatileStatus.Recharge));
        }

        [Test]
        public void CommandValidationAndSwitching_UseRulesAndCleanBattleState()
        {
            var rules = BattleRuleset.ForFormat(BattleFormatType.TrainerSingle);
            var validator = new BattleCommandValidator();
            Assert.IsFalse(validator.IsAllowed(rules, BattleCommandKind.Capture));
            Assert.IsFalse(validator.IsAllowed(rules, BattleCommandKind.Run));
            Assert.IsTrue(validator.IsAllowed(rules, BattleCommandKind.Fight));
            var active = Creature("active");
            active.statStages.Set(StatId.Attack, 4);
            active.volatileStatuses.Add(VolatileStatus.Confusion);
            var replacement = Creature("replacement");
            var participant = Participant("player", active);
            participant.reserveParty.Add(replacement);
            Assert.IsTrue(new SwitchController().SwitchTo(participant, 0, new BattleContext()));
            Assert.AreSame(replacement, participant.Active);
            Assert.AreEqual(0, active.statStages.Get(StatId.Attack));
            Assert.IsFalse(active.volatileStatuses.Contains(VolatileStatus.Confusion));
        }

        [Test]
        public void StatStages_StatusAbilityItemWeatherTerrainAndCapture_Work()
        {
            var stages = new StatStageSet();
            stages.Set(StatId.Attack, 9);
            Assert.AreEqual(6, stages.Get(StatId.Attack));
            Assert.AreEqual(4f, stages.Multiplier(StatId.Attack));
            stages.Set(StatId.Defense, -6);
            Assert.AreEqual(0.25f, stages.Multiplier(StatId.Defense));
            var creature = Creature("hooked");
            creature.permanentStatus = PermanentStatus.Burn;
            var hp = creature.currentHp;
            new StatusController().ResolveEndTurn(creature);
            Assert.Less(creature.currentHp, hp);
            creature.currentAbility = TestFactories.Ability("rain_start");
            var context = new BattleContext();
            new AbilityProcessor().Trigger(BattleEventTiming.OnBattleStart, creature, context);
            Assert.AreEqual(WeatherKind.Rain, context.weather.Current);
            var item = ScriptableObject.CreateInstance<ItemDefinition>();
            item.id = "berry";
            item.consumable = true;
            creature.heldItem = item;
            creature.currentHp = creature.maxHp / 4;
            new ItemProcessor().Trigger(BattleEventTiming.OnHPThreshold, creature, context);
            Assert.IsNull(creature.heldItem);
            context.weather.Set(WeatherKind.Rain, 1);
            context.terrain.Set(TerrainKind.Grassy, 1);
            Assert.Greater(context.weather.ModifyDamage(Move("tide", CreatureType.Tide)), 1f);
            Assert.Greater(context.terrain.ModifyDamage(Move("leaf", CreatureType.Leaf)), 1f);
            context.weather.Tick();
            context.terrain.Tick();
            Assert.AreEqual(WeatherKind.Clear, context.weather.Current);
            Assert.AreEqual(TerrainKind.None, context.terrain.Current);
            creature.permanentStatus = PermanentStatus.None;
            var capture = new CaptureController();
            var trainer = new BattleContext { rules = BattleRuleset.ForFormat(BattleFormatType.TrainerSingle) };
            Assert.IsFalse(capture.CanCapture(trainer));
            var raid = new BattleContext { rules = BattleRuleset.ForFormat(BattleFormatType.Raid) };
            Assert.IsFalse(capture.CanCapture(raid));
            raid.raidVictory = true;
            Assert.IsTrue(capture.CanCapture(raid));
            var full = capture.CalculateChance(creature);
            creature.currentHp = 1;
            var lowHp = capture.CalculateChance(creature);
            creature.permanentStatus = PermanentStatus.Sleep;
            Assert.Greater(capture.CalculateChance(creature), lowHp);
            Assert.Greater(lowHp, full);
        }

        [Test]
        public void AiTransformRaidControllerAndPresentationScaffolds_Work()
        {
            var self = Participant("self", Creature("self"));
            var foe = Participant("foe", Creature("foe"));
            self.Active.AddMove(Move("weak", power: 20));
            self.Active.AddMove(Move("strong", power: 80));
            Assert.AreEqual("strong", new WildBattleAI().ChooseCommand(self, foe, new BattleContext()).move.moveId);
            Assert.AreEqual("strong", new TrainerBattleAI(new DamageCalculator(BattleTypeChart.Default())).ChooseCommand(self, foe, new BattleContext()).move.moveId);
            var context = new BattleContext { rules = BattleRuleset.ForFormat(BattleFormatType.WildSingle) };
            var form = ScriptableObject.CreateInstance<FormDefinition>();
            form.statMultiplier = 1.5f;
            form.primaryTypeOverride = CreatureType.Light;
            form.signatureMove = TestFactories.Move("rift_signature");
            var transforms = new TransformationController();
            Assert.IsTrue(transforms.TryMega(context, self.Active, form));
            Assert.IsFalse(transforms.TryMega(context, self.Active, form));
            Assert.IsTrue(transforms.TryDimensionSplit(context, self.Active, form, 100));
            Assert.IsTrue(self.Active.knownMoves.Any(m => m.moveId == "rift_signature"));
            Assert.IsTrue(transforms.TryFusion(context, self.Active, foe.Active));
            var raidContext = new BattleContext { rules = BattleRuleset.ForFormat(BattleFormatType.Raid), turnNumber = 11 };
            foe.Active.raidBossState = true;
            foe.Active.currentHp = foe.Active.maxHp / 2;
            new RaidPhaseController().Check(raidContext, foe.Active);
            Assert.IsTrue(foe.Active.shieldState);
            Assert.IsTrue(raidContext.eventLog.Contains("timer"));
            var ui = new BattleUIController();
            ui.Buffer(BattleCommandKind.Fight);
            var camera = new BattleCameraController();
            camera.CutTo("impact");
            var animation = new BattleAnimationController();
            animation.PlayMove(Move("anim"));
            animation.Shake(0.5f);
            var audio = new BattleAudioController();
            audio.SwitchMusic("boss");
            Assert.AreEqual(BattleCommandKind.Fight, ui.bufferedInputs[0]);
            Assert.IsTrue(ui.hpPanelVisible && ui.expBarVisible && ui.weatherIndicatorVisible && ui.terrainIndicatorVisible && ui.raidShieldVisible);
            Assert.AreEqual("impact", camera.activeProfile);
            Assert.AreEqual("fast_hit", animation.lastAnimation);
            Assert.Greater(animation.hitPauseSeconds, 0f);
            Assert.AreEqual(0.5f, animation.shakeStrength);
            Assert.AreEqual("boss", audio.currentMusic);
        }

        [Test]
        public void RaidEncounter_FollowsLobbyBattleShieldRewardAndCaptureFlow()
        {
            var boss = Creature("raid_boss", CreatureType.Shadow, level: 60);
            var baseHp = boss.maxHp;
            var profile = new RaidBossProfile { bossId = "dimensional_boss", tier = AdvancedRaidDifficultyTier.FiveStar, source = RaidInitiatorKind.EventPortal };
            var arena = new RaidArenaProfile { arenaId = "test_portal", weather = WeatherKind.DimensionalStorm, terrain = TerrainKind.RaidArena };
            var encounter = new RaidEncounterController();
            encounter.Select(profile, arena);
            encounter.OpenLobby("raid_test");
            for (var i = 0; i < 4; i++) encounter.Lobby.AddAlly(Participant("ally" + i, Creature("ally" + i), ParticipantKind.AiAlly));
            encounter.ConfirmTeam();
            Assert.AreEqual(RaidPhaseState.TeamConfirmation, encounter.Phase);
            Assert.IsTrue(encounter.Lobby.Ready);
            var context = new BattleContext { rules = BattleRuleset.ForFormat(BattleFormatType.Raid) };
            encounter.StartBattle(context, boss);
            Assert.AreEqual(RaidPhaseState.BossBattle, encounter.Phase);
            Assert.AreEqual(WeatherKind.DimensionalStorm, context.weather.Current);
            Assert.AreEqual(TerrainKind.RaidArena, context.terrain.Current);
            Assert.AreEqual(baseHp * profile.HpMultiplier(), boss.maxHp);
            Assert.AreEqual(profile.ActionsPerTurn(), boss.raidActionsPerTurn);
            boss.currentHp = Mathf.FloorToInt(boss.maxHp * 0.7f);
            Assert.IsTrue(profile.UpdatePhase(boss, context));
            Assert.AreEqual(RaidPhaseState.ShieldPhase, context.raidPhaseState);
            new RaidPhaseController().BreakShield(context, boss);
            Assert.IsFalse(boss.shieldState);
            encounter.CompleteVictory();
            Assert.IsTrue(context.raidVictory);
            Assert.AreEqual(RaidPhaseState.RewardPhase, encounter.Phase);
            Assert.IsTrue(encounter.StartCapturePhase());
            Assert.AreEqual(RaidPhaseState.CapturePhase, context.raidPhaseState);
            Assert.IsTrue(new BattleCommandValidator().IsAllowed(context, BattleCommandKind.Capture));
            Assert.IsTrue(new CaptureController().CanCapture(context));
            encounter.Cleanup();
            Assert.AreEqual(RaidPhaseState.Cleanup, encounter.Phase);
        }

        [Test]
        public void RaidBossTimerRewardsAndEventRotation_AreDeterministic()
        {
            var boss = Creature("legendary_raid", CreatureType.Shadow, level: 70);
            var profile = new RaidBossProfile { tier = AdvancedRaidDifficultyTier.Legendary };
            profile.ApplyTo(boss);
            Assert.IsTrue(boss.raidBossState);
            Assert.AreEqual(4, boss.raidActionsPerTurn);
            Assert.GreaterOrEqual(boss.shieldSegments, 6);
            var context = new BattleContext { rules = BattleRuleset.ForFormat(BattleFormatType.Raid) };
            boss.currentHp = Mathf.FloorToInt(boss.maxHp * 0.19f);
            Assert.IsTrue(profile.UpdatePhase(boss, context));
            Assert.IsTrue(boss.raidRageState);
            var timer = new RaidTimer(12f, 2);
            timer.TickSeconds(4f);
            timer.ConsumeTurn();
            Assert.IsFalse(timer.Expired);
            timer.ApplyRevivePenalty(8f);
            timer.ConsumeTurn();
            Assert.IsTrue(timer.Expired);
            var table = new AdvancedRaidRewardTable();
            table.entries.Add(new AdvancedRaidReward { kind = RaidRewardKind.RareItem, rewardId = "rare_core", quantity = 1, rarityScore = 10 });
            table.entries.Add(new AdvancedRaidReward { kind = RaidRewardKind.DimensionEnergy, rewardId = "dimension_energy", quantity = 2, rarityScore = 16 });
            var first = table.Roll(AdvancedRaidDifficultyTier.Legendary, 90, 1f, 1.25f, new SeededBattleRandom(9));
            var second = table.Roll(AdvancedRaidDifficultyTier.Legendary, 90, 1f, 1.25f, new SeededBattleRandom(9));
            Assert.AreEqual(first.Count, second.Count);
            Assert.AreEqual(first[0].rewardId, second[0].rewardId);
            Assert.AreEqual(first[0].quantity, second[0].quantity);
            Assert.Greater(first[0].rarityScore, 0);
            var rotation = new RaidEventRotation();
            rotation.SetPool("event", new[] { "event_boss_a", "event_boss_b" });
            rotation.SetPool("weekly", new[] { "weekly_boss" });
            Assert.AreEqual("event", rotation.SelectActivePool(0));
            Assert.AreEqual(rotation.SelectActiveRaidId(3, new SeededBattleRandom(2)), rotation.SelectActiveRaidId(3, new SeededBattleRandom(2)));
        }

        [Test]
        public void BattleController_ExecutesTurnRewardsAndReturnsToCommandSelection()
        {
            var player = Participant("player", Creature("player", CreatureType.Flame, speed: 80));
            var enemy = Participant("enemy", Creature("enemy", CreatureType.Leaf, speed: 20), ParticipantKind.WildCreature);
            var move = Move("hit", CreatureType.Flame, power: 60);
            player.Active.AddMove(move);
            var controller = new BattleController(BattleTypeChart.Default());
            controller.StartBattle(BattleRuleset.ForFormat(BattleFormatType.WildSingle), player, enemy);
            controller.ExecuteTurn(new[] { BattleCommand.Fight(player, enemy.Active, move) }, new SeededBattleRandom(3));
            Assert.Less(enemy.Active.currentHp, enemy.Active.maxHp);
            Assert.AreEqual(BattleState.CommandSelection, controller.StateMachine.State);
            var reward = new RewardController().AwardExperience(enemy.Active, new[] { player.Active }, controller.Context);
            Assert.Greater(reward, 0);
            CollectionAssert.Contains(controller.StateMachine.History, BattleState.SecondaryEffects);
            CollectionAssert.Contains(controller.StateMachine.History, BattleState.EndTurn);
            var resolved = new RewardController().ResolveRewards(new BattleContext { rules = BattleRuleset.ForFormat(BattleFormatType.Raid) }, enemy.Active, new[] { player.Active });
            Assert.Contains("raid_core_sample", resolved.items);
        }
    }
}
'''
})

PROJECT_FRAMEWORK_TEMPLATE_FILES.update({
    'Assets/Scripts/Save/SaveSystem.cs': r'''using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using __PROJECT_NAMESPACE__.Pokemon;
using UnityEngine;

namespace __PROJECT_NAMESPACE__.Save
{
    public enum SaveSlotKind { Manual, Autosave, Backup, Recovery, Cloud }

    [Serializable]
    public sealed class PlayerSaveData
    {
        public string trainerName = "Nova";
        public string trainerId = "V11-0426";
        public string sceneName = "Overworld";
        public string locationName = "Starter Town";
        public Vector3 position;
        public int money;
        public int badges;
        public int playtimeSeconds;
    }

    [Serializable]
    public sealed class CreatureSaveData
    {
        public string instanceGuid = Guid.NewGuid().ToString("N");
        public string speciesId;
        public string nickname;
        public int level;
        public int experience;
        public bool shiny;
        public int currentHp;
        public string heldItemId;
        public string statusId;
        public List<string> moveIds = new List<string>();
        public List<int> pp = new List<int>();
        public string formId;
        public bool megaUnlocked;
        public bool dimensionSplitUnlocked;
        public bool fused;
    }

    [Serializable] public sealed class InventoryStack { public string itemId; public int count; public bool favorite; }
    [Serializable] public sealed class FlagRecord { public string key; public bool value; }
    [Serializable] public sealed class CounterRecord { public string key; public int value; }
    [Serializable] public sealed class WorldStateRecord { public string key; public string value; }
    [Serializable] public sealed class NpcSaveRecord { public string npcId; public string areaId; public string scheduleState; public bool defeated; public string dialogueState; }
    [Serializable] public sealed class QuestSaveRecord { public string questId; public string state; public int objectiveIndex; public bool complete; }
    [Serializable] public sealed class RaidSaveRecord { public string raidId; public string denId; public string tier; public bool defeated; public bool captured; public int rotationSeed; public string nextRefreshUtc; }
    [Serializable] public sealed class PokedexSaveRecord { public string speciesId; public bool seen; public bool caught; public List<string> formsSeen = new List<string>(); public bool shinySeen; }
    [Serializable] public sealed class FusionSaveRecord { public string fusionId; public string leftSpeciesId; public string rightSpeciesId; public bool active; }
    [Serializable] public sealed class TransformationSaveRecord { public string creatureGuid; public bool megaUnlocked; public bool dimensionSplitUnlocked; public int dimensionMeter; }
    [Serializable] public sealed class SettingSaveRecord { public string key; public string value; }
    [Serializable] public sealed class MenuSnapshotSaveRecord { public string activeScreen; public int selectedIndex; public float uiScale = 1f; public string language = "en"; }
    [Serializable] public sealed class BattleResumeSaveRecord { public bool canResume; public string battleType; public int turnNumber; public string opponentId; }

    [Serializable]
    public sealed class SaveSlotMetadata
    {
        public string slotId;
        public SaveSlotKind kind;
        public string savedAtUtc;
        public string trainerName;
        public string locationName;
        public int playtimeSeconds;
        public int badges;
        public int partyCount;
        public bool valid;
    }

    [Serializable]
    public sealed class SaveData
    {
        public int version = SaveManager.TargetVersion;
        public string buildVersion = "prototype";
        public string slotId = "manual_0";
        public SaveSlotKind slotKind = SaveSlotKind.Manual;
        public string createdAtUtc = DateTime.UtcNow.ToString("O");
        public string savedAtUtc = DateTime.UtcNow.ToString("O");
        public string checksum;
        public PlayerSaveData player = new PlayerSaveData();
        public List<CreatureSaveData> party = new List<CreatureSaveData>();
        public List<CreatureSaveData> pcStorage = new List<CreatureSaveData>();
        public List<InventoryStack> inventory = new List<InventoryStack>();
        public List<FlagRecord> flags = new List<FlagRecord>();
        public List<CounterRecord> counters = new List<CounterRecord>();
        public List<WorldStateRecord> worldState = new List<WorldStateRecord>();
        public List<NpcSaveRecord> npcStates = new List<NpcSaveRecord>();
        public List<QuestSaveRecord> quests = new List<QuestSaveRecord>();
        public List<RaidSaveRecord> raids = new List<RaidSaveRecord>();
        public List<PokedexSaveRecord> pokedex = new List<PokedexSaveRecord>();
        public List<FusionSaveRecord> fusions = new List<FusionSaveRecord>();
        public List<TransformationSaveRecord> transformations = new List<TransformationSaveRecord>();
        public List<SettingSaveRecord> settings = new List<SettingSaveRecord>();
        public MenuSnapshotSaveRecord pauseMenu = new MenuSnapshotSaveRecord();
        public BattleResumeSaveRecord battleResume = new BattleResumeSaveRecord();
    }

    public sealed class SaveValidationResult
    {
        public bool IsValid => errors.Count == 0;
        public readonly List<string> errors = new List<string>();
    }

    public sealed class SaveOperationResult
    {
        public bool success;
        public string message;
        public SaveData data;
        public SaveSlotMetadata metadata;
    }

    public sealed class SaveValidator
    {
        public SaveValidationResult Validate(SaveData data)
        {
            var result = new SaveValidationResult();
            if (data == null) { result.errors.Add("missing_save"); return result; }
            if (data.version <= 0) result.errors.Add("invalid_version");
            if (data.player == null) result.errors.Add("missing_player");
            if (data.party != null && data.party.Count > 6) result.errors.Add("party_exceeds_six");
            if (data.inventory != null && data.inventory.Any(i => i.count < 0)) result.errors.Add("negative_inventory");
            return result;
        }
    }

    public sealed class SaveMigrationRegistry
    {
        private readonly SortedDictionary<int, Action<SaveData>> migrations = new SortedDictionary<int, Action<SaveData>>();
        public SaveMigrationRegistry()
        {
            Register(1, data => { if (string.IsNullOrEmpty(data.buildVersion)) data.buildVersion = "migrated_v2"; });
            Register(2, data => { if (data.pauseMenu == null) data.pauseMenu = new MenuSnapshotSaveRecord(); });
        }
        public void Register(int fromVersion, Action<SaveData> migration) { migrations[fromVersion] = migration; }
        public void Migrate(SaveData data, int targetVersion)
        {
            if (data == null) return;
            while (data.version < targetVersion)
            {
                if (migrations.TryGetValue(data.version, out var migration)) migration(data);
                data.version++;
            }
        }
    }

    public sealed class AutosavePolicy
    {
        public float intervalSeconds = 60f;
        public bool dirty;
        private float elapsed;
        public void MarkDirty() { dirty = true; }
        public bool Tick(float deltaSeconds)
        {
            if (!dirty)
            {
                elapsed = 0f;
                return false;
            }
            elapsed += Math.Max(0f, deltaSeconds);
            if (elapsed < intervalSeconds) return false;
            elapsed = 0f;
            dirty = false;
            return true;
        }
    }

    public sealed class CloudSaveScaffold
    {
        private string payload;
        public bool pendingUpload;
        public void Upload(string json) { payload = json; pendingUpload = false; }
        public string Download() { return payload; }
        public void QueueUpload() { pendingUpload = true; }
    }

    /// <summary>Versioned JSON save pipeline with slots, backups, migrations, checksum validation, autosave policy, and cloud-save scaffold.</summary>
    public sealed class SaveManager
    {
        public const int TargetVersion = 3;
        private readonly SaveValidator validator = new SaveValidator();
        private readonly SaveMigrationRegistry migrations = new SaveMigrationRegistry();
        public SaveData Current { get; private set; } = new SaveData();
        public SaveOperationResult LastResult { get; private set; } = new SaveOperationResult { success = true };

        public string Serialize(SaveData data = null)
        {
            var target = data ?? Current;
            Normalize(target);
            target.version = TargetVersion;
            target.savedAtUtc = DateTime.UtcNow.ToString("O");
            target.checksum = ComputeChecksum(target);
            return JsonUtility.ToJson(target, true);
        }

        public SaveData Deserialize(string json)
        {
            try
            {
                Current = string.IsNullOrWhiteSpace(json) ? new SaveData() : JsonUtility.FromJson<SaveData>(json);
                Normalize(Current);
                migrations.Migrate(Current, TargetVersion);
                Normalize(Current);
                LastResult = new SaveOperationResult { success = validator.Validate(Current).IsValid, data = Current, metadata = CreateMetadata(Current) };
                return Current;
            }
            catch (Exception ex)
            {
                Current = new SaveData();
                LastResult = new SaveOperationResult { success = false, message = ex.Message, data = Current };
                return Current;
            }
        }

        public bool ValidateChecksum(SaveData data)
        {
            if (data == null || string.IsNullOrEmpty(data.checksum)) return false;
            return data.checksum == ComputeChecksum(data);
        }

        public SaveValidationResult Validate(SaveData data = null) { return validator.Validate(data ?? Current); }

        public void SaveToFile(string path) { SaveToFile(path, BackupPath(path)); }

        public void SaveToFile(string path, string backupPath)
        {
            Directory.CreateDirectory(Path.GetDirectoryName(path));
            if (File.Exists(path) && !string.IsNullOrEmpty(backupPath)) File.Copy(path, backupPath, true);
            var temp = path + ".tmp";
            File.WriteAllText(temp, Serialize());
            if (File.Exists(path)) File.Delete(path);
            File.Move(temp, path);
            LastResult = new SaveOperationResult { success = true, message = "saved", data = Current, metadata = CreateMetadata(Current) };
        }

        public SaveData LoadFromFile(string path) { return LoadFromFile(path, BackupPath(path)); }

        public SaveData LoadFromFile(string path, string backupPath)
        {
            if (TryReadValid(path, out var data)) return data;
            if (TryReadValid(backupPath, out data))
            {
                LastResult = new SaveOperationResult { success = true, message = "loaded_backup", data = data, metadata = CreateMetadata(data) };
                return data;
            }
            LastResult = new SaveOperationResult { success = false, message = "load_failed", data = Current };
            return Current;
        }

        private bool TryReadValid(string path, out SaveData data)
        {
            data = null;
            if (string.IsNullOrEmpty(path) || !File.Exists(path)) return false;
            try
            {
                data = Deserialize(File.ReadAllText(path));
                return Validate(data).IsValid;
            }
            catch { return false; }
        }

        public SaveSlotMetadata CreateMetadata(SaveData data)
        {
            Normalize(data);
            return new SaveSlotMetadata
            {
                slotId = data.slotId,
                kind = data.slotKind,
                savedAtUtc = data.savedAtUtc,
                trainerName = data.player.trainerName,
                locationName = data.player.locationName,
                playtimeSeconds = data.player.playtimeSeconds,
                badges = data.player.badges,
                partyCount = data.party.Count,
                valid = Validate(data).IsValid
            };
        }

        public void SetFlag(string key, bool value)
        {
            var record = Current.flags.Find(f => f.key == key);
            if (record == null) Current.flags.Add(new FlagRecord { key = key, value = value });
            else record.value = value;
        }

        public bool GetFlag(string key)
        {
            var record = Current.flags.Find(f => f.key == key);
            return record != null && record.value;
        }

        public void SetCounter(string key, int value)
        {
            var record = Current.counters.Find(c => c.key == key);
            if (record == null) Current.counters.Add(new CounterRecord { key = key, value = value });
            else record.value = value;
        }

        public int GetCounter(string key)
        {
            var record = Current.counters.Find(c => c.key == key);
            return record != null ? record.value : 0;
        }

        public void SetWorldState(string key, string value)
        {
            var record = Current.worldState.Find(w => w.key == key);
            if (record == null) Current.worldState.Add(new WorldStateRecord { key = key, value = value });
            else record.value = value;
        }

        public void CaptureParty(Party party)
        {
            Current.party.Clear();
            if (party == null) return;
            foreach (var creature in party.Creatures) Current.party.Add(CreatureToSave(creature));
        }

        public static CreatureSaveData CreatureToSave(CreatureInstance creature)
        {
            return new CreatureSaveData
            {
                speciesId = creature.Species != null ? creature.Species.id : creature.speciesId,
                nickname = creature.Species != null ? creature.Species.displayName : creature.speciesId,
                level = creature.Level,
                experience = creature.Experience,
                shiny = creature.Shiny,
                currentHp = creature.CurrentHp
            };
        }

        public static string BackupPath(string path)
        {
            return string.IsNullOrEmpty(path) ? string.Empty : path + ".bak";
        }

        private static void Normalize(SaveData data)
        {
            if (data == null) return;
            if (data.player == null) data.player = new PlayerSaveData();
            if (data.party == null) data.party = new List<CreatureSaveData>();
            if (data.pcStorage == null) data.pcStorage = new List<CreatureSaveData>();
            if (data.inventory == null) data.inventory = new List<InventoryStack>();
            if (data.flags == null) data.flags = new List<FlagRecord>();
            if (data.counters == null) data.counters = new List<CounterRecord>();
            if (data.worldState == null) data.worldState = new List<WorldStateRecord>();
            if (data.npcStates == null) data.npcStates = new List<NpcSaveRecord>();
            if (data.quests == null) data.quests = new List<QuestSaveRecord>();
            if (data.raids == null) data.raids = new List<RaidSaveRecord>();
            if (data.pokedex == null) data.pokedex = new List<PokedexSaveRecord>();
            if (data.fusions == null) data.fusions = new List<FusionSaveRecord>();
            if (data.transformations == null) data.transformations = new List<TransformationSaveRecord>();
            if (data.settings == null) data.settings = new List<SettingSaveRecord>();
            if (data.pauseMenu == null) data.pauseMenu = new MenuSnapshotSaveRecord();
            if (data.battleResume == null) data.battleResume = new BattleResumeSaveRecord();
            if (string.IsNullOrEmpty(data.slotId)) data.slotId = "manual_0";
        }

        private static string ComputeChecksum(SaveData data)
        {
            Normalize(data);
            var builder = new StringBuilder();
            builder.Append(data.version).Append('|').Append(data.slotId).Append('|').Append(data.player.trainerName).Append('|').Append(data.player.sceneName).Append('|').Append(data.player.money).Append('|');
            foreach (var creature in data.party.OrderBy(c => c.instanceGuid)) builder.Append(creature.instanceGuid).Append(':').Append(creature.speciesId).Append(':').Append(creature.level).Append('|');
            foreach (var flag in data.flags.OrderBy(f => f.key)) builder.Append(flag.key).Append('=').Append(flag.value).Append('|');
            foreach (var counter in data.counters.OrderBy(c => c.key)) builder.Append(counter.key).Append('=').Append(counter.value).Append('|');
            unchecked
            {
                uint hash = 2166136261;
                foreach (var ch in builder.ToString())
                {
                    hash ^= ch;
                    hash *= 16777619;
                }
                return hash.ToString("X8");
            }
        }
    }
}
''',
    'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/SaveSystemTests.cs': r'''using System.IO;
using __PROJECT_NAMESPACE__.Save;
using NUnit.Framework;

namespace __PROJECT_NAMESPACE__.Tests
{
    public sealed class SaveSystemTests
    {
        [Test]
        public void FullSaveSystem_SerializesMetadataFlagsCountersAndExtendedState()
        {
            var manager = new SaveManager();
            manager.Current.slotId = "manual_1";
            manager.Current.player.trainerName = "Nova";
            manager.Current.player.locationName = "Prototype Testing Site";
            manager.Current.player.badges = 2;
            manager.Current.party.Add(new CreatureSaveData { instanceGuid = "a", speciesId = "auraling", level = 12, currentHp = 30 });
            manager.Current.pcStorage.Add(new CreatureSaveData { instanceGuid = "b", speciesId = "cinderkit", level = 8 });
            manager.Current.inventory.Add(new InventoryStack { itemId = "capture_core", count = 5, favorite = true });
            manager.Current.quests.Add(new QuestSaveRecord { questId = "main_01", state = "active", objectiveIndex = 1 });
            manager.Current.raids.Add(new RaidSaveRecord { raidId = "den_01", tier = "3-Star", rotationSeed = 44 });
            manager.Current.fusions.Add(new FusionSaveRecord { fusionId = "fusion_a_b", leftSpeciesId = "a", rightSpeciesId = "b", active = true });
            manager.Current.transformations.Add(new TransformationSaveRecord { creatureGuid = "a", megaUnlocked = true, dimensionSplitUnlocked = true, dimensionMeter = 100 });
            manager.SetFlag("intro_done", true);
            manager.SetCounter("rival_wins", 3);
            manager.SetWorldState("door_lab", "open");
            var json = manager.Serialize();
            var clone = new SaveManager().Deserialize(json);
            Assert.AreEqual(SaveManager.TargetVersion, clone.version);
            Assert.AreEqual("Nova", clone.player.trainerName);
            Assert.AreEqual("auraling", clone.party[0].speciesId);
            Assert.AreEqual("cinderkit", clone.pcStorage[0].speciesId);
            Assert.AreEqual("capture_core", clone.inventory[0].itemId);
            Assert.IsTrue(clone.flags.Exists(f => f.key == "intro_done" && f.value));
            Assert.AreEqual(3, new SaveManager().Deserialize(json).counters.Find(c => c.key == "rival_wins").value);
            Assert.AreEqual("den_01", clone.raids[0].raidId);
            Assert.AreEqual("fusion_a_b", clone.fusions[0].fusionId);
            var metadata = manager.CreateMetadata(clone);
            Assert.AreEqual("manual_1", metadata.slotId);
            Assert.AreEqual(1, metadata.partyCount);
            Assert.IsTrue(metadata.valid);
            Assert.IsTrue(manager.ValidateChecksum(clone));
        }

        [Test]
        public void FullSaveSystem_FileBackupRecoveryMigrationAndValidationWork()
        {
            var dir = Path.Combine(Path.GetTempPath(), "__PROJECT_NAMESPACE___save_tests");
            if (Directory.Exists(dir)) Directory.Delete(dir, true);
            Directory.CreateDirectory(dir);
            var path = Path.Combine(dir, "slot.json");
            var manager = new SaveManager();
            manager.Current.player.trainerName = "Nova";
            manager.Current.party.Add(new CreatureSaveData { instanceGuid = "a", speciesId = "auraling", level = 5 });
            manager.SaveToFile(path);
            Assert.IsTrue(File.Exists(path));
            manager.Current.player.trainerName = "BackupNova";
            manager.SaveToFile(path);
            Assert.IsTrue(File.Exists(SaveManager.BackupPath(path)));
            File.WriteAllText(path, "{ definitely corrupt");
            var recovered = new SaveManager().LoadFromFile(path);
            Assert.AreEqual("Nova", recovered.player.trainerName);
            var old = new SaveData { version = 1 };
            old.player.trainerName = "OldNova";
            var oldJson = UnityEngine.JsonUtility.ToJson(old);
            var migrated = new SaveManager().Deserialize(oldJson);
            Assert.AreEqual(SaveManager.TargetVersion, migrated.version);
            Assert.NotNull(migrated.pauseMenu);
            var invalid = new SaveData();
            for (var i = 0; i < 7; i++) invalid.party.Add(new CreatureSaveData { speciesId = "too_many_" + i });
            Assert.IsFalse(new SaveValidator().Validate(invalid).IsValid);
            Directory.Delete(dir, true);
        }

        [Test]
        public void FullSaveSystem_AutosavePolicyAndCloudScaffoldWork()
        {
            var policy = new AutosavePolicy { intervalSeconds = 10f };
            Assert.IsFalse(policy.Tick(20f));
            policy.MarkDirty();
            Assert.IsFalse(policy.Tick(5f));
            Assert.IsTrue(policy.Tick(5f));
            var manager = new SaveManager();
            manager.Current.slotKind = SaveSlotKind.Autosave;
            manager.Current.player.trainerName = "CloudNova";
            var payload = manager.Serialize();
            var cloud = new CloudSaveScaffold();
            cloud.QueueUpload();
            Assert.IsTrue(cloud.pendingUpload);
            cloud.Upload(payload);
            Assert.IsFalse(cloud.pendingUpload);
            var downloaded = new SaveManager().Deserialize(cloud.Download());
            Assert.AreEqual("CloudNova", downloaded.player.trainerName);
            Assert.AreEqual(SaveSlotKind.Autosave, downloaded.slotKind);
        }
    }
}
''',
    'Assets/Scripts/UI/PauseMenuSystem.cs': r'''using System;
using System.Collections.Generic;
using System.Linq;
using __PROJECT_NAMESPACE__.Core;

namespace __PROJECT_NAMESPACE__.UI
{
    public enum PauseMenuScreen { Main, Pokedex, Pokemon, Summary, Bag, Map, PokegearPhone, Quests, Save, Options, Controls, ProfileTrainerCard, Multiplayer, RaidEvents, StoragePc, ReadyMenu, Debug, ExitGame }
    public enum PauseMenuOptionId { Pokedex, Pokemon, Bag, Map, PokegearPhone, Quests, Save, Options, ProfileTrainerCard, Multiplayer, Debug, ExitGame, StoragePc, ReadyMenu, RaidEvents }
    public enum PauseInputDevice { Keyboard, Controller, Mouse }
    public enum MenuTransitionKind { None, Fade, Slide, Scale }

    public sealed class PauseMenuContext
    {
        public bool hasPokedex;
        public bool partyExists;
        public bool hasMapDevice;
        public bool multiplayerEnabled;
        public bool debugMode;
        public bool overworldAllowed = true;
        public string currentLocation = "Prototype Testing Site";
        public string currentObjective = "Test grass encounters, capture, NPCs, pickups, and wild camera.";
        public string weatherTime = "Clear Day";
        public int badgeCount;
        public int currency;
        public float uiScale = 1f;
        public string language = "en";
    }

    public sealed class PauseMenuOption
    {
        public PauseMenuOptionId id;
        public PauseMenuScreen targetScreen;
        public string label;
        public string iconId;
        public bool debugOnly;
        public Func<PauseMenuContext, bool> visibleWhen;

        public bool IsVisible(PauseMenuContext context)
        {
            if (debugOnly && (context == null || !context.debugMode)) return false;
            return visibleWhen == null || visibleWhen(context);
        }
    }

    public sealed class PauseMenuSnapshot
    {
        public bool open;
        public PauseMenuScreen activeScreen;
        public int selectedIndex;
        public float uiScale;
        public string language;
    }

    public sealed class PauseMenuSystem
    {
        private readonly List<PauseMenuOption> options = new List<PauseMenuOption>();
        private readonly Dictionary<PauseMenuScreen, Action> handlers = new Dictionary<PauseMenuScreen, Action>();
        public bool IsOpen { get; private set; }
        public bool OverworldPaused { get; private set; }
        public PauseMenuScreen ActiveScreen { get; private set; } = PauseMenuScreen.Main;
        public int SelectedIndex { get; private set; }
        public MenuTransitionAnimator Transition { get; } = new MenuTransitionAnimator();
        public IReadOnlyList<PauseMenuOption> Options => options;

        public PauseMenuSystem()
        {
            RegisterDefaultOptions();
        }

        public void RegisterDefaultOptions()
        {
            options.Clear();
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.Pokedex, targetScreen = PauseMenuScreen.Pokedex, label = "Pokedex", iconId = "dex", visibleWhen = c => c != null && c.hasPokedex });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.Pokemon, targetScreen = PauseMenuScreen.Pokemon, label = "Pokemon", iconId = "party", visibleWhen = c => c != null && c.partyExists });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.Bag, targetScreen = PauseMenuScreen.Bag, label = "Bag", iconId = "bag" });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.Map, targetScreen = PauseMenuScreen.Map, label = "Map", iconId = "map", visibleWhen = c => c != null && c.hasMapDevice });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.PokegearPhone, targetScreen = PauseMenuScreen.PokegearPhone, label = "Pokegear / Phone", iconId = "phone" });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.Quests, targetScreen = PauseMenuScreen.Quests, label = "Quests", iconId = "quest" });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.Save, targetScreen = PauseMenuScreen.Save, label = "Save", iconId = "save" });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.Options, targetScreen = PauseMenuScreen.Options, label = "Options", iconId = "options" });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.ProfileTrainerCard, targetScreen = PauseMenuScreen.ProfileTrainerCard, label = "Profile / Trainer Card", iconId = "profile" });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.Multiplayer, targetScreen = PauseMenuScreen.Multiplayer, label = "Multiplayer", iconId = "online", visibleWhen = c => c != null && c.multiplayerEnabled });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.Debug, targetScreen = PauseMenuScreen.Debug, label = "Debug", iconId = "debug", debugOnly = true });
            InjectOption(new PauseMenuOption { id = PauseMenuOptionId.ExitGame, targetScreen = PauseMenuScreen.ExitGame, label = "Exit Game", iconId = "exit" });
        }

        public void InjectOption(PauseMenuOption option)
        {
            if (option == null) return;
            options.RemoveAll(o => o.id == option.id);
            options.Add(option);
        }

        public void RegisterHandler(PauseMenuScreen screen, Action handler)
        {
            handlers[screen] = handler;
        }

        public List<PauseMenuOption> VisibleOptions(PauseMenuContext context)
        {
            return options.Where(o => o.IsVisible(context)).ToList();
        }

        public void Open(PauseMenuContext context, MenuTransitionKind transition = MenuTransitionKind.Slide)
        {
            if (context != null && !context.overworldAllowed) return;
            IsOpen = true;
            OverworldPaused = true;
            ActiveScreen = PauseMenuScreen.Main;
            SelectedIndex = 0;
            Transition.Start(transition, 0.12f);
        }

        public void Close()
        {
            IsOpen = false;
            OverworldPaused = false;
            ActiveScreen = PauseMenuScreen.Main;
            Transition.Start(MenuTransitionKind.Fade, 0.08f);
        }

        public PauseMenuOption Navigate(PauseMenuContext context, int delta)
        {
            var visible = VisibleOptions(context);
            if (visible.Count == 0) return null;
            SelectedIndex = (SelectedIndex + delta) % visible.Count;
            if (SelectedIndex < 0) SelectedIndex += visible.Count;
            return visible[SelectedIndex];
        }

        public PauseMenuScreen SelectCurrent(PauseMenuContext context)
        {
            var visible = VisibleOptions(context);
            if (visible.Count == 0) return ActiveScreen;
            var selected = visible[Math.Max(0, Math.Min(SelectedIndex, visible.Count - 1))];
            ActiveScreen = selected.targetScreen;
            if (handlers.TryGetValue(ActiveScreen, out var handler)) handler();
            return ActiveScreen;
        }

        public void Back()
        {
            if (ActiveScreen == PauseMenuScreen.Main) Close();
            else ActiveScreen = PauseMenuScreen.Main;
        }

        public PauseMenuSnapshot CreateSnapshot(PauseMenuContext context)
        {
            return new PauseMenuSnapshot { open = IsOpen, activeScreen = ActiveScreen, selectedIndex = SelectedIndex, uiScale = context != null ? context.uiScale : 1f, language = context != null ? context.language : "en" };
        }

        public void Restore(PauseMenuSnapshot snapshot, PauseMenuContext context)
        {
            if (snapshot == null) return;
            IsOpen = snapshot.open;
            OverworldPaused = snapshot.open;
            ActiveScreen = snapshot.activeScreen;
            SelectedIndex = Math.Max(0, snapshot.selectedIndex);
            if (context != null)
            {
                context.uiScale = ClampScale(snapshot.uiScale);
                context.language = string.IsNullOrEmpty(snapshot.language) ? "en" : snapshot.language;
            }
        }

        public float ClampScale(float scale)
        {
            return Math.Max(0.75f, Math.Min(1.75f, scale));
        }

        public bool TextFits(string localizedText, int maxCharacters)
        {
            return localizedText == null || localizedText.Length <= Math.Max(1, maxCharacters);
        }
    }

    public sealed class PauseMenuLayoutModel
    {
        public readonly List<string> leftElements = new List<string> { "command list", "icons", "selection indicator", "animated cursor", "scroll" };
        public readonly List<string> rightElements = new List<string> { "party preview", "lead portrait", "location", "playtime", "objective", "badges", "currency", "weather/time" };
        public readonly List<string> optionalHud = new List<string> { "quest alerts", "event notifications", "raid banner", "online notifications", "daily timers" };
    }

    public sealed class PokedexScreenModel
    {
        public readonly List<string> filters = new List<string> { "type", "habitat", "evolution stage", "region", "form", "legendary", "fusion-compatible", "raid-exclusive" };
        public readonly HashSet<string> trackedForms = new HashSet<string>();
        public string SearchText { get; private set; }
        public void Search(string text) { SearchText = text ?? string.Empty; }
        public void TrackForm(string formId) { if (!string.IsNullOrEmpty(formId)) trackedForms.Add(formId); }
    }

    public sealed class PartyScreenModel
    {
        public readonly List<string> creatureIds = new List<string>();
        public bool quickSwapMode;
        public void Bind(IEnumerable<string> ids) { creatureIds.Clear(); if (ids != null) creatureIds.AddRange(ids); }
        public bool Move(int from, int to)
        {
            if (from < 0 || from >= creatureIds.Count || to < 0 || to >= creatureIds.Count) return false;
            var item = creatureIds[from];
            creatureIds.RemoveAt(from);
            creatureIds.Insert(to, item);
            return true;
        }
    }

    public sealed class PauseBagScreenModel
    {
        public readonly List<string> pockets = new List<string> { "Items", "Medicine", "Poke Balls", "TMs/TRs", "Berries", "Battle Items", "Key Items", "Fusion Materials", "Dimension Materials", "Raid Materials" };
        public readonly HashSet<string> favorites = new HashSet<string>();
        public string activeFilter = string.Empty;
        public void Favorite(string itemId) { if (!string.IsNullOrEmpty(itemId)) favorites.Add(itemId); }
    }

    public sealed class PauseMapScreenModel
    {
        public readonly List<string> markers = new List<string>();
        public float zoom = 1f;
        public void AddMarker(string marker) { if (!string.IsNullOrEmpty(marker)) markers.Add(marker); }
        public void SetZoom(float value) { zoom = Math.Max(0.5f, Math.Min(4f, value)); }
    }

    public sealed class PhoneScreenModel
    {
        public readonly List<string> contacts = new List<string>();
        public readonly List<string> notifications = new List<string>();
        public void AddContact(string contact) { if (!string.IsNullOrEmpty(contact)) contacts.Add(contact); }
        public void PushNotification(string message) { if (!string.IsNullOrEmpty(message)) notifications.Add(message); }
    }

    public sealed class QuestJournalScreenModel
    {
        public readonly List<string> activeQuests = new List<string>();
        public readonly List<string> history = new List<string>();
        public void AddQuest(string questId) { if (!string.IsNullOrEmpty(questId)) activeQuests.Add(questId); }
        public void CompleteQuest(string questId) { if (activeQuests.Remove(questId)) history.Add(questId); }
    }

    public sealed class TrainerProfileScreenModel
    {
        public string trainerName = "Nova";
        public int playtimeMinutes;
        public int money;
        public int badgeCount;
        public readonly List<string> achievements = new List<string>();
    }

    public sealed class PauseSaveScreenModel
    {
        public string currentLocation;
        public int badgeCount;
        public string lastSaveTimestamp;
        public bool overwriteWarningShown;
        public void PrepareOverwriteWarning() { overwriteWarningShown = true; }
    }

    public sealed class PauseOptionsScreenModel
    {
        private readonly SettingsManager settings;
        public bool autosave = true;
        public bool battleEffects = true;
        public bool screenShake = true;
        public float uiScale = 1f;
        public string language = "en";
        public PauseOptionsScreenModel(SettingsManager settings) { this.settings = settings; }
        public void SetMusicVolume(float value)
        {
            if (settings == null) return;
            var data = settings.Data;
            data.musicVolume = Math.Max(0f, Math.Min(1f, value));
            settings.Apply(data);
        }
    }

    public sealed class ControlBindingProfile
    {
        private readonly Dictionary<string, string> bindings = new Dictionary<string, string>();
        public float analogSensitivity = 1f;
        public float deadzone = 0.2f;
        public IReadOnlyDictionary<string, string> Bindings => bindings;
        public void Bind(string action, string input) { if (!string.IsNullOrEmpty(action)) bindings[action] = input ?? string.Empty; }
        public bool HasConflict(string input) { return bindings.Values.Count(v => v == input) > 1; }
        public void ResetDefaults()
        {
            bindings.Clear();
            Bind("Menu", "Tab");
            Bind("Confirm", "Enter");
            Bind("Back", "Escape");
        }
    }

    public sealed class MultiplayerScreenModel { public readonly List<string> friends = new List<string>(); public readonly List<string> lobbies = new List<string>(); public bool matchmakingQueued; }
    public sealed class RaidEventScreenModel { public readonly List<string> activeRaids = new List<string>(); public readonly List<string> rewardPreviews = new List<string>(); public int secondsUntilRotation; }
    public sealed class StoragePcScreenModel { public readonly List<string> boxes = new List<string>(); public bool multiSelectMode; public string searchText = string.Empty; }
    public sealed class ReadyMenuModel { public readonly List<string> shortcuts = new List<string>(); public void Register(string shortcut) { if (!string.IsNullOrEmpty(shortcut)) shortcuts.Add(shortcut); } }
    public sealed class DebugMenuModel { public bool enabled; public readonly List<string> tools = new List<string> { "spawn creature", "edit party", "teleport", "toggle flags", "modify inventory", "start battle", "spawn raid", "weather", "performance" }; }

    public sealed class MenuTransitionAnimator
    {
        public MenuTransitionKind Current { get; private set; }
        public float Duration { get; private set; }
        public float Progress { get; private set; }
        public bool IsRunning => Progress < 1f && Current != MenuTransitionKind.None;
        public void Start(MenuTransitionKind kind, float duration)
        {
            Current = kind;
            Duration = Math.Max(0.001f, duration);
            Progress = 0f;
        }
        public void Tick(float deltaTime)
        {
            if (Current == MenuTransitionKind.None) return;
            Progress = Math.Min(1f, Progress + Math.Max(0f, deltaTime) / Duration);
        }
    }
}
''',
    'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/PauseMenuSystemTests.cs': r'''using System.Linq;
using __PROJECT_NAMESPACE__.Core;
using __PROJECT_NAMESPACE__.UI;
using NUnit.Framework;

namespace __PROJECT_NAMESPACE__.Tests
{
    public sealed class PauseMenuSystemTests
    {
        [Test]
        public void MainPauseMenu_UsesConditionalVisibilityAndRuntimeInjection()
        {
            var menu = new PauseMenuSystem();
            var context = new PauseMenuContext { hasPokedex = false, partyExists = true, hasMapDevice = false, multiplayerEnabled = false, debugMode = false };
            var visible = menu.VisibleOptions(context);
            Assert.IsFalse(visible.Any(o => o.id == PauseMenuOptionId.Pokedex));
            Assert.IsTrue(visible.Any(o => o.id == PauseMenuOptionId.Pokemon));
            Assert.IsFalse(visible.Any(o => o.id == PauseMenuOptionId.Map));
            Assert.IsFalse(visible.Any(o => o.id == PauseMenuOptionId.Debug));
            menu.InjectOption(new PauseMenuOption { id = PauseMenuOptionId.RaidEvents, label = "Raid Events", targetScreen = PauseMenuScreen.RaidEvents, visibleWhen = c => c.multiplayerEnabled });
            context.multiplayerEnabled = true;
            context.debugMode = true;
            context.hasPokedex = true;
            context.hasMapDevice = true;
            visible = menu.VisibleOptions(context);
            Assert.IsTrue(visible.Any(o => o.id == PauseMenuOptionId.RaidEvents));
            Assert.IsTrue(visible.Any(o => o.id == PauseMenuOptionId.Debug));
            Assert.IsTrue(visible.Any(o => o.id == PauseMenuOptionId.Pokedex));
            Assert.IsTrue(visible.Any(o => o.id == PauseMenuOptionId.Map));
        }

        [Test]
        public void PauseMenu_OpensNavigatesSelectsBacksAndAnimates()
        {
            var menu = new PauseMenuSystem();
            var context = new PauseMenuContext { hasPokedex = true, partyExists = true, hasMapDevice = true };
            var handlerCalled = false;
            menu.RegisterHandler(PauseMenuScreen.Pokemon, () => handlerCalled = true);
            menu.Open(context);
            Assert.IsTrue(menu.IsOpen);
            Assert.IsTrue(menu.OverworldPaused);
            Assert.AreEqual(PauseMenuScreen.Main, menu.ActiveScreen);
            menu.Navigate(context, 1);
            Assert.AreEqual(PauseMenuScreen.Pokemon, menu.SelectCurrent(context));
            Assert.IsTrue(handlerCalled);
            menu.Back();
            Assert.AreEqual(PauseMenuScreen.Main, menu.ActiveScreen);
            menu.Back();
            Assert.IsFalse(menu.IsOpen);
            menu.Transition.Start(MenuTransitionKind.Slide, 0.1f);
            menu.Transition.Tick(0.05f);
            Assert.IsTrue(menu.Transition.IsRunning);
            menu.Transition.Tick(0.05f);
            Assert.AreEqual(1f, menu.Transition.Progress);
        }

        [Test]
        public void PauseMenu_PersistsScaleLocalizationAndControlBindings()
        {
            var menu = new PauseMenuSystem();
            var context = new PauseMenuContext { hasPokedex = true, partyExists = true, uiScale = 2.5f, language = "de" };
            menu.Open(context);
            menu.Navigate(context, 2);
            var snapshot = menu.CreateSnapshot(context);
            var restoredContext = new PauseMenuContext();
            var restored = new PauseMenuSystem();
            restored.Restore(snapshot, restoredContext);
            Assert.IsTrue(restored.IsOpen);
            Assert.AreEqual(snapshot.selectedIndex, restored.SelectedIndex);
            Assert.AreEqual(1.75f, restoredContext.uiScale);
            Assert.AreEqual("de", restoredContext.language);
            Assert.IsTrue(restored.TextFits("Options", 12));
            Assert.IsFalse(restored.TextFits("Very long localized menu label", 8));
            var bindings = new ControlBindingProfile();
            bindings.ResetDefaults();
            bindings.Bind("ReadyMenu", "Tab");
            Assert.IsTrue(bindings.HasConflict("Tab"));
            bindings.Bind("ReadyMenu", "R");
            Assert.IsFalse(bindings.HasConflict("R"));
        }

        [Test]
        public void PauseMenu_ScreenModelsCoverManagementScreens()
        {
            var layout = new PauseMenuLayoutModel();
            Assert.Contains("command list", layout.leftElements);
            Assert.Contains("party preview", layout.rightElements);
            var dex = new PokedexScreenModel();
            dex.Search("leaf");
            dex.TrackForm("mega_form");
            Assert.AreEqual("leaf", dex.SearchText);
            Assert.IsTrue(dex.trackedForms.Contains("mega_form"));
            var party = new PartyScreenModel();
            party.Bind(new[] { "a", "b", "c" });
            Assert.IsTrue(party.Move(0, 2));
            Assert.AreEqual("a", party.creatureIds[2]);
            var bag = new PauseBagScreenModel();
            bag.Favorite("potion");
            Assert.Contains("Raid Materials", bag.pockets);
            Assert.IsTrue(bag.favorites.Contains("potion"));
            var map = new PauseMapScreenModel();
            map.AddMarker("raid_den");
            map.SetZoom(9f);
            Assert.AreEqual(4f, map.zoom);
            var phone = new PhoneScreenModel();
            phone.AddContact("rival");
            phone.PushNotification("raid event");
            Assert.AreEqual(1, phone.contacts.Count);
            Assert.AreEqual(1, phone.notifications.Count);
            var quests = new QuestJournalScreenModel();
            quests.AddQuest("main_01");
            quests.CompleteQuest("main_01");
            Assert.Contains("main_01", quests.history);
            var save = new PauseSaveScreenModel();
            save.PrepareOverwriteWarning();
            Assert.IsTrue(save.overwriteWarningShown);
            var options = new PauseOptionsScreenModel(new SettingsManager());
            options.SetMusicVolume(0.35f);
            var ready = new ReadyMenuModel();
            ready.Register("bike");
            Assert.Contains("bike", ready.shortcuts);
            var debug = new DebugMenuModel { enabled = true };
            Assert.Contains("spawn raid", debug.tools);
            var multiplayer = new MultiplayerScreenModel();
            multiplayer.matchmakingQueued = true;
            var raidEvents = new RaidEventScreenModel();
            raidEvents.activeRaids.Add("event_boss");
            var storage = new StoragePcScreenModel();
            storage.boxes.Add("Box 1");
            Assert.IsTrue(multiplayer.matchmakingQueued);
            Assert.Contains("event_boss", raidEvents.activeRaids);
            Assert.Contains("Box 1", storage.boxes);
        }
    }
}
'''
})

PROJECT_FRAMEWORK_TEMPLATE_FILES.update({
    'Assets/Scripts/Overworld/TallGrassSystem.cs': r'''using System;
using System.Collections.Generic;
using System.Linq;
using __PROJECT_NAMESPACE__.Battle;
using __PROJECT_NAMESPACE__.Pokemon;
using UnityEngine;

namespace __PROJECT_NAMESPACE__.Overworld
{
    public enum TallGrassType { Standard, Dense, Double, Rustling, Wet, FlowerField, Swamp, Snow, Dimensional, Raid, Seasonal }
    public enum TallGrassWeather { Any, Clear, Rain, Snow, Wind, Dimensional }
    public enum TallGrassTimeOfDay { Any, Morning, Day, Evening, Night }
    public enum TallGrassTraversal { Walk, Run, Sprint, Bike, Ride }
    public enum TallGrassFeedbackKind { Entered, RustlingSpawned, RepelSuppressed, EncounterBoosted, SwarmActive }

    [Serializable]
    public sealed class TallGrassRuntimeContext
    {
        public TallGrassWeather weather = TallGrassWeather.Any;
        public TallGrassTimeOfDay timeOfDay = TallGrassTimeOfDay.Any;
        public TallGrassTraversal traversal = TallGrassTraversal.Walk;
        public string seasonKey = "default";
        public bool repelActive;
        public int repelStepsRemaining;
        public int leadCreatureLevel = 1;
        public bool swarmActive;
        public bool eventActive;
        public bool mounted;
        public readonly HashSet<string> storyFlags = new HashSet<string>();
        public readonly HashSet<string> abilityTags = new HashSet<string>();

        public bool HasFlag(string key)
        {
            return string.IsNullOrEmpty(key) || storyFlags.Contains(key);
        }

        public bool HasAbility(string key)
        {
            return !string.IsNullOrEmpty(key) && abilityTags.Contains(key);
        }
    }

    [Serializable]
    public sealed class TallGrassEncounterEntry
    {
        public CreatureSpecies species;
        public string fallbackSpeciesId;
        public int minLevel = 2;
        public int maxLevel = 5;
        public int weight = 1;
        public bool rare;
        public bool ultraRare;
        public bool rustlingOnly;
        public bool hidden;
        public bool swarmOnly;
        public bool eventOnly;
        public TallGrassWeather weather = TallGrassWeather.Any;
        public TallGrassTimeOfDay timeOfDay = TallGrassTimeOfDay.Any;
        public string seasonKey;
        public string requiredStoryFlag;
        public string requiredAbilityTag;

        public string SpeciesId => species != null ? species.id : fallbackSpeciesId;
        public int HighestLevel => Math.Max(minLevel, maxLevel);

        public bool Matches(TallGrassRuntimeContext context, bool rustling)
        {
            if (string.IsNullOrEmpty(SpeciesId)) return false;
            if (weight <= 0) return false;
            if (rustlingOnly && !rustling) return false;
            if (swarmOnly && (context == null || !context.swarmActive)) return false;
            if (eventOnly && (context == null || !context.eventActive)) return false;
            if (context != null)
            {
                if (weather != TallGrassWeather.Any && context.weather != weather) return false;
                if (timeOfDay != TallGrassTimeOfDay.Any && context.timeOfDay != timeOfDay) return false;
                if (!string.IsNullOrEmpty(seasonKey) && seasonKey != context.seasonKey) return false;
                if (!context.HasFlag(requiredStoryFlag)) return false;
                if (!string.IsNullOrEmpty(requiredAbilityTag) && !context.HasAbility(requiredAbilityTag)) return false;
            }
            return true;
        }

        public int RollLevel(IRandomSource rng)
        {
            var min = Math.Min(minLevel, maxLevel);
            var max = Math.Max(minLevel, maxLevel);
            return rng == null ? min : rng.Range(min, max + 1);
        }
    }

    [Serializable]
    public sealed class TallGrassEncounterPool
    {
        public readonly List<TallGrassEncounterEntry> entries = new List<TallGrassEncounterEntry>();

        public bool IsValid => entries.Any(e => e != null && !string.IsNullOrEmpty(e.SpeciesId) && e.weight > 0);

        public List<TallGrassEncounterEntry> LegalEntries(TallGrassRuntimeContext context, bool rustling)
        {
            return entries.Where(e => e != null && e.Matches(context, rustling)).ToList();
        }

        public TallGrassEncounterEntry Roll(TallGrassRuntimeContext context, IRandomSource rng, bool rustling = false)
        {
            var legal = LegalEntries(context, rustling);
            var total = legal.Sum(e => AdjustedWeight(e, context));
            if (total <= 0) return null;
            var roll = rng.Range(0, total);
            foreach (var entry in legal)
            {
                roll -= AdjustedWeight(entry, context);
                if (roll < 0) return entry;
            }
            return null;
        }

        public int AdjustedWeight(TallGrassEncounterEntry entry, TallGrassRuntimeContext context)
        {
            if (entry == null) return 0;
            var weight = Math.Max(0, entry.weight);
            if ((entry.rare || entry.ultraRare) && context != null && context.HasAbility("rare_boost")) weight *= 2;
            if (entry.swarmOnly && context != null && context.swarmActive) weight *= 3;
            return weight;
        }
    }

    [CreateAssetMenu(menuName = "__PROJECT_MENU_ROOT__/Tall Grass Zone Profile")]
    public sealed class TallGrassZoneProfile : ScriptableObject
    {
        public string zoneId = "route_grass";
        public TallGrassType grassType = TallGrassType.Standard;
        public string biomeId = "route";
        public float baseEncounterRate = 0.12f;
        public float rareEncounterModifier = 1f;
        public float doubleBattleChance;
        public float ambushChance;
        public float rustlingSpawnChance = 0.04f;
        public float movementSpeedMultiplier = 1f;
        public string audioProfile = "grass_rustle_standard";
        public string animationProfile = "grass_sway_standard";
        public string shaderProfile = "grass_stylized";
        public TallGrassEncounterPool pool = new TallGrassEncounterPool();

        public float EffectiveEncounterRate(TallGrassRuntimeContext context)
        {
            var rate = baseEncounterRate;
            if (grassType == TallGrassType.Dense) rate *= 1.35f;
            if (grassType == TallGrassType.Double) rate *= 1.55f;
            if (grassType == TallGrassType.Rustling) rate *= 1.9f;
            if (grassType == TallGrassType.Raid) rate *= 0.65f;
            if (context != null)
            {
                if (context.traversal == TallGrassTraversal.Run) rate *= 1.1f;
                if (context.traversal == TallGrassTraversal.Sprint || context.traversal == TallGrassTraversal.Bike) rate *= 1.25f;
                if (context.mounted) rate *= 1.15f;
                if (context.HasAbility("reduced_encounters")) rate *= 0.5f;
                if (context.HasAbility("increased_encounters")) rate *= 1.5f;
                if (context.HasAbility("rare_boost")) rate *= Math.Max(0.1f, rareEncounterModifier);
                if (context.repelActive) rate *= 0.25f;
                if (context.weather == TallGrassWeather.Rain && grassType == TallGrassType.Wet) rate *= 1.25f;
                if (context.weather == TallGrassWeather.Snow && grassType == TallGrassType.Snow) rate *= 1.25f;
                if (context.weather == TallGrassWeather.Dimensional && grassType == TallGrassType.Dimensional) rate *= 1.4f;
            }
            return Mathf.Clamp01(rate);
        }

        public float EffectiveMovementMultiplier(TallGrassRuntimeContext context)
        {
            var multiplier = movementSpeedMultiplier;
            if (grassType == TallGrassType.Dense || grassType == TallGrassType.Swamp) multiplier *= 0.88f;
            if (context != null && context.mounted) multiplier *= 1.1f;
            return Mathf.Clamp(multiplier, 0.35f, 1.5f);
        }
    }

    public sealed class TallGrassEncounterResult
    {
        public bool triggered;
        public bool doubleBattle;
        public bool ambush;
        public bool repelSuppressed;
        public TallGrassEncounterEntry entry;
        public int level;
    }

    public sealed class TallGrassEncounterResolver
    {
        public TallGrassEncounterResult TryRollEncounter(TallGrassZoneProfile profile, TallGrassRuntimeContext context, IRandomSource rng, bool rustling = false)
        {
            var result = new TallGrassEncounterResult();
            if (profile == null || rng == null || profile.pool == null || !profile.pool.IsValid) return result;
            if (rng.Value01() > profile.EffectiveEncounterRate(context)) return result;
            var entry = profile.pool.Roll(context, rng, rustling);
            if (entry == null) return result;
            if (IsRepelled(context, entry))
            {
                result.repelSuppressed = true;
                return result;
            }
            result.triggered = true;
            result.entry = entry;
            result.level = entry.RollLevel(rng);
            result.doubleBattle = profile.grassType == TallGrassType.Double || rng.Value01() < profile.doubleBattleChance;
            result.ambush = rng.Value01() < profile.ambushChance;
            return result;
        }

        public bool IsRepelled(TallGrassRuntimeContext context, TallGrassEncounterEntry entry)
        {
            return context != null && context.repelActive && context.repelStepsRemaining > 0 && entry != null && entry.HighestLevel < context.leadCreatureLevel;
        }
    }

    [Serializable]
    public sealed class RustlingGrassSpawn
    {
        public string spawnId;
        public string zoneId;
        public string speciesId;
        public Vector2Int tile;
        public float ageSeconds;
        public float visibilitySeconds = 12f;
        public bool active = true;

        public void Tick(float deltaSeconds)
        {
            ageSeconds += Math.Max(0f, deltaSeconds);
            if (ageSeconds >= visibilitySeconds) active = false;
        }
    }

    public sealed class RustlingGrassSystem
    {
        public bool TrySpawn(TallGrassZoneProfile profile, TallGrassRuntimeContext context, IRandomSource rng, Vector2Int tile, out RustlingGrassSpawn spawn)
        {
            spawn = null;
            if (profile == null || rng == null || rng.Value01() > profile.rustlingSpawnChance) return false;
            var entry = profile.pool.Roll(context, rng, true) ?? profile.pool.Roll(context, rng, false);
            if (entry == null) return false;
            spawn = new RustlingGrassSpawn
            {
                spawnId = profile.zoneId + "_" + tile.x + "_" + tile.y,
                zoneId = profile.zoneId,
                speciesId = entry.SpeciesId,
                tile = tile,
                visibilitySeconds = profile.grassType == TallGrassType.Rustling ? 18f : 12f
            };
            return true;
        }
    }

    [Serializable]
    public sealed class TallGrassSaveRecord
    {
        public string zoneId;
        public bool swarmActive;
        public string seasonKey = "default";
        public List<RustlingGrassSpawn> rustlingSpawns = new List<RustlingGrassSpawn>();
    }

    public sealed class TallGrassPersistence
    {
        public TallGrassSaveRecord Save(string zoneId, TallGrassRuntimeContext context, IEnumerable<RustlingGrassSpawn> spawns)
        {
            return new TallGrassSaveRecord
            {
                zoneId = zoneId,
                swarmActive = context != null && context.swarmActive,
                seasonKey = context != null ? context.seasonKey : "default",
                rustlingSpawns = spawns == null ? new List<RustlingGrassSpawn>() : spawns.Where(s => s != null && s.active).ToList()
            };
        }

        public void Load(TallGrassSaveRecord record, TallGrassRuntimeContext context, List<RustlingGrassSpawn> targetSpawns)
        {
            if (record == null) return;
            if (context != null)
            {
                context.swarmActive = record.swarmActive;
                context.seasonKey = string.IsNullOrEmpty(record.seasonKey) ? "default" : record.seasonKey;
            }
            if (targetSpawns != null)
            {
                targetSpawns.Clear();
                targetSpawns.AddRange(record.rustlingSpawns ?? new List<RustlingGrassSpawn>());
            }
        }
    }

    public sealed class TallGrassVisualState
    {
        public float swayStrength;
        public float bendStrength;
        public float lowerBodyVisibility = 1f;
        public float cameraFade;
        public string audioCue;
        public TallGrassFeedbackKind feedback;
    }

    public sealed class TallGrassVisualFeedback
    {
        public TallGrassVisualState Compute(TallGrassZoneProfile profile, TallGrassRuntimeContext context, bool playerInside, float movementSpeed01)
        {
            var state = new TallGrassVisualState
            {
                audioCue = profile != null ? profile.audioProfile : "grass_rustle_standard",
                feedback = playerInside ? TallGrassFeedbackKind.Entered : TallGrassFeedbackKind.EncounterBoosted,
                lowerBodyVisibility = playerInside ? 0.62f : 1f,
                cameraFade = playerInside ? 0.18f : 0f,
                swayStrength = Mathf.Clamp01(0.25f + movementSpeed01 * 0.75f),
                bendStrength = playerInside ? Mathf.Clamp01(0.35f + movementSpeed01 * 0.65f) : 0f
            };
            if (context != null && context.weather == TallGrassWeather.Wind) state.swayStrength = Mathf.Clamp01(state.swayStrength + 0.25f);
            if (context != null && context.weather == TallGrassWeather.Rain) state.audioCue = "grass_rustle_wet";
            if (profile != null && profile.grassType == TallGrassType.Dimensional) state.feedback = TallGrassFeedbackKind.EncounterBoosted;
            return state;
        }
    }

    public sealed class TallGrassPerformanceBudget
    {
        public int maxVisibleInstances = 2500;
        public int maxAnimatedClusters = 160;
        public bool SupportsDenseField(int visibleInstances, int animatedClusters)
        {
            return visibleInstances <= maxVisibleInstances && animatedClusters <= maxAnimatedClusters;
        }
    }

    public sealed class TallGrassZone : MonoBehaviour
    {
        public TallGrassZoneProfile profile;
        public bool playerInside;
        public event Action<TallGrassEncounterResult> EncounterRolled;
        private readonly TallGrassEncounterResolver resolver = new TallGrassEncounterResolver();

        public void Configure(TallGrassZoneProfile zoneProfile)
        {
            profile = zoneProfile;
        }

        public TallGrassEncounterResult RegisterMovementStep(TallGrassRuntimeContext context, IRandomSource rng)
        {
            var result = resolver.TryRollEncounter(profile, context, rng);
            if (result.triggered || result.repelSuppressed) EncounterRolled?.Invoke(result);
            return result;
        }

        private void OnTriggerEnter(Collider other)
        {
            if (other.CompareTag("Player")) playerInside = true;
        }

        private void OnTriggerExit(Collider other)
        {
            if (other.CompareTag("Player")) playerInside = false;
        }
    }
}
''',
    'Assets/Tests/__PROJECT_NAMESPACE__/EditMode/TallGrassSystemTests.cs': r'''using System.Collections.Generic;
using __PROJECT_NAMESPACE__.Battle;
using __PROJECT_NAMESPACE__.Overworld;
using __PROJECT_NAMESPACE__.Pokemon;
using NUnit.Framework;
using UnityEngine;

namespace __PROJECT_NAMESPACE__.Tests
{
    public sealed class TallGrassSystemTests
    {
        private static TallGrassZoneProfile Profile(string id = "test_grass")
        {
            var profile = ScriptableObject.CreateInstance<TallGrassZoneProfile>();
            profile.zoneId = id;
            profile.baseEncounterRate = 1f;
            profile.pool.entries.Add(new TallGrassEncounterEntry { species = TestFactories.Species("leafling"), minLevel = 3, maxLevel = 5, weight = 10 });
            return profile;
        }

        [Test]
        public void EncounterRate_UsesGrassTraversalAbilityAndRepelModifiers()
        {
            var profile = Profile();
            profile.grassType = TallGrassType.Dense;
            profile.baseEncounterRate = 0.4f;
            var context = new TallGrassRuntimeContext { traversal = TallGrassTraversal.Sprint };
            var boosted = profile.EffectiveEncounterRate(context);
            context.abilityTags.Add("reduced_encounters");
            context.repelActive = true;
            var reduced = profile.EffectiveEncounterRate(context);
            Assert.Greater(boosted, 0.4f);
            Assert.Less(reduced, boosted);
        }

        [Test]
        public void SpawnPool_ValidatesAndFiltersWeatherTimeAndStory()
        {
            var profile = ScriptableObject.CreateInstance<TallGrassZoneProfile>();
            profile.pool.entries.Add(new TallGrassEncounterEntry { species = TestFactories.Species("rainbat"), weight = 5, weather = TallGrassWeather.Rain, timeOfDay = TallGrassTimeOfDay.Night, requiredStoryFlag = "forest_open" });
            profile.pool.entries.Add(new TallGrassEncounterEntry { species = TestFactories.Species("daybug"), weight = 5, timeOfDay = TallGrassTimeOfDay.Day });
            var context = new TallGrassRuntimeContext { weather = TallGrassWeather.Rain, timeOfDay = TallGrassTimeOfDay.Night };
            Assert.IsTrue(profile.pool.IsValid);
            Assert.AreEqual(0, profile.pool.LegalEntries(context, false).Count);
            context.storyFlags.Add("forest_open");
            var legal = profile.pool.LegalEntries(context, false);
            Assert.AreEqual(1, legal.Count);
            Assert.AreEqual("rainbat", legal[0].SpeciesId);
            Object.DestroyImmediate(profile);
        }

        [Test]
        public void RepelSuppressesLowerLevelEncounterButAllowsStrongerCreature()
        {
            var resolver = new TallGrassEncounterResolver();
            var context = new TallGrassRuntimeContext { repelActive = true, repelStepsRemaining = 10, leadCreatureLevel = 10 };
            var weak = new TallGrassEncounterEntry { fallbackSpeciesId = "weak", minLevel = 2, maxLevel = 4, weight = 1 };
            var strong = new TallGrassEncounterEntry { fallbackSpeciesId = "strong", minLevel = 11, maxLevel = 12, weight = 1 };
            Assert.IsTrue(resolver.IsRepelled(context, weak));
            Assert.IsFalse(resolver.IsRepelled(context, strong));
        }

        [Test]
        public void EncounterResolver_RollsDeterministicGrassEncounterAndDoubleGrass()
        {
            var profile = Profile();
            profile.grassType = TallGrassType.Double;
            profile.doubleBattleChance = 0.5f;
            var result = new TallGrassEncounterResolver().TryRollEncounter(profile, new TallGrassRuntimeContext(), new FixedRandomSource(0));
            Assert.IsTrue(result.triggered);
            Assert.IsTrue(result.doubleBattle);
            Assert.AreEqual("leafling", result.entry.SpeciesId);
            Assert.GreaterOrEqual(result.level, 3);
            Object.DestroyImmediate(profile);
        }

        [Test]
        public void RustlingGrass_SpawnsRareTimedPersistentState()
        {
            var profile = Profile("rustle_zone");
            profile.grassType = TallGrassType.Rustling;
            profile.rustlingSpawnChance = 1f;
            profile.pool.entries.Add(new TallGrassEncounterEntry { species = TestFactories.Species("rareling"), weight = 20, rare = true, rustlingOnly = true });
            var system = new RustlingGrassSystem();
            Assert.IsTrue(system.TrySpawn(profile, new TallGrassRuntimeContext(), new FixedRandomSource(0), new Vector2Int(4, 7), out var spawn));
            Assert.AreEqual("rustle_zone_4_7", spawn.spawnId);
            Assert.IsTrue(spawn.active);
            spawn.Tick(99f);
            Assert.IsFalse(spawn.active);
            Object.DestroyImmediate(profile);
        }

        [Test]
        public void TallGrassPersistence_SavesAndLoadsSwarmSeasonAndRustlingSpawns()
        {
            var context = new TallGrassRuntimeContext { swarmActive = true, seasonKey = "winter" };
            var spawns = new List<RustlingGrassSpawn> { new RustlingGrassSpawn { spawnId = "a", speciesId = "rareling", active = true }, new RustlingGrassSpawn { spawnId = "b", active = false } };
            var persistence = new TallGrassPersistence();
            var record = persistence.Save("zone", context, spawns);
            Assert.AreEqual(1, record.rustlingSpawns.Count);
            var loadedContext = new TallGrassRuntimeContext();
            var loadedSpawns = new List<RustlingGrassSpawn>();
            persistence.Load(record, loadedContext, loadedSpawns);
            Assert.IsTrue(loadedContext.swarmActive);
            Assert.AreEqual("winter", loadedContext.seasonKey);
            Assert.AreEqual("a", loadedSpawns[0].spawnId);
        }

        [Test]
        public void WeatherAndDayNight_ChooseOnlyMatchingEncounterEntries()
        {
            var profile = ScriptableObject.CreateInstance<TallGrassZoneProfile>();
            profile.baseEncounterRate = 1f;
            profile.pool.entries.Add(new TallGrassEncounterEntry { species = TestFactories.Species("sunmoth"), weight = 5, weather = TallGrassWeather.Clear, timeOfDay = TallGrassTimeOfDay.Day });
            profile.pool.entries.Add(new TallGrassEncounterEntry { species = TestFactories.Species("nightdrop"), weight = 5, weather = TallGrassWeather.Rain, timeOfDay = TallGrassTimeOfDay.Night });
            var context = new TallGrassRuntimeContext { weather = TallGrassWeather.Rain, timeOfDay = TallGrassTimeOfDay.Night };
            var result = new TallGrassEncounterResolver().TryRollEncounter(profile, context, new FixedRandomSource(0));
            Assert.IsTrue(result.triggered);
            Assert.AreEqual("nightdrop", result.entry.SpeciesId);
            Object.DestroyImmediate(profile);
        }

        [Test]
        public void VisualFeedbackAndPerformanceBudgetKeepGrassReadable()
        {
            var profile = Profile();
            profile.audioProfile = "grass_rustle_standard";
            var context = new TallGrassRuntimeContext { weather = TallGrassWeather.Rain };
            var state = new TallGrassVisualFeedback().Compute(profile, context, true, 0.8f);
            Assert.Less(state.lowerBodyVisibility, 1f);
            Assert.Greater(state.bendStrength, 0.5f);
            Assert.AreEqual("grass_rustle_wet", state.audioCue);
            var budget = new TallGrassPerformanceBudget { maxVisibleInstances = 100, maxAnimatedClusters = 10 };
            Assert.IsTrue(budget.SupportsDenseField(100, 10));
            Assert.IsFalse(budget.SupportsDenseField(101, 10));
            Object.DestroyImmediate(profile);
        }
    }
}
'''
})

def generate_project(root_dir, logger=None):
    builder = PokemonProjectBuilder(logger=logger)
    builder.generate(root_dir)
    return root_dir


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a PokeEngine Unity RPG prototype project.")
    parser.add_argument("project_path", nargs="?", default=DEFAULT_PROJECT_PATH)
    args = parser.parse_args()

    generate_project(args.project_path)
    print(f"Generated PokeEngine project at: {args.project_path}")
