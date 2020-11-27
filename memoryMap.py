import json

# Loading json file (directories) in the dictionary
directories_structure = open("data.json")
directories_structure = json.load(directories_structure)

# Updating directory structure to print a tree structure
tree_structure = json.dumps(directories_structure, indent=4)
tree_structure = tree_structure.replace("\n    ", "\n")
tree_structure = tree_structure.replace('"', "")
tree_structure = tree_structure.replace(',', "")
tree_structure = tree_structure.replace("{", "")
tree_structure = tree_structure.replace("}", "")
tree_structure = tree_structure.replace("    ", " | ")
tree_structure = tree_structure.replace("  ", " ")

print("\n------------------>>> MEMORY MAP <<<------------------")
print(tree_structure)