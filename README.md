# Make Sure You Subscribe To our Channel 😊😊
[Devs Do Code](https://www.youtube.com/channel/@devsdocode)

🚀 Dive into the world of coding with [Devs Do Code](https://www.youtube.com/channel/@devsdocode) - where passion meets programming! Make sure to hit that Subscribe button to stay tuned for exciting content! 😊✨

**Pro Tip:** For optimal performance and a seamless experience, we recommend using the default library versions demonstrated in this demo. Your coding journey just got even better! Happy coding! 🖥️💻

## Automate-YT-Shorts-Video-Resource

Create YouTube Shorts without any effort, simply by providing a video topic to talk about.

### Installation

```bash
# Clone the REPO
git clone https://github.com/SreejanPersonal/Automate-YT-Shorts-Video-Resource-.git

# Install the required dependencies
pip install -r requirements.txt

# Set the Environment Variables
ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
IMAGEMAGICK_BINARY = os.getenv("IMAGEMAGICK_BINARY") # IF ISSUE OCCURS THEN CHANGE FILE LOCATION IN conf.py

# Run the backend server
python main.py
     # OR
python main.ipynb
```
If any error occurs for FFMPEG then follow these steps
```powershell admin
# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install FFMPEG
choco install ffmpeg
```

See [`.env`](.env) for the required environment variables.

If you need help, open [ENV.md](ENV.md) for more information.

### Usage

1. Fill `.env` file with the required values
1. Enter a topic to talk about
1. Run the `main.py` file
1. Wait for the video to be generated
1. The video's location is `temp/output.mp4`

## Fonts

Add your fonts to the `fonts/` folder, and load them by specifiying the font name in `Backend/video.py`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

See [`LICENSE`](LICENSE) file for more information.
