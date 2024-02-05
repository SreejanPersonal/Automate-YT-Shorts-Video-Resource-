import requests
from typing import List
from termcolor import colored

def search_for_stock_videos(tags: list, api_key: str) -> List[str]:
    """
    Searches for stock videos based on a query.

    """
    
    # Build headers
    headers = {
        "Authorization": api_key
    }

    links = []

    for tag in tags:

        # Build URL
        url = f"https://api.pexels.com/videos/search?query={tag}&per_page=1"

        # Send the request
        r = requests.get(url, headers=headers)

        # Parse the response
        response = r.json()

        # Get first video url
        video_urls = []
        video_url = ""
        try:
            video_urls = response["videos"][0]["video_files"]
            # print(video_urls)
        except:
            print(colored("[-] No Videos found.", "red"))
            print(colored(response, "red"))

        # Loop through video urls
        for video in video_urls:
            # Check if video has a download link
            if ".com/external" in video["link"]:
                # Set video url
                video_url = video["link"]
                # print(f"{video_url} | {video['quality']} | {video['width']}/{video['height']}")

        # Let user know
        print(colored(f"\t=> {video_url}", "cyan"))

        # Return the video url
        links.append(video_url)

    return links

if __name__ == "__main__":

    tags = ["how to make money online videos", "online money-making tutorials", "earning money online videos", "making money online tips", "online income strategies", "ways to make money online videos", "online money-making techniques", "earning money from home videos", "online business ideas for making money", "passive income online videos"]

    links = search_for_stock_videos(tags)
    print(links)

