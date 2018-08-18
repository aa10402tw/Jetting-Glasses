from __future__ import print_function

import time

from pyspin.spin import make_spin, Default


# Choose a spin style and the words when showing the spin.
@make_spin(Default, "Downloading...")
def download_video():
    time.sleep(10)

if __name__ == '__main__':
    print("I'm going to download a video, and it'll cost much time.")
    download_video()
    print("Done!")

