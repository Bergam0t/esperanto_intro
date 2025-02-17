import xml.etree.ElementTree as ET

SUFFIXES = {
    "Adjective": "a",
    "Noun": "o",
    "Noun (Accusitive)": "on",
    "Noun (Plural)": "oj",
    "Noun (Plural Accusitive)": "ojn",
    "Verb (Infinitive)": "i",
    "Verb (Present Tense)": "as",
    "Verb (Past Tense)": "is",
    "Verb (Future Tense)": "os",
}

def generate_options(word, target_form="adjective", provided_root=False,
                     options=["Adjective", "Noun", "Verb (Present Tense)"]):
    
    if not provided_root:
        root = word[:-1]
    else:
        root = word

    if target_form == "Adjective":
        correct = f"{root}{SUFFIXES['Adjective']}"
    elif target_form == "Noun":
        correct = f"{root}{SUFFIXES['Noun']}"
    # elif target_form == "Noun (Accusitive)":
    #     correct = f"{root}{SUFFIXES["Noun (Accusitive)"]}"
    # elif target_form == "Noun (Plural)":
    #     correct = f"{root}{SUFFIXES["Noun (Plural)"]}"
    # elif target_form == "Noun (Plural Accusitive)":
    #     correct = f"{root}{SUFFIXES["Noun (Plural Accusitive)"]}"
    # elif target_form == "Verb (Infinitive)":
    #     correct = f"{root}{SUFFIXES["Verb (Infinitive)"]}"
    # elif target_form == "Verb (Present Tense)":
    #     correct = f"{root}{SUFFIXES["Verb (Present Tense)"]}"
    # elif target_form == "Verb (Past Tense)":
    #     correct = f"{root}{SUFFIXES["Verb (Past Tense)"]}"
    # elif target_form == "Verb (Future Tense)":
    #     correct = f"{root}{SUFFIXES["Verb (Future Tense)"]}"

    bait_suffixes = {key: SUFFIXES[key] for key in SUFFIXES if key in options}
    bait = [f"{root}{bait_suffixes[i]}" for i in len(bait_suffixes)]

    return ([correct], bait)

def save_svg_with_declaration(tree, file_path):
    # Add XML declaration manually
    with open(file_path, 'wb') as f:
        f.write(b'<?xml version="1.0" encoding="UTF-8"?>\n')
        tree.write(f)

def change_svg_color(svg_file,  new_color, output_file="image.svg", string=True):
    # Parse the SVG file
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # Find all elements that might have a 'fill' or 'stroke' attribute
    for elem in root.iter():
        # Change the 'fill' attribute if it exists
        if 'fill' in elem.attrib:
            elem.attrib['fill'] = new_color
        # Change the 'stroke' attribute if it exists
        if 'stroke' in elem.attrib:
            elem.attrib['stroke'] = new_color

    
    # Save the modified SVG
    if not string:
        save_svg_with_declaration(tree, output_file)
    else:
        return ET.tostring(root, encoding='unicode')
