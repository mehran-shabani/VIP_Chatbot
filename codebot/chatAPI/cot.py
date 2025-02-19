import re

def apply_cot(response_text):
    """
    Enhance the Chain-of-Thought (CoT) formatting for a given response.
    
    This function:
      - Trims the input text.
      - Removes any existing "Chain of Thought:" header.
      - Splits the text into logical steps using newlines. 
        If only one line is found, it attempts to split by period.
      - Filters out empty steps.
      - Returns the final output with a header and numbered steps.
    
    :param response_text: The raw response text from the model.
    :return: A formatted string with the chain-of-thought steps.
    """
    header = "Chain of Thought:"
    text = response_text.strip()
    
    # Remove any existing header to avoid duplication
    if text.startswith(header):
        text = text[len(header):].strip()
    
    # Try splitting by newlines first
    lines = text.splitlines()
    if len(lines) <= 1:
        # If only one line is found, try splitting by period followed by a space.
        lines = re.split(r'\.\s+', text)
    
    # Remove empty entries and strip whitespace from each step
    steps = [line.strip() for line in lines if line.strip()]
    
    # If no clear steps are found, return the original text under the header.
    if not steps:
        return f"{header}\n{text}"
    
    # Number each step and join them
    enumerated_steps = [f"{i+1}. {step}" for i, step in enumerate(steps)]
    return f"{header}\n" + "\n".join(enumerated_steps)
