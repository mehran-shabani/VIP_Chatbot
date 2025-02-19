import re
import random
from collections import defaultdict

# Optional dependencies: sentence-transformers and language_tool_python
# Install them if you want semantic similarity and grammar checking features.
try:
    from sentence_transformers import SentenceTransformer, util
    _HAS_SBERT = True
except ImportError:
    _HAS_SBERT = False

try:
    import language_tool_python
    _HAS_LT = True
except ImportError:
    _HAS_LT = False

def apply_self_consistency(responses, user_query):
    """
    Select the best (most consistent) response from a list of responses 
    by combining frequency-based scoring and a custom quality check.

    1) Frequency Scoring:
       - If multiple models produce exactly the same response, that response
         is considered more reliable and gets a higher base score.

    2) Quality Scoring:
       - For each response, measure multiple criteria via 'measure_response_quality'.
    
    Finally, pick the response with the highest overall score.
    
    :param responses: A list of raw response strings from different models.
    :param user_query: The user's original query for reference (used in semantic similarity).
    :return: The single best response string.
    """
    if not responses:
        return ""
    if len(responses) == 1:
        return responses[0]

    # Count frequency of each response
    freq_map = defaultdict(int)
    for resp in responses:
        freq_map[resp] += 1

    # Calculate final score for each response
    score_map = {}
    for resp in responses:
        # Base score from frequency
        base_score = freq_map[resp] * 10

        # Quality score from various metrics
        quality_score = measure_response_quality(resp, user_query)

        final_score = base_score + quality_score
        score_map[resp] = final_score

    # Select the response with the highest overall score
    best_response = max(score_map, key=score_map.get)
    return best_response

def measure_response_quality(response, user_query):
    """
    Compute a quality score for a single response by combining:
      - Response length
      - Number of code blocks
      - Keyword matches
      - Semantic similarity to the user's query (optional)
      - Grammar check (optional)
      - Language model scoring (dummy random function by default)
    
    :param response: The raw text of the response.
    :param user_query: The user's query for semantic similarity calculation.
    :return: A floating-point score representing the quality of the response.
    """
    total_score = 0.0

    # 1) Length of the response (longer might be more thorough)
    total_score += len(response) * 0.01

    # 2) Code blocks (identified by triple backticks)
    code_block_count = len(re.findall(r'```', response))
    total_score += code_block_count * 5.0

    # 3) Keyword matches (e.g. "django", "flutter", "api", etc.)
    total_score += count_keyword_score(response)

    # 4) Semantic similarity (if sentence-transformers is installed)
    total_score += measure_semantic_similarity(response, user_query, weight=1.0)

    # 5) Grammar check (if language_tool_python is installed)
    total_score += measure_grammar_quality(response, weight=1.0)

    # 6) Language model or random scoring (demo)
    total_score += measure_lm_score(response, weight=1.0)

    return total_score

def count_keyword_score(text):
    """
    Assign a small bonus for each occurrence of specific keywords.
    This can be easily extended to suit your project's needs.
    """
    keywords = ["django", "flutter", "api", "model", "python", "dart", "database"]
    score = 0.0
    text_lower = text.lower()
    for kw in keywords:
        occurrences = len(re.findall(r'\b' + re.escape(kw.lower()) + r'\b', text_lower))
        score += occurrences * 2.0
    return score

def measure_semantic_similarity(response, user_query, weight=1.0):
    """
    Calculate semantic similarity between response and user_query using 
    Sentence Transformers (if installed). The similarity is scaled from 0 to 10.
    
    :param response: The response text to evaluate.
    :param user_query: The user's original query.
    :param weight: A multiplier to adjust the importance of this metric.
    :return: A score (0 to 10) * weight, or 0 if SBERT is not available.
    """
    if not _HAS_SBERT:
        return 0.0

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    emb_resp = model.encode(response, convert_to_tensor=True)
    emb_query = model.encode(user_query, convert_to_tensor=True)
    similarity = float(util.pytorch_cos_sim(emb_resp, emb_query))

    # Scale 0..1 to 0..10
    return similarity * 10.0 * weight

def measure_grammar_quality(text, weight=1.0):
    """
    Evaluate grammar quality using language_tool_python (if installed).
    Fewer errors yield a higher score. The score is scaled between 0 and 10.
    
    :param text: The text to check.
    :param weight: A multiplier for this metric.
    :return: A grammar-based score (0..10) * weight, or 0 if the library is unavailable.
    """
    if not _HAS_LT:
        return 0.0

    tool = language_tool_python.LanguageTool('en-US')  # Adjust for other languages if needed
    matches = tool.check(text)
    errors_count = len(matches)

    # Example scoring: 10 - (errors_count / 5)
    raw_score = 10.0 - (errors_count / 5.0)
    if raw_score < 0:
        raw_score = 0

    return raw_score * weight

def measure_lm_score(response, weight=1.0):
    """
    Placeholder for a language model scoring mechanism.
    Currently returns a random value (5..10) to simulate a model-based score.
    
    :param response: The response text
    :param weight: Weight for this metric
    :return: A random score * weight
    """
    return random.uniform(5.0, 10.0) * weight
