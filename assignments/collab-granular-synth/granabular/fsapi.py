import os
import sys
import datetime
import freesound
import subprocess

class fsc:
    def __init__(self):

        api_key = os.getenv('FREESOUND_API_KEY', None)
        if api_key is None:
            print("You need to set your API key as an evironment variable",)
            print("named FREESOUND_API_KEY")
            sys.exit(-1)

        self.freesound_client = freesound.FreesoundClient()
        self.freesound_client.set_token(api_key)


    def retrieve_sound_preview(self, sound, directory):
        """Download the high-quality OGG sound preview of a given Freesound sound object to the given directory.
        """
        return freesound.FSRequest.retrieve(
            sound.previews.preview_hq_ogg,
            self.freesound_client,
            os.path.join(directory, sound.previews.preview_hq_ogg.split('/')[-1])
        )

    def download_grains(self, query, n=5):

        results_pager = self.freesound_client.text_search(
            query=query,
            filter="duration:[1.0 TO 15.0]",
            sort="rating_desc",
            fields="id,name,previews,username"
        )

        wavfilepaths = []

        print(f"Query: {query} - Results: {results_pager.count}")
        for idx, sound in enumerate(results_pager):

            # download the ogg preview 
            outputdir = 'grains'
            oggfilepath, http = self.retrieve_sound_preview(sound, outputdir)
            fileid = os.path.basename(oggfilepath).split("_")[0]
            wavfilepath = f"grains/fs{fileid}.wav"
            wavfilepaths.append(wavfilepath)

            print(f"Downloaded {oggfilepath}.")

            # convert ogg to wav file with ffmpeg
            subprocess.run(["ffmpeg",  "-i",  oggfilepath, \
            "-ac", "1", "-f", "wav", wavfilepath, "-r", "44100", "-y", "-loglevel", "quiet"])

            # remove the ogg file
            os.remove(oggfilepath)

            # only download n sounds
            if (idx+1) >= n:
                break

        return wavfilepaths
