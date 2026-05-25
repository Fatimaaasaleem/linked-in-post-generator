import json
from llm_helper import llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


def clean_text(text):
    """
    Removes broken unicode/surrogate characters safely.
    """
    if not isinstance(text, str):
        return ""

    try:
        # Remove surrogates and invalid UTF-8, keep valid Unicode
        cleaned = text.encode("utf-8", "ignore").decode("utf-8", "ignore").strip()
        return cleaned
    except Exception as e:
        print(f"Error cleaning text: {e}")
        return ""


def clean_dict(obj):
    """
    Recursively clean all string values in a dictionary.
    """
    if isinstance(obj, dict):
        return {key: clean_dict(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [clean_dict(item) for item in obj]
    elif isinstance(obj, str):
        return clean_text(obj)
    else:
        return obj


def process_posts(raw_file_path, processed_file_path=None):

    try:
        with open(raw_file_path, "r", encoding="utf-8", errors="replace") as file:
            content = file.read()
        posts = json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading JSON file: {e}")
        posts = []

    enriched_posts = []

    for post in posts:

        # Clean post text before sending to LLM
        cleaned_post_text = clean_text(post.get("text", ""))

        try:
            metadata = extract_metadata(cleaned_post_text)

            # Clean the entire post object before adding metadata
            cleaned_post = clean_dict(post)
            post_with_metadata = cleaned_post | metadata

            enriched_posts.append(post_with_metadata)

        except Exception as e:
            print(f"Error processing post: {e}")

    unified_tags = get_unified_tags(enriched_posts)

    for post in enriched_posts:

        current_tags = post.get("tags", [])

        new_tags = {
            unified_tags.get(tag, tag)
            for tag in current_tags
        }

        post["tags"] = list(new_tags)

    # Clean all posts one more time before saving
    enriched_posts = clean_dict(enriched_posts)

    with open(processed_file_path, "w", encoding="utf-8") as outfile:
        json.dump(
            enriched_posts,
            outfile,
            indent=4,
            ensure_ascii=False
        )


def extract_metadata(post):
    
    # Clean the post before sending
    post = clean_text(post)
    if not post:
        return {
            "line_count": 0,
            "language": "Unknown",
            "tags": []
        }

    template = '''
    You are given a LinkedIn post.

    You need to extract:
    1. Number of lines
    2. Language of the post
    3. Tags

    Rules:
    1. Return ONLY valid JSON.
    2. JSON should contain exactly:
       - line_count
       - language
       - tags
    3. tags should contain maximum 2 tags.
    4. Language should be either:
       - English
       - Hinglish

    Post:
    {post}
    '''

    pt = PromptTemplate.from_template(template)

    chain = pt | llm

    try:
        response = chain.invoke({"post": post})

        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)

    except OutputParserException:
        print("Failed parsing metadata response.")
        res = {
            "line_count": 0,
            "language": "Unknown",
            "tags": []
        }
    except Exception as e:
        print(f"Error in extract_metadata: {e}")
        res = {
            "line_count": 0,
            "language": "Unknown",
            "tags": []
        }

    return res


def get_unified_tags(posts_with_metadata):

    unique_tags = set()

    for post in posts_with_metadata:
        unique_tags.update(post.get("tags", []))

    if not unique_tags:
        return {}

    unique_tags_list = ",".join(unique_tags)

    template = '''
    I will give you a list of tags.

    You need to unify tags.

    Rules:
    1. Similar tags should merge together.
    2. Use title case.
    3. Return ONLY valid JSON.
    4. Output format:
       {
         "Old Tag": "Unified Tag"
       }

    Tags:
    {tags}
    '''

    pt = PromptTemplate.from_template(template)

    chain = pt | llm

    try:
        response = chain.invoke({
            "tags": unique_tags_list
        })

        json_parser = JsonOutputParser()
        res = json_parser.parse(response.content)

    except OutputParserException:
        print("Failed parsing unified tags.")
        res = {}
    except Exception as e:
        print(f"Error in get_unified_tags: {e}")
        res = {}

    return res


if __name__ == "__main__":

    process_posts(
        "data/raw_posts.json",
        "data/processed_posts.json"
    )