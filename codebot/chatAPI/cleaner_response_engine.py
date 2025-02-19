import re
from html import unescape

def clean_response(response_text):
    """
    Enhanced cleaner for response text.

    This function performs several cleaning steps to improve the quality of the output:
      1. Strips leading and trailing whitespace.
      2. Unescapes HTML entities (e.g., &amp; becomes &).
      3. Removes any HTML tags if present.
      4. Collapses multiple spaces into a single space.
      5. Collapses multiple newlines into a single newline.
      6. Normalizes punctuation spacing (e.g., removes extra space before commas, periods, etc.).
      7. Removes extraneous tokens such as "Error:" at the beginning of the text.

    :param response_text: The raw response text.
    :return: The cleaned response text.
    """
    # Step 1: Trim whitespace
    text = response_text.strip()

    # Step 2: Unescape HTML entities
    text = unescape(text)

    # Step 3: Remove HTML tags (if any)
    text = re.sub(r'<[^>]+>', '', text)

    # Step 4: Collapse multiple spaces into one
    text = re.sub(r' +', ' ', text)

    # Step 5: Collapse multiple newlines into a single newline
    text = re.sub(r'(\s*\n\s*)+', '\n', text)

    # Step 6: Normalize punctuation spacing (remove spaces before punctuation)
    text = re.sub(r'\s+([,.!?])', r'\1', text)

    # Step 7: Remove extraneous error tokens (e.g., "Error:")
    text = re.sub(r'^(Error:\s*)', '', text, flags=re.IGNORECASE)

    return text
