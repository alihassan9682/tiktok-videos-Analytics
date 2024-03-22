import pandas as pd


names = [
    "xxenni",
    "7ikayatzamanlxqivfa",
    "_tarmo",
    "abbadoonvalpyro",
    "ai.dreamcontent",
    "ai4klivewallpapers",
    "ai_harmonies",
    "aidiffuser",
    "aigeschichte",
    "airem1x",
    "aleksandeer821",
    "ascane.09",
    "azlinda.alin",
    "beautyinbits",
    "blueblood_5",
    "bluefan20002023",
    "cars.bikes.ai",
    "cartoonscovers",
    "casos.basados",
    "celestial.muse",
    "celestialair_oficial",
    "charlyb_83",
    "chescosol",
    "corridones.ia",
    "cowieowie_",
    "crishxextrem",
    "croyances.superst",
    "cxaxrxexe",
    "cyberland.ai",
    "dautay.net",
    "davidross988",
    "diablesseguerriere",
    "digitart2050",
    "distopyanworld.ia",
    "drew_learning_ai",
    "duchessart",
    "el_moko_ke_kamina",
    "ellionz",
    "elpanaraul.2.0",
    "evilcorp.zima",
    "expandai",
    "f1covers",
    "fakeunivers1",
    "gbdowntown",
    "gpt_coderman",
    "gsm.ai",
    "gthvil",
    "halfblood.princesss",
    "iamso.hot",
    "idynkt",
    "ildeepfaker",
    "ilforonelmondo2",
    "ilyxoxohim",
    "imagine.if.ai1",
    "jane_morelli",
    "jorchhoffman",
    "killingdnyx",
    "kloverremix",
    "laliboall",
    "litficcreative",
    "luna_virtua",
    "makktu.b",
    "malfoy.mariamalfoy",
    "mangaain",
    "mb.art.nook",
    "mcantonio87",
    "miamizusan",
    "multandolphin",
    "nirasmiley",
    "otageekk",
    "outer_worlds.ai",
    "pahlawansuperai",
    "palimpalim228",
    "panorama.ia",
    "peetfrfr",
    "pinky.spider27",
    "pixelgenius8",
    "planet.ai",
    "rebirthai",
    "robin_lochmann",
    "ryan_.williams1",
    "sane.art",
    "scraggydog1",
    "sevsevseverus",
    "slava081984",
    "spdrgrleve",
    "summergram",
    "talesoftime1337",
    "techaivisions",
    "tenthousandscrolls",
    "theaibeatles",
    "thejasonpower_",
    "tomokoworks",
    "tonkenken.ai",
    "transeunte_prompts",
    "twanmillion",
    "vikthor_stone",
    "wanderingweb",
    "wiwispiderm4noc",
    "worldofwondev",
    "xcwenty",
    "xxheichouxx",
    "zo6262",
]


page = [
    "xxenni",
    "7ikayatzamanlxqivfa",
    "_tarmo",
    "abbadoonvalpyro",
    "ai.dreamcontent",
    "ai4klivewallpapers",
    "ai_harmonies",
    "aidiffuser",
    "aigeschichte",
    "airem1x",
    "aleksandeer821",
    "ascane.09",
    "azlinda.alin",
    "beautyinbits",
    "blueblood_5",
    "bluefan20002023",
    "cars.bikes.ai",
    "cartoonscovers",
    "casos.basados",
    "celestial.muse",
    "charlyb_83",
    "chescosol",
    "corridones.ia",
    "cowieowie_",
    "crishxextrem",
    "croyances.superst",
    "cxaxrxexe",
    "cyberland.ai",
    "dautay.net",
    "davidross988",
    "digitart2050",
    "distopyanworld.ia",
    "drew_learning_ai",
    "duchessart",
    "el_moko_ke_kamina",
    "ellionz",
    "evilcorp.zima",
    "expandai",
    "f1covers",
    "fakeunivers1",
    "gbdowntown",
    "gpt_coderman",
    "gsm.ai",
    "gthvil",
    "halfblood.princesss",
    "iamso.hot",
    "idynkt",
    "ildeepfaker",
    "ilforonelmondo2",
    "ilyxoxohim",
    "imagine.if.ai1",
    "jane_morelli",
    "killingdnyx",
    "kloverremix",
    "laliboall",
    "litficcreative",
    "luna_virtua",
    "malfoy.mariamalfoy",
    "mangaain",
    "mb.art.nook",
    "mcantonio87",
    "miamizusan",
    "multandolphin",
    "nirasmiley",
    "otageekk",
    "outer_worlds.ai",
    "pahlawansuperai",
    "palimpalim228",
    "panorama.ia",
    "peetfrfr",
    "pinky.spider27",
    "pixelgenius8",
    "planet.ai",
    "rebirthai",
    "robin_lochmann",
    "ryan_.williams1",
    "sane.art",
    "scraggydog1",
    "sevsevseverus",
    "slava081984",
    "spdrgrleve",
    "summergram",
    "talesoftime1337",
    "techaivisions",
    "tenthousandscrolls",
    "theaibeatles",
    "thejasonpower_",
    "tomokoworks",
    "tonkenken.ai",
    "transeunte_prompts",
    "twanmillion",
    "vikthor_stone",
    "wanderingweb",
    "wiwispiderm4noc",
    "worldofwondev",
    "xcwenty",
    "xxheichouxx",
    "zo6262",
]

def compare_lists(list1, list2):
    # Convert lists to sets for efficient comparison
    set1 = set(list1)
    set2 = set(list2)

    # Find elements that exist in list1 but not in list2
    difference = set1 - set2

    # Convert the difference set back to a list
    difference_list = list(difference)

    return difference_list


def read_excel_column(excel_path, column_number):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_path)
    except pd.errors.ParserError:
        # Handle parsing error
        print("Error parsing Excel file. Please check the file format.")
        return None

    # Get the values of the specified column
    column_values = df.iloc[:, column_number].tolist()

    return column_values


# Example usage:
excel_path = "E:\\TikTok Scrapping\\auth.xlsx"  # Path to the Excel file
column_number = 1  # Second column (0-indexed)

# column_data = read_excel_column(excel_path, page)


# Example usage:
list1 = [1, 2, 3, 4, 5]
list2 = [4, 5, 6, 7, 8]

result = compare_lists(names, page)
print("Elements in list1 but not in list2:", result)
