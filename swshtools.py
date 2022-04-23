import argparse
import json
import os
import struct


# ----------------------------------------------------------------------------------------------------------------------
# File helper functions to read and write binary or JSON data.
# ----------------------------------------------------------------------------------------------------------------------
def read_bin_file(file_path: str) -> bytearray:
    with open(file_path, "rb") as f:
        ret = f.read()
    return bytearray(ret)


def write_bin_file(file_path: str, buffer):
    if buffer is None:
        raise ValueError("Tried to write non-existent data to file.")

    # Try to create parent directories if necessary
    if file_path.find("/") != -1:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(buffer)
        f.flush()


def read_json_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def write_json_file(file_path: str, data, encoder=json.JSONEncoder):
    # Try to create parent directories if necessary
    if file_path.find("/") != -1:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False, cls=encoder)
        f.flush()


# ----------------------------------------------------------------------------------------------------------------------
# Constants and enumeration names for easier-to-read and context-clear JSON files. The following categories exist:
#
# pokemon         | Unique identifiers for all Pokémon and their respective forms
# moves           | Unique identifiers for all moves
# types           | Identifiers for all types
# abilities       | Identifiers for every ability in the game
# items           | Unique identifiers for all items
# egg_groups      | Available egg groups
# growth_types    | Available growth rates/types
# dex_colors      | Available dex colors
# tms             | List of available TM moves
# trs             | List of available TR moves
# move_tutors     | List of available Tutor moves
# armor_tutors    | List of available Tutor moves from the Isle of Armor
# evolution_types | All available evolution condition types
# genders         | Gender types for icon list
# ----------------------------------------------------------------------------------------------------------------------
__CONSTANTS__ = read_json_file("constants.json")


def cnstname(category: str, cval: int) -> str:
    return __CONSTANTS__[category][cval]


def cnstval(category: str, cname: str) -> int:
    return __CONSTANTS__[category].index(cname)


# ----------------------------------------------------------------------------------------------------------------------
# Pokémon base stats (personal_total.bin)
# ----------------------------------------------------------------------------------------------------------------------
__BLANK_PRSNL_ENTRY__ = bytes.fromhex("000000000000000000000000000000000000FF0000000000000000000000000000400000000000"
                                      "000000000000000000000000000000000000000000000000000000000000000000000000000000"
                                      "000000000000000000000000000000000000010001000100010001000000000000000000000000"
                                      "000000000000000000000000000001010101010101010101010101010100000000000000000000"
                                      "0000000000000000000000000000000000000000")
__PERSONAL_ENTRY_STRUCT__ = struct.Struct("<10B4H6B4H2B3H16s4s16sI8H72s4s2H")


