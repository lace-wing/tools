from io import TextIOWrapper
import os
from os.path import isfile
import re
import csv
import json
import matplotlib.pyplot as plt
from matplotlib.typing import ColorType

CONFIG_FILE = 'retro.conf.json'

CONFIG_ITEMS: list[str] = [
    'theme_path',
    'theme_name',
    'input_path',
    'output_dir'
]
CELL_COLOR_KEYS: list[str] = [
    'fore',
    'back',
    'edge'
]

FALLBACK_FORE: ColorType = '#000000' # black
FALLBACK_BACK: ColorType = '#FFFFFF' # white
FALLBACK_EDGE: ColorType = '#000000'

FALLBACK_SUB_FORE: ColorType = '#000000'
FALLBACK_SUB_BACK: ColorType = '#FFFFCB' # xkcd ivory

FALLBACK_GOOD_FORE: ColorType = '#000000'
FALLBACK_GOOD_BACK: ColorType = '#15B01A' # xkcd green
FALLBACK_OK_FORE: ColorType = '#000000'
FALLBACK_OK_BACK: ColorType = '#FFD700' # css4 gold
FALLBACK_BAD_FORE: ColorType = '#000000'
FALLBACK_BAD_BACK: ColorType = '#FC5A50' # xkcd coral
FALLBACK_DEAD_FORE: ColorType = '#FFFFFF'
FALLBACK_DEAD_BACK: ColorType = '#000000'

FALLBACK_THEME = {
    'fore': FALLBACK_FORE,
    'back': FALLBACK_BACK,
    'edge': FALLBACK_EDGE,
    'subject': {
        'fore': FALLBACK_SUB_FORE,
        'back': FALLBACK_SUB_BACK
    },
    'tags': {
        'good': {
            'fore': FALLBACK_GOOD_FORE,
            'back': FALLBACK_GOOD_BACK
        },
        'ok': {
            'fore': FALLBACK_OK_FORE,
            'back': FALLBACK_OK_BACK
        },
        'bad': {
            'fore': FALLBACK_BAD_FORE,
            'back': FALLBACK_BAD_BACK
        },
        'dead': {
            'fore': FALLBACK_DEAD_FORE,
            'back': FALLBACK_DEAD_BACK
        }
    }
}

config_data = {}
theme_name: str = ''
theme_path: str = './'
input_path: str = './'
output_dir: str = './'

theme: dict = {}
theme_data: dict = {}
theme_files: list[str] = []
input_dir: str = ''
input_list: list[str] = []
theme_data = FALLBACK_THEME
subjects: dict[str, list[str]] = {}
subject: list[str] = []
lines: dict[str, tuple[list[str], dict[str, list[str]]]] = {}
rowlabels = []
celltexts = []
length: int = 1
height = 1

def info(text: str) -> None:
    print(f"[Info] {text}")

def warning(text: str) -> None:
    print(f"[Warning] {text}")

def error(text: str) -> None:
    print(f"[Error] {text}")

def checkJSON(file: TextIOWrapper, filename: str) -> dict:
    ve: ValueError | None = None
    data = {}
    try:
        data = json.load(file)
    except ValueError as e:
        ve = e
    finally:
        if ve != None:
            error(f"File {filename} has invalid JSON, conversion aborted.\nPlease see the following message to identify the error:\n{ve}")
            quit()
        return data

def getFiles(path:str, suf:str) -> list[str]:
    dir, file = os.path.split(path)
    files: list[str] = []
    if dir != '':
        if not os.path.exists(dir):
            error(f"Path {dir} does not exist!")
            quit()
        if isfile(dir):
            error(f"{dir} is a file, not a directory!")
            quit()
    else:
        dir = './'

    for filename in os.listdir(dir):
        matched = re.match(rf"{file}\.{suf}$", filename)
        if matched != None:
            files.append(os.path.join(input_dir, matched.string))

    return files


def toCellColors(theme: dict) -> dict[str, ColorType]:
    colors: dict[str, ColorType] = {}
    for name in CELL_COLOR_KEYS:
        if theme.__contains__(name):
            colors[name] = theme[name]
    return colors

def updateCellColors(colors: dict[str, ColorType], newtheme: dict) -> dict[str, ColorType]:
    new_colors: dict[str, ColorType] = colors.copy()
    for name in CELL_COLOR_KEYS:
        if colors.__contains__(name) and newtheme.__contains__(name):
            new_colors[name] = newtheme[name]
    return new_colors

