import os

import gpt
import search
import video

from dotenv import load_dotenv
from moviepy.config import change_settings

load_dotenv(r"C:\Users\sreej\OneDrive\Desktop\PROJECTS\YT SERIES PRACTICE\EXTRAORDINARY\AUTOMATION\YOUTUBE SHORTS\MoneyPrinter\.env") 

change_settings({"IMAGEMAGICK_BINARY": os.getenv("IMAGEMAGICK_BINARY")})

ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
IMAGEMAGICK_BINARY = os.getenv("IMAGEMAGICK_BINARY")

topic = "how to make money online"

script = gpt.generate_script(topic)
tags = gpt.get_search_terms(topic, 10, script)

links = search.search_for_stock_videos(tags)

video_paths = video.save_video(links)
speech_file_path = video.text_to_speech(script)
subtitle_path = video.generate_subtitles(speech_file_path)

combined_video_path = video.combine_videos(video_paths, video.AudioFileClip(speech_file_path).duration)
video.generate_video(combined_video_path, speech_file_path, subtitle_path)



