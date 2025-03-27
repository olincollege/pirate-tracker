import re

# Load and read your description file
with open("incident_descriptions.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split incidents based on numbering like '1.', '2.', etc.
incident_blocks = re.findall(r"\d+\.\s+(.*?)(?=\n\d+\.|\Z)", text, re.DOTALL)

# Normalize to lowercase for case-insensitive matching
incident_blocks = [block.lower() for block in incident_blocks]

# Phrases to search for
phrases = [
    "not injured",
    "nothing was stolen",
    "were accounted for",
    "no further assistance was required",
    "no property stolen",
    "no injuries were reported",
    "parts were stolen",
    "nothing was reported stolen",
    "were reported stolen",
    "no property was stolen",
    "was safe"
]

# Count matches
phrase_counts = {phrase: 0 for phrase in phrases}

for desc in incident_blocks:
    for phrase in phrases:
        if phrase in desc:
            phrase_counts[phrase] += 1

# Sort by count (descending) and display
# Turn the dictionary into a list of tuples
items = list(phrase_counts.items())

# Manual sorting using a simple selection sort
for i in range(len(items)):
    for j in range(i + 1, len(items)):
        if items[j][1] > items[i][1]:
            items[i], items[j] = items[j], items[i]  # Swap

# Now 'items' is sorted by count (descending)
for phrase, count in items:
    print(f'"{phrase}": {count}')
