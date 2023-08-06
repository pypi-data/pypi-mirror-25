# podcast-dl

Command-line program for downloading and tagging podcasts

## System requirements
- Python 3

## Installation

### Ubuntu
    sudo apt update
    sudo apt install -y python python-pip python3 python3-pip
    pip3 install podcast_dl

### CentOS 7
    yum install epel-release
    sudo yum install python34-setuptools
    sudo easy_install-3.4 pip
    pip3 install podcast_dl

### Windows 7+
- Install [chocolatey](https://chocolatey.org/install)
- Launch new `cmd` shell
- Run `choco install python & pip install podcast_dl`

## Options
    Usage: podcast-dl [OPTIONS] SOURCE

    Options:
      -c, --clear                    Clear all tags before writing.
      -m, --match                    Match and import existing files.
      -o, --output <directory>       Download directory.
      -p, --preview                  Preview download and tagging output.
      -q, --quiet                    Disable stdout logging.
      -r, --rename                   Rename episodes with XML data.
      -s, --subdir                   Generate and download to subdirectory.
      -t, --tag                      Tag episodes with XML data.
      -v, --verbose                  Enable verbose logging.
      --drop                         Empty database.
      --limit <int>                  Episode download limit.
      --offline                      Import only mode.
      --offset <int>                 Episode download offset.
      --order [asc|desc]             Episode download order.  [default: desc]
      --purge                        Empty destination folder.
      --track-src [index|release]    Source for track tag.  [default: index]
      --image-src [episode|podcast]  Source for image tag  [default: podcast]
      --album <string>               Override album tag.
      --albumartist <string>         Override album artist tag.
      --artist <string>              Override artist tag.
      --comment <string>             Override comment tag.
      --composer <string>            Override composer tag.
      --genre <string>               Override genre tag.
      --image <file>                 Override image tag.
      -h, --help                     Show this message and exit.

## Examples

### Basic
    $ podcast-dl -ps --limit 1 -o ~/Downloads https://www.npr.org/rss/podcast.php?id=510289
    #586: How Stuff Gets Cheaper
    In: https://play.podtrac.com/npr-510289/npr.mc.tritondigital.com/NPR_510289/media/anon.npr-mp3/npr/pmoney/2017/07/20170705_pmoney_pmmpod586rerun.mp3
    Out: ~/Downloads/planet-money/20170705_pmoney_pmmpod586rerun.mp3

### Renaming
    $ podcast-dl -psr --limit 1 -o ~/Downloads https://www.npr.org/rss/podcast.php?id=510289
    ...
    Out: ~/Downloads/planet-money/2017-07-05 - planet-money - 586-how-stuff-gets-cheaper.mp3

### Tagging
    $ podcast-dl -pst --limit 1 -o ~/Downloads https://www.npr.org/rss/podcast.php?id=510289
    In: https://media.npr.org/assets/img/2015/12/18/planetmoney_sq-c7d1c6f957f3b7f701f8e1d5546695cebd523720.jpg
    Out: ~/Downloads/planet-money/cover.jpg
    ...
    Tags:
    { 'album': 'Planet Money (2017)',
      'albumartist': 'Planet Money',
      'artist': 'Planet Money',
      'comment': 'We visit a company where people work on figuring out how to make '
                 'stuff get cheaper.',
      'composer': 'Planet Money',
      'date': '2017-07-05',
      'genre': 'Podcast',
      'image': '~/Downloads/planet-money/cover.jpg',
      'title': '#586: How Stuff Gets Cheaper',
      'track': 1
    }

### Episode image source
    $ podcast-dl -pstr --image-src episode --limit 1 -o ~/Downloads https://www.npr.org/rss/podcast.php?id=510289
    ...
    In: https://media.npr.org/assets/img/2017/07/05/3944564178_f3be719d7b_o_wide-4a7624a64905abf00f39b3107105dfe33bcb42dd.jpg
    Out: ~/Downloads/planet-money/2017-07-05 - planet-money - 586-how-stuff-gets-cheaper.jpg

    In: https://play.podtrac.com/npr-510289/npr.mc.tritondigital.com/NPR_510289/media/anon.npr-mp3/npr/pmoney/2017/07/20170705_pmoney_pmmpod586rerun.mp3
    Out: ~/Downloads/planet-money/2017-07-05 - planet-money - 586-how-stuff-gets-cheaper.mp3

    Tags:
    { ...
      'image': '~/Downloads/planet-money/2017-07-05 - planet-money - '
               '586-how-stuff-gets-cheaper.jpg'
    }

### Release track source
    $ podcast-dl -pst --track-src release --limit 1 -o ~/Downloads https://www.npr.org/rss/podcast.php?id=510289
    ...
    Tags:
    { ...
      'title': '#586: How Stuff Gets Cheaper',
      'track': '586'
    }