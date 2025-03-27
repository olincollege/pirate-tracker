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

# Display results
for phrase, count in phrase_counts.items():
    print(f'"{phrase}": {count}')
