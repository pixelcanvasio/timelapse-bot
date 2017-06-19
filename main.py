import sched
import time
import canvas
import datetime

s = sched.scheduler(time.time, time.sleep)

# https://stackoverflow.com/questions/13294919/can-you-stream-images-to-ffmpeg-to-construct-a-video-instead-of-saving-them-t

INTERVAL = 60  # seconds
# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds-in-python


class TimeLapseBot:
    def save_frame(self):
        print "Building frame..."
        now = datetime.datetime.utcnow().strftime("%Y%m%d%H%MUTC")
        im = canvas.fetch()
        im.save(now + '.png')
        s.enter(INTERVAL, 1, self.save_frame, tuple())


bot = TimeLapseBot()
bot.save_frame()
s.run()