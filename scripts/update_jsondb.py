import json
import shutil
from os.path import dirname, isfile

from youtube_archivist import YoutubeMonitor


archive = YoutubeMonitor(db_name="WorldMovieCentral",
                                      blacklisted_kwords=["trailer", "teaser", "movie scene",
                                                          "movie clip", "behind the scenes", "movie analysis",
                                                          "Movie Preview", "soundtrack", " OST", "opening theme"],
                                      min_duration=30 * 60)

# load previous cache
cache_file = f"{dirname(dirname(__file__))}/bootstrap.json"
if isfile(cache_file):
    try:
        with open(cache_file) as f:
            data = json.load(f)
            archive.db.update(data)
            archive.db.store()
    except:
        pass  # corrupted for some reason

    shutil.rmtree(cache_file, ignore_errors=True)

for url in [
    "https://www.youtube.com/channel/UCNbnH_iXdGphKO-AGe-GbLA"
]:
    # parse new vids
    archive.parse_videos(url)

# save bootstrap cache
shutil.copy(archive.db.path, cache_file)
