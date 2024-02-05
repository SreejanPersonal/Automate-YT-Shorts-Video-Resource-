import os
import requests
import srt_equalizer
import assemblyai as aai

from typing import List
from moviepy.editor import *
from termcolor import colored
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip


def save_video(video_urls: list, directory: str = "./temp") -> str:
    """
    Saves a video from a given URL and returns the path to the video.

    Args:
        video_url (str): The URL of the video to save.

    Returns:
        str: The path to the saved video.
    """
    os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist
    video_paths = []
    for video_id, video_url in enumerate(video_urls):
        video_path = f"{directory}/{video_id+1}.mp4"
        with open(video_path, "wb") as f:
            f.write(requests.get(video_url).content)

        print(video_path)
        video_paths.append(video_path)
    
    return video_paths

def text_to_speech(text, output_path_location="output.mp3"):  # Define a function to speak text using edge-tts

    voice = "en-CA-LiamNeural"  # Choose the voice for the speech (professional Canadian accent)

    # Choose the voice you want for the speech
    # Here are some Available options with nice indian accent & are good for conversation:
    # - en-US-JennyNeural: A clear and professional-sounding American female voice
    # - en-SG-LunaNeural: A friendly and approachable Singaporean female voice
    # - en-AU-NatashaNeural: A warm and friendly Australian female voice
    # - en-CA-ClaraNeural: A crisp and articulate Canadian female voice

    # Build the edge-tts command string, including voice, text, and output media
    command = f"edge-tts --voice \"{voice}\" --text \"{text}\" --write-media \"{output_path_location}\""
    # print(command)

    # Execute the edge-tts command using the system shell
    os.system(command)

    return output_path_location

def generate_subtitles(audio_path: str, ASSEMBLY_AI_API_KEY: str, directory: str =  "./subtitles") -> str:
    """
    Generates subtitles from a given audio file and returns the path to the subtitles.

    Args:
        audio_path (str): The path to the audio file to generate subtitles from.

    Returns:
        str: The path to the generated subtitles.
    """
    def equalize_subtitles(srt_path: str, max_chars: int = 10) -> None:
      # Equalize subtitles
      srt_equalizer.equalize_srt_file(srt_path, srt_path, max_chars)

    print(ASSEMBLY_AI_API_KEY)

    aai.settings.api_key = ASSEMBLY_AI_API_KEY

    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(audio_path)


    os.makedirs(directory, exist_ok=True) 
    # Save subtitles
    subtitles_path = f"{directory}/audio.srt"

    subtitles = transcript.export_subtitles_srt()

    with open(subtitles_path, "w") as f:
        f.write(subtitles)

    # Equalize subtitles
    equalize_subtitles(subtitles_path)

    print(colored("[+] Subtitles generated.", "green"))

    return subtitles_path



def combine_videos(video_paths: List[str], max_duration: int) -> str:
    """
    Combines a list of videos into one video and returns the path to the combined video.

    Args:
        video_paths (list): A list of paths to the videos to combine.
        max_duration (int): The maximum duration of the combined video.

    Returns:
        str: The path to the combined video.
    """
    combined_video_path = f"./temp/combined_video.mp4"

    print(colored("[+] Combining videos...", "blue"))
    print(colored(f"[+] Each video will be {max_duration / len(video_paths)} seconds long.", "blue"))

    clips = []
    for video_path in video_paths:
        clip = VideoFileClip(video_path)
        clip = clip.without_audio()       
        clip = clip.subclip(0, max_duration / len(video_path))
        clip = clip.set_fps(30)

        # Not all videos are same size,
        # so we need to resize them
        clip = crop(clip, width=1080, height=1920, \
                    x_center=clip.w / 2, \
                        y_center=clip.h / 2)
        clip = clip.resize((1080, 1920))

        clips.append(clip)

    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_fps(30)
    final_clip.write_videofile(combined_video_path, threads=3)

    return combined_video_path

