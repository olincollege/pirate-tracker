import re


def extract_top_contextual_phrases(file_path):
    # define core keywords by category
    keywords = {
        "hostage": [
            "tied",
            "hostage",
            "injured",
            "escaped",
            "locked",
            "crew",
            "abducted",
            "assaulted",
        ],
        "theft": ["stolen", "missing", "robbed", "took", "taken", "removed"],
        "spare_parts": ["spare", "parts", "engine", "equipment"],
    }

    # context words
    context_words = [
        "not",
        "no",
        "nothing",
        "were",
        "was",
        "reported",
        "appeared",
        "accounted",
    ]

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # split incidents
    incident_blocks = re.findall(
        r"\d+\.\s+(.*?)(?=\n\d+\.|\Z)", text, re.DOTALL
    )
    incident_blocks = [
        re.sub(r"[^\w\s]", "", block.lower()) for block in incident_blocks
    ]

    N = 5
    relevant_phrases = {}

    all_keywords = set(sum(keywords.values(), [])) | set(context_words)

    for block in incident_blocks:
        words = block.split()
        ngrams = zip(*[words[i:] for i in range(N)])

        for gram in ngrams:
            gram_set = set(gram)
            if gram_set & all_keywords:
                if any(
                    k in gram
                    for k in keywords["theft"]
                    + keywords["spare_parts"]
                    + keywords["hostage"]
                ):
                    gram_str = " ".join(gram)
                    if gram_str not in relevant_phrases:
                        relevant_phrases[gram_str] = 1
                    else:
                        relevant_phrases[gram_str] += 1

    # sorting by frequency (descending)
    sorted_phrases = list(relevant_phrases.items())
    for i in range(len(sorted_phrases)):
        for j in range(i + 1, len(sorted_phrases)):
            if sorted_phrases[j][1] > sorted_phrases[i][1]:
                sorted_phrases[i], sorted_phrases[j] = (
                    sorted_phrases[j],
                    sorted_phrases[i],
                )

    # top 20 phrases
    print("\nTop 20 contextual phrases:")
    for phrase, count in sorted_phrases[:20]:
        print(f'"{phrase}": {count}')