def getCellColor(row: int, col: int, color_tag: str) -> dict[str, ColorType]:
    cell_color = toCellColors(theme)

    if col == -1:
        cell_color = updateCellColors(cell_color, theme['subject'])
    if dict(theme['tags']).__contains__(color_tag):
        cell_color = updateCellColors(cell_color, theme['tags'][color_tag])

    return cell_color

def getCellTags(row: int, col: int) -> list[str]:
    rowkey = rowlabels[row]
    if col == -1:
        return lines[rowkey][0]
    colkey = celltexts[row][col]
    if colkey == '':
        return []
    return lines[rowkey][1][colkey]

#load config

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as config_json:
        config_data:dict = checkJSON(config_json, CONFIG_FILE)
        for item in CONFIG_ITEMS:
            if config_data.__contains__(item):
                globals()[item] = config_data[item]
else:
    warning(f"Configuration file {CONFIG_FILE} not found, using the default configuration...\n"
          + f"To use a custom configuration, put \"{CONFIG_FILE}\" in the same directory as this script."
    )

# get input file(s)

if input_path == '':
    input_path = input('\nEnter name/regex of the .csv file(s) without \".csv\": ')

input_list = getFiles(input_path, 'csv')

file_num = input_list.__len__()
if file_num < 1:
    error(f"No .csv file under {input_dir} matches {input_path}\\.csv$, no file to convert!")
    quit()
elif file_num > 256:
    warning(f"There are {file_num} files to convert, which might be too many.")
    choice = input("Continue? <[y]es|[N]o>: ")
    if not choice.lower() == 'y':
        info("Aborted conversion.\nYou may want to specify fewer files to convert.")
        quit()

# check output dir

if not os.path.exists(output_dir):
    error(f"Output directory {output_dir} does not exist!")
    quit()

# get theme

if theme_name != '':
    theme_files = getFiles(theme_path, 'json')
    for filename in theme_files:
        info(f"Reading the theme file {filename}...")
        with open(filename) as theme_json:
            theme_data = checkJSON(theme_json, os.path.join(theme_path, filename))
            if theme_data.__contains__(theme_name):
                theme = theme_data[theme_name]
                info(f"Using \"{theme_name}\" in {filename}...")
                break
    if theme == {}:
        theme = FALLBACK_THEME
        warning(f"Theme \"{theme_name}\" not found! Falling back to default theme...")
else:
    theme = FALLBACK_THEME
    info("No theme specified, using the default theme...")

# start converting

for filename in input_list:
    info(f"Reading {filename}...")
    with open(filename) as file:
        sc = csv.reader(file)
        for row in sc:
            if len(row) < 2:
                continue
            while(row.count('')):
                row.remove('')
            for i in range(len(row)):
                row[i] = row[i].strip()
            subjects[row[0]] = row[1:]

    if subjects.__len__() < 1:
        warning(f"{filename} has nothing to convert!")
        continue

    info(f"Converting {filename}...")

    for row in subjects:
        row_and_tag = str(row).split('#')
        row_name = row_and_tag[0]
        lines[row_name] = ([] if len(row_and_tag) < 2 else row_and_tag[1:], {})
        subject = subjects[row]
        for item_with_tag in subject:
            items = str(item_with_tag).split('#')
            lines[row_name][1][items[0]] = [] if len(items) < 2 else items[1:]

    for rowkey in lines:
        rowlabels.append(rowkey)
        line: dict = lines[rowkey][1]
        celltexts.append(list(line.keys()))

    for l in celltexts:
        if len(l) > length:
            length = len(l)
    for i in range(len(celltexts)):
        while len(celltexts[i]) < length:
            celltexts[i].append('')

    fig, ax = plt.subplots()

    fig.patch.set_visible(False)
    ax.axis('off')

    table = ax.table(
        celltexts,
        cellLoc = 'center',
        rowLabels = rowlabels,
        loc = 'center',
    )

    height = len(rowlabels)
    cells = table.get_celld()

    for row in range(height):
        for col in range(-1, length):
            tags = getCellTags(row, col) #TODO multiple tags
            tagtext = '' if tags.__len__() < 1 else tags[0]
            colors = getCellColor(row, col, tagtext)
            cells[(row, col)].get_text().set_color(colors['fore'])
            cells[(row, col)].set_color(colors['back'])
            cells[(row, col)].set_edgecolor(colors['edge'])

    fig.tight_layout()

    info(f"Saving {filename} into a picture...")
    plt.savefig(f"{os.path.join(output_dir, filename.removesuffix('.csv'))}.png", dpi=256)

info(f"Finished conversion, output to {output_dir}.")