def generate_video(combined_video_path: str, tts_path: str, subtitles_path: str, output_file_name: str = "main_output.mp4") -> str:
    """
    This function creates the final video, with subtitles and audio.

    Args:
        combined_video_path (str): The path to the combined video.
        tts_path (str): The path to the text-to-speech audio.
        subtitles_path (str): The path to the subtitles.

    Returns:
        str: The path to the final video.
    """
    # Make a generator that returns a TextClip when called with consecutive
    generator = lambda txt: TextClip(txt, font=fr"MoneyPrinter\fonts\bold_font.ttf", fontsize=100, color="#FFFF00",
    stroke_color="black", stroke_width=5)

    # Burn the subtitles into the video
    subtitles = SubtitlesClip(subtitles_path, generator)
    result = CompositeVideoClip([
        VideoFileClip(combined_video_path),
        subtitles.set_pos(("center", "center"))
    ])

    # Add the audio
    audio = AudioFileClip(tts_path)
    result = result.set_audio(audio)

    result.write_videofile("./temp/output.mp4", threads=3)

    return output_file_name

def list_files_in_directory(directory):
    try:
        # Get a list of all files in the specified directory
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return files
    
    except FileNotFoundError:
        print(f"Directory not found: {directory}")
        return []



if __name__ == "__main__":

    # path = text_to_speech('''Discover diverse online income avenues with this guide! Freelancing offers a platform for writers, designers, programmers, and marketers to showcase skills and secure clients. Dive into lucrative affiliate marketing by promoting products for commissions. Consider starting an e-commerce business to tap into the global market. Content creation, whether through blogging, vlogging, or online courses, monetizes expertise. Emphasizing diversification, explore multiple income streams for financial stability. Making money online demands dedication, perseverance, and learning. It's not a quick fix, but with the right mindset, you can build a sustainable online income. For more insights or questions, leave a comment below. Happy money-making''')
    # print(path)

    links = ['https://player.vimeo.com/external/493894149.sd.mp4?s=c882caa9e51f67e259185992e97340c902c65624&profile_id=164&oauth2_token_id=57447761', 
            'https://player.vimeo.com/external/504027534.hd.mp4?s=3dcefc44fde76f92996332f9aff164453815ee99&profile_id=174&oauth2_token_id=57447761', 
            'https://player.vimeo.com/external/507877197.hd.mp4?s=e6047c0fde051a074dc4cf1a9c99ec1a6c9080e1&profile_id=170&oauth2_token_id=57447761', 
            'https://player.vimeo.com/external/533386598.hd.mp4?s=f37c8671c211b59b0aa6b24108ce752b18081aa8&profile_id=174&oauth2_token_id=57447761', 
            'https://player.vimeo.com/external/539033394.sd.mp4?s=8813ecbaf896b6ea024b4fff6eab1246e81758ac&profile_id=164&oauth2_token_id=57447761', 
            'https://player.vimeo.com/external/493894149.sd.mp4?s=c882caa9e51f67e259185992e97340c902c65624&profile_id=164&oauth2_token_id=57447761', 
            'https://player.vimeo.com/external/441945918.hd.mp4?s=39454433911b7835677a3925b93b0593ee3bf3ad&profile_id=175&oauth2_token_id=57447761', 
            'https://player.vimeo.com/external/507878934.hd.mp4?s=349c086fb23a938b6ca97bad042f044e04e0487d&profile_id=172&oauth2_token_id=57447761', 
            'https://player.vimeo.com/external/533386598.hd.mp4?s=f37c8671c211b59b0aa6b24108ce752b18081aa8&profile_id=174&oauth2_token_id=57447761', 
            'https://player.vimeo.com/external/436375789.hd.mp4?s=ea9af22125a91895ef74ae54ba2ad033a686ccf1&profile_id=170&oauth2_token_id=57447761']

    # temp_audio = AudioFileClip("output.mp3")
    # print(temp_audio.duration)

    # video_paths = save_video(links)
    # print(video_paths)
    
    # speech_file_path = text_to_speech("TOPIC")
    # subtitle_path = generate_subtitles(r"output.mp3", 'fd937dda8dbf4258b7ec098b7c419bfe')

    # combined_video_path = combine_videos(video_paths, temp_audio.duration)
    # combined_video_path = f"./temp/combined_video.mp4"
    # generate_video(combined_video_path, "output.mp3", r"subtitles\audio.srt")
