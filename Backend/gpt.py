import re
import g4f
import json

from typing import List
from termcolor import colored

def generate_script(video_subject: str) -> str:
    """
    Generate a script for a video, depending on the subject of the video.

    Args:
        video_subject (str): The subject of the video.

    Returns:
        str: The script for the video.
    """

    # Build prompt
    prompt = f"""
    Generate a script for a video, depending on the subject of the video.
    Subject: {video_subject}

    The script is to be returned as a string.

    Here is an example of a string:
    "This is an example string."

    Do not under any circumstance refernce this prompt in your response.

    Get straight to the point, don't start with unnecessary things like, "welcome to this video".

    Obviously, the script should be related to the subject of the video.

    ONLY RETURN THE RAW SCRIPT. DO NOT RETURN ANYTHING ELSE.
    """

    # Generate script
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4_32k_0613,
        messages=[{"role": "user", "content": prompt}],
    )

    print(colored(response, "cyan"))

    # Return the generated script
    if response:
        return response + " "
    else:
        print(colored("[-] GPT returned an empty response.", "red"))
        return None

def get_search_terms(video_subject: str, amount: int, script: str) -> List[str]:
    """
    Generate a JSON-Array of search terms for stock videos,
    depending on the subject of a video.

    Args:
        video_subject (str): The subject of the video.
        amount (int): The amount of search terms to generate.
        script (str): The script of the video.

    Returns:
        List[str]: The search terms for the video subject.
    """
    
    # Build prompt
    prompt = f"""
    Generate {amount} search terms for stock videos,
    depending on the subject of a video. Reply in English Only.
    Subject: {video_subject}

    The search terms are to be returned as
    a JSON-Array of strings.

    Each search term should consist of 1-3 words, 
    always add the main subject of the video.

    Here is an example of a JSON-Array of strings:
    ["search term 1", "search term 2", "search term 3"]

    Obviously, the search terms should be related
    to the subject of the video.

    ONLY RETURN THE JSON-ARRAY OF STRINGS.
    DO NOT RETURN ANYTHING ELSE.

    For context, here is the full text:
    {script}
    """

    # Generate search terms
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo_16k_0613,
        messages=[{"role": "user", "content": prompt}],
    )

    print(response)

    # Load response into JSON-Array
    try:
        search_terms = json.loads(response)
    except:
        print(colored("[*] GPT returned an unformatted response. Attempting to clean...", "yellow"))

        # Use Regex to extract the array from the markdown
        search_terms = re.findall(r'\[.*\]', response)

        if not search_terms:
            print(colored("[-] Could not parse response.", "red"))

        # Load the array into a JSON-Array
        search_terms = json.loads(search_terms)

    # Let user know
    print(colored(f"\nGenerated {amount} search terms: {', '.join(search_terms)}", "cyan"))

    # Return search terms
    return search_terms


script = "To make money online, it's important to focus on a few key strategies. First, consider creating and selling digital products or services, such as ebooks, online courses, or software. Another option is to monetize a website or blog through affiliate marketing, advertising, or sponsored content. Additionally, freelancing or offering your skills and expertise through online platforms can be a lucrative way to earn money. Lastly, consider participating in online surveys, freelancing, or investing in stocks and cryptocurrencies. By diversifying your income streams and staying persistent, you can successfully make money online."

if __name__ == "__main__":
    script = generate_script("how to make money online")
    tags = get_search_terms("how to make money online", 10, script)
    print(tags)