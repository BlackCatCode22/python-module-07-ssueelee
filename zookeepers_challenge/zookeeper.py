import datetime

# helper functions

def gen_birth_date(age, season=None):
    """Generate birth date in ISO format based on age and optional birth season."""
    today = datetime.date(2024, 3, 26)  # Fixed arrival date
    birth_year = today.year - age

    season_dates = {
        "spring": (3, 21),
        "summer": (6, 21),
        "fall":   (9, 21),
        "winter": (12, 21)
    }

    if season:
        month, day = season_dates.get(season.lower(), (today.month, today.day))
    else:
        month, day = today.month, today.day

    return datetime.date(birth_year, month, day).isoformat()


def gen_unique_id(species, counter_dict):
    """Generate a unique ID for each species based on a counter dictionary."""
    prefix = species[:2].capitalize()
    counter_dict[species] = counter_dict.get(species, 0) + 1
    return f"{prefix}{counter_dict[species]:02}"


def parse_animal_line(line):
    """Parse one line of arrivingAnimals.txt and return structured data."""
    name_part, rest = line.strip().split(" - ", 1)
    parts = rest.split(', ')
    main_info = parts[0].split()  # e.g., "4 year old female hyena"

    age = int(main_info[0])
    sex = main_info[3]
    species = main_info[4]

    season = None
    if "born in" in parts[1]:
        season = parts[1].split()[2]

    color = parts[2].replace(" color", "")
    weight = int(parts[3].split()[0])
    origin = parts[4].replace("from ", "")

    return {
        "name": name_part.strip(),
        "age": age,
        "sex": sex,
        "species": species,
        "season": season,
        "color": color,
        "weight": weight,
        "origin": origin
    }

# main program

def main():
    habitats = {}
    id_counter = {}

    try:
        with open("arrivingAnimals.txt") as animal_file:
            for line in animal_file:
                data = parse_animal_line(line)

                unique_id = gen_unique_id(data["species"], id_counter)
                birth_date = gen_birth_date(data["age"], data["season"])
                arrival_date = "2024-03-26"

                animal = {
                    "id": unique_id,
                    "name": data["name"],
                    "birth_date": birth_date,
                    "color": data["color"],
                    "sex": data["sex"],
                    "weight": data["weight"],
                    "origin": data["origin"],
                    "arrival_date": arrival_date
                }

                species = data["species"]
                if species not in habitats:
                    habitats[species] = []
                habitats[species].append(animal)

        with open("zooPopulation.txt", "w") as report_file:
            for species, animals in habitats.items():
                report_file.write(f"{species.capitalize()} Habitat:\n\n")
                for animal in animals:
                    line = (
                        f"{animal['id']}; {animal['name']}; birth date: {animal['birth_date']}; "
                        f"{animal['color']} color; {animal['sex']}; {animal['weight']} pounds; "
                        f"from {animal['origin']}; arrived {animal['arrival_date']}\n"
                    )
                    report_file.write(line)
                report_file.write("\n")

        print("✅ zooPopulation.txt has been created successfully.")

    except FileNotFoundError as e:
        print(f"❌ File not found: {e.filename}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

# point of entry

if __name__ == "__main__":
    main()
