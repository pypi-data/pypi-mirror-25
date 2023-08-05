avideo - download videos from youtube.com or other video platforms

- [INSTALLATION](#installation)
- [DESCRIPTION](#description)
- [OPTIONS](#options)
- [CONFIGURATION](#configuration)
- [OUTPUT TEMPLATE](#output-template)
- [FORMAT SELECTION](#format-selection)
- [VIDEO SELECTION](#video-selection)
- [FAQ](#faq)
- [DEVELOPER INSTRUCTIONS](#developer-instructions)
- [EMBEDDING AVIDEO](#embedding-avideo)
- [BUGS](#bugs)
- [COPYRIGHT](#copyright)

# INSTALLATION

To install it right away for all users on an apt-based system, add our apt repository using some commands in your terminal. Firstly, add an avideo repository \(latest is recommended\) and the signing key:

    sudo bash -c 'echo "deb https://notabug.org/GPast/avideo/raw/archive/repos/latest /" >> /etc/apt/sources.list'
    wget -qO - https://notabug.org/GPast/avideo/raw/archive/repos/repokey | sudo apt-key add -

Finally, install apt\-transport\-https, update your apt database, and install avideo:

    sudo apt install apt-transport-https && sudo apt update && sudo apt install avideo
    
You can alternatively install the Python package directly, using pip:

    sudo pip install avideo

Otherwise, or if you would like to install from source, download the source tarball. Extract it, and then run the following in a terminal:

    cd <PATH TO EXTRACTED TARBALL DIRECTORY>
    sudo make install

Alternatively, refer to the [developer instructions](#developer-instructions) for how to check out and work with the git repository. For further options see the [avideo Download Page](https://notabug.org/GPast/avideo/wiki/Downloads).

# DESCRIPTION
**avideo** is a command-line program to download videos from YouTube.com and a few more sites. It is fully libre, requires the Python interpreter, version 2.6, 2.7, or 3.2+, and is supported on GNU/Linux. It is released under the GPLv3+, which means you can modify it, redistribute it or use it however you like, so long as you give others the same rights.

    avideo [OPTIONS] URL [URL...]

# OPTIONS
    -h, --help                       Print this help text and exit
    -i, --ignore-errors              Continue on download errors, for example to
                                     skip unavailable videos in a playlist
    --abort-on-error                 Abort downloading of further videos (in the
                                     playlist or the command line) if an error
                                     occurs
    --dump-user-agent                Display the current browser identification
    --list-extractors                List all supported extractors
    --extractor-descriptions         Output descriptions of all supported
                                     extractors
    --force-generic-extractor        Force extraction to use the generic
                                     extractor
    --default-search PREFIX          Use this prefix for unqualified URLs. For
                                     example "gvsearch2:" downloads two videos
                                     from google videos for avideo "large
                                     apple". Use the value "auto" to let avideo
                                     guess ("auto_warning" to emit a warning
                                     when guessing). "error" just throws an
                                     error. The default value "fixup_error"
                                     repairs broken URLs, but emits an error if
                                     this is not possible instead of searching.
    --ignore-config                  Do not read configuration files. When given
                                     in the global configuration file
                                     /etc/avideo.conf: Do not read the user
                                     configuration in ~/.config/avideo/config
    --config-location PATH           Location of the configuration file; either
                                     the path to the config or its containing
                                     directory.
    --flat-playlist                  Do not extract the videos of a playlist,
                                     only list them.
    --mark-watched                   Mark videos watched (YouTube only)
    --no-mark-watched                Do not mark videos watched (YouTube only)
    --no-color                       Do not emit color codes in output

## Network Options:
    --proxy URL                      Use the specified HTTP/HTTPS/SOCKS proxy.
                                     To enable experimental SOCKS proxy, specify
                                     a proper scheme. For example
                                     socks5://127.0.0.1:1080/. Pass in an empty
                                     string (--proxy "") for direct connection
    --socket-timeout SECONDS         Time to wait before giving up, in seconds
    --source-address IP              Client-side IP address to bind to
    -4, --force-ipv4                 Make all connections via IPv4
    -6, --force-ipv6                 Make all connections via IPv6

## Geo Restriction:
    --geo-verification-proxy URL     Use this proxy to verify the IP address for
                                     some geo-restricted sites. The default
                                     proxy specified by --proxy (or none, if the
                                     options is not present) is used for the
                                     actual downloading.
    --geo-bypass                     Bypass geographic restriction via faking X
                                     -Forwarded-For HTTP header (experimental)
    --no-geo-bypass                  Do not bypass geographic restriction via
                                     faking X-Forwarded-For HTTP header
                                     (experimental)
    --geo-bypass-country CODE        Force bypass geographic restriction with
                                     explicitly provided two-letter ISO 3166-2
                                     country code (experimental)

## Video Selection:
    --playlist-start NUMBER          Playlist video to start at (default is 1)
    --playlist-end NUMBER            Playlist video to end at (default is last)
    --playlist-items ITEM_SPEC       Playlist video items to download. Specify
                                     indices of the videos in the playlist
                                     separated by commas like: "--playlist-items
                                     1,2,5,8" if you want to download videos
                                     indexed 1, 2, 5, 8 in the playlist. You can
                                     specify range: "--playlist-items
                                     1-3,7,10-13", it will download the videos
                                     at index 1, 2, 3, 7, 10, 11, 12 and 13.
    --match-title REGEX              Download only matching titles (regex or
                                     caseless sub-string)
    --reject-title REGEX             Skip download for matching titles (regex or
                                     caseless sub-string)
    --max-downloads NUMBER           Abort after downloading NUMBER files
    --min-filesize SIZE              Do not download any videos smaller than
                                     SIZE (e.g. 50k or 44.6m)
    --max-filesize SIZE              Do not download any videos larger than SIZE
                                     (e.g. 50k or 44.6m)
    --date DATE                      Download only videos uploaded in this date
    --datebefore DATE                Download only videos uploaded on or before
                                     this date (i.e. inclusive)
    --dateafter DATE                 Download only videos uploaded on or after
                                     this date (i.e. inclusive)
    --min-views COUNT                Do not download any videos with less than
                                     COUNT views
    --max-views COUNT                Do not download any videos with more than
                                     COUNT views
    --match-filter FILTER            Generic video filter. Specify any key (see
                                     the "OUTPUT TEMPLATE" for a list of
                                     available keys) to match if the key is
                                     present, !key to check if the key is not
                                     present, key > NUMBER (like "comment_count
                                     > 12", also works with >=, <, <=, !=, =) to
                                     compare against a number, key = 'LITERAL'
                                     (like "uploader = 'Mike Smith'", also works
                                     with !=) to match against a string literal
                                     and & to require multiple matches. Values
                                     which are not known are excluded unless you
                                     put a question mark (?) after the operator.
                                     For example, to only match videos that have
                                     been liked more than 100 times and disliked
                                     less than 50 times (or the dislike
                                     functionality is not available at the given
                                     service), but who also have a description,
                                     use --match-filter "like_count > 100 &
                                     dislike_count <? 50 & description" .
    --no-playlist                    Download only the video, if the URL refers
                                     to a video and a playlist.
    --yes-playlist                   Download the playlist, if the URL refers to
                                     a video and a playlist.
    --age-limit YEARS                Download only videos suitable for the given
                                     age
    --download-archive FILE          Download only videos not listed in the
                                     archive file. Record the IDs of all
                                     downloaded videos in it.
    --include-ads                    Download advertisements as well
                                     (experimental)

## Download Options:
    -r, --limit-rate RATE            Maximum download rate in bytes per second
                                     (e.g. 50K or 4.2M)
    -R, --retries RETRIES            Number of retries (default is 10), or
                                     "infinite".
    --fragment-retries RETRIES       Number of retries for a fragment (default
                                     is 10), or "infinite" (DASH, hlsnative and
                                     ISM)
    --skip-unavailable-fragments     Skip unavailable fragments (DASH, hlsnative
                                     and ISM)
    --abort-on-unavailable-fragment  Abort downloading when some fragment is not
                                     available
    --keep-fragments                 Keep downloaded fragments on disk after
                                     downloading is finished; fragments are
                                     erased by default
    --buffer-size SIZE               Size of download buffer (e.g. 1024 or 16K)
                                     (default is 1024)
    --no-resize-buffer               Do not automatically adjust the buffer
                                     size. By default, the buffer size is
                                     automatically resized from an initial value
                                     of SIZE.
    --playlist-reverse               Download playlist videos in reverse order
    --playlist-random                Download playlist videos in random order
    --xattr-set-filesize             Set file xattribute ytdl.filesize with
                                     expected file size (experimental)
    --hls-prefer-native              Use the native HLS downloader instead of
                                     ffmpeg
    --hls-prefer-ffmpeg              Use ffmpeg instead of the native HLS
                                     downloader
    --hls-use-mpegts                 Use the mpegts container for HLS videos,
                                     allowing to play the video while
                                     downloading (some players may not be able
                                     to play it)
    --external-downloader COMMAND    Use the specified external downloader.
                                     Currently supports
                                     aria2c,avconv,axel,curl,ffmpeg,httpie,wget
    --external-downloader-args ARGS  Give these arguments to the external
                                     downloader

## Filesystem Options:
    -a, --batch-file FILE            File containing URLs to download ('-' for
                                     stdin)
    --id                             Use only video ID in file name
    -o, --output TEMPLATE            Output filename template, see the "OUTPUT
                                     TEMPLATE" for all the info
    --autonumber-start NUMBER        Specify the start value for %(autonumber)s
                                     (default is 1)
    --restrict-filenames             Restrict filenames to only ASCII
                                     characters, and avoid "&" and spaces in
                                     filenames
    -w, --no-overwrites              Do not overwrite files
    -c, --continue                   Force resume of partially downloaded files.
                                     By default, avideo will resume downloads if
                                     possible.
    --no-continue                    Do not resume partially downloaded files
                                     (restart from beginning)
    --no-part                        Do not use .part files - write directly
                                     into output file
    --no-mtime                       Do not use the Last-modified header to set
                                     the file modification time
    --write-description              Write video description to a .description
                                     file
    --write-info-json                Write video metadata to a .info.json file
    --write-annotations              Write video annotations to a
                                     .annotations.xml file
    --load-info-json FILE            JSON file containing the video information
                                     (created with the "--write-info-json"
                                     option)
    --cookies FILE                   File to read cookies from and dump cookie
                                     jar in
    --cache-dir DIR                  Location in the filesystem where avideo can
                                     store some downloaded information
                                     permanently. By default
                                     $XDG_CACHE_HOME/avideo or ~/.cache/avideo .
                                     At the moment, only YouTube player files
                                     (for videos with obfuscated signatures) are
                                     cached, but that may change.
    --no-cache-dir                   Disable filesystem caching
    --rm-cache-dir                   Delete all filesystem cache files

## Thumbnail images:
    --write-thumbnail                Write thumbnail image to disk
    --write-all-thumbnails           Write all thumbnail image formats to disk
    --list-thumbnails                Simulate and list all available thumbnail
                                     formats

## Verbosity / Simulation Options:
    -q, --quiet                      Activate quiet mode
    --no-warnings                    Ignore warnings
    -s, --simulate                   Do not download the video and do not write
                                     anything to disk
    --skip-download                  Do not download the video
    -g, --get-url                    Simulate, quiet but print URL
    -e, --get-title                  Simulate, quiet but print title
    --get-id                         Simulate, quiet but print id
    --get-thumbnail                  Simulate, quiet but print thumbnail URL
    --get-description                Simulate, quiet but print video description
    --get-duration                   Simulate, quiet but print video length
    --get-filename                   Simulate, quiet but print output filename
    --get-format                     Simulate, quiet but print output format
    -j, --dump-json                  Simulate, quiet but print JSON information.
                                     See the "OUTPUT TEMPLATE" for a description
                                     of available keys.
    -J, --dump-single-json           Simulate, quiet but print JSON information
                                     for each command-line argument. If the URL
                                     refers to a playlist, dump the whole
                                     playlist information in a single line.
    --print-json                     Be quiet and print the video information as
                                     JSON (video is still being downloaded).
    --newline                        Output progress bar as new lines
    --no-progress                    Do not print progress bar
    --console-title                  Display progress in console titlebar
    -v, --verbose                    Print various debugging information
    --dump-pages                     Print downloaded pages encoded using base64
                                     to debug problems (very verbose)
    --write-pages                    Write downloaded intermediary pages to
                                     files in the current directory to debug
                                     problems
    --print-traffic                  Display sent and read HTTP traffic
    -C, --call-home                  Contact the avideo server for debugging
    --no-call-home                   Do NOT contact the avideo server for
                                     debugging

## Workarounds:
    --encoding ENCODING              Force the specified encoding (experimental)
    --no-check-certificate           Suppress HTTPS certificate validation
    --prefer-insecure                Use an unencrypted connection to retrieve
                                     information about the video. (Currently
                                     supported only for YouTube)
    --user-agent UA                  Specify a custom user agent
    --referer URL                    Specify a custom referer, use if the video
                                     access is restricted to one domain
    --add-header FIELD:VALUE         Specify a custom HTTP header and its value,
                                     separated by a colon ':'. You can use this
                                     option multiple times
    --bidi-workaround                Work around terminals that lack
                                     bidirectional text support. Requires bidiv
                                     or fribidi executable in PATH
    --sleep-interval SECONDS         Number of seconds to sleep before each
                                     download when used alone or a lower bound
                                     of a range for randomized sleep before each
                                     download (minimum possible number of
                                     seconds to sleep) when used along with
                                     --max-sleep-interval.
    --max-sleep-interval SECONDS     Upper bound of a range for randomized sleep
                                     before each download (maximum possible
                                     number of seconds to sleep). Must only be
                                     used along with --min-sleep-interval.

## Video Format Options:
    -f, --format FORMAT              Video format code, see the "FORMAT
                                     SELECTION" for all the info
    --all-formats                    Download all available video formats
    --prefer-free-formats            Prefer free video formats unless a specific
                                     one is requested
    -F, --list-formats               List all available formats of requested
                                     videos
    --youtube-skip-dash-manifest     Do not download the DASH manifests and
                                     related data on YouTube videos
    --merge-output-format FORMAT     If a merge is required (e.g.
                                     bestvideo+bestaudio), output to given
                                     container format. One of mkv, mp4, ogg,
                                     webm, flv. Ignored if no merge is required

## Subtitle Options:
    --write-sub                      Write subtitle file
    --write-auto-sub                 Write automatically generated subtitle file
                                     (YouTube only)
    --all-subs                       Download all the available subtitles of the
                                     video
    --list-subs                      List all available subtitles for the video
    --sub-format FORMAT              Subtitle format, accepts formats
                                     preference, for example: "srt" or
                                     "ass/srt/best"
    --sub-lang LANGS                 Languages of the subtitles to download
                                     (optional) separated by commas, use --list-
                                     subs for available language tags

## Authentication Options:
    -u, --username USERNAME          Login with this account ID
    -p, --password PASSWORD          Account password. If this option is left
                                     out, avideo will ask interactively.
    -2, --twofactor TWOFACTOR        Two-factor authentication code
    -n, --netrc                      Use .netrc authentication data
    --video-password PASSWORD        Video password (vimeo, smotri, youku)

## Adobe Pass Options:
    --ap-mso MSO                     Adobe Pass multiple-system operator (TV
                                     provider) identifier, use --ap-list-mso for
                                     a list of available MSOs
    --ap-username USERNAME           Multiple-system operator account login
    --ap-password PASSWORD           Multiple-system operator account password.
                                     If this option is left out, avideo will ask
                                     interactively.
    --ap-list-mso                    List all supported multiple-system
                                     operators

## Post-processing Options:
    -x, --extract-audio              Convert video files to audio-only files
                                     (requires ffmpeg or avconv and ffprobe or
                                     avprobe)
    --audio-format FORMAT            Specify audio format: "best", "aac",
                                     "flac", "mp3", "m4a", "opus", "vorbis", or
                                     "wav"; "best" by default; No effect without
                                     -x
    --audio-quality QUALITY          Specify ffmpeg/avconv audio quality, insert
                                     a value between 0 (better) and 9 (worse)
                                     for VBR or a specific bitrate like 128K
                                     (default 5)
    --recode-video FORMAT            Encode the video to another format if
                                     necessary (currently supported:
                                     mp4|flv|ogg|webm|mkv|avi)
    --postprocessor-args ARGS        Give these arguments to the postprocessor
    -k, --keep-video                 Keep the video file on disk after the post-
                                     processing; the video is erased by default
    --no-post-overwrites             Do not overwrite post-processed files; the
                                     post-processed files are overwritten by
                                     default
    --embed-subs                     Embed subtitles in the video (only for mp4,
                                     webm and mkv videos)
    --embed-thumbnail                Embed thumbnail in the audio as cover art
    --add-metadata                   Write metadata to the video file
    --metadata-from-title FORMAT     Parse additional metadata like song title /
                                     artist from the video title. The format
                                     syntax is the same as --output. Regular
                                     expression with named capture groups may
                                     also be used. The parsed parameters replace
                                     existing values. Example: --metadata-from-
                                     title "%(artist)s - %(title)s" matches a
                                     title like "Coldplay - Paradise". Example
                                     (regex): --metadata-from-title
                                     "(?P<artist>.+?) - (?P<title>.+)"
    --xattrs                         Write metadata to the video file's xattrs
                                     (using dublin core and xdg standards)
    --fixup POLICY                   Automatically correct known faults of the
                                     file. One of never (do nothing), warn (only
                                     emit a warning), detect_or_warn (the
                                     default; fix file if we can, warn
                                     otherwise)
    --prefer-avconv                  Prefer avconv over ffmpeg for running the
                                     postprocessors (default)
    --prefer-ffmpeg                  Prefer ffmpeg over avconv for running the
                                     postprocessors
    --ffmpeg-location PATH           Location of the ffmpeg/avconv binary;
                                     either the path to the binary or its
                                     containing directory.
    --exec CMD                       Execute a command on the file after
                                     downloading, similar to find's -exec
                                     syntax. Example: --exec 'adb push {}
                                     /sdcard/Music/ && rm {}'
    --convert-subs FORMAT            Convert the subtitles to other format
                                     (currently supported: srt|ass|vtt)

# CONFIGURATION

You can configure avideo by placing any supported command line option to a configuration file. The system wide configuration file is located at `/etc/avideo.conf` and the user wide configuration file at `~/.config/avideo/config`. Note that by default configuration file may not exist so you may need to create it yourself.

For example, with the following configuration file avideo will always extract the audio, not copy the mtime, use a proxy and save all videos under `Movies` directory in your home directory:
```
# Lines starting with # are comments

# Always extract audio
-x

# Do not copy the mtime
--no-mtime

# Use this proxy
--proxy 127.0.0.1:3128

# Save all videos under Movies directory in your home directory
-o ~/Movies/%(title)s.%(ext)s
```

Note that options in configuration file are just the same options aka switches used in regular command line calls thus there **must be no whitespace** after `-` or `--`, e.g. `-o` or `--proxy` but not `- o` or `-- proxy`.

You can use `--ignore-config` if you want to disable the configuration file for a particular avideo run.

You can also use `--config-location` if you want to use custom configuration file for a particular avideo run.

### Authentication with `.netrc` file

You may also want to configure automatic credentials storage for extractors that support authentication (by providing login and password with `--username` and `--password`) in order not to pass credentials as command line arguments on every avideo execution and prevent tracking plain text passwords in the shell command history. You can achieve this using a [`.netrc` file](http://stackoverflow.com/tags/.netrc/info) on a per extractor basis. For that you will need to create a `.netrc` file in your `$HOME` and restrict permissions to read/write by only you:
```
touch $HOME/.netrc
chmod a-rwx,u+rw $HOME/.netrc
```
After that you can add credentials for an extractor in the following format, where *extractor* is the name of the extractor in lowercase:
```
machine <extractor> login <login> password <password>
```
For example:
```
machine youtube login myaccount@gmail.com password my_youtube_password
machine twitch login my_twitch_account_name password my_twitch_password
```
To activate authentication with the `.netrc` file you should pass `--netrc` to avideo or place it in the [configuration file](#configuration).

# OUTPUT TEMPLATE

The `-o` option allows users to indicate a template for the output file names.

**tl;dr:** [navigate me to examples](#output-template-examples).

The basic usage is not to set any template arguments when downloading a single file, like in `avideo -o funny_video.flv "http://some/video"`. However, it may contain special sequences that will be replaced when downloading each video. The special sequences may be formatted according to [python string formatting operations](https://docs.python.org/2/library/stdtypes.html#string-formatting). For example, `%(NAME)s` or `%(NAME)05d`. To clarify, that is a percent symbol followed by a name in parentheses, followed by a formatting operations. Allowed names along with sequence type are:

 - `id` (string): Video identifier
 - `title` (string): Video title
 - `url` (string): Video URL
 - `ext` (string): Video filename extension
 - `alt_title` (string): A secondary title of the video
 - `display_id` (string): An alternative identifier for the video
 - `uploader` (string): Full name of the video uploader
 - `license` (string): License name the video is licensed under
 - `creator` (string): The creator of the video
 - `release_date` (string): The date (YYYYMMDD) when the video was released
 - `timestamp` (numeric): UNIX timestamp of the moment the video became available
 - `upload_date` (string): Video upload date (YYYYMMDD)
 - `uploader_id` (string): Nickname or id of the video uploader
 - `location` (string): Physical location where the video was filmed
 - `duration` (numeric): Length of the video in seconds
 - `view_count` (numeric): How many users have watched the video on the platform
 - `like_count` (numeric): Number of positive ratings of the video
 - `dislike_count` (numeric): Number of negative ratings of the video
 - `repost_count` (numeric): Number of reposts of the video
 - `average_rating` (numeric): Average rating give by users, the scale used depends on the webpage
 - `comment_count` (numeric): Number of comments on the video
 - `age_limit` (numeric): Age restriction for the video (years)
 - `format` (string): A human-readable description of the format 
 - `format_id` (string): Format code specified by `--format`
 - `format_note` (string): Additional info about the format
 - `width` (numeric): Width of the video
 - `height` (numeric): Height of the video
 - `resolution` (string): Textual description of width and height
 - `tbr` (numeric): Average bitrate of audio and video in KBit/s
 - `abr` (numeric): Average audio bitrate in KBit/s
 - `acodec` (string): Name of the audio codec in use
 - `asr` (numeric): Audio sampling rate in Hertz
 - `vbr` (numeric): Average video bitrate in KBit/s
 - `fps` (numeric): Frame rate
 - `vcodec` (string): Name of the video codec in use
 - `container` (string): Name of the container format
 - `filesize` (numeric): The number of bytes, if known in advance
 - `filesize_approx` (numeric): An estimate for the number of bytes
 - `protocol` (string): The protocol that will be used for the actual download
 - `extractor` (string): Name of the extractor
 - `extractor_key` (string): Key name of the extractor
 - `epoch` (numeric): Unix epoch when creating the file
 - `autonumber` (numeric): Five-digit number that will be increased with each download, starting at zero
 - `playlist` (string): Name or id of the playlist that contains the video
 - `playlist_index` (numeric): Index of the video in the playlist padded with leading zeros according to the total length of the playlist
 - `playlist_id` (string): Playlist identifier
 - `playlist_title` (string): Playlist title


Available for the video that belongs to some logical chapter or section:
 - `chapter` (string): Name or title of the chapter the video belongs to
 - `chapter_number` (numeric): Number of the chapter the video belongs to
 - `chapter_id` (string): Id of the chapter the video belongs to

Available for the video that is an episode of some series or programme:
 - `series` (string): Title of the series or programme the video episode belongs to
 - `season` (string): Title of the season the video episode belongs to
 - `season_number` (numeric): Number of the season the video episode belongs to
 - `season_id` (string): Id of the season the video episode belongs to
 - `episode` (string): Title of the video episode
 - `episode_number` (numeric): Number of the video episode within a season
 - `episode_id` (string): Id of the video episode

Available for the media that is a track or a part of a music album:
 - `track` (string): Title of the track
 - `track_number` (numeric): Number of the track within an album or a disc
 - `track_id` (string): Id of the track
 - `artist` (string): Artist(s) of the track
 - `genre` (string): Genre(s) of the track
 - `album` (string): Title of the album the track belongs to
 - `album_type` (string): Type of the album
 - `album_artist` (string): List of all artists appeared on the album
 - `disc_number` (numeric): Number of the disc or other physical medium the track belongs to
 - `release_year` (numeric): Year (YYYY) when the album was released

Each aforementioned sequence when referenced in an output template will be replaced by the actual value corresponding to the sequence name. Note that some of the sequences are not guaranteed to be present since they depend on the metadata obtained by a particular extractor. Such sequences will be replaced with `NA`.

For example for `-o %(title)s-%(id)s.%(ext)s` and an mp4 video with title `avideo test video` and id `BaW_jenozKcj`, this will result in a `avideo test video-BaW_jenozKcj.mp4` file created in the current directory.

For numeric sequences you can use numeric related formatting, for example, `%(view_count)05d` will result in a string with view count padded with zeros up to 5 characters, like in `00042`.

Output templates can also contain arbitrary hierarchical path, e.g. `-o '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s'` which will result in downloading each video in a directory corresponding to this path template. Any missing directory will be automatically created for you.

To use percent literals in an output template use `%%`. To output to stdout use `-o -`.

The current default template is `%(title)s-%(id)s.%(ext)s`.

In some cases, you don't want special characters such as 中, spaces, or &, such as when transferring the downloaded filename to a Windows system or the filename through an 8bit-unsafe channel. In these cases, add the `--restrict-filenames` flag to get a shorter title:

#### Output template examples

```bash
$ avideo --get-filename -o '%(title)s.%(ext)s' BaW_jenozKc
avideo test video ''_ä↭𝕐.mp4    # All kinds of weird characters

$ avideo --get-filename -o '%(title)s.%(ext)s' BaW_jenozKc --restrict-filenames
avideo_test_video_.mp4          # A simple file name

# Download YouTube playlist videos in separate directory indexed by video order in a playlist
$ avideo -o '%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' https://www.youtube.com/playlist?list=PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re

# Download all playlists of YouTube channel/user keeping each playlist in separate directory:
$ avideo -o '%(uploader)s/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' https://www.youtube.com/user/TheLinuxFoundation/playlists

# Download Udemy course keeping each chapter in separate directory under MyVideos directory in your home
$ avideo -u user -p password -o '~/MyVideos/%(playlist)s/%(chapter_number)s - %(chapter)s/%(title)s.%(ext)s' https://www.udemy.com/java-tutorial/

# Download entire series season keeping each series and each season in separate directory under C:/MyVideos
$ avideo -o "C:/MyVideos/%(series)s/%(season_number)s - %(season)s/%(episode_number)s - %(episode)s.%(ext)s" http://videomore.ru/kino_v_detalayah/5_sezon/367617

# Stream the video being downloaded to stdout
$ avideo -o - BaW_jenozKc
```

# FORMAT SELECTION

By default avideo tries to download the best available quality, i.e. if you want the best quality you **don't need** to pass any special options, avideo will guess it for you by **default**.

But sometimes you may want to download in a different format, for example when you are on a slow or intermittent connection. The key mechanism for achieving this is so-called *format selection* based on which you can explicitly specify desired format, select formats based on some criterion or criteria, setup precedence and much more.

The general syntax for format selection is `--format FORMAT` or shorter `-f FORMAT` where `FORMAT` is a *selector expression*, i.e. an expression that describes format or formats you would like to download.

**tl;dr:** [navigate me to examples](#format-selection-examples).

The simplest case is requesting a specific format, for example with `-f 22` you can download the format with format code equal to 22. You can get the list of available format codes for particular video using `--list-formats` or `-F`. Note that these format codes are extractor specific. 

You can also use a file extension (currently `3gp`, `aac`, `flv`, `m4a`, `mp3`, `mp4`, `ogg`, `wav`, `webm` are supported) to download the best quality format of a particular file extension served as a single file, e.g. `-f webm` will download the best quality format with the `webm` extension served as a single file.

You can also use special names to select particular edge case formats:
 - `best`: Select the best quality format represented by a single file with video and audio.
 - `worst`: Select the worst quality format represented by a single file with video and audio.
 - `bestvideo`: Select the best quality video-only format (e.g. DASH video). May not be available.
 - `worstvideo`: Select the worst quality video-only format. May not be available.
 - `bestaudio`: Select the best quality audio only-format. May not be available.
 - `worstaudio`: Select the worst quality audio only-format. May not be available.

For example, to download the worst quality video-only format you can use `-f worstvideo`.

If you want to download multiple videos and they don't have the same formats available, you can specify the order of preference using slashes. Note that slash is left-associative, i.e. formats on the left hand side are preferred, for example `-f 22/17/18` will download format 22 if it's available, otherwise it will download format 17 if it's available, otherwise it will download format 18 if it's available, otherwise it will complain that no suitable formats are available for download.

If you want to download several formats of the same video use a comma as a separator, e.g. `-f 22,17,18` will download all these three formats, of course if they are available. Or a more sophisticated example combined with the precedence feature: `-f 136/137/mp4/bestvideo,140/m4a/bestaudio`.

You can also filter the video formats by putting a condition in brackets, as in `-f "best[height=720]"` (or `-f "[filesize>10M]"`).

The following numeric meta fields can be used with comparisons `<`, `<=`, `>`, `>=`, `=` (equals), `!=` (not equals):
 - `filesize`: The number of bytes, if known in advance
 - `width`: Width of the video, if known
 - `height`: Height of the video, if known
 - `tbr`: Average bitrate of audio and video in KBit/s
 - `abr`: Average audio bitrate in KBit/s
 - `vbr`: Average video bitrate in KBit/s
 - `asr`: Audio sampling rate in Hertz
 - `fps`: Frame rate

Also filtering work for comparisons `=` (equals), `!=` (not equals), `^=` (begins with), `$=` (ends with), `*=` (contains) and following string meta fields:
 - `ext`: File extension
 - `acodec`: Name of the audio codec in use
 - `vcodec`: Name of the video codec in use
 - `container`: Name of the container format
 - `protocol`: The protocol that will be used for the actual download, lower-case (`http`, `https`, `rtsp`, `rtmp`, `rtmpe`, `mms`, `f4m`, `ism`, `m3u8`, or `m3u8_native`)
 - `format_id`: A short description of the format

Note that none of the aforementioned meta fields are guaranteed to be present since this solely depends on the metadata obtained by particular extractor, i.e. the metadata offered by the video hoster.

Formats for which the value is not known are excluded unless you put a question mark (`?`) after the operator. You can combine format filters, so `-f "[height <=? 720][tbr>500]"` selects up to 720p videos (or videos where the height is not known) with a bitrate of at least 500 KBit/s.

You can merge the video and audio of two formats into a single file using `-f <video-format>+<audio-format>` (requires ffmpeg or avconv installed), for example `-f bestvideo+bestaudio` will download the best video-only format, the best audio-only format and mux them together with ffmpeg/avconv.

Format selectors can also be grouped using parentheses, for example if you want to download the best mp4 and webm formats with a height lower than 480 you can use `-f '(mp4,webm)[height<480]'`.

Since the end of April 2015 and version 2015.04.26, avideo uses `-f bestvideo+bestaudio/best` as the default format selection (see [#5447](https://github.com/rg3/youtube-dl/issues/5447), [#5456](https://github.com/rg3/youtube-dl/issues/5456)). If ffmpeg or avconv are installed this results in downloading `bestvideo` and `bestaudio` separately and muxing them together into a single file giving the best overall quality available. Otherwise it falls back to `best` and results in downloading the best available quality served as a single file. `best` is also needed for videos that don't come from YouTube because they don't provide the audio and video in two different files. If you want to only download some DASH formats (for example if you are not interested in getting videos with a resolution higher than 1080p), you can add `-f bestvideo[height<=?1080]+bestaudio/best` to your configuration file. Note that if you use avideo to stream to `stdout` (and most likely to pipe it to your media player then), i.e. you explicitly specify output template as `-o -`, avideo still uses `-f best` format selection in order to start content delivery immediately to your player and not to wait until `bestvideo` and `bestaudio` are downloaded and muxed.

If you want to preserve the old format selection behavior (prior to avideo 2015.04.26), i.e. you want to download the best available quality media served as a single file, you should explicitly specify your choice with `-f best`. You may want to add it to the [configuration file](#configuration) in order not to type it every time you run avideo.

#### Format selection examples

```bash
# Download best mp4 format available or any other best if no mp4 available
$ avideo -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

# Download best format available but not better that 480p
$ avideo -f 'bestvideo[height<=480]+bestaudio/best[height<=480]'

# Download best video only format but no bigger than 50 MB
$ avideo -f 'best[filesize<50M]'

# Download best format available via direct link over HTTP/HTTPS protocol
$ avideo -f '(bestvideo+bestaudio/best)[protocol^=http]'

# Download the best video format and the best audio format without merging them
$ avideo -f 'bestvideo,bestaudio' -o '%(title)s.f%(format_id)s.%(ext)s'
```
Note that in the last example, an output template is recommended as bestvideo and bestaudio may have the same file name.


# VIDEO SELECTION

Videos can be filtered by their upload date using the options `--date`, `--datebefore` or `--dateafter`. They accept dates in two formats:

 - Absolute dates: Dates in the format `YYYYMMDD`.
 - Relative dates: Dates in the format `(now|today)[+-][0-9](day|week|month|year)(s)?`
 
Examples:

```bash
# Download only the videos uploaded in the last 6 months
$ avideo --dateafter now-6months

# Download only the videos uploaded on January 1, 1970
$ avideo --date 19700101

$ # Download only the videos uploaded in the 200x decade
$ avideo --dateafter 20000101 --datebefore 20091231
```

# FAQ

### Why did you remove the JS/SWF/SDK interpreters when they are required for some functionality?

These interpreters run contrary to avideo's aim to deliver freedom as a number 1 priority.

It was discovered in 2017 on the [Trisquel GNU/Linux fora](https://trisquel.info/en/forum/do-youtube-dlhtml5-video-everywhere-run-nonfree-js) that youtube\-dl included the quite unexpected functionality to run JavaScript.
Further investigation by Grace Past revealed this to be a component of [DRM on YouTube](https://superuser.com/questions/773719/how-do-all-of-these-save-video-from-youtube-services-work#answer-773998), meaning the non-free code sourced from YouTube is an
[unethical means](https://www.gnu.org/philosophy/proprietary.html) to an [unethical end](https://www.defectivebydesign.org/what_is_drm_digital_restrictions_management). Thus, in order to provide you with control over your computer, such a sacrifice unfortunately must be made.
[Further research by rain1](http://lists.nongnu.org/archive/html/gnu-linux-libre/2017-07/msg00003.html) has made the scope of this initial assessment more precise, suggesting that the interpreter is not as bad as perhaps thought, albeit still unacceptable and even plausibly a vector for exploits.

Similar reasoning applies to the other cases of interpreters for non-free software packaged with the parent. If any methods of addressing these issues arise that allow them to be attacked without compromising core values, they shall be promptly implemented;
however, aside from such a possible workaround, it is avideo's aim to avoid compromising [user freedom](https://www.gnu.org/philosophy/free-sw.html).

### How do I update avideo?

If you've followed [our manual installation instructions](#installation) for apt-based systems, simply run `sudo apt update` to update. If you used the instructions for source packages, you will need to check the [Downloads Page](https://notabug.org/GPast/avideo/wiki/Downloads) for the most recent version. If it is newer than what is installed, download the latest version and follow [our manual installation instructions](#installation) to install over the outdated variant.

If you have installed avideo using a package manager like *apt-get* or *yum*, use the standard system update mechanism to update. Distribution packages may be outdated.

For installations made using pip, the command `sudo pip install -U avideo` will update to the latest version.

As a last resort, you can also uninstall the version installed by your package manager and follow our manual installation instructions. For that, remove the distribution's package, with a line like

    sudo apt-get remove -y avideo

Afterwards, simply follow [our manual installation instructions](#installation).

### I'm getting an error when trying to use output template: `error: using output template conflicts with using title, video ID or auto number`

Make sure you are not using `-o` with any of these options `-t`, `--title`, `--id`, `-A` or `--auto-number` set in command line or in a configuration file. Remove the latter if any.

### Do I always have to pass `-citw`?

By default, avideo intends to have the best options (incidentally, if you have a convincing case that these should be different, [please file an issue where you explain that](https://notabug.org/GPast/avideo/issues)). Therefore, it is unnecessary and sometimes harmful to copy long option strings from webpages. In particular, the only option out of `-citw` that is regularly useful is `-i`.

### I get HTTP error 402 when trying to download a video. What's this?

Apparently YouTube requires you to pass a CAPTCHA test if you download too much. We're [considering to provide a way to let you solve the CAPTCHA](https://github.com/rg3/youtube-dl/issues/154), but at the moment, your best course of action is pointing a web browser to the youtube URL, solving the CAPTCHA, and restart avideo.

### Do I need any other programs?

avideo works fine on its own on most sites. However, if you want to convert video/audio, you'll need [avconv](https://libav.org/) or [ffmpeg](https://www.ffmpeg.org/). On some sites - most notably YouTube - videos can be retrieved in a higher quality format without sound. avideo will detect whether avconv/ffmpeg is present and automatically pick the best option.

Videos or video formats streamed via RTMP protocol can only be downloaded when [rtmpdump](https://rtmpdump.mplayerhq.hu/) is installed. Downloading MMS and RTSP videos requires either [mplayer](http://mplayerhq.hu/) or [mpv](https://mpv.io/) to be installed.

### I have downloaded a video but how can I play it?

Once the video is fully downloaded, use any video player, such as [mpv](https://mpv.io/), [vlc](http://www.videolan.org/) or [mplayer](http://www.mplayerhq.hu/).

### I extracted a video URL with `-g`, but it does not play on another machine / in my web browser.

It depends a lot on the service. In many cases, requests for the video (to download/play it) must come from the same IP address and with the same cookies and/or HTTP headers. Use the `--cookies` option to write the required cookies into a file, and advise your downloader to read cookies from that file. Some sites also require a common user agent to be used, use `--dump-user-agent` to see the one in use by avideo. You can also get necessary cookies and HTTP headers from JSON output obtained with `--dump-json`.

It may be beneficial to use IPv6; in some cases, the restrictions are only applied to IPv4. Some services (sometimes only for a subset of videos) do not restrict the video URL by IP address, cookie, or user-agent, but these are the exception rather than the rule.

Please bear in mind that some URL protocols are **not** supported by browsers out of the box, including RTMP. If you are using `-g`, your own downloader must support these as well.

If you want to play the video on a machine that is not running avideo, you can relay the video content from the machine that runs avideo. You can use `-o -` to let avideo stream a video to stdout, or simply allow the player to download the files written by avideo in turn.

### Video URL contains an ampersand and I'm getting some strange output `[1] 2839` or `'v' is not recognized as an internal or external command`

That's actually the output from your shell. Since ampersand is one of the special shell characters it's interpreted by the shell preventing you from passing the whole URL to avideo. To disable your shell from interpreting the ampersands (or any other special characters) you have to either put the whole URL in quotes or escape them with a backslash (which approach will work depends on your shell).

For example if your URL is https://www.youtube.com/watch?t=4&v=BaW_jenozKc you should end up with following command:

```avideo 'https://www.youtube.com/watch?t=4&v=BaW_jenozKc'```

or

```avideo https://www.youtube.com/watch?t=4\&v=BaW_jenozKc```

### `Youtube's DRM has prevented this software from obtaining the video URL` or `iQiyi's non-free authentication algorithm has made login impossible`

Either of these error messages indicates the service providing the video is demanding you run proprietary software.

YouTube applies what is termed *signature encryption* to some (mainly music) videos. In order to get the URL of the actual video, the video ID (the sequence of letters and numbers in the link to the video page) has to be unscrambled by the user using a script provided by YouTube. Although relatively menial, the code can be changed at any time by YouTube.

iQiyi requires some number\-shifting in order to authenticate users. Like YouTube's signature extraction, this is performed by the client with a script from the service. The script is quite menial, but can be changed at any time by the service\- preventing the user from knowing what it does.

If you encounter either of these errors, we recommend you contact the service you were using and express your discontent. There is currently no practical way to work around these issues whilst still ensuring the user possesses the [four software freedoms](https://www.gnu.org/philosophy/free-sw) they deserve, and so the services must change.

### HTTP Error 429: Too Many Requests or 402: Payment Required

These two error codes indicate that the service is blocking your IP address because of overuse. Contact the service and ask them to unblock your IP address, or - if you have acquired a whitelisted IP address already - use the [`--proxy` or `--source-address` options](#network-options) to select another IP address.

### SyntaxError: Non-ASCII character

The error

    File "avideo", line 2
    SyntaxError: Non-ASCII character '\x93' ...

means you're using an outdated version of Python. Please update to Python 2.6 or 2.7.

### How do I put downloads into a specific folder?

Use the `-o` to specify an [output template](#output-template), for example `-o "/home/user/videos/%(title)s-%(id)s.%(ext)s"`. If you want this for all of your downloads, put the option into your [configuration file](#configuration).

### How do I download a video starting with a `-`?

Either prepend `http://www.youtube.com/watch?v=` or separate the ID from the options with `--`:

    avideo -- -wNyEUrxzFU
    avideo "http://www.youtube.com/watch?v=-wNyEUrxzFU"

### How do I pass cookies to avideo?

Use the `--cookies` option, for example `--cookies /path/to/cookies/file.txt`.

In order to extract cookies from browser use any conforming browser extension for exporting cookies. For example, [cookies.txt](https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg) (for Chrome) or [Export Cookies](https://addons.mozilla.org/en-US/firefox/addon/export-cookies/) (for Firefox).

Note that the cookies file must be in Mozilla/Netscape format and the first line of the cookies file must be either `# HTTP Cookie File` or `# Netscape HTTP Cookie File`. Make sure you have correct [newline format](https://en.wikipedia.org/wiki/Newline) in the cookies file and convert newlines if necessary to correspond with your OS, namely `LF` (`\n`). `HTTP Error 400: Bad Request` when using `--cookies` is a good sign of invalid newline format.

Passing cookies to avideo is a good way to workaround login when a particular extractor does not implement it explicitly. Another use case is working around [CAPTCHA](https://en.wikipedia.org/wiki/CAPTCHA) some websites require you to solve in particular cases in order to get access (e.g. YouTube, CloudFlare).

### How do I stream directly to media player?

You will first need to tell avideo to stream media to stdout with `-o -`, and also tell your media player to read from stdin (it must be capable of this for streaming) and then pipe former to latter. For example, streaming to [vlc](http://www.videolan.org/) can be achieved with:

    avideo -o - "http://www.youtube.com/watch?v=BaW_jenozKcj" | vlc -

### How do I download only new videos from a playlist?

Use download-archive feature. With this feature you should initially download the complete playlist with `--download-archive /path/to/download/archive/file.txt` that will record identifiers of all the videos in a special file. Each subsequent run with the same `--download-archive` will download only new videos and skip all videos that have been downloaded before. Note that only successful downloads are recorded in the file.

For example, at first,

    avideo --download-archive archive.txt "https://www.youtube.com/playlist?list=PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re"

will download the complete `PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re` playlist and create a file `archive.txt`. Each subsequent run will only download new videos if any:

    avideo --download-archive archive.txt "https://www.youtube.com/playlist?list=PLwiyx1dc3P2JR9N8gQaQN_BCvlSlap7re"

### Should I add `--hls-prefer-native` into my config?

When avideo detects an HLS video, it can download it either with the built-in downloader or ffmpeg. Since many HLS streams are slightly invalid and ffmpeg/avideo each handle some invalid cases better than the other, there is an option to switch the downloader if needed.

When avideo knows that one particular downloader works better for a given website, that downloader will be picked. Otherwise, avideo will pick the best downloader for general compatibility, which at the moment happens to be ffmpeg. This choice may change in future versions of avideo, with improvements of the built-in downloader and/or ffmpeg.

In particular, the generic extractor (used when your website is not in the [list of supported sites by avideo](http://notabug.org/GPast/avideo/wiki/Supported+Sites) cannot mandate one specific downloader.

If you put either `--hls-prefer-native` or `--hls-prefer-ffmpeg` into your configuration, a different subset of videos will fail to download correctly. Instead, it is much better to [file an issue](https://notabug.org/GPast/avideo/issues) or a pull request which details why the native or the ffmpeg HLS downloader is a better choice for your use case.

### Can you add support for this anime video site, or site which shows current movies for free?

As a matter of legality, avideo does not include support for services that specialize in infringing copyright. As a rule of thumb, if you cannot easily find a video that the service is quite obviously allowed to distribute (i.e. that has been uploaded by the creator, the creator's distributor, or is published under a free license), the service is probably unfit for inclusion to avideo.

A note on the service that they don't host infringe, but just link to those who do, is evidence that the service should **not** be included into avideo. The same goes for any DMCA note when the whole front page of the service is filled with videos they are not allowed to distribute. A "fair use" note is equally unconvincing if the service shows copyright-protected videos in full without authorization.

Support requests for services that **do** purchase the rights for distribution are perfectly fine though. If in doubt, you can simply include a source that mentions the legitimate purchase of hosted media.

### How can I speed up work on my issue?

(Also known as: Help, my important issue not being solved!) The avideo core developer team is quite small. While we do our best to solve as many issues as possible, sometimes that can take quite a while. To speed up your issue, here's what you can do:

First of all, please do report the issue [at our issue tracker](https://notabug.org/GPast/avideo/issues). That allows us to coordinate all efforts by users and developers, and serves as a unified point. Unfortunately, the avideo project has grown too large to use personal email as an effective communication channel.

Please read the [bug reporting instructions](#bugs) below. A lot of bugs lack all the necessary information. If you can, offer proxy, VPN, or shell access to the avideo developers. If you are able to, test the issue from multiple computers in multiple countries to exclude local censorship or misconfiguration issues.

If nobody is interested in solving your issue, you are welcome to take matters into your own hands and submit a pull request (or coerce/pay somebody else to do so).

Feel free to bump the issue from time to time by writing a small comment ("Issue is still present in avideo version ...from France, but fixed from Belgium"), but please not more than once a month. Please do not declare your issue as `important` or `urgent`.

### How can I detect whether a given URL is supported by avideo?

For one, have a look at the [list of supported sites](https://notabug.org/GPast/avideo/wiki/Supported+Sites). Note that it can sometimes happen that the site changes its URL scheme (say, from http://example.com/video/1234567 to http://example.com/v/1234567 ) and avideo reports an URL of a service in that list as unsupported. In that case, simply report a bug.

It is *not* possible to detect whether a URL is supported or not. That's because avideo contains a generic extractor which matches **all** URLs. You may be tempted to disable, exclude, or remove the generic extractor, but the generic extractor not only allows users to extract videos from lots of websites that embed a video from another service, but may also be used to extract video from a service that it's hosting itself. Therefore, we neither recommend nor support disabling, excluding, or removing the generic extractor.

If you want to find out whether a given URL is supported, simply call avideo with it. If you get no videos back, chances are the URL is either not referring to a video or unsupported. You can find out which by examining the output (if you run avideo on the console) or catching an `UnsupportedError` exception if you run it from a Python program.

# Why do I need to go through that much red tape when filing bugs?

Before we had the issue template, despite our extensive [bug reporting instructions](#bugs), about 80% of the issue reports we got were useless, for instance because people used ancient versions hundreds of releases old, because of simple syntactic errors (not in avideo but in general shell usage), because the problem was already reported multiple times before, because people did not actually read an error message, even if it said "please install ffmpeg", because people did not mention the URL they were trying to download and many more simple, easy-to-avoid problems, many of whom were totally unrelated to avideo.

avideo is a free software project manned by too few volunteers, so we'd rather spend time fixing bugs where we are certain none of those simple problems apply, and where we can be reasonably confident to be able to reproduce the issue without asking the reporter repeatedly. As such, the output of `avideo -v YOUR_URL_HERE` is really all that's required to file an issue. The issue template also guides you through some basic steps you can do, such as checking that your version of avideo is current.

# DEVELOPER INSTRUCTIONS

To run the program as a developer, you don't need to build anything. Simply execute

    python -m avideo

To run the test, simply invoke your favorite test runner, or execute a test file directly; any of the following work:

    python -m unittest discover
    python test/test_download.py
    nosetests

If you want to create a build of avideo yourself, you'll need

* python
* make (only GNU make is supported)
* pandoc
* nosetests

For information on contributing, please see the [Developer Documentation](https://notabug.org/GPast/avideo/wiki/Developer+Documentation).

### CODING CONVENTIONS

Although they aren't strictly enforced, avideo asks that all developers aim to comply with the GNU coding conventions.

# EMBEDDING AVIDEO

avideo makes the best effort to be a good command-line program, and thus should be callable from any programming language. If you encounter any problems parsing its output, feel free to [create a report](https://notabug.org/GPast/avideo/issues/new).

From a Python program, you can embed avideo in a more powerful fashion, like this:

```python
from __future__ import unicode_literals
import avideo

ydl_opts = {}
with avideo.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
```

Most likely, you'll want to use various options. For a list of options available, have a look at [`avideo/YoutubeDL.py`](https://notabug.org/GPast/avideo/src/master/avideo/YoutubeDL.py#L129-L279) \(TODO: Find somewhere to host the tarball opened\). For a start, if you want to intercept avideo's output, set a `logger` object.

Here's a more complete example of a program that outputs only errors (and a short message after the download is finished), and downloads/converts the video to an mp3 file:

```python
from __future__ import unicode_literals
import avideo


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
}
with avideo.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])
```

# BUGS

Bugs and suggestions should be reported at: <https://notabug.org/GPast/avideo/issues>. Unless you were prompted to or there is another pertinent reason (e.g. GitHub fails to accept the bug report), please do not send bug reports via personal email.

**Please include the full output of avideo when run with `-v`**, i.e. **add** `-v` flag to **your command line**, copy the **whole** output and post it in the issue body wrapped in \`\`\` for better formatting. It should look similar to this:
```
$ avideo -v <your command line>
[debug] System config: []
[debug] User config: []
[debug] Command-line args: [u'-v', u'http://www.youtube.com/watch?v=BaW_jenozKcj']
[debug] Encodings: locale cp1251, fs mbcs, out cp866, pref cp1251
[debug] avideo version 2015.12.06
[debug] Git HEAD: 135392e
[debug] Python version 2.6.6 - Windows-2003Server-5.2.3790-SP2
[debug] exe versions: ffmpeg N-75573-g1d0487f, ffprobe N-75573-g1d0487f, rtmpdump 2.4
[debug] Proxy map: {}
...
```
**Do not post screenshots of verbose logs; only plain text is acceptable.**

The output (including the first lines) contains important debugging information. Issues without the full output are often not reproducible and therefore do not get solved in short order, if ever.

Please re-read your issue once again to avoid a couple of common mistakes (you can and should use this as a checklist):

### Is the description of the issue itself sufficient?

We often get issue reports that we cannot really decipher. While in most cases we eventually get the required information after asking back multiple times, this poses an unnecessary drain on our resources. Many contributors, including myself, are also not native speakers, so we may misread some parts.

So please elaborate on what feature you are requesting, or what bug you want to be fixed. Make sure that it's obvious

- What the problem is
- How it could be fixed
- How your proposed solution would look like

If your report is shorter than two lines, it is almost certainly missing some of these, which makes it hard for us to respond to it. We're often too polite to close the issue outright, but the missing info makes misinterpretation likely. As a committer myself, I often get frustrated by these issues, since the only possible way for me to move forward on them is to ask for clarification over and over.

For bug reports, this means that your report should contain the *complete* output of avideo when called with the `-v` flag. The error message you get for (most) bugs even says so, but you would not believe how many of our bug reports do not contain this information.

If your server has multiple IPs or you suspect censorship, adding `--call-home` may be a good idea to get more diagnostics. If the error is `ERROR: Unable to extract ...` and you cannot reproduce it from multiple countries, add `--dump-pages` (warning: this will yield a rather large output, redirect it to the file `log.txt` by adding `>log.txt 2>&1` to your command-line) or upload the `.dump` files you get when you add `--write-pages` [somewhere](https://gist.github.com/) \(TODO: am I libre?\).

**Site support requests must contain an example URL**. An example URL is a URL you might want to download, like `http://www.youtube.com/watch?v=BaW_jenozKc`. There should be an obvious video present. Except under very special circumstances, the main page of a video service (e.g. `http://www.youtube.com/`) is *not* an example URL.

###  Are you using the latest version?

Before logging any issue, check that the version reported by `avideo -v`is listed as the latest on the [Downloads Page](https://notabug.org/GPast/avideo/wiki/Downloads). About 20% of the reports we receive are already fixed, but people are using outdated versions. This goes for feature requests as well.

###  Is the issue already documented?

Make sure that someone has not already opened the issue you're trying to open. Search at the top of the window or browse the [Issues](https://notabug.org/GPast/avideo/issues) of this repository. If there is an issue, feel free to write something along the lines of "This affects me as well, with version 2015.01.01. Here is some more information on the issue: ...". While some issues may be old, a new post into them often spurs rapid activity.

###  Why are existing options not enough?

Before requesting a new feature, please have a quick peek at [the list of supported options](#options). Many feature requests are for features that actually exist already! Please, absolutely do show off your work in the issue report and detail how the existing similar options do *not* solve your problem.

###  Is there enough context in your bug report?

People want to solve problems, and often think they do us a favor by breaking down their larger problems (e.g. wanting to skip already downloaded files) to a specific request (e.g. requesting us to look whether the file exists before downloading the info page). However, what often happens is that they break down the problem into two steps: One simple, and one impossible (or extremely complicated one).

We are then presented with a very complicated request when the original problem could be solved far easier, e.g. by recording the downloaded video IDs in a separate file. To avoid this, you must include the greater context where it is non-obvious. In particular, every feature request that does not consist of adding support for a new site should contain a use case scenario that explains in what situation the missing feature would be useful.

###  Does the issue involve one problem, and one problem only?

Some of our users seem to think there is a limit of issues they can or should open. There is no limit of issues they can or should open. While it may seem appealing to be able to dump all your issues into one ticket, that means that someone who solves one of your issues cannot mark the issue as closed. Typically, reporting a bunch of issues leads to the ticket lingering since nobody wants to attack that behemoth, until someone mercifully splits the issue into multiple ones.

In particular, every site support request issue should only pertain to services at one site (generally under a common domain, but always using the same backend technology). Do not request support for vimeo user videos, White house podcasts, and Google Plus pages in the same issue. Also, make sure that you don't post bug reports alongside feature requests. As a rule of thumb, a feature request does not include outputs of avideo that are not immediately related to the feature at hand. Do not post reports of a network error alongside the request for a new video service.

###  Is anyone going to need the feature?

Only post features that you (or an incapacitated friend you can personally talk to) require. Do not post features because they seem like a good idea. If they are really useful, they will be requested by someone who requires them.

###  Is your question about avideo?

It may sound strange, but some bug reports we receive are completely unrelated to avideo and relate to a different, or even the reporter's own, application. Please make sure that you are actually using avideo. If you are using a UI for avideo, report the bug to the maintainer of the actual application providing the UI. On the other hand, if your UI for avideo fails in some way you believe is related to avideo, by all means, go ahead and report the bug.

# COPYRIGHT

avideo is released by the copyright holders under the GPLv3 as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
