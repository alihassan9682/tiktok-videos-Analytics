from userPosts import getTiktokUserPosts
import asyncio
import csv
import os

USERS = [
    ".xxenni",
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

usersNOTfound = []


def write_to_csv(data,directory ,filename):
    # Specify the fieldnames for the CSV
    fieldnames = list(data[0].keys())

    if not os.path.exists(directory):
        os.makedirs(directory)

    # Construct the full file path
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write each row of data
        for item in data:
            writer.writerow(item)


async def fetch_posts(user):
    try:
        url = f"https://www.tiktok.com/@{user}"
        print(url)
        data = await getTiktokUserPosts(url)
        write_to_csv(data, 'userCSVs', f"{user}.csv")
    except:
        print('not found : ',user)
        usersNOTfound.append(user)


async def main():
    tasks = [fetch_posts(user) for user in USERS]
    await asyncio.gather(*tasks)


# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
    print(usersNOTfound)
