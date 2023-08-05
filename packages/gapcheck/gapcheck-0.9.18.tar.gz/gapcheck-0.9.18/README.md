# GAPCHECK

[![pypi-version][badge-pypi-version]][pypi]
[![License][badge-license]][license]

Check gap between tracks. Join the tracks if you want.

## Motivation

My hated (and loved at the same time) stereo.

## Description

Test if one song continues with the next. Like all songs from
*The Dark Side of the Moon*. Optionally join songs.

## System requirements

* Python3
* [SoX] binary
* [shntool] binary

## Installation

```shell
$ pip install gapcheck
```

## Help
### Usage
```
usage: gapcheck [-h] [-e EXTENSION] [-p PATH] [-s SECONDS] [-a MAX_AMPLITUDE]
                [-f] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -e EXTENSION, --file-extension EXTENSION
                        File extension (default FLAC)
  -p PATH, --path PATH  Path (default current path)
  -s SECONDS, --last-analyzed-seconds SECONDS
                        Last analyzed seconds (default 0.2)
  -a MAX_AMPLITUDE, --limit-maximum-amplitude MAX_AMPLITUDE
                        Limit maximum amplitude (default 0.0099)
  -j, --join-files-with-gap
  -f, --analyze-already-tested
                        Analyze files already tested
  -v, --version         show program's version number and exit
```

### About check gap

To detect if a track has a gap:

 - Analyze the last 0.2 seconds
 - Analyze whether the maximum amplitude is greater than 0.0099

Both values are parameterizable

### About join songs

When joining songs in a new file, the following tags are added:

 - `GAPLESS_JOIN`: Total songs joined
 - `GAPLESS_LAST_TRACK`: Last song joined
 - `GAPLESS_LAST_DISCNUMBER`: Last disc song joined

The title of the song will be the union of all the songs joined.


### Examples
```shell
# Check all flac from current dir recursive, with last 5 seconds
$ gapcheck -p . -e 'flac' -s 5.0

# Check, but ignore files in __backup or with gapcheck.log file present
$ gapcheck -f

# Check and join
$ gapcheck -j
...
```

#### A real example

Let's test it with **Tool**'s masterpiece: *AEnima*.
```shell
$ pwd
music/1996-Tool-AEnima

$ gapcheck
directory: music/1996-Tool-AEnima
date: 2017-06-22 15:09:45
extension: flac
sox_last_seconds: 0.2
sox_max_amplitude: 0.0099
files_checked: 15
files_ignored: 0
files_with_gaps: 3
 - 03-tool-h..flac
 - 04-tool-useful_idiot.flac
 - 08-tool-intermission.flac
```

Another test and join with **Radiohead**'s album *OK Computer*.
```shell
$ pwd
music/1997-Radiohead-OK_Computer

$ gapcheck -j
directory: music/1997-Radiohead-OK_Computer
date: 2017-08-09 09:17:52
extension: flac
sox_last_seconds: 0.2
sox_max_amplitude: 0.0099
files_checked: 12
files_ignored: 0
files_with_gaps: 4
 - 01-radiohead-airbag.flac
 - 04-radiohead-exit_music_(for_a_film).flac
 - 06-radiohead-karma_police.flac
 - 07-radiohead-fitter_happier.flac
file_joined: 01-radiohead-airbag__GAPLESS.flac
 - 01-radiohead-airbag.flac
 - 02-radiohead-paranoid_android.flac
file_joined: 04-radiohead-exit_music_(for_a_film)__GAPLESS.flac
 - 04-radiohead-exit_music_(for_a_film).flac
 - 05-radiohead-let_down.flac
file_joined: 06-radiohead-karma_police__GAPLESS.flac
 - 06-radiohead-karma_police.flac
 - 07-radiohead-fitter_happier.flac
 - 08-radiohead-electioneering.flac
```

## License

MIT

[SoX]:sox.sourceforge.net
[shntool]:http://www.etree.org/shnutils/shntool
[badge-travis]:https://api.travis-ci.org/penicolas/gapcheck.svg?branch=master
[badge-coveralls]:https://coveralls.io/repos/github/penicolas/gapcheck/badge.svg?branch=master
[badge-issues]:http://img.shields.io/github/issues/penicolas/gapcheck.svg
[badge-license]:http://img.shields.io/badge/license-MIT-blue.svg
[badge-pypi-version]:https://img.shields.io/pypi/v/gapcheck.svg
[badge-codacy]:https://api.codacy.com/project/badge/Grade/c44200f768744b00bd7785f6fc39f52a
[travis]:https://travis-ci.org/penicolas/gapcheck
[coveralls]:https://coveralls.io/github/penicolas/gapcheck?branch=master
[codacy]:https://www.codacy.com/app/penicolas/gapcheck?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=penicolas/gapcheck&amp;utm_campaign=Badge_Grade
[heuristics]:https://github.com/penicolas/gapcheck/issues/2
[issues]:https://github.com/penicolas/gapcheck/issues
[pypi]:https://pypi.python.org/pypi?:action=display&name=gapcheck
[license]:LICENSE
