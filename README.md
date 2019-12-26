# lglivephoto

## purpose
* Recent LG smart phones have a feature "Live Photo" that works 'almost' like iPhone's but with a big flaw. You can play short movie of your photo on you phone, but you cannot find any movie file. (iPhone makes 1 still image file and 1 movie file for 1 shutter click)
* I found that LG mobile phone saves the movie(MP4) in jpeg file after EOI marker and it makes jpeg file larger.
* The purpose of this project is to extract the movie data and saves jpeg and mp4 separately.

## usage
`python3 main.py [-h|--help] [-r|--recursive] [-t|--target=<path>]`
* -h: show help
* -r: find jpeg files recursively
* -t: target path or file
