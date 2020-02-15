'''
Simple YouTube scraper - scrapes audio, video without audio, video based on user's preference

Run program using command: python yt-scraper.py --url <URL> --output <OUTPUT_DIRECTORY> --download <DOWNLOAD_OPTION>

Eg: (Downloads "Avicii - Wake Me Up (Official Video)" with all options to current directory)
python yt-scraper.py --url https://www.youtube.com/watch?v=IcrbM1l_BoI --output . --download 111
'''

import os
import argparse
import pafy

def main():
    args = get_arguments()
    url = args["url"]
    downloadOptions = args["download"]
    outputDirectory = args["output"]

    if downloadOptions == "000":
        raise Exception("Nothing to download! Try another option with --download")

    download_options_from_url(url, downloadOptions, outputDirectory)

def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--url", required=True, help="YouTube video URL")
    ap.add_argument("-o", "--output", required=True, help="Path to output directory")
    ap.add_argument("-d", "--download", default="001", help="'111' downloads audio, video-only and video. '000' downloads nothing")
    args = vars(ap.parse_args())
    return args

def prepend_filename(prefix, fileObject):
    fileName = fileObject.title + "." + fileObject.extension
    newFileName = prefix + "_" + fileName
    os.rename(fileName, newFileName)

def download_options_from_url(url, downloadOptions, outputDirectory):
    # change to output directory
    os.chdir(outputDirectory)
    # unpack downloadOptions, convert each element to int and assign each to corresponding variable
    downloadAudio, downloadVideoOnly, downloadVideo = list(map(lambda x:int(x), list(downloadOptions)))
    # create a "pafy" object from the YouTube URL
    video = pafy.new(url)
    # download audio/only video/video according to options specified
    if downloadAudio:
        bestAudio = video.getbestaudio()
        bestAudio.download(filepath=outputDirectory)
        prepend_filename("audio", bestAudio)

    if downloadVideoOnly:
        bestVideo = video.getbestvideo()
        bestVideo.download(filepath=outputDirectory)
        prepend_filename("video_only", bestVideo)

    if downloadVideo:
        bestResolution = video.getbest()
        bestResolution.download(filepath=outputDirectory)

if __name__ == "__main__":
    main()
