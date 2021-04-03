# BatchAudioSegment
Batch AudioFiles Segmentation

Batch cut audio, make each audio segment has same size.

```python
usage: AudioSegment.py [-h] [-w [SIZE]] [-c [TIME]] [-o [Path]] [Path]

AudioFiles Segmentation

positional arguments:
  [Path]                specify an audio file path or dir path

optional arguments:
  -h, --help            show this help message and exit
  -w [SIZE], --window-size [SIZE]
                        input segment window size(second) (default: 1)
  -c [TIME], --cut-ends [TIME]
                        break off both ends(second) (default: 1)
  -o [Path], --output [Path]
                        specify an output path (default: ./output/)
```
