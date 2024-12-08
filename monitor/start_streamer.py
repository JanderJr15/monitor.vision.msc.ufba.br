import subprocess

DEVICE = '/dev/video0'
IMG_SIZE = '720x360'
FRAMES = '1'
PORT = '8080'


# mjpg-streamer -i "input_uvc.so -d /dev/video0 -r 720x360 -f 1" -o "output_http.so -p 8080 -w /usr/share/mjpg-streamer/www"
def start_mjpg_streamer():
    try:
        command = (
            'mjpg_streamer '
            f'-i "input_uvc.so -d {DEVICE} -r {IMG_SIZE} -f {FRAMES}" '
            f'-o "output_http.so -p {PORT} -w /usr/share/mjpg-streamer/www"'
        )
        print("Starting o MJPG-Streamer...")
        # subprocess.run(command, shell=True, check=True)
        subprocess.Popen(command, shell=True)

        print("MJPG-Streamer closed.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")

# start_mjpg_streamer()
# if __name__ == "__main__":
#     start_mjpg_streamer()
