import subprocess

DEVICE = '/dev/video0'
IMG_SIZE = '720x360'
FRAMES = '1'
PORT = '8080'

def start_mjpg_streamer():
    try:
        command = (
            'mjpg_streamer '
            f'-i "input_uvc.so -d {DEVICE} -r {IMG_SIZE} -f {FRAMES} -n" '
            f'-o "output_http.so -p {PORT} -w /usr/share/mjpg-streamer/www"'
        )
        print("Starting o MJPG-Streamer...")
        subprocess.Popen(command, shell=True)

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

if __name__ == "__main__":
    start_mjpg_streamer()