def unpack_personal(in_file: str, out_file: str) -> None:
    buffer = read_bin_file(in_file)
    len_buffer = len(buffer)

    entries = dict()

    for i in range(len_buffer // 0xB0):
        entry = dict()
        offset = i * 0xB0

        # Unpack binary entry data
        base_hp, base_atk, base_def, base_spd, base_sp_atk, base_sp_def, type_1, type_2, catch_rate, evolution_stage,\
        ev_yield, common_item, rare_item, very_rare_item, gender_rate, hatch_cycles, base_friendship, growth_type,\
        egg_group_1, egg_group_2, ability_1, ability_2, hidden_ability, first_form_index, form_count, pokedex_bits,\
        base_exp, height, weight, tm_bits, move_tutors_bits, tr_bits, icon_id, special_z_item, special_z_base_move,\
        special_z_move, egg_species, egg_form, special_species_flags, pokedex_number, unk5E, unk60, armor_tutors_bits,\
        armor_dex_number, crown_dex_number = __PERSONAL_ENTRY_STRUCT__.unpack_from(buffer, offset)

        # Create JSON entry from unpacked data. The order was chosen to put related elements closer to each other
        entry["type_1"] = cnstname("types", type_1)
        entry["type_2"] = cnstname("types", type_2)
        entry["base_hp"] = base_hp
        entry["base_atk"] = base_atk
        entry["base_def"] = base_def
        entry["base_sp_atk"] = base_sp_atk
        entry["base_sp_def"] = base_sp_def
        entry["base_spd"] = base_spd
        entry["ability_1"] = cnstname("abilities", ability_1)
        entry["ability_2"] = cnstname("abilities", ability_2)
        entry["hidden_ability"] = cnstname("abilities", hidden_ability)
        entry["height"] = height
        entry["weight"] = weight
        entry["evs_hp"] = ev_yield & 3
        entry["evs_atk"] = (ev_yield >> 2) & 3
        entry["evs_def"] = (ev_yield >> 4) & 3
        entry["evs_sp_atk"] = (ev_yield >> 8) & 3
        entry["evs_sp_def"] = (ev_yield >> 10) & 3
        entry["evs_spd"] = (ev_yield >> 6) & 3
        entry["fail_telekinesis"] = bool((ev_yield >> 12) & 3)
        entry["catch_rate"] = catch_rate
        entry["gender_rate"] = gender_rate
        entry["base_exp"] = base_exp
        entry["growth_type"] = cnstname("growth_types", growth_type)
        entry["special_z_item"] = cnstname("items", special_z_item)
        entry["special_z_base_move"] = cnstname("moves", special_z_base_move)
        entry["special_z_move"] = cnstname("moves", special_z_move)
        entry["egg_group_1"] = cnstname("egg_groups", egg_group_1)
        entry["egg_group_2"] = cnstname("egg_groups", egg_group_2)
        entry["evolution_stage"] = evolution_stage
        entry["egg_species"] = cnstname("pokemon", egg_species)
        entry["egg_form"] = egg_form
        entry["hatch_cycles"] = hatch_cycles
        entry["base_friendship"] = base_friendship
        entry["common_item"] = cnstname("items", common_item)
        entry["rare_item"] = cnstname("items", rare_item)
        entry["very_rare_item"] = cnstname("items", very_rare_item)
        entry["first_form_index"] = cnstname("pokemon", first_form_index)
        entry["form_count"] = form_count
        entry["icon_id"] = icon_id
        entry["pokedex_number"] = pokedex_number
        entry["armor_dex_number"] = armor_dex_number
        entry["crown_dex_number"] = crown_dex_number
        entry["dex_color"] = cnstname("dex_colors", pokedex_bits & 0x3F)
        entry["has_dex_entry"] = bool(pokedex_bits & 0x40)
        entry["is_visual_form"] = bool(pokedex_bits & 0x80)
        entry["is_regional_form"] = bool(special_species_flags & 0x1)
        entry["can_not_dynamax"] = bool(special_species_flags & 0x4)
        entry["tms"] = list()
        entry["trs"] = list()
        entry["move_tutors"] = list()
        entry["armor_tutors"] = list()
        entry["unk5E"] = unk5E
        entry["unk60"] = unk60.hex()

        # TMs/TRs/etc. learnsets are stored as bitflags. We'll have to unpack those first
        def parse_learnset_bits(consts_name: str, bits: bytes):
            for index, move in enumerate(__CONSTANTS__[consts_name]):
                if bits[index >> 3] & (1 << (index & 7)):
                    entry[consts_name].append(move)

        parse_learnset_bits("tms", tm_bits)
        parse_learnset_bits("trs", tr_bits)
        parse_learnset_bits("move_tutors", move_tutors_bits)
        parse_learnset_bits("armor_tutors", armor_tutors_bits)

        entries[cnstname("pokemon", i)] = entry

    write_json_file(out_file, entries)


def pack_personal(in_file: str, out_file: str) -> None:
    entries = read_json_file(in_file)
    buffer = bytearray(len(__CONSTANTS__["pokemon"]) * __BLANK_PRSNL_ENTRY__)
    offset = 0

    for pokemon_name, entry in entries.items():
        def pack_learnset_bits(consts_name: str, size: int):
            bits = bytearray(size)
            for index, move in enumerate(__CONSTANTS__[consts_name]):
                if move in entry[consts_name]:
                    bits[index >> 3] |= 1 << (index & 7)
            return bits

        tm_bits = pack_learnset_bits("tms", 16)
        move_tutors_bits = pack_learnset_bits("move_tutors", 4)
        tr_bits = pack_learnset_bits("trs", 16)
        armor_tutors_bits = pack_learnset_bits("armor_tutors", 4)

        type_1 = cnstval("types", entry["type_1"])
        type_2 = cnstval("types", entry["type_2"])
        ev_yield = entry["evs_hp"] & 3
        ev_yield |= (entry["evs_atk"] & 3) << 2
        ev_yield |= (entry["evs_def"] & 3) << 4
        ev_yield |= (entry["evs_spd"] & 3) << 6
        ev_yield |= (entry["evs_sp_atk"] & 3) << 8
        ev_yield |= (entry["evs_sp_def"] & 3) << 10
        ev_yield |= (1 if entry["fail_telekinesis"] else 0) << 12
        common_item = cnstval("items", entry["common_item"])
        rare_item = cnstval("items", entry["rare_item"])
        very_rare_item = cnstval("items", entry["very_rare_item"])
        growth_type = cnstval("growth_types", entry["growth_type"])
        egg_group_1 = cnstval("egg_groups", entry["egg_group_1"])
        egg_group_2 = cnstval("egg_groups", entry["egg_group_2"])
        ability_1 = cnstval("abilities", entry["ability_1"])
        ability_2 = cnstval("abilities", entry["ability_2"])
        hidden_ability = cnstval("abilities", entry["hidden_ability"])
        first_form_index = cnstval("pokemon", entry["first_form_index"])
        pokedex_bits = cnstval("dex_colors", entry["dex_color"])
        pokedex_bits |= 0x40 if entry["has_dex_entry"] else 0
        pokedex_bits |= 0x80 if entry["is_visual_form"] else 0
        special_z_item = cnstval("items", entry["special_z_item"])
        special_z_base_move = cnstval("moves", entry["special_z_base_move"])
        special_z_move = cnstval("moves", entry["special_z_move"])
        egg_species = cnstval("pokemon", entry["egg_species"])
        special_species_flags = 1 if entry["is_regional_form"] else 0
        special_species_flags |= 4 if entry["can_not_dynamax"] else 0

        __PERSONAL_ENTRY_STRUCT__.pack_into(buffer, offset, entry["base_hp"], entry["base_atk"], entry["base_def"],
                                            entry["base_spd"], entry["base_sp_atk"], entry["base_sp_def"], type_1,
                                            type_2, entry["catch_rate"], entry["evolution_stage"], ev_yield, common_item,
                                            rare_item, very_rare_item, entry["gender_rate"], entry["hatch_cycles"],
                                            entry["base_friendship"], growth_type, egg_group_1, egg_group_2, ability_1,
                                            ability_2, hidden_ability, first_form_index, entry["form_count"],
                                            pokedex_bits, entry["base_exp"], entry["height"], entry["weight"], tm_bits,
                                            move_tutors_bits, tr_bits, entry["icon_id"], special_z_item,
                                            special_z_base_move, special_z_move, egg_species, entry["egg_form"],
                                            special_species_flags, entry["pokedex_number"], entry["unk5E"],
                                            bytes.fromhex(entry["unk60"]), armor_tutors_bits, entry["armor_dex_number"],
                                            entry["crown_dex_number"])
        offset += 0xB0

    write_bin_file(out_file, buffer)


# ----------------------------------------------------------------------------------------------------------------------
# Level-up learnsets (wazaoboe_total.bin)
# ----------------------------------------------------------------------------------------------------------------------
def unpack_wazaoboe(in_file: str, out_file: str) -> None:
    buffer = read_bin_file(in_file)
    len_buffer = len(buffer)

    entries = dict()

    for i in range(len_buffer // 0x104):
        moves_list = list()
        offset = i * 0x104

        for j in range(65):
            move, level = struct.unpack_from("<2H", buffer, offset)
            offset += 4

            if move != 65535 and level != 65535:
                moves_list.append({
                    "level": level,
                    "move": cnstname("moves", move)
                })

        entries[__CONSTANTS__["pokemon"][i]] = moves_list

    # Overriding JSONEncoder.encode is a real mess, so we will have to stay with this ugly solution for now. Basically,
    # this ensures that all move entries are kept on a single line to make the output more appealing to look at.
    unpacked_raw = json.dumps(entries, indent=4, ensure_ascii=False).replace("{\n            ", "{ ")
    unpacked_raw = unpacked_raw.replace(",\n            \"move\"", ", \"move\"")
    unpacked_raw = unpacked_raw.replace("\n        },\n", " },\n")
    unpacked_raw = unpacked_raw.replace("\n        }\n", " }\n")

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(unpacked_raw)
        f.flush()


def pack_wazaoboe(in_file: str, out_file: str) -> None:
    entries = read_json_file(in_file)
    buffer = bytearray(len(__CONSTANTS__["pokemon"]) * 0x104 * [0xFF])

    for pokemon_name, move_list in entries.items():
        offset = cnstval("pokemon", pokemon_name) * 0x104
        num_entries = len(move_list)

        if num_entries > 65:
            num_entries = 65
            print(f"Warning! You can have up to 65 level-up moves for {pokemon_name}, remaining ones will be dropped!")

        for i in range(num_entries):
            entry = move_list[i]
            struct.pack_into("<2H", buffer, offset, cnstval("moves", entry["move"]), entry["level"])
            offset += 4

    write_bin_file(out_file, buffer)


# ----------------------------------------------------------------------------------------------------------------------
# pokecaplist.bin -- Pokémon Icon List
# ----------------------------------------------------------------------------------------------------------------------
__POKECAPLIST_ENTRY_STRUCT__ = struct.Struct("<3Hx?")


def unpack_pokecaplist(in_file: str, out_file: str) -> None:
    buffer = read_bin_file(in_file)
    len_buffer = len(buffer)
    offset = 0

    entries = list()

    while offset < len_buffer:
        icon_id, form_id, gender_type, is_gigantamax = __POKECAPLIST_ENTRY_STRUCT__.unpack_from(buffer, offset)
        offset += 8

        entries.append({
            "icon_id": icon_id,
            "form_id": form_id,
            "gender_type": cnstname("genders", gender_type),
            "is_gigantamax": is_gigantamax
        })

    write_json_file(out_file, entries)


def pack_pokecaplist(in_file: str, out_file: str) -> None:
    entries = read_json_file(in_file)
    buffer = bytearray(len(entries) * 8)
    offset = 0

    for entry in entries:
        icon_id = entry["icon_id"]
        form_id = entry["form_id"]
        gender_type = cnstval("genders", entry["gender_type"])
        is_gigantamax = entry["is_gigantamax"]

        __POKECAPLIST_ENTRY_STRUCT__.pack_into(buffer, offset, icon_id, form_id, gender_type, is_gigantamax)
        offset += 8

    write_bin_file(out_file, buffer)


# ----------------------------------------------------------------------------------------------------------------------
# Entry point and input parsing
# ----------------------------------------------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="")
    subs = parser.add_subparsers(dest="command", help="Command")
    subs.required = True

    unpack_personal_parser = subs.add_parser("upersonal", description="Dump personal data to JSON file.")
    unpack_wazaoboe_parser = subs.add_parser("uwazaoboe", description="Dump wazaoboe data to JSON file.")
    unpack_pokecaplist_parser = subs.add_parser("upokecaplist", description="Dump pokecaplist data to JSON file.")
    pack_personal_parser = subs.add_parser("ppersonal", description="Pack personal data from JSON file.")
    pack_wazaoboe_parser = subs.add_parser("pwazaoboe", description="Pack wazaoboe data from JSON file.")
    pack_pokecaplist_parser = subs.add_parser("ppokecaplist", description="Pack pokecaplist data from JSON file.")

    for sub_parser in [unpack_personal_parser, unpack_wazaoboe_parser, unpack_pokecaplist_parser,
                       pack_personal_parser, pack_wazaoboe_parser, pack_pokecaplist_parser]:
        sub_parser.add_argument("in_path", help="Path to input file.")
        sub_parser.add_argument("out_path", help="Path to output file.")

    unpack_personal_parser.set_defaults(func=lambda args: unpack_personal(args.in_path, args.out_path))
    unpack_wazaoboe_parser.set_defaults(func=lambda args: unpack_wazaoboe(args.in_path, args.out_path))
    unpack_pokecaplist_parser.set_defaults(func=lambda args: unpack_pokecaplist(args.in_path, args.out_path))
    pack_personal_parser.set_defaults(func=lambda args: pack_personal(args.in_path, args.out_path))
    pack_wazaoboe_parser.set_defaults(func=lambda args: pack_wazaoboe(args.in_path, args.out_path))
    pack_pokecaplist_parser.set_defaults(func=lambda args: pack_pokecaplist(args.in_path, args.out_path))

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
