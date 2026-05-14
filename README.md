# This project is made with A.I 

# PokeEngine

PokeEngine is a desktop studio hub for generating and editing a Unity 2022.3.62f3 2.5D monster-catching RPG framework. It creates a ready-to-open Unity project from the local `components/` template tree, then gives you focused tools for editing generated gameplay data.

## Main Files

- `Pokeengine.pyw` - desktop UI launcher and data-management interface.
- `Pokeengine_core.py` - project generation engine that copies and tokenizes the framework files.
- `components/` - Unity scripts, editor tools, tests, StreamingAssets data, and content-pipeline templates used by generated projects.
- `pokeengine_settings.json` - saved app preferences and recent project metadata.
- `logs/` - app, generation, and legacy log files.

## What The Tool Offers

### Home

- Launches new framework projects.
- Opens existing generated projects.
- Shows recent projects for quick access.
- Displays the active project destination.
- Creates a Unity framework project using the selected project name and destination folder.
- Copies framework assets from `components/` into the generated Unity project.
- Applies project-name namespace tokens such as `__PROJECT_NAMESPACE__`.

### Pokedex Manager

- Finds and opens generated gameplay JSON databases.
- Supports Pokedex-focused files such as `pokedex_database.json`, `pokemon_species.json`, `pokemon.json`, `pokemon_forms.json`, `moves.json`, `types.json`, `abilities.json`, `natures.json`, `status_conditions.json`, `encounter_tables.json`, `region_map.json`, and `quests.json`.
- Provides sidebar shortcuts for Data files: Pokemon, Pokedex, Moves, Abilities, Types, Items, and Natures.
- Provides sidebar shortcuts for Level Design files: Zones, Groups, Trainers, and Quests.
- Provides a Pokemon table view with ID, Dex #, Pokemon, and Typing.
- Shows a tabbed Pokemon detail view for Pokemon overview, move pool, and resource references.
- Adds new Pokemon records with default schema-compatible fields.
- Imports Pokemon lists from JSON, CSV, or plain text files.
- Skips duplicate imported Pokemon by ID or name.
- Edits Pokemon types from the detail view.
- Adds a Pokemon form from the detail view.
- Edits the full forms list from the detail view.
- Edits the Pokemon move pool/learnset from the detail view using one move per line or `level, move-name`.
- Deletes all Pokemon records from the selected Pokedex database after confirmation.
- Falls back to a generic JSON record editor for non-specialized Pokedex data files.

### Items Manager

- Finds and opens inventory-focused JSON databases.
- Supports item files such as `items.json`, `key_items.json`, `berries.json`, `tms_by_generation.json`, `hms_by_generation.json`, and `backpack_categories.json`.
- Adds new item records with default fields.
- Edits item name, sprite path, script location, category, price, and description.
- Opens a sprite picker for item sprite paths.
- Provides generic JSON editing for item-family files that do not use the specialized item form.

### Generic Database Editing

- Searches records in the selected JSON file.
- Displays compact record summaries.
- Edits a selected record as formatted JSON.
- Adds generic records.
- Deletes selected records after confirmation.
- Saves changes back to the active JSON database file.
- Handles list files, dictionary-with-list files, dictionary keyed by record ID, and single-record JSON files.

### README Page

- Shows this `README.md` inside the app from the sidebar menu.
- Reloads the file from disk so documentation edits can be reviewed without restarting the app.

### Settings And Logs

- Stores project name, destination, and recent project settings.
- Shows live app output and generation progress.
- Writes generation logs to `logs/generation/`.
- Keeps app logs under `logs/app/`.
- Provides a shortcut to the logs folder.

## Generated Unity Framework Content

The generated Unity project includes framework code and data for:

- Core runtime bootstrap and feature registry.
- Pokemon species data and runtime database.
- Battle systems, advanced battle scaffolding, transformations, fusion, and raids.
- Overworld movement, camera controls, encounters, pickups, tall grass, Pokemon Center transitions, and world streaming.
- Save systems.
- UI scaffolds, HUD, pause menu, and world prompts.
- Interaction, event, flag, and cutscene systems.
- Audio/visual scaffolds.
- Unity editor menu tools.
- EditMode and PlayMode test scaffolds.
- StreamingAssets JSON databases for Pokemon, moves, items, abilities, forms, evolutions, encounters, region maps, quests, type charts, battle config, storage config, raid/bossfight config, localization, and settings schema.

## Content Pipeline

- `components/Tools/ContentPipeline/build_full_pokemon_database.py` can build a fuller local Pokemon fangame JSON database from PokeAPI data.
- Generated or curated data can be imported into the Pokedex Manager when it is converted to JSON, CSV, or text list form.



