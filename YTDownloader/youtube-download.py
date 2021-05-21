import os
import sys

user = os.getlogin()


def run(link, soundonly=False):
    from html import unescape
    from pytube import YouTube, Playlist
    print(link)
    if not soundonly:
        if not isinstance(link, tuple):
            if not link.startswith("https://www.youtube.com/playlist"):
                yt = YouTube(link)
                ys = yt.streams.get_highest_resolution()
                try:
                    os.makedirs(r"/home/elie/Desktop/YoutubeVideos")
                except FileExistsError:
                    pass
                finally:
                    print(
                        f"OK, let's download '{unescape(yt.title)}', with a resolution of {ys.resolution}"
                    )
                    ys.download(r"/home/elie/Desktop/YoutubeVideos")
            else:
                yt = Playlist(link)
                if not os.path.exists(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(yt.title))
                ):
                    os.makedirs(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(yt.title))
                    )
                for ys in yt.videos:
                    print(
                        f"OK, let's download '{unescape(ys.title)}, with a resolution of {ys.streams.get_highest_resolution().resolution}"
                    )
                    ys.streams.get_highest_resolution().download(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(yt.title))
                    )
        else:
            from youtube_search import YoutubeSearch

            results = YoutubeSearch(link[0]).to_dict()
            if not results:
                print("Heh, pas de r\u00e9sultats !")
                exit()
            result = results[0]
            link = "https://youtube.com/" + result["url_suffix"]
            run(link, soundonly)
    else:
        from moviepy.editor import VideoFileClip

        if not isinstance(link, tuple):

            if not link.startswith("https://www.youtube.com/playlist"):
                yt = YouTube(link)
                ys = yt.streams.get_highest_resolution()
                try:
                    os.makedirs(r"/home/elie/Desktop/YoutubeVideos")
                except FileExistsError:
                    pass
                finally:
                    print(f"OK, let's download '{unescape(yt.title)}'")
                    ys.download(
                        r"/home/elie/Desktop/YoutubeVideos",
                        unescape(yt.title).replace(" ", "_"),
                    )
                    video = VideoFileClip(
                        r"/home/elie/Desktop/YoutubeVideos/%s.mp4"
                        % (unescape(yt.title).replace(" ", "_").replace(".", ""))
                    )
                    video.audio.write_audiofile(
                        r"/home/elie/Desktop/YoutubeVideos/%s.mp3"
                        % (unescape(yt.title))
                    )
            else:
                ytP = Playlist(link)
                if not os.path.exists(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title))
                ):
                    os.makedirs(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title))
                    )
                for yt in ytP.videos:
                    print(f"OK, let's download '{unescape(yt.title)}'")
                    yt.streams.get_highest_resolution().download(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title)),
                        unescape(yt.title).replace(" ", "_"),
                    )
                    video = VideoFileClip(
                        r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp4"
                        % (
                            unescape(ytP.title),
                            unescape(yt.title).replace(" ", "_").replace(".", ""),
                        )
                    )
                    video.audio.write_audiofile(
                        r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp4"
                        % (unescape(ytP.title), unescape(yt.title))
                    )
        else:
            from youtube_search import YoutubeSearch

            results = YoutubeSearch(link[0]).to_dict()
            if not results:
                print("Heh, pas de r\u00e9sultats !")
                exit()
            result = results[0]
            link = "https://youtube.com/" + result["url_suffix"]
            run(link, soundonly)


if "-h" in sys.argv or "--help" in sys.argv:
    print(
        """
            SYNOPSIS : yt-dl [url | search [query] ] [OPTIONS]
                        Download the video that has the specified url or download a video that matches with the query
            OPTIONS :
                        -s --soundonly          download the video, but as a .mp3
                        -h --help               shows this
            """
    )
    exit()
if "search" in sys.argv[:2]:
    keys = sys.argv
    link = (keys[keys.index("search") + 1].replace("+", " "),)
else:
    link = sys.argv[1]
run(link, soundonly="--soundonly" in sys.argv)
