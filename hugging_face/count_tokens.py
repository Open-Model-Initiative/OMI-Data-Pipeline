from transformers import LlamaTokenizer

# Tokenizer configuration
TOKENIZER_NAME = "hf-internal-testing/llama-tokenizer"

# Initialize the tokenizer
tokenizer = LlamaTokenizer.from_pretrained(TOKENIZER_NAME)


def count_tokens(text):
    """
    Count the number of tokens in the given text using the LlamaTokenizer.

    Args:
    text (str): The input text to tokenize and count.

    Returns:
    int: The number of tokens in the input text.
    """
    if not text:
        return 0
    return len(tokenizer.encode(text))
