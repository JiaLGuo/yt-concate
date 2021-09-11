import time
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter
from .step import Step
from .step import StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for yt in data:
            print('downloading existing caption file', yt.url)
            if utils.caption_file_exists(yt):
                print('found existing caption file')
                continue

            try:
                video_id = yt.get_video_id_from_url(yt.url)
                captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                formatter = WebVTTFormatter()
                WebVTTFormattered = formatter.format_transcript(captions)
                with open(yt.caption_filepath, 'w', encoding='utf-8') as vtt_file:
                    vtt_file.write(WebVTTFormattered)

            # except (KeyError, AttributeError):
            except Exception as e:
                print('Error when downloading caption for', e)
                continue

        end = time.time()
        print('took', end - start)
        return data
