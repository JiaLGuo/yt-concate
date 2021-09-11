from moviepy.editor import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from .step import Step


class EditVideo(Step):
    def process(self, data, inputs, utils):
        clips = []
        for found in data:
            print(found.time)
            start, end = self.parse_caption_time(found.time)  # ex: ((0, 11, 26.63), (0, 11, 51.85))
            print(f'start{start} > end{end}')
            video = VideoFileClip(found.yt.video_filepath).subclip(start, end)

            clips.append(video)
            if len(clips) >= inputs['limit']:
                break
            final_clip = concatenate_videoclips(clips)
            output_filepath = utils.get_output_filepath(inputs['channel_id'], inputs['search_word'])
            final_clip.write_videofile(output_filepath)
        return data

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)  # return tuple

    def parse_time_str(self, time_str):
        h, m, s = time_str.split(':')
        s, ms = s.split('.')
        return int(h), int(m), int(s) + int(ms) / 1000  # return tuple (h, m, s)

# from moviepy.video.compositing.concatenate import concatenate_videoclips
#
# from .step import Step
#
# from moviepy.editor import VideoFileClip
#
# class EditVideo(Step):
#     def process(self, data, inputs, utils):
#         clips = []
#         for found in data:
#             print(found, found.time)
#             start, end = self.parse_caption_time(found.time)
#             video = VideoFileClip(found.yt.video_filepath).subclip(30, 35)
#             clips.append(video)
#             if len(clips) >= inputs['limit']:
#                 break
#
#         final_clip = concatenate_videoclips(clips)
#         output_filepath = utils.get_output_filepath(inputs['channel_id'], inputs['search_word'])
#         final_clip.write_videofile(output_filepath)
#         return data
#
#     def parse_caption_time(self, caption_time):
#         start, end = caption_time.split(' --> ')
#         return self.parse_caption_str(start), self.parse_caption_str(end)
#
#     def parse_caption_str(self, time_str):
#         h, m, s = time_str.split(':')
#         s, ms = s.split('.')
#         return int(h), int(m), int(s) + int(ms) / 1000

