import yt_dlp
import argparse
import os

class CLIOutputLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def download_youtube_audio(url, output_path='.', output_format='mp3'):
    os.makedirs(output_path, exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': output_format,
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'logger': CLIOutputLogger(),
        'progress_hooks': [lambda d: _show_progress(d)],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            print(f"\nSuccessfully downloaded:")
            print(f"  Title: {info_dict.get('title', 'Unknown')}")
            print(f"  Duration: {_format_duration(info_dict.get('duration'))}")
            print(f"  Saved to: {os.path.abspath(output_path)}")
            print(f"  Format: {output_format.upper()}")
            
    except Exception as e:
        print(f"\nError: {str(e)}")

def _show_progress(data):
    if data['status'] == 'downloading':
        percent = data.get('_percent_str', '?').strip()
        speed = data.get('_speed_str', '?').strip()
        print(f"\rDownloading: {percent} at {speed}", end='', flush=True)
    elif data['status'] == 'finished':
        print("\rConverting audio...", end='', flush=True)

def _format_duration(seconds):
    if not seconds: return 'Unknown'
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download YouTube audio')
    parser.add_argument('-u', '--url', required=True, help='YouTube URL')
    parser.add_argument('-o', '--output', default='.', 
                       help='Output directory (default: current)')
    parser.add_argument('-f', '--format', default='mp3', 
                       choices=['mp3', 'wav', 'aac', 'm4a', 'ogg'],
                       help='Audio format (default: mp3)')
    
    args = parser.parse_args()
    download_youtube_audio(args.url, args.output, args.format)
