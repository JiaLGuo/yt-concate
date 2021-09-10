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
                # 'format': '[bestvideo[height <= 360, ext=MP4] + bestaudio / best[height <= 360]',
                'outtmpl': yt.video_filepath,
                'noplaylist': True,
                'progress_hooks': [my_hook],
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
            except:
                os.system(f"""youtube-dl -o "song.%(ext)s" --extract-audio -x --audio-format mp3 {video_url}""")
        return data
