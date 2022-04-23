# swshtools
**swshtools** is a collection of Python tools to help with several binary files found in *Pokémon Sword and Shield*. These were originally created to develop a private project that has already been abandoned. The tools can convert data between BIN and JSON files. It should run fine with at least **Python 3.6**.

To convert a Pokémon parameters file (personal_total.bin) to JSON:
```sh
python upersonal IN_FILE_PATH OUT_FILE_PATH
```

To convert a Pokémon parameters JSON file to personal_total.bin:
```sh
python ppersonal IN_FILE_PATH OUT_FILE_PATH
```

To convert a Pokémon learnset file (wazaoboe.bin) to JSON:
```sh
python uwazaoboe IN_FILE_PATH OUT_FILE_PATH
```

To convert a Pokémon learnset JSON file to wazaoboe.bin:
```sh
python pwazaoboe IN_FILE_PATH OUT_FILE_PATH
```

To convert a Pokémon icons file (pokecaplist.bin) to JSON:
```sh
python upokecaplist IN_FILE_PATH OUT_FILE_PATH
```

To convert a Pokémon icons JSON file to pokecaplist.bin:
```sh
python ppokecaplist IN_FILE_PATH OUT_FILE_PATH
```
