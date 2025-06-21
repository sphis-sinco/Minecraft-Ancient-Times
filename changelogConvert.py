import re

# Map markdown section headers to GameBanana types
type_map = {
    "Added": "Addition",
    "Fixed": "Bugfix",
    "Changed": "Adjustment",
    "Removed": "Removal",
    "Security": "",
    "Deprecated": "Overhaul"
}

def convert_changelog(text):
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    # Find all version entries
    version_blocks = re.findall(r'## \[(.*?)\] - (.*?)\n(.*?)(?=^## |\Z)', text, re.DOTALL | re.MULTILINE)

    output = []

    for version, date, block in version_blocks:
        # Find all sections (### Title)
        section_blocks = re.findall(r'### (.*?)\n(.*?)(?=^### |\Z)', block, re.DOTALL | re.MULTILINE)

        for section, items in section_blocks:
            gb_type = type_map.get(section.strip(), section.strip())
            for line in items.strip().splitlines():
                line = line.strip()
                if line.startswith("- "):
                    entry = line[2:].strip()
                    output.append(f"{entry}, {gb_type}")

    return "\n".join(output)

if __name__ == "__main__":
    # Load the changelog file
    with open("CHANGELOG_ENTRY.txt", "r", encoding="utf-8") as f:
        changelog_text = f.read()

    # Convert
    converted_text = convert_changelog(changelog_text)

    # Save result
    with open("gamebanana_changelog.txt", "w", encoding="utf-8") as f:
        f.write(converted_text)

    print("Converted GameBanana-style changelog saved to 'gamebanana_changelog.txt'")
    print("\nPreview:\n")
    print(converted_text)
