import os
from .step import Step
from youtube_dl import YoutubeDL


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


class DownloadVideos(Step):
    def process(self, data, inputs, utils):

        yt_set = set([found.yt for found in data])
        print('videos to download=', len(yt_set))

        for yt in yt_set:

            ydl_opts = {
                'format': 'worst',  # bestvideo[height<360]+bestaudio/best[height<360]',  # bestvideo[height<=360][ext=mp4]+bestaudio/best[height<=360]
                'outtmpl': yt.video_filepath,
                # 'noplaylist': True,
                # 'progress_hooks': [my_hook],
            }
            url = yt.url

            if utils.video_file_exists(yt):
                print(f'found existing video file for {url}, skipping')
                continue
            try:
                print('downloading', url)
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            # except YoutubeDL.report_error(ydl_opts, 'ERROR:'):
            except Exception as e:
                print('Error when downloading video for', e)
                continue

        return data
