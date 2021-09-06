from youtube_transcript_api import YouTubeTranscriptApi
import json
from .step import Step
from .step import StepException
import time


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for url in data:
            print('downloading existing caption file', url)
            if utils.caption_file_exists(url):
                print('found existing caption file')
                continue

            try:
                video_id = utils.get_video_id_from_url(url)
                captions = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                captions_l = list(json.dumps(i) for i in captions)
                with open(utils.get_caption_filepath(url), 'w', encoding='utf-8') as fp:
                    for i in captions_l:
                        fp.write(i + '\n')
                    fp.close()
            # except (KeyError, AttributeError):
            except Exception as e:
                print('Error when downloading caption for', e)
                continue



        end = time.time()
        print('took', end - start)