def evaluate_response(responses):
    """
    Evaluate and select the best response from a list using multiple heuristics.
    
    For each response, this function calculates a score based on:
      - The number of steps in the chain-of-thought (more steps may indicate detailed reasoning).
      - The average length of each step (longer steps may reflect more thorough explanations).
      - A bonus for having a clearly formatted chain-of-thought.
    
    The response with the highest overall score is returned.
    
    :param responses: A list of response strings (preferably already processed by apply_cot).
    :return: The single best response as a string.
    """
    best_score = -1
    best_response = ""
    
    for resp in responses:
        # Assume that the response is structured with a header and numbered steps
        if not resp:
            continue

        # Split the response into lines and filter out the header if present
        lines = resp.splitlines()
        if lines and lines[0].strip().lower() == "chain of thought:":
            steps = [line for line in lines[1:] if line.strip()]
        else:
            steps = [line for line in lines if line.strip()]

        num_steps = len(steps)
        
        # Calculate average step length
        avg_length = sum(len(step) for step in steps) / num_steps if num_steps > 0 else 0
        
        # Heuristic scoring: each step contributes 1.5 points; average length contributes 0.01 points per character.
        score = num_steps * 1.5 + avg_length * 0.01
        
        # Optionally, add a bonus if the response clearly follows the chain-of-thought format.
        if resp.startswith("Chain of Thought:"):
            score += 2.0

        if score > best_score:
            best_score = score
            best_response = resp

    return best_response
