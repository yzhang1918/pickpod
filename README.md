# Pickpod


[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue.svg)]()
[![License](https://img.shields.io/badge/License-MIT-informational.svg)]()
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]()

Integrated tools to transfer internet audio to text, extract unpopular views, and pick up podcasts for you.

**`Pickpod`** helps to build your private wiki efficiently.

This repository contains:

1. A `Python` package that can easily call specified tasks.

2. A `Streamlit` app that provides a web UI to manage your podcast library.

3. Several package usage examples of complete tasks for target audio.

Welcome to our commercial deployment: [Pickpod](https://pickpod.shixiangcap.com/welcome), implementation with `Java` and microservice architecture.

Compared to the personal open-source prototype in this repository, the commercial version provides powerful performance and stable services.


## Table of Contents

- [Background](#background)

- [Install](#install)

- [Usage](#usage)

- [Examples](#examples)

- [Related Efforts](#related-efforts)

- [Maintainers](#maintainers)

- [Contributing](#contributing)

- [License](#license)


## Background

OpenAI released [Whisper](https://openai.com/research/whisper) in September 2022, with good `Speech-To-Text (STT)` performance.

Based on this, the optimization by [CTranslate2](https://github.com/OpenNMT/CTranslate2) for [Transformers](https://huggingface.co/docs/transformers/index) allows [faster-whisper](https://github.com/guillaumekln/faster-whisper) to improve significantly computational efficiency compared to [Whisper](https://openai.com/research/whisper). And [faster-whisper](https://github.com/guillaumekln/faster-whisper) can output transcribed text results step by step while leveraging the local `GPU` to reduce costs.

With the integration of [faster-whisper](https://github.com/guillaumekln/faster-whisper) with [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [pyannote-audio](https://github.com/pyannote/pyannote-audio), **`Pickpod`** can complete tasks from downloading to `STT` and speaker diarization for most audio and video on the internet through a single link, with `JSON` export formats to meet a wide range of needs.

In addition to the standard `STT` service, based on [LISTEN NOTES Podcast API](https://www.listennotes.com/api/docs/), **`Pickpod`** can automatically perform podcast transcription based on user-customized filtering rules, for example, topics of interest, podcast release time, the list of concerned podcasts, etc. Users can obtain transcribed text in batches regularly to improve the efficiency of information acquisition.

Further utilizing the popular `Large Language Model (LLM)`, based on the [Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api), for all audio transcription, in addition to the basic keyword and summary extraction function, **`Pickpod`** has more value in extracting unpopular views from the audio, allowing users to evaluate the results based on matters such as freshness and importance of the information.

The goals for **`Pickpod`** are:

1. High-quality integration with [yt-dlp](https://github.com/yt-dlp/yt-dlp), [faster-whisper](https://github.com/guillaumekln/faster-whisper), and [pyannote-audio](https://github.com/pyannote/pyannote-audio), so that users can quickly obtain the text result of the corresponding audio transcription by simply inputting a link or a local file.

2. Multiple user options support for audio transcription, including language, prompt, whether speaker diarization is required, etc. And provide various formats for export.

3. The convenient use of [LISTEN NOTES Podcast API](https://www.listennotes.com/api/docs/). After the user completes the necessary settings and makes a task, **`Pickpod`** can get the list of eligible podcasts regularly according to the specified release period. Thus, the transcription task can be completed in batch.

4. The convenient use of [Claude API](https://docs.anthropic.com/claude/reference/getting-started-with-the-api). For each transcribed text, **`Pickpod`** can extract the corresponding keywords, summaries, and views based on the built-in prompts for the user's reference and evaluation, and the user can also modify them at any time.

5. Rapid deployment for local environments, so that when the user launches the project, all features are easily accessible in the browser.


## Install

Since [ffmpeg and ffprobe](https://www.ffmpeg.org/) are strongly recommended by [yt-dlp](https://github.com/yt-dlp/yt-dlp#strongly-recommended), it is necessary to install the `ffmpeg binary` within the system before installing **`Pickpod`**.

You can refer to the installation method provided by [pydub](https://github.com/jiaaro/pydub#getting-ffmpeg-set-up), or go to the [ffmpeg download page](https://ffmpeg.org/download.html) and [ffmpeg compilation guide](http://trac.ffmpeg.org/wiki/CompilationGuide) for more.

Moreover, please see the note about `hugging face` access token fetching in [pyannote-audio](https://github.com/pyannote/pyannote-audio#tldr-) for more information on using [speaker-diarization](https://huggingface.co/pyannote/speaker-diarization).

If you need to filter the list of podcasts to be batch transcribed based on customized rules or use `LLM` to analyze the transcribed text, please refer to the `API` documentation provided by [Listen Notes](https://www.listennotes.com/api/pricing/) and [Anthropic](https://docs.anthropic.com/claude/reference/getting-started-with-the-api#accessing-the-api) to obtain the necessary `Access Keys`, respectively.

### ❗️Warning

According to our experiments, the latest branch of [pyannote-audio](https://github.com/pyannote/pyannote-audio) using `torch>=2.0.0` may [not detect GPU and run only on CPU](https://github.com/pyannote/pyannote-audio/issues/1354), so **`Pickpod`** requires `pyannote.audio==2.1.1` using `torch==1.13.1`.

Due to **`Pickpod`** strictly restricting the version of used `Python` packages, [pyannote-audio](https://github.com/pyannote/pyannote-audio) or other packages may automatically solve conflicts and remove some packages that you have installed before, such as `torch>=2.0.0`. To avoid unnecessary conflicts or damage to your environment, we strongly recommend installing **`Pickpod`** in a brand new `Python` environment or a `Python` virtual environment.

### Python

You don't need this source code if you just want to use the package. Just run:

```sh
$ pip install --upgrade pickpod
```

If you want to modify the package, install from source with:

```sh
$ pip install ./pickpod
```

If you want to run the `Streamlit` app that provides a web UI, install from source with:

```sh
$ pip install -r ./pickpod/app/requirements.txt
$ streamlit run ./pickpod/app/Home.py --server.port 8051
```

Then visit `http://127.0.0.1:8051` in your local browser.

### Installation in a typical environment

We chose [nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04](https://hub.docker.com/layers/nvidia/cuda/11.8.0-cudnn8-runtime-ubuntu22.04/images/sha256-b4c8cec91bd17d5b8dd42a2ef5fb104eb39d9203f889f0f3f17a5bf45f7bccc0) as a typical system environment to try to install **`Pickpod`**. The docker image has the following base configuration:

```sh
$ python3 -V

  Python 3.10.12


$ nvidia-smi

  Tue Aug 15 08:06:56 2023
  +-----------------------------------------------------------------------------+
    NVIDIA-SMI 525.105.17   Driver Version: 525.105.17   CUDA Version: 12.0     |
  |-------------------------------+----------------------+----------------------+
    GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
                                  |                      |               MIG M. |
  |===============================+======================+======================|
      0  NVIDIA GeForce ...  On   | 00000000:65:00.0 Off |                  N/A |
     0%   43C    P8    23W / 370W |   1481MiB / 24576MiB |      0%      Default |
                                  |                      |                  N/A |
  +-------------------------------+----------------------+----------------------+

  +-----------------------------------------------------------------------------+
    Processes:                                                                  |
     GPU   GI   CI        PID   Type   Process name                  GPU Memory |
           ID   ID                                                   Usage      |
  |=============================================================================|
  +-----------------------------------------------------------------------------+
```

First, we need to install `ffmpeg`, `python3-pip`, and other essential tools, then upgrade the software packages.

```sh
$ sudo apt-get -y install cmake libsndfile1 ffmpeg python3-pip
$ sudo apt update && apt upgrade -y
```

We can verify if `ffmpeg` is installed successfully in the following way:

```sh
$ ffmpeg -version

  ffmpeg version 4.4.2-0ubuntu0.22.04.1 Copyright (c) 2000-2021 the FFmpeg developers
  built with gcc 11 (Ubuntu 11.2.0-19ubuntu1)
  configuration: --prefix=/usr --extra-version=0ubuntu0.22.04.1 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-gnutls --enable-ladspa --enable-libaom --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libjack --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librabbitmq --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libsrt --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-libzmq --enable-libzvbi --enable-lv2 --enable-omx --enable-openal --enable-opencl --enable-opengl --enable-sdl2 --enable-pocketsphinx --enable-librsvg --enable-libmfx --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libx264 --enable-shared
  libavutil      56. 70.100 / 56. 70.100
  libavcodec     58.134.100 / 58.134.100
  libavformat    58. 76.100 / 58. 76.100
  libavdevice    58. 13.100 / 58. 13.100
  libavfilter     7.110.100 /  7.110.100
  libswscale      5.  9.100 /  5.  9.100
  libswresample   3.  9.100 /  3.  9.100
  libpostproc    55.  9.100 / 55.  9.100
```

After downloading the source code and running `setup.py`, we can import **`Pickpod`** in `Python`.

```sh
$ git clone https://github.com/shixiangcap/pickpod.git
$ pip install ./pickpod
```


## Usage

### Do internet **`Pickpod`** task

```python
from pickpod.config import TaskConfig
from pickpod.doc import AudioDocument
from pickpod.task import PickpodTask

HUGGING_FACE_KEY = "YOUR_HUGGING_FACE_KEY"

# For example: https://www.youtube.com/watch?v=xxxxxxxxxxx
audio_url = "YOUR_AUDIO_URL_ON_INTERNET"

# Set audio information
audio_doc = AudioDocument(audio_url=audio_url)
# Config pickpod task
task_config = TaskConfig(key_hugging_face=HUGGING_FACE_KEY, pipeline=True)
# Initial pickpod task
pickpod_task = PickpodTask(audio_doc, task_config)
# Start pickpod task
pickpod_task.pickpod_with_url()
# Get the result of pickpod task
print(pickpod_task.audio_doc.__dict__)
```

### Do local **`Pickpod`** task

```python
from pickpod.config import TaskConfig
from pickpod.doc import AudioDocument
from pickpod.task import PickpodTask

HUGGING_FACE_KEY = "YOUR_HUGGING_FACE_KEY"

# For example: xxxxxxxxxxx.m4a
audio_path = "YOUR_LOCAL_FILE_PATH"

# Set audio information
audio_doc = AudioDocument(audio_path=audio_path)
# Config pickpod task
task_config = TaskConfig(key_hugging_face=HUGGING_FACE_KEY, pipeline=False)
# Initial pickpod task
pickpod_task = PickpodTask(audio_doc, task_config)
# Start pickpod task
pickpod_task.pickpod_with_local()
# Save the result of pickpod task
pickpod_task.audio_doc.save_as_json()
```


## Examples

### A complete transcription result of a audio file

If the target `YouTube` video is [Introducing GPT-4](https://www.youtube.com/watch?v=--khbXchTeE), the **`Pickpod`** can get the `JSON` file:

<details>
<summary>Show more</summary>
<p>

```json
{
    "uuid": "afeb5810-25ee-426d-aa88-7b58484d4c6f",
    "title": "Introducing GPT-4",
    "ext": "m4a",
    "web": "https://www.youtube.com/watch?v=--khbXchTeE",
    "url": "https://www.youtube.com/watch?v=--khbXchTeE",
    "length": 192.493,
    "description": "GPT-4 is OpenAI’s most advanced system, producing safer and more useful responses.\n\nhttps://openai.com/product/gpt-4",
    "keywords": [
        "GPT-4",
        "AI capabilities",
        "Education",
        "Microsoft partnership",
        "Safety",
        "Usefulness",
        "Early adopters",
        "Transistor",
        "Programming languages",
        "Future generations"
    ],
    "path": "/opt/pickpod/app/library/audio/afeb5810-25ee-426d-aa88-7b58484d4c6f.m4a",
    "sentence": [
        {
            "start": 0.0,
            "end": 4.88,
            "content": "GPT-4 takes what you prompt it with and just runs with it.",
            "speaker": 7
        },
        {
            "start": 4.88,
            "end": 6.54,
            "content": "From one perspective, it's a tool,",
            "speaker": 7
        },
        {
            "start": 6.54,
            "end": 11.84,
            "content": "a thing you can use to get useful tasks done in language.",
            "speaker": 7
        },
        {
            "start": 11.84,
            "end": 13.5,
            "content": "From another perspective, it's a system",
            "speaker": 7
        },
        {
            "start": 13.5,
            "end": 17.04,
            "content": "that can make dreams, thoughts, ideas flourish",
            "speaker": 7
        },
        {
            "start": 17.04,
            "end": 19.080000000000002,
            "content": "in text in front of you.",
            "speaker": 7
        },
        {
            "start": 19.080000000000002,
            "end": 23.2,
            "content": "GPT-4 is incredibly advanced and sophisticated.",
            "speaker": 6
        },
        {
            "start": 23.2,
            "end": 27.96,
            "content": "It can take in and generate up to 25,000 words of text,",
            "speaker": 6
        },
        {
            "start": 28.0,
            "end": 31.200000000000003,
            "content": "around eight times more than chat GPT.",
            "speaker": 6
        },
        {
            "start": 31.200000000000003,
            "end": 34.0,
            "content": "It understands images and can express",
            "speaker": 6
        },
        {
            "start": 34.0,
            "end": 36.0,
            "content": "logical ideas about them.",
            "speaker": 6
        },
        {
            "start": 36.0,
            "end": 38.2,
            "content": "For example, it can tell us that",
            "speaker": 6
        },
        {
            "start": 38.2,
            "end": 40.120000000000005,
            "content": "if the strings in this image were cut,",
            "speaker": 6
        },
        {
            "start": 40.120000000000005,
            "end": 42.08,
            "content": "the balloons would fly away.",
            "speaker": 6
        },
        {
            "start": 42.08,
            "end": 44.760000000000005,
            "content": "This is the place where you just get turbocharged",
            "speaker": 4
        },
        {
            "start": 44.760000000000005,
            "end": 46.24,
            "content": "by these AIs.",
            "speaker": 4
        },
        {
            "start": 46.24,
            "end": 47.56,
            "content": "They're not perfect, they make mistakes,",
            "speaker": 4
        },
        {
            "start": 47.56,
            "end": 49.480000000000004,
            "content": "and so you really need to make sure that you know",
            "speaker": 4
        },
        {
            "start": 49.480000000000004,
            "end": 52.400000000000006,
            "content": "the work is being done to your level of expectation.",
            "speaker": 4
        },
        {
            "start": 52.400000000000006,
            "end": 55.040000000000006,
            "content": "But I think that it is fundamentally about",
            "speaker": 4
        },
        {
            "start": 55.040000000000006,
            "end": 57.2,
            "content": "amplifying what every person is able to do.",
            "speaker": 4
        },
        {
            "start": 58.04,
            "end": 60.84,
            "content": "GPT-4 training finished last August,",
            "speaker": 1
        },
        {
            "start": 60.84,
            "end": 63.56,
            "content": "and everything that's been happening in the past few months,",
            "speaker": 1
        },
        {
            "start": 63.56,
            "end": 64.84,
            "content": "up until we've released it,",
            "speaker": 1
        },
        {
            "start": 64.84,
            "end": 67.16,
            "content": "has been a giant sprint to make it safer,",
            "speaker": 1
        },
        {
            "start": 67.16,
            "end": 69.16,
            "content": "more aligned, and also more useful.",
            "speaker": 1
        },
        {
            "start": 69.16,
            "end": 72.84,
            "content": "We have put in already a lot of internal guardrails",
            "speaker": 1
        },
        {
            "start": 72.84,
            "end": 75.24000000000001,
            "content": "around things like adversarial usage,",
            "speaker": 1
        },
        {
            "start": 75.24000000000001,
            "end": 78.24000000000001,
            "content": "unwanted content, and privacy concerns.",
            "speaker": 1
        },
        {
            "start": 78.24000000000001,
            "end": 81.28,
            "content": "And when we release a model, we know things are not done.",
            "speaker": 1
        },
        {
            "start": 81.28,
            "end": 83.92,
            "content": "We know we have to learn, we know we have to update,",
            "speaker": 1
        },
        {
            "start": 83.92,
            "end": 87.32,
            "content": "we know we have to keep improving all the systems around it",
            "speaker": 1
        },
        {
            "start": 87.36000000000001,
            "end": 89.88000000000001,
            "content": "to make it suitable for society.",
            "speaker": 1
        },
        {
            "start": 89.88000000000001,
            "end": 93.08000000000001,
            "content": "To me, the most compelling use cases of these technologies",
            "speaker": 7
        },
        {
            "start": 93.08000000000001,
            "end": 96.80000000000001,
            "content": "will come from starting with a real human need.",
            "speaker": 7
        },
        {
            "start": 96.80000000000001,
            "end": 98.68,
            "content": "The obvious one where these systems have",
            "speaker": 7
        },
        {
            "start": 98.68,
            "end": 101.84,
            "content": "really incredible potential is in education.",
            "speaker": 7
        },
        {
            "start": 101.84,
            "end": 104.96000000000001,
            "content": "GPT-4 can teach a huge range of subjects.",
            "speaker": 5
        },
        {
            "start": 104.96000000000001,
            "end": 108.12,
            "content": "Imagine giving a fifth grader a personal math tutor",
            "speaker": 5
        },
        {
            "start": 108.12,
            "end": 110.60000000000001,
            "content": "with unlimited time and patience.",
            "speaker": 5
        },
        {
            "start": 110.60000000000001,
            "end": 113.24000000000001,
            "content": "It's a great tool to bring learning to everyone",
            "speaker": 5
        },
        {
            "start": 113.24000000000001,
            "end": 116.04,
            "content": "in a way that is personalized to their skill level.",
            "speaker": 5
        },
        {
            "start": 117.04,
            "end": 119.92,
            "content": "GPT-4 brings the dream of having",
            "speaker": 2
        },
        {
            "start": 119.92,
            "end": 122.64,
            "content": "the most useful, helpful assistant to life.",
            "speaker": 2
        },
        {
            "start": 122.64,
            "end": 124.52000000000001,
            "content": "It's really about adding as much value",
            "speaker": 2
        },
        {
            "start": 124.52000000000001,
            "end": 126.04,
            "content": "to everyday life as possible.",
            "speaker": 2
        },
        {
            "start": 127.24000000000001,
            "end": 129.76000000000002,
            "content": "The partnership that OpenAI has with Microsoft",
            "speaker": 3
        },
        {
            "start": 129.76000000000002,
            "end": 131.68,
            "content": "is to shape this technology",
            "speaker": 3
        },
        {
            "start": 131.68,
            "end": 134.96,
            "content": "into something that's gonna be useful for the world.",
            "speaker": 3
        },
        {
            "start": 134.96,
            "end": 136.56,
            "content": "The power of AI, hopefully,",
            "speaker": 0
        },
        {
            "start": 136.56,
            "end": 139.04000000000002,
            "content": "is that it can help us be more productive,",
            "speaker": 0
        },
        {
            "start": 139.04000000000002,
            "end": 141.92000000000002,
            "content": "which ultimately leads to better quality of life.",
            "speaker": 0
        },
        {
            "start": 141.92000000000002,
            "end": 143.28,
            "content": "The development of the transistor",
            "speaker": 8
        },
        {
            "start": 143.28,
            "end": 144.72,
            "content": "of the computer of the intranet,",
            "speaker": 8
        },
        {
            "start": 144.92,
            "end": 146.4,
            "content": "the semiconductor industry,",
            "speaker": 8
        },
        {
            "start": 146.4,
            "end": 147.68,
            "content": "all the programming languages,",
            "speaker": 8
        },
        {
            "start": 147.68,
            "end": 151.88,
            "content": "everything came together to produce AI technology.",
            "speaker": 8
        },
        {
            "start": 151.88,
            "end": 153.56,
            "content": "And while it is very limited,",
            "speaker": 8
        },
        {
            "start": 153.56,
            "end": 156.0,
            "content": "it is already easy to imagine what the impact",
            "speaker": 8
        },
        {
            "start": 156.0,
            "end": 159.68,
            "content": "of a successor many generations down the line will look like.",
            "speaker": 8
        },
        {
            "start": 159.68,
            "end": 163.2,
            "content": "We think that GPT-4 will be the world's first experience",
            "speaker": 6
        },
        {
            "start": 163.2,
            "end": 166.68,
            "content": "with a highly capable and advanced AI system.",
            "speaker": 6
        },
        {
            "start": 166.68,
            "end": 171.04,
            "content": "So we really care about this model being useful to everyone,",
            "speaker": 6
        },
        {
            "start": 171.04,
            "end": 173.32,
            "content": "not just the early adopters",
            "speaker": 6
        },
        {
            "start": 173.35999999999999,
            "end": 176.2,
            "content": "or people very close to technology.",
            "speaker": 6
        },
        {
            "start": 176.2,
            "end": 178.23999999999998,
            "content": "So it is really important to us",
            "speaker": 6
        },
        {
            "start": 178.23999999999998,
            "end": 181.28,
            "content": "that as many people as possible participate",
            "speaker": 6
        },
        {
            "start": 181.28,
            "end": 182.84,
            "content": "so that we can learn more",
            "speaker": 6
        },
        {
            "start": 182.84,
            "end": 184.84,
            "content": "about how it can be helpful to everyone.",
            "speaker": 6
        }
    ],
    "summary": [
        {
            "start": 0,
            "content": "Introducing GPT-4 and its capabilities"
        },
        {
            "start": 39,
            "content": "GPT-4 can generate long, coherent text and understand images"
        },
        {
            "start": 68,
            "content": "GPT-4 amplifies human abilities but still makes mistakes"
        },
        {
            "start": 88,
            "content": "Work done since August to make GPT-4 safer and more useful "
        },
        {
            "start": 109,
            "content": "Internal guardrails added around potential risks"
        },
        {
            "start": 124,
            "content": "Improvements will continue after release"
        },
        {
            "start": 139,
            "content": "Most compelling use cases start with human needs"
        },
        {
            "start": 151,
            "content": "Huge potential for education and personalized learning  "
        },
        {
            "start": 170,
            "content": "Can serve as a helpful unlimited assistant "
        },
        {
            "start": 184,
            "content": "Partnership with Microsoft to shape useful technology"
        },
        {
            "start": 197,
            "content": "Goal to increase productivity and quality of life"
        },
        {
            "start": 211,
            "content": "AI builds on decades of advances in computing  "
        },
        {
            "start": 230,
            "content": "GPT-4 will provide first experience of advanced AI"
        },
        {
            "start": 245,
            "content": "Important that GPT-4 benefits everyone beyond early adopters"
        },
        {
            "start": 259,
            "content": "Broad participation will maximize learning about helpful uses"
        }
    ],
    "views": [
        {
            "content": "Here are 5 unconventional or sharp attitudes in the transcript:",
            "mark": false
        },
        {
            "content": "Calling GPT-4 \"incredibly advanced and sophisticated\" and able to generate 8 times more text than ChatGPT contradicts the view that these systems still have major limitations. ",
            "mark": false
        },
        {
            "content": "Saying GPT-4 can \"make dreams, thoughts, ideas flourish in text\" suggests it has near-human creative abilities, which is likely an overstatement.",
            "mark": false
        },
        {
            "content": "Claiming GPT-4 can be a personal math tutor with \"unlimited time and patience\" exaggerates its capabilities and usefulness in education.",
            "mark": false
        },
        {
            "content": "Stating GPT-4 brings the \"dream of the most useful, helpful assistant to life\" implies it is more capable than it likely is.",
            "mark": false
        },
        {
            "content": "Calling GPT-4 the \"world's first experience with a highly capable and advanced AI system\" disregards earlier advanced systems and oversells its abilities.",
            "mark": false
        }
    ],
    "origin": "web",
    "ctime": 1692685244,
    "utime": 1692685309
}
```

</p>
</details>

If the target `小宇宙` podcast is [EP 35. ICML现场对话AI研究员符尧：亲历AI诸神之战，解读LLM前沿研究，Llama 2，AI Agents](https://www.xiaoyuzhoufm.com/episode/64d0c50ae490c5dee5ca5721), the **`Pickpod`** can get the `JSON` file:

<details>
<summary>Show more</summary>
<p>

```json
{
    "uuid": "93aa3140-300d-4af6-9d9c-2c41e9095821",
    "title": "EP 35. ICML现场对话AI研究员符尧：亲历AI诸神之战，解读LLM前沿研究，Llama 2，AI Agents",
    "ext": "m4a",
    "web": "https://www.xiaoyuzhoufm.com/episode/64d0c50ae490c5dee5ca5721",
    "url": "https://www.xiaoyuzhoufm.com/episode/64d0c50ae490c5dee5ca5721",
    "length": 4158.251,
    "description": "听《OnBoard!》上小宇宙。 Hello World, who is OnBoard!? 两个爱码字的投资人关于软件、创业与投资的真诚对话。\n\n关注主播：\n\nMonica：美元VC投资人，前 AWS 硅谷团队+AI创业公司打工人，公众号M小姐研习录 (ID: MissMStudy) 主理人 | 即刻：莫妮卡同学\n\nGN：前SaaS及科技投资人，Global SaaS社区Linkloud发起人，公众号我思锅我在 (ID: thinkxcloud) 主理人。| 即刻：High 宁\n\n\n同名 Podcast 在各大平台都有哦：\n\n喜马拉雅, Apple Podcasts, Spotify, Google Podcasts, Overcast 都可以找到~",
    "keywords": [
        "大语言模型",
        "模型能力",
        "数据组成",
        "知识遗忘",
        "模型安全性",
        "ICML",
        "业内交流 ",
        "模型训练",
        "强化学习",
        "AI agents"
    ],
    "path": "/opt/pickpod/app/library/audio/93aa3140-300d-4af6-9d9c-2c41e9095821.m4a",
    "sentence": [
        {
            "start": 0.0,
            "end": 9.0,
            "content": "欢迎来到onboard,真实的一线经验,走新的投资思考。我是Monica。",
            "speaker": 0
        },
        {
            "start": 9.0,
            "end": 12.0,
            "content": "我是高宁。我们一起聊聊软件如何改变世界。",
            "speaker": 1
        },
        {
            "start": 16.0,
            "end": 19.0,
            "content": "大家好,好久不见,我是Monica。",
            "speaker": 0
        },
        {
            "start": 19.0,
            "end": 25.0,
            "content": "Monica最近一个月都在硅谷,要兼顾中美两边的工作实在不容易,更新都怠慢了。",
            "speaker": 0
        },
        {
            "start": 25.0,
            "end": 34.0,
            "content": "不过,大家不要着急,我们已经有好几期的精彩储备,未来的一个月肯定是精彩不断,赶紧关注onboard。",
            "speaker": 0
        },
        {
            "start": 34.0,
            "end": 45.0,
            "content": "这次的节目非常特别,是在ICML2023,就是International Conference on Machine Learning国际机器学习盛会的现场录制的。",
            "speaker": 0
        },
        {
            "start": 45.0,
            "end": 52.0,
            "content": "这次的嘉宾傅瑶更是众望所归,相信最近关注大语言模型的朋友都不陌生。",
            "speaker": 0
        },
        {
            "start": 52.0,
            "end": 63.0,
            "content": "她的论文也入选了本次的ICML,她的好几篇关于大语言模型能力研究的文章都被广为流传,可以说每一篇都是业内必读。",
            "speaker": 0
        },
        {
            "start": 63.0,
            "end": 72.0,
            "content": "正如傅瑶在知乎的一篇总结文章中所说,ICML2023,OpenAI Anthropic,Google DeepMind,Meta,",
            "speaker": 0
        },
        {
            "start": 72.0,
            "end": 83.0,
            "content": "各大名校的Rising Star PhD,顶级对冲基金与VC,最著名的Startup都悉数到场,这里是诸神之战的最前线。",
            "speaker": 0
        },
        {
            "start": 83.0,
            "end": 95.0,
            "content": "这次Monica跟傅瑶回顾了在ICML与各位大神现场交流的见闻,还有傅瑶对于数据、RHF等大模型核心研究领域的思考,",
            "speaker": 0
        },
        {
            "start": 95.0,
            "end": 101.0,
            "content": "还有对于振动业界的最近发布的Lama2的看法,可谓是新鲜出炉。",
            "speaker": 0
        },
        {
            "start": 101.0,
            "end": 110.0,
            "content": "这次在室外录制,而且傅瑶身体不适,还坚持与我们完成了Podcast,不免有些杂音,还请大家理解担待。",
            "speaker": 0
        },
        {
            "start": 110.0,
            "end": 115.0,
            "content": "但是我想,这对于关注干货的听众来说,应该都不是问题。",
            "speaker": 0
        },
        {
            "start": 115.0,
            "end": 124.0,
            "content": "Monica非常喜欢傅瑶一贯的精神,不讨论小道消息,一切从定义性原理出发,相信你也会受益匪浅。Enjoy!",
            "speaker": 0
        },
        {
            "start": 125.0,
            "end": 130.0,
            "content": "这一期的onboard非常特别,我们是在Hawaii录制的,大家不要羡慕我。",
            "speaker": 1
        },
        {
            "start": 130.0,
            "end": 139.0,
            "content": "其实Monica也是来这边工作,来这边参加一个可以说是Machine Learning和AI界的盛会ICML。",
            "speaker": 1
        },
        {
            "start": 139.0,
            "end": 148.0,
            "content": "然后在ICML可以说聚集了各路大神,非常适合我们活捉一个Podcast的嘉宾。",
            "speaker": 1
        },
        {
            "start": 148.0,
            "end": 154.0,
            "content": "于是我就在ICML活捉了一位一直非常期待能够约到的一位嘉宾。",
            "speaker": 1
        },
        {
            "start": 154.0,
            "end": 158.0,
            "content": "小赛在ICML遇到了,我们就说择日不撞日。",
            "speaker": 1
        },
        {
            "start": 158.0,
            "end": 169.0,
            "content": "在刚刚听完了大神Jones Grumman的演讲之后,我们在会场旁边看着Hawaii的蓝天来跟大家随性地聊一聊。",
            "speaker": 1
        },
        {
            "start": 169.0,
            "end": 172.0,
            "content": "这一次我们邀请到的嘉宾就是傅瑶。",
            "speaker": 1
        },
        {
            "start": 172.0,
            "end": 178.0,
            "content": "我想很多听众可能已经知道傅瑶在LM大圆模型方面的很多研究,",
            "speaker": 1
        },
        {
            "start": 178.0,
            "end": 185.0,
            "content": "但是对于不大了解傅瑶的同学,我想傅瑶可以跟大家简单介绍一下你自己,",
            "speaker": 1
        },
        {
            "start": 185.0,
            "end": 189.0,
            "content": "以及你是如何进入到大圆模型研究的领域的。",
            "speaker": 1
        },
        {
            "start": 189.0,
            "end": 195.0,
            "content": "大家好,我叫傅瑶,我现在是爱丁堡大学最后一年的PhD学生。",
            "speaker": 2
        },
        {
            "start": 195.0,
            "end": 199.0,
            "content": "我的本科是在北京大学,硕士是在哥伦比亚大学。",
            "speaker": 2
        },
        {
            "start": 199.0,
            "end": 205.0,
            "content": "所以基本上经历了中国、美国和英国三个国家的AI发展的历程。",
            "speaker": 2
        },
        {
            "start": 205.0,
            "end": 212.0,
            "content": "然后我自己入这行其实是在2014年,那个时候深度学习刚刚兴起,",
            "speaker": 2
        },
        {
            "start": 212.0,
            "end": 216.0,
            "content": "在那个时候开始做自然语言处理相关的学习和研究。",
            "speaker": 2
        },
        {
            "start": 216.0,
            "end": 221.0,
            "content": "然后我开始研究大圆模型其实是在2022年的年初,",
            "speaker": 2
        },
        {
            "start": 221.0,
            "end": 227.0,
            "content": "在那个时候基本上是以Chair-GPT发布提前一年,",
            "speaker": 2
        },
        {
            "start": 227.0,
            "end": 231.0,
            "content": "然后各种涌现能力啊,模型测试啊,",
            "speaker": 2
        },
        {
            "start": 231.0,
            "end": 234.0,
            "content": "然后Prompting啊,Train of Thought啊,",
            "speaker": 2
        },
        {
            "start": 234.0,
            "end": 238.0,
            "content": "这些现在大家都已经比较熟悉的概念刚刚兴起的时候。",
            "speaker": 2
        },
        {
            "start": 238.0,
            "end": 242.0,
            "content": "从那个时候开始,我是基本上以Train of Thought,",
            "speaker": 2
        },
        {
            "start": 242.0,
            "end": 246.0,
            "content": "思维念以及涌现能力这两个题目为切入点,",
            "speaker": 2
        },
        {
            "start": 246.0,
            "end": 251.0,
            "content": "然后自己研究了GPT的演化历程,",
            "speaker": 2
        },
        {
            "start": 251.0,
            "end": 255.0,
            "content": "然后大模型能力如何涌现,如何为模型注入能力,",
            "speaker": 2
        },
        {
            "start": 255.0,
            "end": 259.0,
            "content": "如何把模型约束在我们想要的方向。",
            "speaker": 2
        },
        {
            "start": 259.0,
            "end": 264.0,
            "content": "我最近也有关的工作是跟很多推理相关的工作,",
            "speaker": 2
        },
        {
            "start": 264.0,
            "end": 268.0,
            "content": "包括如何通过Prompting的方式来增加模型的推理,",
            "speaker": 2
        },
        {
            "start": 268.0,
            "end": 270.0,
            "content": "如何通过Fine-Tune的方式,",
            "speaker": 2
        },
        {
            "start": 270.0,
            "end": 274.0,
            "content": "这也是我这次在ICML做Oral Presentation的内容。",
            "speaker": 2
        },
        {
            "start": 274.0,
            "end": 277.0,
            "content": "我可以跟大家简单介绍一下ICML,",
            "speaker": 1
        },
        {
            "start": 277.0,
            "end": 280.0,
            "content": "你提到的你的论文所在的领域,",
            "speaker": 1
        },
        {
            "start": 280.0,
            "end": 284.0,
            "content": "我想也是在做大元模型的很多人都很关注的,",
            "speaker": 1
        },
        {
            "start": 284.0,
            "end": 289.0,
            "content": "你可以跟大家简单的介绍一下你这次Present的论文。",
            "speaker": 1
        },
        {
            "start": 289.0,
            "end": 292.0,
            "content": "OK,没问题。ICML是一个,",
            "speaker": 2
        },
        {
            "start": 292.0,
            "end": 296.0,
            "content": "它的全称叫做International Conference for Machine Learning,",
            "speaker": 2
        },
        {
            "start": 296.0,
            "end": 299.0,
            "content": "是专门研究机器学习的一个会议,",
            "speaker": 2
        },
        {
            "start": 299.0,
            "end": 302.0,
            "content": "这个会议其实成立的时间蛮久的,",
            "speaker": 2
        },
        {
            "start": 302.0,
            "end": 307.0,
            "content": "在深度学习之前就已经有很多前机器学习的内容投到这个会议,",
            "speaker": 2
        },
        {
            "start": 307.0,
            "end": 309.0,
            "content": "然后这个会议每年开一次,",
            "speaker": 2
        },
        {
            "start": 309.0,
            "end": 311.0,
            "content": "每次都在不同的地方,",
            "speaker": 2
        },
        {
            "start": 311.0,
            "end": 315.0,
            "content": "然后学术会议当它选在风景优美的地方的时候,",
            "speaker": 2
        },
        {
            "start": 315.0,
            "end": 317.0,
            "content": "它的投稿率就会特别的高,",
            "speaker": 2
        },
        {
            "start": 317.0,
            "end": 319.0,
            "content": "然后它今年选在了夏威夷,",
            "speaker": 2
        },
        {
            "start": 319.0,
            "end": 321.0,
            "content": "之前我听说在那个巴尔的摩,",
            "speaker": 1
        },
        {
            "start": 321.0,
            "end": 323.0,
            "content": "然后就没什么人去,",
            "speaker": 1
        },
        {
            "start": 323.0,
            "end": 326.0,
            "content": "之前在巴尔的摩,",
            "speaker": 2
        },
        {
            "start": 326.0,
            "end": 329.0,
            "content": "就是去的话都是那种比较急性跳蚤的去的,",
            "speaker": 2
        },
        {
            "start": 329.0,
            "end": 331.0,
            "content": "对,然后今年选在夏威夷,",
            "speaker": 2
        },
        {
            "start": 331.0,
            "end": 333.0,
            "content": "于是就是想去的不想去的,",
            "speaker": 2
        },
        {
            "start": 333.0,
            "end": 335.0,
            "content": "有这种文章没这种文章就都来了,",
            "speaker": 2
        },
        {
            "start": 335.0,
            "end": 337.0,
            "content": "我听说OpenAI来了80多个人,",
            "speaker": 2
        },
        {
            "start": 337.0,
            "end": 339.0,
            "content": "基本上全球都来了,",
            "speaker": 2
        },
        {
            "start": 339.0,
            "end": 341.0,
            "content": "大家都还想来的一个很大的原因,",
            "speaker": 2
        },
        {
            "start": 341.0,
            "end": 343.0,
            "content": "是因为现在Top3的选手,",
            "speaker": 2
        },
        {
            "start": 343.0,
            "end": 345.0,
            "content": "OpenAI,Answerpick,Kip Mann,",
            "speaker": 2
        },
        {
            "start": 345.0,
            "end": 347.0,
            "content": "当然Meta也非常的强,",
            "speaker": 2
        },
        {
            "start": 347.0,
            "end": 350.0,
            "content": "然后相当于是,",
            "speaker": 2
        },
        {
            "start": 350.0,
            "end": 353.0,
            "content": "我会把它叫做Biggest Party in the World,",
            "speaker": 2
        },
        {
            "start": 353.0,
            "end": 355.0,
            "content": "就基本上做National Language Model的,",
            "speaker": 2
        },
        {
            "start": 355.0,
            "end": 358.0,
            "content": "然后业内的一些一个比较领先的选手都在这里,",
            "speaker": 2
        },
        {
            "start": 358.0,
            "end": 362.0,
            "content": "那自然而然这些个人的向心力就会聚集起来,",
            "speaker": 2
        },
        {
            "start": 362.0,
            "end": 365.0,
            "content": "非常非常多对这个方向感兴趣的人,",
            "speaker": 2
        },
        {
            "start": 365.0,
            "end": 368.0,
            "content": "在前天的中午H6Z,",
            "speaker": 2
        },
        {
            "start": 368.0,
            "end": 370.0,
            "content": "一个风投的机构,",
            "speaker": 2
        },
        {
            "start": 370.0,
            "end": 372.0,
            "content": "然后就是做一个午饭的局,",
            "speaker": 2
        },
        {
            "start": 372.0,
            "end": 374.0,
            "content": "然后基本上把OpenAI,",
            "speaker": 2
        },
        {
            "start": 374.0,
            "end": 376.0,
            "content": "Answerpick,Meta,Kip Mann,",
            "speaker": 2
        },
        {
            "start": 376.0,
            "end": 378.0,
            "content": "就叫在一起吃中饭,",
            "speaker": 2
        },
        {
            "start": 378.0,
            "end": 380.0,
            "content": "那确确实实就是,",
            "speaker": 2
        },
        {
            "start": 380.0,
            "end": 382.0,
            "content": "大神云集,",
            "speaker": 2
        },
        {
            "start": 382.0,
            "end": 384.0,
            "content": "群星云集,",
            "speaker": 2
        },
        {
            "start": 384.0,
            "end": 387.0,
            "content": "并且现在各个公司竞争的非常的激烈,",
            "speaker": 2
        },
        {
            "start": 387.0,
            "end": 390.0,
            "content": "然后大模型的能力就是一个比一个强,",
            "speaker": 2
        },
        {
            "start": 390.0,
            "end": 392.0,
            "content": "一个版本比一个版本的强,",
            "speaker": 2
        },
        {
            "start": 392.0,
            "end": 394.0,
            "content": "就会很有一种诸神之战的感觉,",
            "speaker": 2
        },
        {
            "start": 394.0,
            "end": 398.0,
            "content": "如果你把就是这些个头部公司的大模型之间的竞争,",
            "speaker": 2
        },
        {
            "start": 398.0,
            "end": 400.0,
            "content": "看成是诸神之战的话,",
            "speaker": 2
        },
        {
            "start": 400.0,
            "end": 402.0,
            "content": "这里就是诸神之战的现场,",
            "speaker": 2
        },
        {
            "start": 402.0,
            "end": 403.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 403.0,
            "end": 406.0,
            "content": "然后关于我自己的文章的话,",
            "speaker": 2
        },
        {
            "start": 406.0,
            "end": 408.0,
            "content": "我其实因为审稿是有周期的,",
            "speaker": 2
        },
        {
            "start": 408.0,
            "end": 410.0,
            "content": "审稿到被接收,",
            "speaker": 2
        },
        {
            "start": 410.0,
            "end": 412.0,
            "content": "然后做准备这些都有周期,",
            "speaker": 2
        },
        {
            "start": 412.0,
            "end": 415.0,
            "content": "我自己的这篇文章只是在半年之前做的,",
            "speaker": 2
        },
        {
            "start": 415.0,
            "end": 417.0,
            "content": "然后那在半年之前的时候,",
            "speaker": 2
        },
        {
            "start": 417.0,
            "end": 420.0,
            "content": "我们发现它是关于大模型能力平衡的问题,",
            "speaker": 2
        },
        {
            "start": 420.0,
            "end": 427.0,
            "content": "我们发现如果你希望为你的已经训练好的模型注入新的能力的话,",
            "speaker": 2
        },
        {
            "start": 427.0,
            "end": 433.0,
            "content": "你是能够让这个模型在你想要新注入的能力的方向得到提升的,",
            "speaker": 2
        },
        {
            "start": 433.0,
            "end": 439.0,
            "content": "但是你会面临的问题就是你原先的能力可能会经历一定程度的遗忘,",
            "speaker": 2
        },
        {
            "start": 439.0,
            "end": 442.0,
            "content": "然后我们的文章就比较细致的研究,",
            "speaker": 2
        },
        {
            "start": 443.0,
            "end": 445.0,
            "content": "注入新能力的时候,",
            "speaker": 2
        },
        {
            "start": 445.0,
            "end": 449.0,
            "content": "新能力的提升跟数据和模型大小的关系,",
            "speaker": 2
        },
        {
            "start": 449.0,
            "end": 454.0,
            "content": "以及旧能力的遗忘跟数据和模型大小的关系,",
            "speaker": 2
        },
        {
            "start": 454.0,
            "end": 457.0,
            "content": "那我们现在也倾向于相信,",
            "speaker": 2
        },
        {
            "start": 457.0,
            "end": 461.0,
            "content": "因为最近有非常非常多的很火的Fan2Nama的文章,",
            "speaker": 2
        },
        {
            "start": 461.0,
            "end": 464.0,
            "content": "他们把Nama变成了一个聊天机器人,",
            "speaker": 2
        },
        {
            "start": 464.0,
            "end": 470.0,
            "content": "那我们相信在我们的我们的文章之中发现的新知识注入,",
            "speaker": 2
        },
        {
            "start": 470.0,
            "end": 473.0,
            "content": "导致旧知识遗忘的这些个问题,",
            "speaker": 2
        },
        {
            "start": 473.0,
            "end": 478.0,
            "content": "在非常非常近期的把Nama变成一个聊天机器人的这些个工作之中,",
            "speaker": 2
        },
        {
            "start": 478.0,
            "end": 480.0,
            "content": "也大家都在遇到,",
            "speaker": 2
        },
        {
            "start": 480.0,
            "end": 485.0,
            "content": "所以这是一个整个领域基本上都还在面临的问题,",
            "speaker": 2
        },
        {
            "start": 485.0,
            "end": 487.0,
            "content": "所以我做Presentation的时候,",
            "speaker": 2
        },
        {
            "start": 487.0,
            "end": 489.0,
            "content": "基本上也引发了比较多的讨论。",
            "speaker": 2
        },
        {
            "start": 489.0,
            "end": 491.0,
            "content": "这个研究是半年之前,",
            "speaker": 1
        },
        {
            "start": 491.0,
            "end": 495.0,
            "content": "那个时候其实这个Chat2D才刚出来几个月的时间,",
            "speaker": 1
        },
        {
            "start": 495.0,
            "end": 498.0,
            "content": "那其实这半年真的发生了天翻地覆的这个变化,",
            "speaker": 1
        },
        {
            "start": 498.0,
            "end": 503.0,
            "content": "那你觉得这几个月对于你的研究会有哪些比较重要的更新吗?",
            "speaker": 1
        },
        {
            "start": 503.0,
            "end": 508.0,
            "content": "其实我在做我的这份研究的时候,",
            "speaker": 2
        },
        {
            "start": 508.0,
            "end": 511.0,
            "content": "首先那个时候并没有GPT-4,",
            "speaker": 2
        },
        {
            "start": 511.0,
            "end": 512.0,
            "content": "也没有全GPT,",
            "speaker": 2
        },
        {
            "start": 512.0,
            "end": 515.0,
            "content": "我们用的是GPT-3.5的基础模型,",
            "speaker": 2
        },
        {
            "start": 515.0,
            "end": 516.0,
            "content": "叫Coda分析002,",
            "speaker": 2
        },
        {
            "start": 516.0,
            "end": 519.0,
            "content": "然后在那个时候我们也没有Nama,",
            "speaker": 2
        },
        {
            "start": 519.0,
            "end": 522.0,
            "content": "我们用的是也比较早期的一个模型叫做T5,",
            "speaker": 2
        },
        {
            "start": 522.0,
            "end": 525.0,
            "content": "然后我们研究的问题是能力平衡,",
            "speaker": 2
        },
        {
            "start": 525.0,
            "end": 527.0,
            "content": "学了新的忘了旧的,",
            "speaker": 2
        },
        {
            "start": 527.0,
            "end": 530.0,
            "content": "但其实让我比较惊讶的是,",
            "speaker": 2
        },
        {
            "start": 530.0,
            "end": 533.0,
            "content": "我本来的预期是经过了半年的时间,",
            "speaker": 2
        },
        {
            "start": 533.0,
            "end": 537.0,
            "content": "这个领域应该对于开源社区,",
            "speaker": 2
        },
        {
            "start": 537.0,
            "end": 543.0,
            "content": "学术界应该对于领域能力的平衡有更多一点点的突破,",
            "speaker": 2
        },
        {
            "start": 543.0,
            "end": 547.0,
            "content": "但是让我比较惊讶的是我在做presentation的时候,",
            "speaker": 2
        },
        {
            "start": 547.0,
            "end": 553.0,
            "content": "我发现我所探讨的一些个还没有被很好解决的问题,",
            "speaker": 2
        },
        {
            "start": 553.0,
            "end": 555.0,
            "content": "就现在还依旧存在,",
            "speaker": 2
        },
        {
            "start": 555.0,
            "end": 557.0,
            "content": "也可能是因为这些问题本身就比较难,",
            "speaker": 2
        },
        {
            "start": 557.0,
            "end": 562.0,
            "content": "所以如果要从简单到难做research的话,",
            "speaker": 2
        },
        {
            "start": 562.0,
            "end": 566.0,
            "content": "可能是一些个比较简单的问题先被解决,",
            "speaker": 2
        },
        {
            "start": 566.0,
            "end": 569.0,
            "content": "这也是最近这半年发生的事情,",
            "speaker": 2
        },
        {
            "start": 569.0,
            "end": 573.0,
            "content": "但是最近这半年就是对于我所present的这个问题,",
            "speaker": 2
        },
        {
            "start": 573.0,
            "end": 576.0,
            "content": "其实并没有看到特别大的进展。",
            "speaker": 2
        },
        {
            "start": 576.0,
            "end": 577.0,
            "content": "这个还挺有意思,",
            "speaker": 1
        },
        {
            "start": 577.0,
            "end": 580.0,
            "content": "因为你刚才讲的这个问题可能就是因为它比较难,",
            "speaker": 1
        },
        {
            "start": 580.0,
            "end": 582.0,
            "content": "所以现在讨论比较少的,",
            "speaker": 1
        },
        {
            "start": 582.0,
            "end": 586.0,
            "content": "这个就要你可以跟大家稍微细节的讲一讲,",
            "speaker": 1
        },
        {
            "start": 586.0,
            "end": 591.0,
            "content": "就是这个遗忘学了新能力,遗忘旧能力的这个事情,",
            "speaker": 1
        },
        {
            "start": 591.0,
            "end": 593.0,
            "content": "你们是怎么发现的?",
            "speaker": 1
        },
        {
            "start": 593.0,
            "end": 596.0,
            "content": "解决它的话,这个难点在哪?",
            "speaker": 1
        },
        {
            "start": 596.0,
            "end": 597.0,
            "content": "它如果不解决的话,",
            "speaker": 1
        },
        {
            "start": 597.0,
            "end": 601.0,
            "content": "现在我们能够看到的实际中的一些影响又是什么?",
            "speaker": 1
        },
        {
            "start": 601.0,
            "end": 602.0,
            "content": "OK,没问题,",
            "speaker": 1
        },
        {
            "start": 602.0,
            "end": 605.0,
            "content": "那我自己当时在做这篇文章的时候,",
            "speaker": 2
        },
        {
            "start": 605.0,
            "end": 607.0,
            "content": "我用的基础模型是F95,",
            "speaker": 2
        },
        {
            "start": 607.0,
            "end": 609.0,
            "content": "当然现在大家可以用南马,",
            "speaker": 2
        },
        {
            "start": 609.0,
            "end": 610.0,
            "content": "那我当时在做的时候,",
            "speaker": 2
        },
        {
            "start": 610.0,
            "end": 613.0,
            "content": "我是希望提高它的做数学题的能力,",
            "speaker": 2
        },
        {
            "start": 613.0,
            "end": 616.0,
            "content": "就是在数学题目之中多部推理的能力,",
            "speaker": 2
        },
        {
            "start": 616.0,
            "end": 618.0,
            "content": "但是这件事情其实是比较容易达到的,",
            "speaker": 2
        },
        {
            "start": 618.0,
            "end": 622.0,
            "content": "你直接拿一个数学题的推理的训练级,",
            "speaker": 2
        },
        {
            "start": 622.0,
            "end": 626.0,
            "content": "或者是funtune的数学级来去funtune一下它,",
            "speaker": 2
        },
        {
            "start": 626.0,
            "end": 629.0,
            "content": "这个模型自然而然就会拥有这样的能力,",
            "speaker": 2
        },
        {
            "start": 629.0,
            "end": 630.0,
            "content": "这其实没什么,",
            "speaker": 2
        },
        {
            "start": 630.0,
            "end": 631.0,
            "content": "但这里的问题是,",
            "speaker": 2
        },
        {
            "start": 631.0,
            "end": 636.0,
            "content": "当它学会了数学方面的多部推理之后,",
            "speaker": 2
        },
        {
            "start": 636.0,
            "end": 639.0,
            "content": "它本来是会其他方面的多部推理的,",
            "speaker": 2
        },
        {
            "start": 639.0,
            "end": 642.0,
            "content": "比如说它会时间上的多部推理,",
            "speaker": 2
        },
        {
            "start": 642.0,
            "end": 647.0,
            "content": "它会一些跟我们日常生活之中的多部推理,",
            "speaker": 2
        },
        {
            "start": 647.0,
            "end": 649.0,
            "content": "早上的时候先洗脸,",
            "speaker": 2
        },
        {
            "start": 649.0,
            "end": 651.0,
            "content": "然后先刷牙还先洗脸,",
            "speaker": 2
        },
        {
            "start": 651.0,
            "end": 655.0,
            "content": "然后有些事情是要有顺序的,",
            "speaker": 2
        },
        {
            "start": 655.0,
            "end": 659.0,
            "content": "然后你在做饭的时候要先开你的煤气灶,",
            "speaker": 2
        },
        {
            "start": 659.0,
            "end": 661.0,
            "content": "然后再放上你的锅,",
            "speaker": 2
        },
        {
            "start": 661.0,
            "end": 662.0,
            "content": "然后再加这些个,",
            "speaker": 2
        },
        {
            "start": 662.0,
            "end": 665.0,
            "content": "就这些个比较日常的多部推理的东西,",
            "speaker": 2
        },
        {
            "start": 665.0,
            "end": 666.0,
            "content": "它就会被忘掉,",
            "speaker": 2
        },
        {
            "start": 666.0,
            "end": 668.0,
            "content": "就相当于你学会了数学的,",
            "speaker": 2
        },
        {
            "start": 668.0,
            "end": 669.0,
            "content": "他们都是推理,",
            "speaker": 2
        },
        {
            "start": 669.0,
            "end": 672.0,
            "content": "但是这个它的泛化能力可能是存在一些问题,",
            "speaker": 2
        },
        {
            "start": 672.0,
            "end": 676.0,
            "content": "你本来会日常生活之中的多部推理的事情,",
            "speaker": 2
        },
        {
            "start": 676.0,
            "end": 678.0,
            "content": "但是你学了数学之后,",
            "speaker": 2
        },
        {
            "start": 678.0,
            "end": 679.0,
            "content": "它可能就忘掉了,",
            "speaker": 2
        },
        {
            "start": 679.0,
            "end": 682.0,
            "content": "然后这是我在半年之前观察到的现象,",
            "speaker": 2
        },
        {
            "start": 682.0,
            "end": 683.0,
            "content": "那在半年之后,",
            "speaker": 2
        },
        {
            "start": 683.0,
            "end": 685.0,
            "content": "大家都在funtune NAMA,",
            "speaker": 2
        },
        {
            "start": 685.0,
            "end": 686.0,
            "content": "funtune NAMA做的事情是,",
            "speaker": 2
        },
        {
            "start": 686.0,
            "end": 688.0,
            "content": "你有一个基础的NAMA的这个模型,",
            "speaker": 2
        },
        {
            "start": 688.0,
            "end": 691.0,
            "content": "然后你把它变成一个chatbot,",
            "speaker": 2
        },
        {
            "start": 691.0,
            "end": 694.0,
            "content": "变成一个就是对话机器人,",
            "speaker": 2
        },
        {
            "start": 694.0,
            "end": 697.0,
            "content": "当你在把NAMAfuntune成一个对话机器人的时候,",
            "speaker": 2
        },
        {
            "start": 697.0,
            "end": 702.0,
            "content": "你做的事情是用一些user会提到的问题去funtune它,",
            "speaker": 2
        },
        {
            "start": 702.0,
            "end": 704.0,
            "content": "那可能会存在的一个能力平衡就是,",
            "speaker": 2
        },
        {
            "start": 704.0,
            "end": 707.0,
            "content": "当你用这一系列的问题,",
            "speaker": 2
        },
        {
            "start": 707.0,
            "end": 709.0,
            "content": "比如说你的user是一个学生,",
            "speaker": 2
        },
        {
            "start": 709.0,
            "end": 712.0,
            "content": "可能跟学习相关的问题funtune NAMA之后,",
            "speaker": 2
        },
        {
            "start": 712.0,
            "end": 715.0,
            "content": "NAMA就自然而然会回答学习相关的问题,",
            "speaker": 2
        },
        {
            "start": 715.0,
            "end": 716.0,
            "content": "但是在这之前,",
            "speaker": 2
        },
        {
            "start": 716.0,
            "end": 717.0,
            "content": "NAMA本身是会回答,",
            "speaker": 2
        },
        {
            "start": 717.0,
            "end": 719.0,
            "content": "比如说其他一些个领域,",
            "speaker": 2
        },
        {
            "start": 719.0,
            "end": 721.0,
            "content": "日常生活中的怎么做饭相关的问题,",
            "speaker": 2
        },
        {
            "start": 721.0,
            "end": 723.0,
            "content": "但是你用学习相关的问题,",
            "speaker": 2
        },
        {
            "start": 723.0,
            "end": 725.0,
            "content": "问它funtune它funtune多少之后,",
            "speaker": 2
        },
        {
            "start": 725.0,
            "end": 728.0,
            "content": "它就会忘掉怎么做饭的问题,",
            "speaker": 2
        },
        {
            "start": 728.0,
            "end": 731.0,
            "content": "然后这些应该也是,",
            "speaker": 2
        },
        {
            "start": 731.0,
            "end": 734.0,
            "content": "虽然说有很多的工作在把NAMA变成一个chatbot,",
            "speaker": 2
        },
        {
            "start": 734.0,
            "end": 739.0,
            "content": "但这应该也是这些工作所共同面临的难点,",
            "speaker": 2
        },
        {
            "start": 739.0,
            "end": 741.0,
            "content": "其实最近Snapher在一个月之前,",
            "speaker": 2
        },
        {
            "start": 741.0,
            "end": 743.0,
            "content": "他们稍微梳理了一下,",
            "speaker": 2
        },
        {
            "start": 743.0,
            "end": 746.0,
            "content": "就是funtune NAMA能够走多远,",
            "speaker": 2
        },
        {
            "start": 746.0,
            "end": 748.0,
            "content": "然后这个也是他们的一个发现,",
            "speaker": 2
        },
        {
            "start": 748.0,
            "end": 752.0,
            "content": "所以这个问题应该至少是目前开源界和学术界,",
            "speaker": 2
        },
        {
            "start": 752.0,
            "end": 755.0,
            "content": "还没有被很好解决的一个问题。",
            "speaker": 2
        },
        {
            "start": 755.0,
            "end": 758.0,
            "content": "那你有测过比如说像GPT-4,",
            "speaker": 1
        },
        {
            "start": 758.0,
            "end": 761.0,
            "content": "或者说刚刚出来的NAMA2,",
            "speaker": 1
        },
        {
            "start": 761.0,
            "end": 765.0,
            "content": "他们在这个问题上有做一定程度的解决吗?",
            "speaker": 1
        },
        {
            "start": 765.0,
            "end": 769.0,
            "content": "我们认为这也是目前NAMA2,",
            "speaker": 2
        },
        {
            "start": 769.0,
            "end": 771.0,
            "content": "在做alignment存在的一个问题,",
            "speaker": 2
        },
        {
            "start": 771.0,
            "end": 773.0,
            "content": "就是NAMA2的alignment,",
            "speaker": 2
        },
        {
            "start": 773.0,
            "end": 774.0,
            "content": "他们是fit到了,",
            "speaker": 2
        },
        {
            "start": 774.0,
            "end": 779.0,
            "content": "他们把模型给fit到了meta自己内部的这些个query,",
            "speaker": 2
        },
        {
            "start": 779.0,
            "end": 780.0,
            "content": "也就是用户会提的问题,",
            "speaker": 2
        },
        {
            "start": 780.0,
            "end": 782.0,
            "content": "用户会提各种各样的问题,",
            "speaker": 2
        },
        {
            "start": 782.0,
            "end": 783.0,
            "content": "meta自己内部,",
            "speaker": 2
        },
        {
            "start": 783.0,
            "end": 787.0,
            "content": "我们倾向于相信meta内部的用户提的问题,",
            "speaker": 2
        },
        {
            "start": 787.0,
            "end": 789.0,
            "content": "只是所有问题其中的一个子集,",
            "speaker": 2
        },
        {
            "start": 789.0,
            "end": 795.0,
            "content": "然后当你去疯狂的去优化所有问题的一些个子集的时候,",
            "speaker": 2
        },
        {
            "start": 795.0,
            "end": 800.0,
            "content": "很有可能会带来在其他的一些个用户也会提的问题,",
            "speaker": 2
        },
        {
            "start": 800.0,
            "end": 803.0,
            "content": "但是没有被训练的时候覆盖到的这些个问题,",
            "speaker": 2
        },
        {
            "start": 803.0,
            "end": 805.0,
            "content": "很可能会使得模型遗忘,",
            "speaker": 2
        },
        {
            "start": 805.0,
            "end": 809.0,
            "content": "我们倾向于相信这是这个版本的NAMA2存在的一个问题,",
            "speaker": 2
        },
        {
            "start": 809.0,
            "end": 812.0,
            "content": "然后GPT-4的话表现可能会好一点,",
            "speaker": 2
        },
        {
            "start": 812.0,
            "end": 815.0,
            "content": "这个完全就是因为GPT-4的用户非常的多,",
            "speaker": 2
        },
        {
            "start": 815.0,
            "end": 818.0,
            "content": "所以它基本上把用户所有的常见的问题,",
            "speaker": 2
        },
        {
            "start": 818.0,
            "end": 820.0,
            "content": "然后各个方面的,",
            "speaker": 2
        },
        {
            "start": 820.0,
            "end": 822.0,
            "content": "然后全部都给cached下来,",
            "speaker": 2
        },
        {
            "start": 822.0,
            "end": 823.0,
            "content": "都给记住了,",
            "speaker": 2
        },
        {
            "start": 823.0,
            "end": 829.0,
            "content": "然后所以GPT-4在面对一些个比较刁钻古怪问题的时候,",
            "speaker": 2
        },
        {
            "start": 829.0,
            "end": 830.0,
            "content": "也能够打得出来,",
            "speaker": 2
        },
        {
            "start": 830.0,
            "end": 833.0,
            "content": "其实很多企业想要做一个内部的这种chatbot的时候,",
            "speaker": 1
        },
        {
            "start": 833.0,
            "end": 835.0,
            "content": "其实这个是挺常见的,",
            "speaker": 1
        },
        {
            "start": 835.0,
            "end": 836.0,
            "content": "要去做这个环境,",
            "speaker": 1
        },
        {
            "start": 836.0,
            "end": 839.0,
            "content": "或者说我要做一些南海做一些领域的时候,",
            "speaker": 1
        },
        {
            "start": 839.0,
            "end": 841.0,
            "content": "最近出现了一些这种法律啊,",
            "speaker": 1
        },
        {
            "start": 841.0,
            "end": 843.0,
            "content": "什么这个医疗啊,",
            "speaker": 1
        },
        {
            "start": 843.0,
            "end": 844.0,
            "content": "这些领域的大模型,",
            "speaker": 1
        },
        {
            "start": 844.0,
            "end": 847.0,
            "content": "这个步骤其实都还挺常见的,",
            "speaker": 1
        },
        {
            "start": 847.0,
            "end": 851.0,
            "content": "那在这些场景中还会遇到这样的挑战吗?",
            "speaker": 1
        },
        {
            "start": 851.0,
            "end": 857.0,
            "content": "我相信这个是现在中文互联网讨论比较多的领域大模型,",
            "speaker": 2
        },
        {
            "start": 857.0,
            "end": 859.0,
            "content": "一个非常常见的挑战,",
            "speaker": 2
        },
        {
            "start": 859.0,
            "end": 861.0,
            "content": "就是当你有一个极左模型,",
            "speaker": 2
        },
        {
            "start": 861.0,
            "end": 863.0,
            "content": "就是说你有一个可商用的NAMA2之后,",
            "speaker": 2
        },
        {
            "start": 863.0,
            "end": 866.0,
            "content": "你想把它给function到你自己的领域里面,",
            "speaker": 2
        },
        {
            "start": 866.0,
            "end": 867.0,
            "content": "第一它有可能,",
            "speaker": 2
        },
        {
            "start": 867.0,
            "end": 869.0,
            "content": "如果这个能力的平衡,",
            "speaker": 2
        },
        {
            "start": 869.0,
            "end": 873.0,
            "content": "它可能会是你的模型知道了你的领域的知识,",
            "speaker": 2
        },
        {
            "start": 873.0,
            "end": 875.0,
            "content": "但是它会忘掉通用的知识,",
            "speaker": 2
        },
        {
            "start": 875.0,
            "end": 877.0,
            "content": "但是很多时候呢,",
            "speaker": 2
        },
        {
            "start": 877.0,
            "end": 880.0,
            "content": "为了去回答一个领域的知识,",
            "speaker": 2
        },
        {
            "start": 880.0,
            "end": 882.0,
            "content": "你首先需要一些个常识,",
            "speaker": 2
        },
        {
            "start": 882.0,
            "end": 883.0,
            "content": "通用的知识来打底,",
            "speaker": 2
        },
        {
            "start": 883.0,
            "end": 887.0,
            "content": "我们相信这个是现在把模型调到任何一个领域,",
            "speaker": 2
        },
        {
            "start": 887.0,
            "end": 890.0,
            "content": "所都要面临的一个问题,",
            "speaker": 2
        },
        {
            "start": 890.0,
            "end": 894.0,
            "content": "同时这件事情也跟极左模型的大小很相关,",
            "speaker": 2
        },
        {
            "start": 894.0,
            "end": 897.0,
            "content": "就是很多时候你的模型比较通用的时候,",
            "speaker": 2
        },
        {
            "start": 897.0,
            "end": 899.0,
            "content": "比较大的时候,",
            "speaker": 2
        },
        {
            "start": 899.0,
            "end": 901.0,
            "content": "那些个专业领域的知识,",
            "speaker": 2
        },
        {
            "start": 901.0,
            "end": 903.0,
            "content": "其实在训练机制中它是见过的,",
            "speaker": 2
        },
        {
            "start": 903.0,
            "end": 908.0,
            "content": "那如果用一个中型的或者是小一点的领域内相关的模型,",
            "speaker": 2
        },
        {
            "start": 908.0,
            "end": 913.0,
            "content": "去跟这样的比较通用的极左的大模型做比较的话,",
            "speaker": 2
        },
        {
            "start": 913.0,
            "end": 917.0,
            "content": "首先你的小模型本身可能就会稍微比大模型弱一点,",
            "speaker": 2
        },
        {
            "start": 917.0,
            "end": 919.0,
            "content": "并且还有各种各样的遗忘的问题,",
            "speaker": 2
        },
        {
            "start": 919.0,
            "end": 920.0,
            "content": "然后你小模型会的,",
            "speaker": 2
        },
        {
            "start": 920.0,
            "end": 921.0,
            "content": "其实大模型也会,",
            "speaker": 2
        },
        {
            "start": 921.0,
            "end": 922.0,
            "content": "为什么它大,",
            "speaker": 2
        },
        {
            "start": 922.0,
            "end": 923.0,
            "content": "因为它数据多,",
            "speaker": 2
        },
        {
            "start": 923.0,
            "end": 924.0,
            "content": "它数据多哪里来的,",
            "speaker": 2
        },
        {
            "start": 924.0,
            "end": 925.0,
            "content": "因为它把领域知识来的,",
            "speaker": 2
        },
        {
            "start": 925.0,
            "end": 929.0,
            "content": "这个领域知识本身就是你在翻车小模型时候用的领域知识,",
            "speaker": 2
        },
        {
            "start": 929.0,
            "end": 932.0,
            "content": "相当于我们倾向于认为通用的更大的模型,",
            "speaker": 2
        },
        {
            "start": 932.0,
            "end": 936.0,
            "content": "是中型的或小一点的领域模型的一个超级,",
            "speaker": 2
        },
        {
            "start": 936.0,
            "end": 939.0,
            "content": "因此在现在这个阶段,",
            "speaker": 2
        },
        {
            "start": 939.0,
            "end": 942.0,
            "content": "我个人比较倾向于去promote,",
            "speaker": 2
        },
        {
            "start": 942.0,
            "end": 946.0,
            "content": "接着去研究通用的更大的模型,",
            "speaker": 2
        },
        {
            "start": 946.0,
            "end": 949.0,
            "content": "而不是把资源花在中型的领域的小模型上面。",
            "speaker": 2
        },
        {
            "start": 949.0,
            "end": 950.0,
            "content": "因为就像你说的,",
            "speaker": 1
        },
        {
            "start": 950.0,
            "end": 958.0,
            "content": "的确大家现在不知道我减少了pre-trained model的大小了以后,",
            "speaker": 1
        },
        {
            "start": 958.0,
            "end": 959.0,
            "content": "我到底损失了什么样的,",
            "speaker": 1
        },
        {
            "start": 959.0,
            "end": 961.0,
            "content": "大家之所以会讲到小模型,",
            "speaker": 1
        },
        {
            "start": 961.0,
            "end": 962.0,
            "content": "除了说要它的一个能力之外,",
            "speaker": 1
        },
        {
            "start": 962.0,
            "end": 964.0,
            "content": "当然另外一个大家讨论的tradeoff,",
            "speaker": 1
        },
        {
            "start": 964.0,
            "end": 966.0,
            "content": "其实就是这个efficiency,",
            "speaker": 1
        },
        {
            "start": 966.0,
            "end": 968.0,
            "content": "是一个比较小的use case,",
            "speaker": 1
        },
        {
            "start": 968.0,
            "end": 971.0,
            "content": "我都要用一个比较大的模型去做的话,",
            "speaker": 1
        },
        {
            "start": 971.0,
            "end": 972.0,
            "content": "就会太贵,",
            "speaker": 1
        },
        {
            "start": 972.0,
            "end": 974.0,
            "content": "你怎么看待这个问题?",
            "speaker": 1
        },
        {
            "start": 974.0,
            "end": 977.0,
            "content": "对,就是模型的通用的能力,",
            "speaker": 2
        },
        {
            "start": 977.0,
            "end": 979.0,
            "content": "然后模型的专业性知识,",
            "speaker": 2
        },
        {
            "start": 979.0,
            "end": 982.0,
            "content": "然后模型上线的时候,",
            "speaker": 2
        },
        {
            "start": 982.0,
            "end": 986.0,
            "content": "它的部署的成本是一个比较难平衡的事情,",
            "speaker": 2
        },
        {
            "start": 986.0,
            "end": 990.0,
            "content": "对于另外一个领域模型的argument是说,",
            "speaker": 2
        },
        {
            "start": 990.0,
            "end": 993.0,
            "content": "我们用一个中型的或小一点的模型,",
            "speaker": 2
        },
        {
            "start": 993.0,
            "end": 994.0,
            "content": "给它灌入领域知识,",
            "speaker": 2
        },
        {
            "start": 994.0,
            "end": 995.0,
            "content": "这样子的话,",
            "speaker": 2
        },
        {
            "start": 995.0,
            "end": 998.0,
            "content": "它的大小本身可以降低它的成本,",
            "speaker": 2
        },
        {
            "start": 998.0,
            "end": 1000.0,
            "content": "这件事情其实是非常重要的,",
            "speaker": 2
        },
        {
            "start": 1001.0,
            "end": 1002.0,
            "content": "但这种情况,",
            "speaker": 2
        },
        {
            "start": 1002.0,
            "end": 1005.0,
            "content": "我们觉得是一个解法,",
            "speaker": 2
        },
        {
            "start": 1005.0,
            "end": 1007.0,
            "content": "然后也有另外一些的解法,",
            "speaker": 2
        },
        {
            "start": 1007.0,
            "end": 1010.0,
            "content": "你首先有一个比较大的模型,",
            "speaker": 2
        },
        {
            "start": 1010.0,
            "end": 1013.0,
            "content": "然后你再把这个大的模型的能力,",
            "speaker": 2
        },
        {
            "start": 1013.0,
            "end": 1017.0,
            "content": "用大的模型去教小一点的模型,",
            "speaker": 2
        },
        {
            "start": 1017.0,
            "end": 1018.0,
            "content": "然后这样子的话,",
            "speaker": 2
        },
        {
            "start": 1018.0,
            "end": 1021.0,
            "content": "你的大的模型本身是有专业性,",
            "speaker": 2
        },
        {
            "start": 1021.0,
            "end": 1022.0,
            "content": "各项能力之间的平衡,",
            "speaker": 2
        },
        {
            "start": 1022.0,
            "end": 1024.0,
            "content": "然后你在教小模型的时候,",
            "speaker": 2
        },
        {
            "start": 1024.0,
            "end": 1027.0,
            "content": "你让大的模型也可以尽量平衡的,",
            "speaker": 2
        },
        {
            "start": 1027.0,
            "end": 1032.0,
            "content": "把大模型的专业能力给针流到小模型里面,",
            "speaker": 2
        },
        {
            "start": 1032.0,
            "end": 1033.0,
            "content": "然后在这个过程之中,",
            "speaker": 2
        },
        {
            "start": 1033.0,
            "end": 1038.0,
            "content": "稍微把它专业的方向的权重提的更高一点点,",
            "speaker": 2
        },
        {
            "start": 1038.0,
            "end": 1039.0,
            "content": "这样子的话,",
            "speaker": 2
        },
        {
            "start": 1039.0,
            "end": 1043.0,
            "content": "我们觉得是一个做好你的模型不是特别大,",
            "speaker": 2
        },
        {
            "start": 1043.0,
            "end": 1044.0,
            "content": "这样的话,",
            "speaker": 2
        },
        {
            "start": 1044.0,
            "end": 1045.0,
            "content": "你部署成本低,",
            "speaker": 2
        },
        {
            "start": 1045.0,
            "end": 1047.0,
            "content": "同时你的模型又足够的通用,",
            "speaker": 2
        },
        {
            "start": 1047.0,
            "end": 1048.0,
            "content": "因为它是从大的模型来的,",
            "speaker": 2
        },
        {
            "start": 1048.0,
            "end": 1050.0,
            "content": "然后在这个过程之中,",
            "speaker": 2
        },
        {
            "start": 1050.0,
            "end": 1052.0,
            "content": "你提高专业领域的权重,",
            "speaker": 2
        },
        {
            "start": 1052.0,
            "end": 1053.0,
            "content": "这样的话,",
            "speaker": 2
        },
        {
            "start": 1053.0,
            "end": 1055.0,
            "content": "你可以模型会通用你会专业领域的知识,",
            "speaker": 2
        },
        {
            "start": 1055.0,
            "end": 1059.0,
            "content": "这个是我们现在看来一个更加好一点的方案,",
            "speaker": 2
        },
        {
            "start": 1059.0,
            "end": 1062.0,
            "content": "针流的这个方案也是提到的,",
            "speaker": 1
        },
        {
            "start": 1062.0,
            "end": 1063.0,
            "content": "这个技术,",
            "speaker": 1
        },
        {
            "start": 1063.0,
            "end": 1065.0,
            "content": "你觉得它已经可以做到什么程度,",
            "speaker": 1
        },
        {
            "start": 1065.0,
            "end": 1068.0,
            "content": "还有哪些学而未决的问题?",
            "speaker": 1
        },
        {
            "start": 1068.0,
            "end": 1071.0,
            "content": "在研究大模型的时候,",
            "speaker": 2
        },
        {
            "start": 1071.0,
            "end": 1074.0,
            "content": "大模型分成两个主要的开发阶段,",
            "speaker": 2
        },
        {
            "start": 1074.0,
            "end": 1075.0,
            "content": "一个scanning,",
            "speaker": 2
        },
        {
            "start": 1075.0,
            "end": 1077.0,
            "content": "就是去训练得到一个很大的基础模型,",
            "speaker": 2
        },
        {
            "start": 1077.0,
            "end": 1078.0,
            "content": "一个是alignment,",
            "speaker": 2
        },
        {
            "start": 1078.0,
            "end": 1079.0,
            "content": "与人类对齐,",
            "speaker": 2
        },
        {
            "start": 1079.0,
            "end": 1083.0,
            "content": "然后alignment又分成两个不同的阶段,",
            "speaker": 2
        },
        {
            "start": 1083.0,
            "end": 1085.0,
            "content": "一个是SFT的阶段,",
            "speaker": 2
        },
        {
            "start": 1085.0,
            "end": 1089.0,
            "content": "就相当于你有一个人类写好的query和回复的数据,",
            "speaker": 2
        },
        {
            "start": 1089.0,
            "end": 1093.0,
            "content": "然后你用这样的数据去fine tune你的模型,",
            "speaker": 2
        },
        {
            "start": 1093.0,
            "end": 1095.0,
            "content": "另外一个就是RLHF,",
            "speaker": 2
        },
        {
            "start": 1095.0,
            "end": 1099.0,
            "content": "用强化学习的方法来让模型变得更好,",
            "speaker": 2
        },
        {
            "start": 1099.0,
            "end": 1103.0,
            "content": "然后针流在这个过程之中,",
            "speaker": 2
        },
        {
            "start": 1103.0,
            "end": 1106.0,
            "content": "它更多的是发生在SFT这个阶段,",
            "speaker": 2
        },
        {
            "start": 1106.0,
            "end": 1109.0,
            "content": "相当于你有一个比较小的基座的模型,",
            "speaker": 2
        },
        {
            "start": 1110.0,
            "end": 1114.0,
            "content": "然后你把这个小的基座模型做一下fine tune,",
            "speaker": 2
        },
        {
            "start": 1114.0,
            "end": 1117.0,
            "content": "然后用大模型的支持和大模型的输出,",
            "speaker": 2
        },
        {
            "start": 1117.0,
            "end": 1119.0,
            "content": "fine tune你的小的基座模型,",
            "speaker": 2
        },
        {
            "start": 1119.0,
            "end": 1123.0,
            "content": "然后这样得到的模型应该是也能用的,",
            "speaker": 2
        },
        {
            "start": 1123.0,
            "end": 1126.0,
            "content": "并且在实际应用之中,",
            "speaker": 2
        },
        {
            "start": 1126.0,
            "end": 1130.0,
            "content": "应该它处于一个可以接受比较不错的一个程度,",
            "speaker": 2
        },
        {
            "start": 1130.0,
            "end": 1135.0,
            "content": "然后当然你也希望它可以变得更好,",
            "speaker": 2
        },
        {
            "start": 1135.0,
            "end": 1137.0,
            "content": "就是如果说60分及格的话,",
            "speaker": 2
        },
        {
            "start": 1137.0,
            "end": 1139.0,
            "content": "可能是比如说有70分这个样子,",
            "speaker": 2
        },
        {
            "start": 1139.0,
            "end": 1141.0,
            "content": "但是你希望它能够做到80分和90分,",
            "speaker": 2
        },
        {
            "start": 1141.0,
            "end": 1144.0,
            "content": "那你希望把它80分到90分的话,",
            "speaker": 2
        },
        {
            "start": 1144.0,
            "end": 1147.0,
            "content": "你可能就要努力一下做一下RL,",
            "speaker": 2
        },
        {
            "start": 1147.0,
            "end": 1151.0,
            "content": "因为SFT,superfine tuning这样的一个学习方式,",
            "speaker": 2
        },
        {
            "start": 1151.0,
            "end": 1153.0,
            "content": "它是有它的上限的,",
            "speaker": 2
        },
        {
            "start": 1153.0,
            "end": 1157.0,
            "content": "然后现在我们倾向于认为SFT有一点点触及到它的上限了,",
            "speaker": 2
        },
        {
            "start": 1157.0,
            "end": 1161.0,
            "content": "所以我们如果希望在这个基础上,",
            "speaker": 2
        },
        {
            "start": 1161.0,
            "end": 1164.0,
            "content": "让小一点的模型在针流的过程之中变得更好的话,",
            "speaker": 2
        },
        {
            "start": 1164.0,
            "end": 1169.0,
            "content": "其实我们是想要做的事情是用强化学习的方法去针流它,",
            "speaker": 2
        },
        {
            "start": 1169.0,
            "end": 1173.0,
            "content": "让它可以突破SFT这种学习方式的上限。",
            "speaker": 2
        },
        {
            "start": 1173.0,
            "end": 1176.0,
            "content": "怎么理解它达到了这个上限?",
            "speaker": 1
        },
        {
            "start": 1176.0,
            "end": 1180.0,
            "content": "这个上限其实可以通过一些个画Scanning的图可以看出来,",
            "speaker": 2
        },
        {
            "start": 1180.0,
            "end": 1183.0,
            "content": "就是当你在做SFT的时候,",
            "speaker": 2
        },
        {
            "start": 1183.0,
            "end": 1186.0,
            "content": "你做的事情是用人类标注好的数据喂给模型,",
            "speaker": 2
        },
        {
            "start": 1186.0,
            "end": 1190.0,
            "content": "然后你可以观察这个模型的能力的上升的曲线,",
            "speaker": 2
        },
        {
            "start": 1190.0,
            "end": 1193.0,
            "content": "随着人类喂进去的数据增多而增多,",
            "speaker": 2
        },
        {
            "start": 1193.0,
            "end": 1196.0,
            "content": "然后它会停在一个点,它是跟数据量有关,",
            "speaker": 2
        },
        {
            "start": 1196.0,
            "end": 1200.0,
            "content": "它跟数据的数量和数据的次量有关,",
            "speaker": 2
        },
        {
            "start": 1200.0,
            "end": 1204.0,
            "content": "然后次量好的数据会让这个模型增长得更快,",
            "speaker": 2
        },
        {
            "start": 1204.0,
            "end": 1206.0,
            "content": "就随着你增多这些个数据,",
            "speaker": 2
        },
        {
            "start": 1206.0,
            "end": 1210.0,
            "content": "次量好的数据会让你的模型的增长曲线的斜率更高,",
            "speaker": 2
        },
        {
            "start": 1210.0,
            "end": 1215.0,
            "content": "随着你增多这个数据,模型本身就有一个增长的曲线,",
            "speaker": 2
        },
        {
            "start": 1215.0,
            "end": 1218.0,
            "content": "然后这个增长的曲线不是一直无限的增长的,",
            "speaker": 2
        },
        {
            "start": 1218.0,
            "end": 1220.0,
            "content": "它会停在一个点,",
            "speaker": 2
        },
        {
            "start": 1220.0,
            "end": 1223.0,
            "content": "在那个点的时候你再加更多的数据,",
            "speaker": 2
        },
        {
            "start": 1223.0,
            "end": 1225.0,
            "content": "模型也不大会上升了。",
            "speaker": 2
        },
        {
            "start": 1225.0,
            "end": 1228.0,
            "content": "这个针灸肠胃被广泛接受的一种做法,",
            "speaker": 1
        },
        {
            "start": 1228.0,
            "end": 1231.0,
            "content": "用到这个生产中你觉得还有什么挑战呢?",
            "speaker": 1
        },
        {
            "start": 1231.0,
            "end": 1234.0,
            "content": "我觉得非常重要的挑战,",
            "speaker": 2
        },
        {
            "start": 1234.0,
            "end": 1238.0,
            "content": "一个是在针灸的过程之中怎么把肠化学习给用好,",
            "speaker": 2
        },
        {
            "start": 1238.0,
            "end": 1240.0,
            "content": "RLHF给用好,",
            "speaker": 2
        },
        {
            "start": 1240.0,
            "end": 1242.0,
            "content": "然后在这一点上,",
            "speaker": 2
        },
        {
            "start": 1242.0,
            "end": 1247.0,
            "content": "学术界和开源界并没有特别多的研究的内容,",
            "speaker": 2
        },
        {
            "start": 1247.0,
            "end": 1252.0,
            "content": "我觉得主要是它跟科学发展的阶段是有关的,",
            "speaker": 2
        },
        {
            "start": 1252.0,
            "end": 1254.0,
            "content": "就是在现在这个阶段,",
            "speaker": 2
        },
        {
            "start": 1254.0,
            "end": 1257.0,
            "content": "就我们现在的科学界还没有发展到这个阶段,",
            "speaker": 2
        },
        {
            "start": 1257.0,
            "end": 1260.0,
            "content": "但我倾向于认为在接下来的半年之中,",
            "speaker": 2
        },
        {
            "start": 1260.0,
            "end": 1264.0,
            "content": "我们会看到越来越多的相关方向的文章和方法,",
            "speaker": 2
        },
        {
            "start": 1264.0,
            "end": 1267.0,
            "content": "所以在可以预期的未来之内,",
            "speaker": 2
        },
        {
            "start": 1267.0,
            "end": 1270.0,
            "content": "虽然说用肠化学习的方法做针灸,",
            "speaker": 2
        },
        {
            "start": 1270.0,
            "end": 1273.0,
            "content": "现在还没有很多的工作,",
            "speaker": 2
        },
        {
            "start": 1273.0,
            "end": 1276.0,
            "content": "但是我觉得在可以预期的接下来半年时间之内,",
            "speaker": 2
        },
        {
            "start": 1276.0,
            "end": 1278.0,
            "content": "我们会看到更多的工作和方法,",
            "speaker": 2
        },
        {
            "start": 1278.0,
            "end": 1280.0,
            "content": "并且它们应该都会有效。",
            "speaker": 2
        },
        {
            "start": 1280.0,
            "end": 1283.0,
            "content": "刚提到说他这个会lose new capability的这个方面,",
            "speaker": 1
        },
        {
            "start": 1283.0,
            "end": 1289.0,
            "content": "还有什么你看现在看到一些可行的一些未来可能的解法?",
            "speaker": 1
        },
        {
            "start": 1289.0,
            "end": 1294.0,
            "content": "对,对于新能力和旧能力的平衡的问题,",
            "speaker": 2
        },
        {
            "start": 1294.0,
            "end": 1303.0,
            "content": "我们现在倾向于相信比较好的解法是找到正确的用户的问题的分布,",
            "speaker": 2
        },
        {
            "start": 1303.0,
            "end": 1305.0,
            "content": "或者说用户问题集合,",
            "speaker": 2
        },
        {
            "start": 1305.0,
            "end": 1311.0,
            "content": "就是一定要非常非常清楚的知道用户到底会问模型什么样的问题,",
            "speaker": 2
        },
        {
            "start": 1311.0,
            "end": 1314.0,
            "content": "因为我们现在倾向于相信,",
            "speaker": 2
        },
        {
            "start": 1314.0,
            "end": 1320.0,
            "content": "就是比如说老是把老是在数学题目上训这个模型的话,",
            "speaker": 2
        },
        {
            "start": 1320.0,
            "end": 1322.0,
            "content": "虽然数学题肯定会变高,",
            "speaker": 2
        },
        {
            "start": 1322.0,
            "end": 1326.0,
            "content": "但是数学题只是用户问模型的其中的一个小部分,",
            "speaker": 2
        },
        {
            "start": 1326.0,
            "end": 1327.0,
            "content": "还有其他的,",
            "speaker": 2
        },
        {
            "start": 1327.0,
            "end": 1330.0,
            "content": "那还有就是日常的对话,",
            "speaker": 2
        },
        {
            "start": 1330.0,
            "end": 1333.0,
            "content": "用日常对话的数学训练模型,",
            "speaker": 2
        },
        {
            "start": 1333.0,
            "end": 1336.0,
            "content": "模型肯定会让日常对话训练能力变得更高,",
            "speaker": 2
        },
        {
            "start": 1336.0,
            "end": 1343.0,
            "content": "但是日常对话也只是模型的用户真实的问题的其中一小部分,",
            "speaker": 2
        },
        {
            "start": 1343.0,
            "end": 1347.0,
            "content": "因为很多时候模型用户问模型是要让这个模型干活的,",
            "speaker": 2
        },
        {
            "start": 1347.0,
            "end": 1349.0,
            "content": "不是跟这个模型瞎扯的,",
            "speaker": 2
        },
        {
            "start": 1349.0,
            "end": 1351.0,
            "content": "是要真的让这个模型成为生产力,",
            "speaker": 2
        },
        {
            "start": 1351.0,
            "end": 1355.0,
            "content": "对,所以找到正确的用户的问题的集合,",
            "speaker": 2
        },
        {
            "start": 1355.0,
            "end": 1360.0,
            "content": "或者说就是找到正确的用户的问题的分布,",
            "speaker": 2
        },
        {
            "start": 1360.0,
            "end": 1362.0,
            "content": "然后去拟合这些分布,",
            "speaker": 2
        },
        {
            "start": 1362.0,
            "end": 1370.0,
            "content": "我觉得是接下来半年需要特别考虑和被攻克的一个问题,",
            "speaker": 2
        },
        {
            "start": 1370.0,
            "end": 1371.0,
            "content": "在这方面的话,",
            "speaker": 2
        },
        {
            "start": 1371.0,
            "end": 1373.0,
            "content": "已经有一些地方有一些工作了,",
            "speaker": 2
        },
        {
            "start": 1373.0,
            "end": 1375.0,
            "content": "比如说LMSYS,",
            "speaker": 2
        },
        {
            "start": 1375.0,
            "end": 1382.0,
            "content": "他们有一个Open Chatbot Arena的一个网站,",
            "speaker": 2
        },
        {
            "start": 1382.0,
            "end": 1387.0,
            "content": "是让用户自己给不同的模型提问,",
            "speaker": 2
        },
        {
            "start": 1387.0,
            "end": 1390.0,
            "content": "然后看那些个模型谁好谁坏,",
            "speaker": 2
        },
        {
            "start": 1390.0,
            "end": 1392.0,
            "content": "然后这样子的话,",
            "speaker": 2
        },
        {
            "start": 1392.0,
            "end": 1395.0,
            "content": "他们就可以收集到用户提的这些个问题,",
            "speaker": 2
        },
        {
            "start": 1395.0,
            "end": 1396.0,
            "content": "这个数据本身,",
            "speaker": 2
        },
        {
            "start": 1396.0,
            "end": 1398.0,
            "content": "然后他们最近也开源了一些个数据,",
            "speaker": 2
        },
        {
            "start": 1398.0,
            "end": 1404.0,
            "content": "我们觉得这个是非常非常的有价值的,",
            "speaker": 2
        },
        {
            "start": 1404.0,
            "end": 1406.0,
            "content": "对,那在这次的会议上面,",
            "speaker": 2
        },
        {
            "start": 1406.0,
            "end": 1410.0,
            "content": "关于数据的组成这方面的研究,",
            "speaker": 2
        },
        {
            "start": 1410.0,
            "end": 1412.0,
            "content": "其实我见到的非常的少,",
            "speaker": 2
        },
        {
            "start": 1412.0,
            "end": 1416.0,
            "content": "就说我自己会研究能力平衡和数据组成之外,",
            "speaker": 2
        },
        {
            "start": 1417.0,
            "end": 1421.0,
            "content": "还有另外一篇叫做The FNAN Connection,",
            "speaker": 2
        },
        {
            "start": 1421.0,
            "end": 1423.0,
            "content": "是MIT的同学发的,",
            "speaker": 2
        },
        {
            "start": 1423.0,
            "end": 1426.0,
            "content": "他的第一作者叫做Shane Lomprey,",
            "speaker": 2
        },
        {
            "start": 1426.0,
            "end": 1428.0,
            "content": "我们在这方面聊过很多次,",
            "speaker": 2
        },
        {
            "start": 1428.0,
            "end": 1434.0,
            "content": "但是似乎就只有我们两个在那里聊你的数据的组成,",
            "speaker": 2
        },
        {
            "start": 1434.0,
            "end": 1435.0,
            "content": "数据的组成应该怎么做,",
            "speaker": 2
        },
        {
            "start": 1435.0,
            "end": 1437.0,
            "content": "但是其他的地方的话,",
            "speaker": 2
        },
        {
            "start": 1437.0,
            "end": 1440.0,
            "content": "就是感觉关注这方面的问题还是比较少。",
            "speaker": 2
        },
        {
            "start": 1440.0,
            "end": 1445.0,
            "content": "最近LM出来以后也跟很多业界学界人去聊,",
            "speaker": 1
        },
        {
            "start": 1445.0,
            "end": 1447.0,
            "content": "我觉得刚才你说这个数据的问题,",
            "speaker": 1
        },
        {
            "start": 1447.0,
            "end": 1449.0,
            "content": "现在我要去验证一个假设,",
            "speaker": 1
        },
        {
            "start": 1449.0,
            "end": 1451.0,
            "content": "需要的算力成本本身就比较高,",
            "speaker": 1
        },
        {
            "start": 1451.0,
            "end": 1453.0,
            "content": "我们就这么一些卡,",
            "speaker": 1
        },
        {
            "start": 1453.0,
            "end": 1454.0,
            "content": "我们的验证也比较有限,",
            "speaker": 1
        },
        {
            "start": 1454.0,
            "end": 1455.0,
            "content": "是不是因为这个原因,",
            "speaker": 1
        },
        {
            "start": 1455.0,
            "end": 1458.0,
            "content": "使得对于data这一方面的一些研究,",
            "speaker": 1
        },
        {
            "start": 1458.0,
            "end": 1461.0,
            "content": "它可能更多还只能在业界去进行。",
            "speaker": 1
        },
        {
            "start": 1461.0,
            "end": 1463.0,
            "content": "学术界对这方面资源的要求,",
            "speaker": 2
        },
        {
            "start": 1463.0,
            "end": 1466.0,
            "content": "其实确实是需要有一定程度的资源的,",
            "speaker": 2
        },
        {
            "start": 1466.0,
            "end": 1472.0,
            "content": "但这个资源可能就是学术界会因为资源有限,",
            "speaker": 2
        },
        {
            "start": 1472.0,
            "end": 1476.0,
            "content": "而被迫做一些资源有限程度下的创新,",
            "speaker": 2
        },
        {
            "start": 1476.0,
            "end": 1481.0,
            "content": "这些个创新在很多时候都是非常有用的,",
            "speaker": 2
        },
        {
            "start": 1481.0,
            "end": 1485.0,
            "content": "其实也比较鼓励学术界做这一类型的创新,",
            "speaker": 2
        },
        {
            "start": 1485.0,
            "end": 1486.0,
            "content": "因为意味着资源有限,",
            "speaker": 2
        },
        {
            "start": 1486.0,
            "end": 1489.0,
            "content": "学术界就要关注以最小的成本,",
            "speaker": 2
        },
        {
            "start": 1489.0,
            "end": 1494.0,
            "content": "做最大的收益的事情,",
            "speaker": 2
        },
        {
            "start": 1494.0,
            "end": 1498.0,
            "content": "然后其实工业界也需要做最小成本最大收益,",
            "speaker": 2
        },
        {
            "start": 1498.0,
            "end": 1501.0,
            "content": "只是工业界的scale是学术界的scale到100倍,",
            "speaker": 2
        },
        {
            "start": 1501.0,
            "end": 1502.0,
            "content": "所以你要做的事情,",
            "speaker": 2
        },
        {
            "start": 1502.0,
            "end": 1507.0,
            "content": "就是你在学术界当你的资源不够的时候,",
            "speaker": 2
        },
        {
            "start": 1507.0,
            "end": 1511.0,
            "content": "去做那些个在成本限制之下能够最大化收益,",
            "speaker": 2
        },
        {
            "start": 1511.0,
            "end": 1513.0,
            "content": "同时要考虑scaleability,",
            "speaker": 2
        },
        {
            "start": 1513.0,
            "end": 1516.0,
            "content": "就是你的成本限制是真的成本限制,",
            "speaker": 2
        },
        {
            "start": 1516.0,
            "end": 1519.0,
            "content": "就当你的成本扩大100倍之后还是受限,",
            "speaker": 2
        },
        {
            "start": 1519.0,
            "end": 1524.0,
            "content": "然后在这种情况之下怎么去最大化,",
            "speaker": 2
        },
        {
            "start": 1524.0,
            "end": 1526.0,
            "content": "就是给了你工业,",
            "speaker": 2
        },
        {
            "start": 1526.0,
            "end": 1528.0,
            "content": "其实就是即使给了你工业界的卡的数量,",
            "speaker": 2
        },
        {
            "start": 1528.0,
            "end": 1531.0,
            "content": "你还是要做一些个取舍和决策,",
            "speaker": 2
        },
        {
            "start": 1531.0,
            "end": 1534.0,
            "content": "然后在这个时候怎么做你的取舍和决策,",
            "speaker": 2
        },
        {
            "start": 1534.0,
            "end": 1537.0,
            "content": "使得在学术界1%的资源下得到的结论,",
            "speaker": 2
        },
        {
            "start": 1537.0,
            "end": 1542.0,
            "content": "也可以泛化到工业界100倍的时候得到的结论,",
            "speaker": 2
        },
        {
            "start": 1542.0,
            "end": 1545.0,
            "content": "如果是希望这个是apply research的话,",
            "speaker": 2
        },
        {
            "start": 1545.0,
            "end": 1549.0,
            "content": "这个其实是一个非常重要的衡量的指标,",
            "speaker": 2
        },
        {
            "start": 1549.0,
            "end": 1550.0,
            "content": "那在这次会议之中,",
            "speaker": 2
        },
        {
            "start": 1550.0,
            "end": 1556.0,
            "content": "我们也其实看到了非常多的比较好的相关insightful的工作,",
            "speaker": 2
        },
        {
            "start": 1556.0,
            "end": 1560.0,
            "content": "就是除了我自己去研究能力平衡之外,",
            "speaker": 2
        },
        {
            "start": 1560.0,
            "end": 1563.0,
            "content": "就是刚刚提到的MIT的同学,",
            "speaker": 2
        },
        {
            "start": 1563.0,
            "end": 1566.0,
            "content": "一个MIT的朋友他们做的the flat connection,",
            "speaker": 2
        },
        {
            "start": 1566.0,
            "end": 1571.0,
            "content": "也基本上是在一个比较小的数量级的情况之下,",
            "speaker": 2
        },
        {
            "start": 1571.0,
            "end": 1576.0,
            "content": "去衡量数据的组成以及模型能力的平衡,",
            "speaker": 2
        },
        {
            "start": 1576.0,
            "end": 1578.0,
            "content": "这样的一些个实验,",
            "speaker": 2
        },
        {
            "start": 1578.0,
            "end": 1581.0,
            "content": "然后他们也画了一些个小范围的scaling的曲线,",
            "speaker": 2
        },
        {
            "start": 1581.0,
            "end": 1585.0,
            "content": "保证他们的曲线可以外推到更大的数量级,",
            "speaker": 2
        },
        {
            "start": 1585.0,
            "end": 1588.0,
            "content": "我觉得这些都是比较有意义的,",
            "speaker": 2
        },
        {
            "start": 1588.0,
            "end": 1592.0,
            "content": "所以虽然说学术界是有一定程度的资源的限制,",
            "speaker": 2
        },
        {
            "start": 1592.0,
            "end": 1597.0,
            "content": "但是资源并不是阻碍创新的最大障碍。",
            "speaker": 2
        },
        {
            "start": 1597.0,
            "end": 1599.0,
            "content": "我觉得这个角度你说的特别好,",
            "speaker": 1
        },
        {
            "start": 1599.0,
            "end": 1601.0,
            "content": "那在这次的这个会议上,",
            "speaker": 1
        },
        {
            "start": 1601.0,
            "end": 1607.0,
            "content": "你有看到哪一些你觉得学术界有提出比较有意思的一些方向,",
            "speaker": 1
        },
        {
            "start": 1607.0,
            "end": 1610.0,
            "content": "或者说一些可能你之前没有关注到的一些问题吗?",
            "speaker": 1
        },
        {
            "start": 1611.0,
            "end": 1614.0,
            "content": "哇,老实说,",
            "speaker": 2
        },
        {
            "start": 1614.0,
            "end": 1616.0,
            "content": "其实在开会的时候,",
            "speaker": 2
        },
        {
            "start": 1616.0,
            "end": 1618.0,
            "content": "就我开会的风格很多时候是,",
            "speaker": 2
        },
        {
            "start": 1618.0,
            "end": 1622.0,
            "content": "就是在开会之前去找到谁会来这个会议,",
            "speaker": 2
        },
        {
            "start": 1622.0,
            "end": 1624.0,
            "content": "然后提前跟他们发消息,",
            "speaker": 2
        },
        {
            "start": 1624.0,
            "end": 1626.0,
            "content": "跟他们约说能不能聊天聊一下,",
            "speaker": 2
        },
        {
            "start": 1626.0,
            "end": 1629.0,
            "content": "然后我开会的前三天每天就是,",
            "speaker": 2
        },
        {
            "start": 1629.0,
            "end": 1631.0,
            "content": "就比如说我在会场八个小时,",
            "speaker": 2
        },
        {
            "start": 1631.0,
            "end": 1632.0,
            "content": "就是一个小时跟一个人聊,",
            "speaker": 2
        },
        {
            "start": 1632.0,
            "end": 1633.0,
            "content": "另外一个小时跟另外一个人聊,",
            "speaker": 2
        },
        {
            "start": 1633.0,
            "end": 1635.0,
            "content": "另外一个小时跟另外一个人聊,",
            "speaker": 2
        },
        {
            "start": 1635.0,
            "end": 1636.0,
            "content": "这样的结果就是,",
            "speaker": 2
        },
        {
            "start": 1636.0,
            "end": 1640.0,
            "content": "其实看poster和听oral的这些机会,",
            "speaker": 2
        },
        {
            "start": 1640.0,
            "end": 1642.0,
            "content": "就是反而被压缩了,",
            "speaker": 2
        },
        {
            "start": 1642.0,
            "end": 1645.0,
            "content": "反正大部分时候都是在已经跟,",
            "speaker": 2
        },
        {
            "start": 1645.0,
            "end": 1649.0,
            "content": "就是工作非常相关的人直接聊相关的research,",
            "speaker": 2
        },
        {
            "start": 1649.0,
            "end": 1650.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 1650.0,
            "end": 1654.0,
            "content": "但回到就是这次会议本身的这些presentation的话,",
            "speaker": 2
        },
        {
            "start": 1654.0,
            "end": 1660.0,
            "content": "我觉得有很多工作也非常的值得讨论,",
            "speaker": 2
        },
        {
            "start": 1660.0,
            "end": 1663.0,
            "content": "一个是把language model作为一种agent,",
            "speaker": 2
        },
        {
            "start": 1663.0,
            "end": 1665.0,
            "content": "这是一个非常火的话题,",
            "speaker": 2
        },
        {
            "start": 1665.0,
            "end": 1668.0,
            "content": "当然again就是这次会议的投稿,",
            "speaker": 2
        },
        {
            "start": 1668.0,
            "end": 1671.0,
            "content": "在完成工作的时候是在半年之前,",
            "speaker": 2
        },
        {
            "start": 1671.0,
            "end": 1674.0,
            "content": "language model作为一个agent是上个月才火的,",
            "speaker": 2
        },
        {
            "start": 1674.0,
            "end": 1675.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 1675.0,
            "end": 1676.0,
            "content": "但是在半年之前,",
            "speaker": 2
        },
        {
            "start": 1676.0,
            "end": 1677.0,
            "content": "至少是半年之前,",
            "speaker": 2
        },
        {
            "start": 1677.0,
            "end": 1680.0,
            "content": "我们已经看到有一些个同学,",
            "speaker": 2
        },
        {
            "start": 1680.0,
            "end": 1683.0,
            "content": "已经非常的futurism,",
            "speaker": 2
        },
        {
            "start": 1683.0,
            "end": 1687.0,
            "content": "就是他们在半年之前就已经考虑到language model作为一个agent,",
            "speaker": 2
        },
        {
            "start": 1687.0,
            "end": 1689.0,
            "content": "需要考虑的一些个问题,",
            "speaker": 2
        },
        {
            "start": 1689.0,
            "end": 1691.0,
            "content": "然后特别是关于函数调用的问题,",
            "speaker": 2
        },
        {
            "start": 1691.0,
            "end": 1695.0,
            "content": "那我参加了一个让我印象很高的poster,",
            "speaker": 2
        },
        {
            "start": 1695.0,
            "end": 1697.0,
            "content": "是Samuel的一个同学,",
            "speaker": 2
        },
        {
            "start": 1697.0,
            "end": 1699.0,
            "content": "他叫做Armand Madem,",
            "speaker": 2
        },
        {
            "start": 1699.0,
            "end": 1704.0,
            "content": "然后他做的事情是去prompt语言模型,",
            "speaker": 2
        },
        {
            "start": 1704.0,
            "end": 1705.0,
            "content": "然后在prompt的时候,",
            "speaker": 2
        },
        {
            "start": 1705.0,
            "end": 1711.0,
            "content": "让语言就是用了一种自然语言和函数编程,",
            "speaker": 2
        },
        {
            "start": 1711.0,
            "end": 1713.0,
            "content": "混合在一起的prompt,",
            "speaker": 2
        },
        {
            "start": 1713.0,
            "end": 1717.0,
            "content": "使得这个模型的输出既有语言又有函数,",
            "speaker": 2
        },
        {
            "start": 1717.0,
            "end": 1719.0,
            "content": "然后这个函数又有函数,",
            "speaker": 2
        },
        {
            "start": 1719.0,
            "end": 1720.0,
            "content": "那这些个函数的话,",
            "speaker": 2
        },
        {
            "start": 1720.0,
            "end": 1724.0,
            "content": "就这些个编程语言可以用来做各种各样的工具的调用,",
            "speaker": 2
        },
        {
            "start": 1724.0,
            "end": 1728.0,
            "content": "然后在这个同时也可以各种用做符号化推理,",
            "speaker": 2
        },
        {
            "start": 1728.0,
            "end": 1732.0,
            "content": "然后这些东西又可以跟自然语言混合在一起,",
            "speaker": 2
        },
        {
            "start": 1732.0,
            "end": 1733.0,
            "content": "然后again,",
            "speaker": 2
        },
        {
            "start": 1733.0,
            "end": 1736.0,
            "content": "这个东西虽然说最近开始领域变得变火,",
            "speaker": 2
        },
        {
            "start": 1736.0,
            "end": 1739.0,
            "content": "但是他做这件事情是在半年之前做的,",
            "speaker": 2
        },
        {
            "start": 1739.0,
            "end": 1740.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 1740.0,
            "end": 1743.0,
            "content": "所以非常我觉得是非常的future thinking的,",
            "speaker": 2
        },
        {
            "start": 1743.0,
            "end": 1746.0,
            "content": "我昨天晚上跟他就是喝酒喝了很久,",
            "speaker": 2
        },
        {
            "start": 1747.0,
            "end": 1748.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 1748.0,
            "end": 1750.0,
            "content": "就讲这些相关的工作,",
            "speaker": 2
        },
        {
            "start": 1750.0,
            "end": 1752.0,
            "content": "然后我当时在他的poster的时候,",
            "speaker": 2
        },
        {
            "start": 1752.0,
            "end": 1754.0,
            "content": "这个工作也就非常的火嘛,",
            "speaker": 2
        },
        {
            "start": 1754.0,
            "end": 1757.0,
            "content": "当时是我在旁边跟他聊,",
            "speaker": 2
        },
        {
            "start": 1757.0,
            "end": 1759.0,
            "content": "然后有两个OpenAI的朋友,",
            "speaker": 2
        },
        {
            "start": 1759.0,
            "end": 1763.0,
            "content": "然后有DeepMind的朋友也在关注他这方面的工作,",
            "speaker": 2
        },
        {
            "start": 1763.0,
            "end": 1766.0,
            "content": "另外一份工作是斯坦福的工作,",
            "speaker": 2
        },
        {
            "start": 1766.0,
            "end": 1767.0,
            "content": "LMSIS的工作,",
            "speaker": 2
        },
        {
            "start": 1767.0,
            "end": 1771.0,
            "content": "他应该是斯坦福博客利和USSD合作的吧,",
            "speaker": 2
        },
        {
            "start": 1771.0,
            "end": 1772.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 1772.0,
            "end": 1775.0,
            "content": "他们当时的他们这份工作叫做FlexChain,",
            "speaker": 2
        },
        {
            "start": 1775.0,
            "end": 1779.0,
            "content": "他做的事情是你的模型在上线推理的时候,",
            "speaker": 2
        },
        {
            "start": 1779.0,
            "end": 1784.0,
            "content": "希望增大模型在推理过程之中最大化它的吞吐量,",
            "speaker": 2
        },
        {
            "start": 1784.0,
            "end": 1785.0,
            "content": "也就是在,",
            "speaker": 2
        },
        {
            "start": 1785.0,
            "end": 1789.0,
            "content": "也就是最大化的降低模型推理的成本,",
            "speaker": 2
        },
        {
            "start": 1789.0,
            "end": 1791.0,
            "content": "Wikuda的作者是吧,",
            "speaker": 1
        },
        {
            "start": 1791.0,
            "end": 1792.0,
            "content": "对,",
            "speaker": 1
        },
        {
            "start": 1792.0,
            "end": 1793.0,
            "content": "Wikuda团队的作者,",
            "speaker": 2
        },
        {
            "start": 1793.0,
            "end": 1794.0,
            "content": "他们的这篇文章,",
            "speaker": 2
        },
        {
            "start": 1794.0,
            "end": 1798.0,
            "content": "他们这篇文章现在Github上面好像已经有上万颗星了,",
            "speaker": 2
        },
        {
            "start": 1798.0,
            "end": 1800.0,
            "content": "所以就是非常的有用,",
            "speaker": 2
        },
        {
            "start": 1800.0,
            "end": 1801.0,
            "content": "因为大家都需要,",
            "speaker": 2
        },
        {
            "start": 1801.0,
            "end": 1803.0,
            "content": "因为大家现在做,",
            "speaker": 2
        },
        {
            "start": 1803.0,
            "end": 1806.0,
            "content": "发现这个的需求来源于对大语言模型,",
            "speaker": 2
        },
        {
            "start": 1806.0,
            "end": 1807.0,
            "content": "一来是上线,",
            "speaker": 2
        },
        {
            "start": 1807.0,
            "end": 1808.0,
            "content": "二来是evaluation,",
            "speaker": 2
        },
        {
            "start": 1808.0,
            "end": 1813.0,
            "content": "然后evaluation的话就需要一次evaluate特别特别多的数据集,",
            "speaker": 2
        },
        {
            "start": 1813.0,
            "end": 1816.0,
            "content": "就需要增加模型在推理时期的吞吐量,",
            "speaker": 2
        },
        {
            "start": 1816.0,
            "end": 1818.0,
            "content": "就是他们解决的问题,",
            "speaker": 2
        },
        {
            "start": 1818.0,
            "end": 1819.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 1819.0,
            "end": 1821.0,
            "content": "我觉得这篇文章也就是做的非常的好,",
            "speaker": 2
        },
        {
            "start": 1821.0,
            "end": 1822.0,
            "content": "非常的impressive,",
            "speaker": 2
        },
        {
            "start": 1822.0,
            "end": 1823.0,
            "content": "我非常的喜欢,",
            "speaker": 2
        },
        {
            "start": 1823.0,
            "end": 1824.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 1824.0,
            "end": 1826.0,
            "content": "然后还有一篇文章,",
            "speaker": 2
        },
        {
            "start": 1826.0,
            "end": 1829.0,
            "content": "还有一些个文章就是研究,",
            "speaker": 2
        },
        {
            "start": 1829.0,
            "end": 1833.0,
            "content": "我刚刚提到的研究返修数据的组成,",
            "speaker": 2
        },
        {
            "start": 1833.0,
            "end": 1835.0,
            "content": "刚才富尧提到这几篇文章,",
            "speaker": 1
        },
        {
            "start": 1835.0,
            "end": 1838.0,
            "content": "我们也会把这个link放到这个show notes里边,",
            "speaker": 1
        },
        {
            "start": 1838.0,
            "end": 1841.0,
            "content": "如果感兴趣的朋友的话也可以去多看一下,",
            "speaker": 1
        },
        {
            "start": 1841.0,
            "end": 1845.0,
            "content": "其实正好你也提到了第一篇跟这个agent相关的这个文章,",
            "speaker": 1
        },
        {
            "start": 1845.0,
            "end": 1848.0,
            "content": "半年就从meta的这个tool former开始,",
            "speaker": 1
        },
        {
            "start": 1848.0,
            "end": 1852.0,
            "content": "发现可以用大模型来去做这种tool using,",
            "speaker": 1
        },
        {
            "start": 1852.0,
            "end": 1858.0,
            "content": "然后就有auto gpt等等的这一系列的这些工程上的一些project出来,",
            "speaker": 1
        },
        {
            "start": 1858.0,
            "end": 1859.0,
            "content": "让大家关注到,",
            "speaker": 1
        },
        {
            "start": 1859.0,
            "end": 1865.0,
            "content": "但你讲的很有意思的一点是学界其实在半年前就已经有人在做方面的尝试,",
            "speaker": 1
        },
        {
            "start": 1865.0,
            "end": 1866.0,
            "content": "那这大半年以来,",
            "speaker": 1
        },
        {
            "start": 1866.0,
            "end": 1871.0,
            "content": "就是你真实看到说这个把大语言模型作为一个agent来做,",
            "speaker": 1
        },
        {
            "start": 1871.0,
            "end": 1875.0,
            "content": "现在出现了有哪一些大家发现了一些挑战,",
            "speaker": 1
        },
        {
            "start": 1875.0,
            "end": 1880.0,
            "content": "还有这半年以前以来这些新的一些解法和突破呢?",
            "speaker": 1
        },
        {
            "start": 1880.0,
            "end": 1881.0,
            "content": "OK,",
            "speaker": 1
        },
        {
            "start": 1881.0,
            "end": 1884.0,
            "content": "我们认为大语言模型作为agent,",
            "speaker": 2
        },
        {
            "start": 1885.0,
            "end": 1889.0,
            "content": "它是一个非常非常有非常非常promising的方向,",
            "speaker": 2
        },
        {
            "start": 1889.0,
            "end": 1891.0,
            "content": "我们觉得它可以开创非常大的未来,",
            "speaker": 2
        },
        {
            "start": 1891.0,
            "end": 1895.0,
            "content": "但是当前也会有非常大的挑战,",
            "speaker": 2
        },
        {
            "start": 1895.0,
            "end": 1898.0,
            "content": "其实最大的挑战就是这个demo都非常的fancy,",
            "speaker": 2
        },
        {
            "start": 1898.0,
            "end": 1899.0,
            "content": "但是在实际用的时候,",
            "speaker": 2
        },
        {
            "start": 1899.0,
            "end": 1900.0,
            "content": "第一,",
            "speaker": 2
        },
        {
            "start": 1900.0,
            "end": 1904.0,
            "content": "他不一定每次都能够完成你给他下达的任务,",
            "speaker": 2
        },
        {
            "start": 1904.0,
            "end": 1905.0,
            "content": "二来,",
            "speaker": 2
        },
        {
            "start": 1905.0,
            "end": 1906.0,
            "content": "他可能能够完成任务,",
            "speaker": 2
        },
        {
            "start": 1906.0,
            "end": 1907.0,
            "content": "但是呢,",
            "speaker": 2
        },
        {
            "start": 1907.0,
            "end": 1910.0,
            "content": "他可能中间会试错错非常非常多回,",
            "speaker": 2
        },
        {
            "start": 1910.0,
            "end": 1912.0,
            "content": "以至于他完成了你的任务,",
            "speaker": 2
        },
        {
            "start": 1912.0,
            "end": 1913.0,
            "content": "但他花的钱实在是太多了,",
            "speaker": 2
        },
        {
            "start": 1913.0,
            "end": 1914.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 1914.0,
            "end": 1919.0,
            "content": "这些是一个现在两个比较pressing的问题,",
            "speaker": 2
        },
        {
            "start": 1919.0,
            "end": 1921.0,
            "content": "然后去拆解这些个问题的话,",
            "speaker": 2
        },
        {
            "start": 1921.0,
            "end": 1924.0,
            "content": "就会拆解的非常非常的细,",
            "speaker": 2
        },
        {
            "start": 1924.0,
            "end": 1927.0,
            "content": "首先它涉及到这些个模型的基础能力,",
            "speaker": 2
        },
        {
            "start": 1927.0,
            "end": 1929.0,
            "content": "这个模型的基础能力的话可以拆解成,",
            "speaker": 2
        },
        {
            "start": 1929.0,
            "end": 1934.0,
            "content": "把自然语言和函数调用混在一起用的能力,",
            "speaker": 2
        },
        {
            "start": 1934.0,
            "end": 1936.0,
            "content": "然后调用函数本身的能力,",
            "speaker": 2
        },
        {
            "start": 1936.0,
            "end": 1938.0,
            "content": "是调用工具本身的能力,",
            "speaker": 2
        },
        {
            "start": 1938.0,
            "end": 1942.0,
            "content": "然后逻辑推理的能力,",
            "speaker": 2
        },
        {
            "start": 1942.0,
            "end": 1944.0,
            "content": "然后常识性的推理的能力,",
            "speaker": 2
        },
        {
            "start": 1944.0,
            "end": 1947.0,
            "content": "因为有些个推理他不像他他没有很多,",
            "speaker": 2
        },
        {
            "start": 1947.0,
            "end": 1951.0,
            "content": "其他他不是他不是非常非常精确的推理,",
            "speaker": 2
        },
        {
            "start": 1951.0,
            "end": 1953.0,
            "content": "很多的推理比较的比较模糊,",
            "speaker": 2
        },
        {
            "start": 1953.0,
            "end": 1955.0,
            "content": "有多种中间路径都可以,",
            "speaker": 2
        },
        {
            "start": 1955.0,
            "end": 1957.0,
            "content": "你要做你要做饭,",
            "speaker": 2
        },
        {
            "start": 1957.0,
            "end": 1959.0,
            "content": "你的也放多一点放少一点,",
            "speaker": 2
        },
        {
            "start": 1959.0,
            "end": 1961.0,
            "content": "这个就是味道都都还ok,",
            "speaker": 2
        },
        {
            "start": 1961.0,
            "end": 1964.0,
            "content": "只要你在那只要你在可以容忍的模糊范围之内,",
            "speaker": 2
        },
        {
            "start": 1964.0,
            "end": 1966.0,
            "content": "但是有些个推理是非常精确的,",
            "speaker": 2
        },
        {
            "start": 1966.0,
            "end": 1968.0,
            "content": "所以你中间每一步都不能错,",
            "speaker": 2
        },
        {
            "start": 1968.0,
            "end": 1972.0,
            "content": "跟函数或工具调用的推理比较涉及到精确的推理,",
            "speaker": 2
        },
        {
            "start": 1972.0,
            "end": 1975.0,
            "content": "然后把函数和工具调用的结果,",
            "speaker": 2
        },
        {
            "start": 1975.0,
            "end": 1978.0,
            "content": "以及他工具调用的过程翻译成自然语言,",
            "speaker": 2
        },
        {
            "start": 1978.0,
            "end": 1981.0,
            "content": "在涉及到精准推理和模糊推理的一种过渡,",
            "speaker": 2
        },
        {
            "start": 1981.0,
            "end": 1983.0,
            "content": "然后在自然语言的空间之中,",
            "speaker": 2
        },
        {
            "start": 1983.0,
            "end": 1985.0,
            "content": "很多推理是模糊性的推理,",
            "speaker": 2
        },
        {
            "start": 1985.0,
            "end": 1991.0,
            "content": "然后怎么样让模型可以在这样子不同的推理方式之下反复横跳,",
            "speaker": 2
        },
        {
            "start": 1991.0,
            "end": 1995.0,
            "content": "应该是一个现在还在尝试解决的事情,",
            "speaker": 2
        },
        {
            "start": 1995.0,
            "end": 1999.0,
            "content": "然后我们发现again还是更大的模型,",
            "speaker": 2
        },
        {
            "start": 1999.0,
            "end": 2002.0,
            "content": "在做这方面的任务的时候可以变得更好,",
            "speaker": 2
        },
        {
            "start": 2002.0,
            "end": 2006.0,
            "content": "但是我们也同样倾向于相信小一点的模型,",
            "speaker": 2
        },
        {
            "start": 2006.0,
            "end": 2008.0,
            "content": "在做这方面的任务,",
            "speaker": 2
        },
        {
            "start": 2008.0,
            "end": 2011.0,
            "content": "他们的能力还没有被挖掘到上限,",
            "speaker": 2
        },
        {
            "start": 2011.0,
            "end": 2013.0,
            "content": "所以我们现在还在挖掘,",
            "speaker": 2
        },
        {
            "start": 2013.0,
            "end": 2015.0,
            "content": "无论是大模型和小模型,",
            "speaker": 2
        },
        {
            "start": 2015.0,
            "end": 2019.0,
            "content": "在这方面我们还在挖掘能力上限的这个过程之中,",
            "speaker": 2
        },
        {
            "start": 2019.0,
            "end": 2021.0,
            "content": "挖掘能力上限又有很多种方法,",
            "speaker": 2
        },
        {
            "start": 2021.0,
            "end": 2024.0,
            "content": "你可以通过prompting的方法,",
            "speaker": 2
        },
        {
            "start": 2024.0,
            "end": 2029.0,
            "content": "把language model调用工具作为agent,",
            "speaker": 2
        },
        {
            "start": 2029.0,
            "end": 2033.0,
            "content": "其实也是在都不是半年之前了,",
            "speaker": 2
        },
        {
            "start": 2033.0,
            "end": 2036.0,
            "content": "是几乎一年之前就开始研究了,",
            "speaker": 2
        },
        {
            "start": 2036.0,
            "end": 2042.0,
            "content": "我自己其实在一年之前也有一篇大模型相关调用工具相关的文章,",
            "speaker": 2
        },
        {
            "start": 2042.0,
            "end": 2046.0,
            "content": "然后Samuel也在一年之前有调用工具相关的文章,",
            "speaker": 2
        },
        {
            "start": 2046.0,
            "end": 2048.0,
            "content": "所以我可以理解说,",
            "speaker": 1
        },
        {
            "start": 2048.0,
            "end": 2054.0,
            "content": "现在agent的这些我们看到的一些应用中的挑战,",
            "speaker": 1
        },
        {
            "start": 2054.0,
            "end": 2061.0,
            "content": "它核心还是由LM底座的能力本身来决定了它的上限,",
            "speaker": 1
        },
        {
            "start": 2061.0,
            "end": 2065.0,
            "content": "在调用的这个project,",
            "speaker": 1
        },
        {
            "start": 2065.0,
            "end": 2068.0,
            "content": "他们又是在什么层面上去解决这些问题?",
            "speaker": 1
        },
        {
            "start": 2068.0,
            "end": 2073.0,
            "content": "他们其实很多时候是在prompting的层面和funtune的层面解决这个问题,",
            "speaker": 2
        },
        {
            "start": 2073.0,
            "end": 2076.0,
            "content": "虽然说底座模型的能力决定的模型,",
            "speaker": 2
        },
        {
            "start": 2076.0,
            "end": 2081.0,
            "content": "作为一个agent在执行任务的时候的效率的上限,",
            "speaker": 2
        },
        {
            "start": 2081.0,
            "end": 2088.0,
            "content": "但是如何通过更好的prompting的方式把底座模型的能力完全发挥出来,",
            "speaker": 2
        },
        {
            "start": 2088.0,
            "end": 2091.0,
            "content": "也是一件非常困难的事情,",
            "speaker": 2
        },
        {
            "start": 2091.0,
            "end": 2098.0,
            "content": "我觉得这个真的是需要在做这方面的人是非常好的prompting engineer,",
            "speaker": 2
        },
        {
            "start": 2098.0,
            "end": 2102.0,
            "content": "我觉得一个比较好的例子是pipelinex.ai这个应用,",
            "speaker": 2
        },
        {
            "start": 2102.0,
            "end": 2104.0,
            "content": "他们是专门做搜索的,",
            "speaker": 2
        },
        {
            "start": 2104.0,
            "end": 2109.0,
            "content": "他们的搜索和他们专门做是AI对话加搜索,",
            "speaker": 2
        },
        {
            "start": 2109.0,
            "end": 2111.0,
            "content": "然后他们的事情做得非常的精细,",
            "speaker": 2
        },
        {
            "start": 2111.0,
            "end": 2113.0,
            "content": "首先他们的prompt写得非常的好,",
            "speaker": 2
        },
        {
            "start": 2113.0,
            "end": 2115.0,
            "content": "然后他们在搜索的时候,",
            "speaker": 2
        },
        {
            "start": 2115.0,
            "end": 2120.0,
            "content": "他们对于他们的信息源和搜索的内容的拆分也拆分的非常的精细,",
            "speaker": 2
        },
        {
            "start": 2120.0,
            "end": 2125.0,
            "content": "然后他们在agent在做搜索,",
            "speaker": 2
        },
        {
            "start": 2125.0,
            "end": 2128.0,
            "content": "返回给用户以及与用户对话,",
            "speaker": 2
        },
        {
            "start": 2128.0,
            "end": 2134.0,
            "content": "然后做新一轮的搜索和整理信息的过程也做得特别的顺滑,",
            "speaker": 2
        },
        {
            "start": 2134.0,
            "end": 2138.0,
            "content": "我觉得这一系列的东西都是需要下功夫的,",
            "speaker": 2
        },
        {
            "start": 2138.0,
            "end": 2141.0,
            "content": "虽然说底座模型决定了能力上限,",
            "speaker": 2
        },
        {
            "start": 2141.0,
            "end": 2152.0,
            "content": "但是我觉得现在业界的平均水准还并没有到把底座模型的上限完全发挥出来的一个状态,",
            "speaker": 2
        },
        {
            "start": 2152.0,
            "end": 2160.0,
            "content": "我是觉得现在的业界平均水准在挖掘底座模型的前提可以远远的得到加强。",
            "speaker": 2
        },
        {
            "start": 2160.0,
            "end": 2163.0,
            "content": "我们现在知道他的底座模型是什么吗?",
            "speaker": 1
        },
        {
            "start": 2163.0,
            "end": 2165.0,
            "content": "也是他自己pre-trained的一个模型吗?",
            "speaker": 1
        },
        {
            "start": 2165.0,
            "end": 2167.0,
            "content": "应该他们是调用的GPT吧。",
            "speaker": 2
        },
        {
            "start": 2167.0,
            "end": 2171.0,
            "content": "所以说他在GPT的基础上,",
            "speaker": 1
        },
        {
            "start": 2171.0,
            "end": 2178.0,
            "content": "然后通过prompt engineering的方式就可以实现一个比较好的agent的实现。",
            "speaker": 1
        },
        {
            "start": 2178.0,
            "end": 2181.0,
            "content": "对,你要真正写agent的prompt engineering的话,",
            "speaker": 2
        },
        {
            "start": 2181.0,
            "end": 2184.0,
            "content": "那个prompt是真的非常的难写,",
            "speaker": 2
        },
        {
            "start": 2184.0,
            "end": 2186.0,
            "content": "就跟写一个代码项目一样,",
            "speaker": 2
        },
        {
            "start": 2186.0,
            "end": 2191.0,
            "content": "但此时你就不是用python写你的项目了,",
            "speaker": 2
        },
        {
            "start": 2191.0,
            "end": 2195.0,
            "content": "你就是用你的自然语言去描述一个代码项目。",
            "speaker": 2
        },
        {
            "start": 2195.0,
            "end": 2198.0,
            "content": "如果你去看写得比较好的prompt代码的话,",
            "speaker": 2
        },
        {
            "start": 2198.0,
            "end": 2199.0,
            "content": "你会发现,",
            "speaker": 2
        },
        {
            "start": 2199.0,
            "end": 2203.0,
            "content": "首先他也就会像一个代码项目一样分成很多个文件,",
            "speaker": 2
        },
        {
            "start": 2203.0,
            "end": 2205.0,
            "content": "然后文件之间有调用,",
            "speaker": 2
        },
        {
            "start": 2205.0,
            "end": 2207.0,
            "content": "因为可能会有一个prompt调用另外一个prompt,",
            "speaker": 2
        },
        {
            "start": 2207.0,
            "end": 2210.0,
            "content": "对,此时被调的prompt本身就变成一种工具。",
            "speaker": 2
        },
        {
            "start": 2210.0,
            "end": 2214.0,
            "content": "对,然后就是还有各种各样的optimization版本的迭代,",
            "speaker": 2
        },
        {
            "start": 2214.0,
            "end": 2217.0,
            "content": "然后对于不同版本底座模型的适配,",
            "speaker": 2
        },
        {
            "start": 2217.0,
            "end": 2221.0,
            "content": "然后这一系列都是需要花挺多的功夫的。",
            "speaker": 2
        },
        {
            "start": 2221.0,
            "end": 2224.0,
            "content": "我曾经问过我的一个同学,",
            "speaker": 2
        },
        {
            "start": 2224.0,
            "end": 2226.0,
            "content": "你在写agent的时候,",
            "speaker": 2
        },
        {
            "start": 2226.0,
            "end": 2228.0,
            "content": "你的prompt engineering大概花多久的时间,",
            "speaker": 2
        },
        {
            "start": 2228.0,
            "end": 2229.0,
            "content": "他说花一个月。",
            "speaker": 2
        },
        {
            "start": 2229.0,
            "end": 2230.0,
            "content": "对,差不多就是。",
            "speaker": 2
        },
        {
            "start": 2230.0,
            "end": 2233.0,
            "content": "其实这不是跟写一个软件的实验一样。",
            "speaker": 1
        },
        {
            "start": 2233.0,
            "end": 2234.0,
            "content": "对,对,对,就是这个样子。",
            "speaker": 1
        },
        {
            "start": 2234.0,
            "end": 2235.0,
            "content": "那如果这样的话,",
            "speaker": 1
        },
        {
            "start": 2235.0,
            "end": 2237.0,
            "content": "你是一个非常重的一个prompt,",
            "speaker": 1
        },
        {
            "start": 2237.0,
            "end": 2242.0,
            "content": "这个会使得我每次run这个agent的成本太高吗?",
            "speaker": 1
        },
        {
            "start": 2242.0,
            "end": 2244.0,
            "content": "这个可以,",
            "speaker": 2
        },
        {
            "start": 2244.0,
            "end": 2246.0,
            "content": "他不是说prompt非常多,",
            "speaker": 2
        },
        {
            "start": 2246.0,
            "end": 2247.0,
            "content": "prompt非常的长,",
            "speaker": 2
        },
        {
            "start": 2247.0,
            "end": 2250.0,
            "content": "而是说你的prompt有很多个文件,",
            "speaker": 2
        },
        {
            "start": 2250.0,
            "end": 2253.0,
            "content": "然后你每次会动态地选一个prompt去调用,",
            "speaker": 2
        },
        {
            "start": 2253.0,
            "end": 2256.0,
            "content": "但是这个单个的被选中的prompt并没有很长。",
            "speaker": 2
        },
        {
            "start": 2256.0,
            "end": 2259.0,
            "content": "最近你在业界有看到有哪些研究,",
            "speaker": 1
        },
        {
            "start": 2259.0,
            "end": 2265.0,
            "content": "你觉得是能够帮大家比较好的去实现agent的这个问题?",
            "speaker": 1
        },
        {
            "start": 2265.0,
            "end": 2268.0,
            "content": "我觉得现在业界里面的研究,",
            "speaker": 2
        },
        {
            "start": 2268.0,
            "end": 2270.0,
            "content": "更多还是关注在怎么,",
            "speaker": 2
        },
        {
            "start": 2270.0,
            "end": 2274.0,
            "content": "一来是prompt你的基础模型,",
            "speaker": 2
        },
        {
            "start": 2274.0,
            "end": 2276.0,
            "content": "让它做更好的工具的调用,",
            "speaker": 2
        },
        {
            "start": 2276.0,
            "end": 2278.0,
            "content": "然后怎么,",
            "speaker": 2
        },
        {
            "start": 2278.0,
            "end": 2283.0,
            "content": "二来是怎么把一个复杂的任务拆解成一些个更加简单的,",
            "speaker": 2
        },
        {
            "start": 2283.0,
            "end": 2285.0,
            "content": "简单的小任务,",
            "speaker": 2
        },
        {
            "start": 2285.0,
            "end": 2287.0,
            "content": "就怎么去做任务的拆分,",
            "speaker": 2
        },
        {
            "start": 2287.0,
            "end": 2293.0,
            "content": "然后就是当你的agent的数量变多之后,",
            "speaker": 2
        },
        {
            "start": 2293.0,
            "end": 2297.0,
            "content": "怎么对于不同的agent之间的任务相互协调,",
            "speaker": 2
        },
        {
            "start": 2297.0,
            "end": 2298.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 2298.0,
            "end": 2305.0,
            "content": "现在我觉得我们就应该是停留在比如说五个以内的agent,",
            "speaker": 2
        },
        {
            "start": 2305.0,
            "end": 2310.0,
            "content": "然后能够调用的工具可能就是十几二十种,",
            "speaker": 2
        },
        {
            "start": 2310.0,
            "end": 2312.0,
            "content": "然后几十种的工具已经算挺多的了,",
            "speaker": 2
        },
        {
            "start": 2312.0,
            "end": 2315.0,
            "content": "当然也有调用一千多种工具这种,",
            "speaker": 2
        },
        {
            "start": 2315.0,
            "end": 2317.0,
            "content": "调用可能就是比较大,",
            "speaker": 2
        },
        {
            "start": 2317.0,
            "end": 2322.0,
            "content": "但是现在就是demo效果比较好的也可能就十几二十种工具,",
            "speaker": 2
        },
        {
            "start": 2322.0,
            "end": 2326.0,
            "content": "然后就是五个以下的agent的数量,",
            "speaker": 2
        },
        {
            "start": 2326.0,
            "end": 2330.0,
            "content": "然后一个问题如果要被拆分的话,",
            "speaker": 2
        },
        {
            "start": 2330.0,
            "end": 2332.0,
            "content": "它可能不会被拆分的,",
            "speaker": 2
        },
        {
            "start": 2332.0,
            "end": 2336.0,
            "content": "可能就是拆分成一个小问题的话,",
            "speaker": 2
        },
        {
            "start": 2336.0,
            "end": 2339.0,
            "content": "可能就是五六步的这样的一个子问题,",
            "speaker": 2
        },
        {
            "start": 2339.0,
            "end": 2341.0,
            "content": "但是如果子问题数量太多的话,",
            "speaker": 2
        },
        {
            "start": 2341.0,
            "end": 2343.0,
            "content": "可能也会比较更难一点,",
            "speaker": 2
        },
        {
            "start": 2343.0,
            "end": 2348.0,
            "content": "我觉得这个是现在学术界存在的状态,",
            "speaker": 2
        },
        {
            "start": 2348.0,
            "end": 2351.0,
            "content": "但我觉得这个状态完完全全没有够到顶,",
            "speaker": 2
        },
        {
            "start": 2351.0,
            "end": 2355.0,
            "content": "我觉得刚刚说到的那些个数字都可以更多一个数量级,",
            "speaker": 2
        },
        {
            "start": 2355.0,
            "end": 2357.0,
            "content": "都可以再往上面加个零,",
            "speaker": 2
        },
        {
            "start": 2357.0,
            "end": 2360.0,
            "content": "这是什么给了你这样的信心?",
            "speaker": 1
        },
        {
            "start": 2360.0,
            "end": 2362.0,
            "content": "因为我自己做过这个,",
            "speaker": 2
        },
        {
            "start": 2362.0,
            "end": 2366.0,
            "content": "我最近的一篇文章就是投给NewRibs的,",
            "speaker": 2
        },
        {
            "start": 2367.0,
            "end": 2373.0,
            "content": "我们当时是一个negotiation的游戏,",
            "speaker": 2
        },
        {
            "start": 2373.0,
            "end": 2376.0,
            "content": "就是让两个模型讨价还价,",
            "speaker": 2
        },
        {
            "start": 2376.0,
            "end": 2379.0,
            "content": "然后在讨价还价的过程之中,",
            "speaker": 2
        },
        {
            "start": 2379.0,
            "end": 2382.0,
            "content": "我们还有第三个模型给他们做教练,",
            "speaker": 2
        },
        {
            "start": 2382.0,
            "end": 2385.0,
            "content": "说你上一轮砍价的过程之中没有发挥好,",
            "speaker": 2
        },
        {
            "start": 2385.0,
            "end": 2387.0,
            "content": "然后告诉他你什么地方没有发挥好,",
            "speaker": 2
        },
        {
            "start": 2387.0,
            "end": 2390.0,
            "content": "然后你的目标就是要买家的话,",
            "speaker": 2
        },
        {
            "start": 2390.0,
            "end": 2391.0,
            "content": "就是买一个东西,",
            "speaker": 2
        },
        {
            "start": 2391.0,
            "end": 2392.0,
            "content": "我们当时买一个气球,",
            "speaker": 2
        },
        {
            "start": 2392.0,
            "end": 2393.0,
            "content": "让他买的更便宜,",
            "speaker": 2
        },
        {
            "start": 2393.0,
            "end": 2396.0,
            "content": "卖家的话就是让他卖的更贵,",
            "speaker": 2
        },
        {
            "start": 2396.0,
            "end": 2400.0,
            "content": "然后我们希望就是他就一轮一轮的砍下来,",
            "speaker": 2
        },
        {
            "start": 2400.0,
            "end": 2404.0,
            "content": "希望每一轮都能够有更好的价格,",
            "speaker": 2
        },
        {
            "start": 2404.0,
            "end": 2406.0,
            "content": "我们当时是做了这样的一件事情,",
            "speaker": 2
        },
        {
            "start": 2406.0,
            "end": 2408.0,
            "content": "然后我们当时还有一个moderator,",
            "speaker": 2
        },
        {
            "start": 2408.0,
            "end": 2410.0,
            "content": "相当于一个裁判,",
            "speaker": 2
        },
        {
            "start": 2410.0,
            "end": 2413.0,
            "content": "来去看就是场上选手们,",
            "speaker": 2
        },
        {
            "start": 2413.0,
            "end": 2415.0,
            "content": "就是在砍价的过程之中,",
            "speaker": 2
        },
        {
            "start": 2415.0,
            "end": 2417.0,
            "content": "有没有遵守规则,",
            "speaker": 2
        },
        {
            "start": 2417.0,
            "end": 2421.0,
            "content": "然后他的价格和photo是否在合理的区间,",
            "speaker": 2
        },
        {
            "start": 2421.0,
            "end": 2422.0,
            "content": "这样的事情,",
            "speaker": 2
        },
        {
            "start": 2422.0,
            "end": 2423.0,
            "content": "你看这就有四个agent,",
            "speaker": 2
        },
        {
            "start": 2423.0,
            "end": 2424.0,
            "content": "一个买家,",
            "speaker": 2
        },
        {
            "start": 2424.0,
            "end": 2425.0,
            "content": "卖家,",
            "speaker": 2
        },
        {
            "start": 2425.0,
            "end": 2426.0,
            "content": "然后一个教练,",
            "speaker": 2
        },
        {
            "start": 2426.0,
            "end": 2427.0,
            "content": "然后一个裁判,",
            "speaker": 2
        },
        {
            "start": 2427.0,
            "end": 2431.0,
            "content": "然后我们在做的这个过程之中,",
            "speaker": 2
        },
        {
            "start": 2431.0,
            "end": 2434.0,
            "content": "我们发现GP3.5就能做,",
            "speaker": 2
        },
        {
            "start": 2434.0,
            "end": 2435.0,
            "content": "但GP4会做更好,",
            "speaker": 2
        },
        {
            "start": 2435.0,
            "end": 2437.0,
            "content": "然后cloud也可以做,",
            "speaker": 2
        },
        {
            "start": 2437.0,
            "end": 2439.0,
            "content": "cloud的不同的模型的版本也都可以做,",
            "speaker": 2
        },
        {
            "start": 2439.0,
            "end": 2441.0,
            "content": "并且我在做这件事情的时候,",
            "speaker": 2
        },
        {
            "start": 2441.0,
            "end": 2446.0,
            "content": "我当时是因为时间关系做了一个多月,",
            "speaker": 2
        },
        {
            "start": 2446.0,
            "end": 2449.0,
            "content": "然后投了文章之后,",
            "speaker": 2
        },
        {
            "start": 2449.0,
            "end": 2452.0,
            "content": "我就没有接着去往下面深挖下去的,",
            "speaker": 2
        },
        {
            "start": 2452.0,
            "end": 2455.0,
            "content": "但是我觉得这个项目在接着push的话,",
            "speaker": 2
        },
        {
            "start": 2455.0,
            "end": 2457.0,
            "content": "就是更多的工具的调用,",
            "speaker": 2
        },
        {
            "start": 2457.0,
            "end": 2459.0,
            "content": "然后更多的agent加进来,",
            "speaker": 2
        },
        {
            "start": 2459.0,
            "end": 2462.0,
            "content": "然后就是比如说你可以有多个教练,",
            "speaker": 2
        },
        {
            "start": 2462.0,
            "end": 2465.0,
            "content": "然后你可以有多个选手,",
            "speaker": 2
        },
        {
            "start": 2465.0,
            "end": 2466.0,
            "content": "然后你不一定需要砍价,",
            "speaker": 2
        },
        {
            "start": 2466.0,
            "end": 2467.0,
            "content": "你可以打狼人杀,",
            "speaker": 2
        },
        {
            "start": 2467.0,
            "end": 2469.0,
            "content": "狼人杀的话至少要五个人,",
            "speaker": 2
        },
        {
            "start": 2469.0,
            "end": 2471.0,
            "content": "所以就这些个东西,",
            "speaker": 2
        },
        {
            "start": 2471.0,
            "end": 2473.0,
            "content": "我在自己做完了一遍之后,",
            "speaker": 2
        },
        {
            "start": 2473.0,
            "end": 2475.0,
            "content": "我就觉得这些东西完全可以做,",
            "speaker": 2
        },
        {
            "start": 2476.0,
            "end": 2480.0,
            "content": "如果我现在能够有一个比如说一周的空闲的时间的话,",
            "speaker": 2
        },
        {
            "start": 2480.0,
            "end": 2484.0,
            "content": "让我去写一个狼人杀的AI,",
            "speaker": 2
        },
        {
            "start": 2484.0,
            "end": 2486.0,
            "content": "然后让他们玩玩圈圈打起来的话,",
            "speaker": 2
        },
        {
            "start": 2486.0,
            "end": 2489.0,
            "content": "我是有信心把这个东西给写出来的,",
            "speaker": 2
        },
        {
            "start": 2489.0,
            "end": 2491.0,
            "content": "所以就是因为我自己,",
            "speaker": 2
        },
        {
            "start": 2491.0,
            "end": 2493.0,
            "content": "那从我自己的现身体会之中,",
            "speaker": 2
        },
        {
            "start": 2493.0,
            "end": 2497.0,
            "content": "我觉得首先我自己当时做那个项目,",
            "speaker": 2
        },
        {
            "start": 2497.0,
            "end": 2499.0,
            "content": "我们后面把它投给NeurIPS,",
            "speaker": 2
        },
        {
            "start": 2499.0,
            "end": 2501.0,
            "content": "那个会议也非常的值得参加,",
            "speaker": 2
        },
        {
            "start": 2501.0,
            "end": 2504.0,
            "content": "会比现在这个会就是人更多,",
            "speaker": 2
        },
        {
            "start": 2505.0,
            "end": 2508.0,
            "content": "我当时把它投给NeurIPS,",
            "speaker": 2
        },
        {
            "start": 2508.0,
            "end": 2511.0,
            "content": "然后我做完之后,",
            "speaker": 2
        },
        {
            "start": 2511.0,
            "end": 2513.0,
            "content": "我就觉得玩玩圈圈有各种各样的东西,",
            "speaker": 2
        },
        {
            "start": 2513.0,
            "end": 2515.0,
            "content": "可以值得被scale up,",
            "speaker": 2
        },
        {
            "start": 2515.0,
            "end": 2520.0,
            "content": "然后我前两天跟Samuel的同学聊这方面的时候,",
            "speaker": 2
        },
        {
            "start": 2520.0,
            "end": 2524.0,
            "content": "就是那个做站语言和函数站语混在一起的同学,",
            "speaker": 2
        },
        {
            "start": 2524.0,
            "end": 2526.0,
            "content": "我们也觉得就这方面完全可以scale up,",
            "speaker": 2
        },
        {
            "start": 2526.0,
            "end": 2528.0,
            "content": "基本上如果在这行的话,",
            "speaker": 2
        },
        {
            "start": 2528.0,
            "end": 2531.0,
            "content": "就会觉得这些东西完全都可以做,",
            "speaker": 2
        },
        {
            "start": 2531.0,
            "end": 2534.0,
            "content": "而且要怎么做也其实还挺清楚的。",
            "speaker": 2
        },
        {
            "start": 2534.0,
            "end": 2536.0,
            "content": "你刚才提到这个negotiation,",
            "speaker": 1
        },
        {
            "start": 2536.0,
            "end": 2538.0,
            "content": "就是这个谈判的这个场景,",
            "speaker": 1
        },
        {
            "start": 2538.0,
            "end": 2542.0,
            "content": "还是在你给定他的一个环境中去发生,",
            "speaker": 1
        },
        {
            "start": 2542.0,
            "end": 2545.0,
            "content": "要做一个所谓个人助手的这些startup,",
            "speaker": 1
        },
        {
            "start": 2545.0,
            "end": 2548.0,
            "content": "大家还是希望说我能够用它来调用很多,",
            "speaker": 1
        },
        {
            "start": 2548.0,
            "end": 2550.0,
            "content": "我现实生活中的一些工具,",
            "speaker": 1
        },
        {
            "start": 2550.0,
            "end": 2552.0,
            "content": "除了大家能够想到的一些API,",
            "speaker": 1
        },
        {
            "start": 2552.0,
            "end": 2554.0,
            "content": "连接方面的之外,",
            "speaker": 1
        },
        {
            "start": 2554.0,
            "end": 2556.0,
            "content": "你觉得还会有哪一些在模型能力,",
            "speaker": 1
        },
        {
            "start": 2556.0,
            "end": 2560.0,
            "content": "或者说在调用层面的一些困难吗?",
            "speaker": 1
        },
        {
            "start": 2561.0,
            "end": 2568.0,
            "content": "就是如果我们的目标是把模型变成一个个人助手的话,",
            "speaker": 2
        },
        {
            "start": 2568.0,
            "end": 2574.0,
            "content": "首先它现在的模型能力一定程度上已经可以做这件事情了,",
            "speaker": 2
        },
        {
            "start": 2574.0,
            "end": 2579.0,
            "content": "就是我比较确信一些个比较强的hacker,",
            "speaker": 2
        },
        {
            "start": 2579.0,
            "end": 2582.0,
            "content": "肯定他们自己已经开发了一套自己的,",
            "speaker": 2
        },
        {
            "start": 2582.0,
            "end": 2585.0,
            "content": "就是电脑上面的模型作为个人助手,",
            "speaker": 2
        },
        {
            "start": 2585.0,
            "end": 2586.0,
            "content": "然后调用各种各样的事情,",
            "speaker": 2
        },
        {
            "start": 2586.0,
            "end": 2588.0,
            "content": "我知道有人在已经做了这个事情了,",
            "speaker": 2
        },
        {
            "start": 2588.0,
            "end": 2592.0,
            "content": "并且我自己也曾经考虑过要不要就是写一下,",
            "speaker": 2
        },
        {
            "start": 2592.0,
            "end": 2595.0,
            "content": "让这个模型可以给我浏览,",
            "speaker": 2
        },
        {
            "start": 2595.0,
            "end": 2599.0,
            "content": "就是每天新发的论文,",
            "speaker": 2
        },
        {
            "start": 2599.0,
            "end": 2602.0,
            "content": "然后把这些个论文通过我的标准,",
            "speaker": 2
        },
        {
            "start": 2602.0,
            "end": 2604.0,
            "content": "把好坏给我筛出来,",
            "speaker": 2
        },
        {
            "start": 2604.0,
            "end": 2606.0,
            "content": "筛完之后给我做一下总结,",
            "speaker": 2
        },
        {
            "start": 2606.0,
            "end": 2609.0,
            "content": "就我曾经想过把这一套东西自动化,",
            "speaker": 2
        },
        {
            "start": 2609.0,
            "end": 2611.0,
            "content": "我觉得这东西是完全可以做的,",
            "speaker": 2
        },
        {
            "start": 2611.0,
            "end": 2616.0,
            "content": "我只是没有一周的那个完完全全空余的时间去写这个代码,",
            "speaker": 2
        },
        {
            "start": 2616.0,
            "end": 2619.0,
            "content": "如果听众中有哪一位这个比方说博士生,",
            "speaker": 1
        },
        {
            "start": 2619.0,
            "end": 2621.0,
            "content": "想要跟傅瑶一起来合作,",
            "speaker": 1
        },
        {
            "start": 2621.0,
            "end": 2623.0,
            "content": "帮他一起来完成这个的,",
            "speaker": 1
        },
        {
            "start": 2623.0,
            "end": 2624.0,
            "content": "我相信会是很有意思的,",
            "speaker": 1
        },
        {
            "start": 2624.0,
            "end": 2627.0,
            "content": "可以在我们留言或者给我们私信,",
            "speaker": 1
        },
        {
            "start": 2627.0,
            "end": 2631.0,
            "content": "对,就是我觉得就是做个人助手这方面很多事情,",
            "speaker": 2
        },
        {
            "start": 2631.0,
            "end": 2634.0,
            "content": "就是完完全全现在就已经能做了,",
            "speaker": 2
        },
        {
            "start": 2634.0,
            "end": 2637.0,
            "content": "然后我们的做研究的话,",
            "speaker": 2
        },
        {
            "start": 2637.0,
            "end": 2640.0,
            "content": "我们其实是在探的是这个模型的上限,",
            "speaker": 2
        },
        {
            "start": 2640.0,
            "end": 2644.0,
            "content": "希望模型在什么样的空间之内能够更大的提高,",
            "speaker": 2
        },
        {
            "start": 2644.0,
            "end": 2650.0,
            "content": "我自己做的那个项目其实是想知道模型在就prompt有多大的程度,",
            "speaker": 2
        },
        {
            "start": 2650.0,
            "end": 2653.0,
            "content": "可以把模型的能力往上面推到多高,",
            "speaker": 2
        },
        {
            "start": 2653.0,
            "end": 2656.0,
            "content": "这个可能是研究和工程的区别,",
            "speaker": 2
        },
        {
            "start": 2656.0,
            "end": 2660.0,
            "content": "研究可能是需要去看这个模型的上限和这个模型的未来,",
            "speaker": 2
        },
        {
            "start": 2660.0,
            "end": 2664.0,
            "content": "然后工程的话就是很多东西都具完完全全现在就可以做,",
            "speaker": 2
        },
        {
            "start": 2664.0,
            "end": 2669.0,
            "content": "然后我们觉得就是首先把它变成个人助手的话,",
            "speaker": 2
        },
        {
            "start": 2670.0,
            "end": 2675.0,
            "content": "就是它可能能力的范围也是一个从窄往上面扩的一个范围,",
            "speaker": 2
        },
        {
            "start": 2675.0,
            "end": 2680.0,
            "content": "就是我觉得一个比较好的approach就是你首先有个非常精准的,",
            "speaker": 2
        },
        {
            "start": 2680.0,
            "end": 2682.0,
            "content": "这样你希望他给你做的事情,",
            "speaker": 2
        },
        {
            "start": 2682.0,
            "end": 2685.0,
            "content": "就是每天把新的论文给我做summarization,",
            "speaker": 2
        },
        {
            "start": 2685.0,
            "end": 2688.0,
            "content": "但是其实不止summarization,",
            "speaker": 2
        },
        {
            "start": 2688.0,
            "end": 2693.0,
            "content": "因为你还需要去上网把那些论文的源头给拿过来,",
            "speaker": 2
        },
        {
            "start": 2693.0,
            "end": 2696.0,
            "content": "然后再把它们汇总在一起,",
            "speaker": 2
        },
        {
            "start": 2696.0,
            "end": 2698.0,
            "content": "变成一个notion的文档,",
            "speaker": 2
        },
        {
            "start": 2698.0,
            "end": 2701.0,
            "content": "然后再变成notion文档之后再做summarization,",
            "speaker": 2
        },
        {
            "start": 2701.0,
            "end": 2706.0,
            "content": "summarization的时候里面的专有名词和数字不可以出错,",
            "speaker": 2
        },
        {
            "start": 2706.0,
            "end": 2709.0,
            "content": "然后summarize完了之后还要告诉我,",
            "speaker": 2
        },
        {
            "start": 2709.0,
            "end": 2712.0,
            "content": "就是他读完之后的take away insights是什么,",
            "speaker": 2
        },
        {
            "start": 2712.0,
            "end": 2719.0,
            "content": "然后我觉得比如说就是从一种比较concrete的应用为基础,",
            "speaker": 2
        },
        {
            "start": 2719.0,
            "end": 2723.0,
            "content": "然后再往外扩是一个比较好的工程上面的路径,",
            "speaker": 2
        },
        {
            "start": 2723.0,
            "end": 2728.0,
            "content": "要不然就是如果你的应用不是刚需的话,",
            "speaker": 2
        },
        {
            "start": 2728.0,
            "end": 2733.0,
            "content": "很可能就是做的东西就是demo很fancy,",
            "speaker": 2
        },
        {
            "start": 2733.0,
            "end": 2737.0,
            "content": "但是稍微比较虚无一点,",
            "speaker": 2
        },
        {
            "start": 2737.0,
            "end": 2740.0,
            "content": "我在我的自己的朋友之中,",
            "speaker": 2
        },
        {
            "start": 2740.0,
            "end": 2748.0,
            "content": "会定期不定期的发一些我自己觉得比较好的文章的一个合集,",
            "speaker": 2
        },
        {
            "start": 2748.0,
            "end": 2750.0,
            "content": "我把它叫做AI Chief's Pick,",
            "speaker": 2
        },
        {
            "start": 2750.0,
            "end": 2752.0,
            "content": "就是主厨推荐,",
            "speaker": 2
        },
        {
            "start": 2752.0,
            "end": 2754.0,
            "content": "当然这个也跟朋友一起做,",
            "speaker": 2
        },
        {
            "start": 2754.0,
            "end": 2755.0,
            "content": "朋友也会一起发,",
            "speaker": 2
        },
        {
            "start": 2755.0,
            "end": 2759.0,
            "content": "然后我们发现如果有这个东西的话,",
            "speaker": 2
        },
        {
            "start": 2759.0,
            "end": 2760.0,
            "content": "就是所有人,",
            "speaker": 2
        },
        {
            "start": 2760.0,
            "end": 2763.0,
            "content": "基本上是在我们这行的所有人都特别的需要,",
            "speaker": 2
        },
        {
            "start": 2763.0,
            "end": 2768.0,
            "content": "但现在他就是在一个就是我们人来去做这件事情,",
            "speaker": 2
        },
        {
            "start": 2768.0,
            "end": 2771.0,
            "content": "但我们倾向于相信机器是可以做的,",
            "speaker": 2
        },
        {
            "start": 2771.0,
            "end": 2776.0,
            "content": "当然也有可能会说就你在挑文章的时候需要一定程度的鉴赏力,",
            "speaker": 2
        },
        {
            "start": 2776.0,
            "end": 2778.0,
            "content": "这个其实非常的重要,",
            "speaker": 2
        },
        {
            "start": 2778.0,
            "end": 2784.0,
            "content": "但是我在这方面对于我写的模型的prompter经过了高强度的优化,",
            "speaker": 2
        },
        {
            "start": 2784.0,
            "end": 2789.0,
            "content": "基本上是我能够把我想到的对于模型的鉴赏力,",
            "speaker": 2
        },
        {
            "start": 2789.0,
            "end": 2792.0,
            "content": "然后使劲浑身献术写这个prompter,",
            "speaker": 2
        },
        {
            "start": 2792.0,
            "end": 2795.0,
            "content": "让这个模型也有这方面的鉴赏力,",
            "speaker": 2
        },
        {
            "start": 2795.0,
            "end": 2801.0,
            "content": "在这个使用LM的时候的一个困难是说,",
            "speaker": 1
        },
        {
            "start": 2801.0,
            "end": 2804.0,
            "content": "比方说我要总结一篇很长的文章,",
            "speaker": 1
        },
        {
            "start": 2804.0,
            "end": 2806.0,
            "content": "他可能只记得头和尾,",
            "speaker": 1
        },
        {
            "start": 2806.0,
            "end": 2810.0,
            "content": "这个现在为什么会有这种现象,",
            "speaker": 1
        },
        {
            "start": 2810.0,
            "end": 2816.0,
            "content": "这个的确很像人的这个理解,",
            "speaker": 2
        },
        {
            "start": 2816.0,
            "end": 2818.0,
            "content": "我们通常不就是看头看尾,",
            "speaker": 1
        },
        {
            "start": 2818.0,
            "end": 2820.0,
            "content": "中间就不怎么看了,",
            "speaker": 1
        },
        {
            "start": 2820.0,
            "end": 2825.0,
            "content": "我觉得可能有很多原因吧,",
            "speaker": 2
        },
        {
            "start": 2825.0,
            "end": 2832.0,
            "content": "首先这个大模型的训练数据就是从人的自然产生的训练数据中得到的,",
            "speaker": 2
        },
        {
            "start": 2832.0,
            "end": 2836.0,
            "content": "然后人在自然写一篇文章的时候,",
            "speaker": 2
        },
        {
            "start": 2836.0,
            "end": 2838.0,
            "content": "比如说你要写论文,",
            "speaker": 2
        },
        {
            "start": 2838.0,
            "end": 2840.0,
            "content": "你天生就会把重点放到头和尾,",
            "speaker": 2
        },
        {
            "start": 2840.0,
            "end": 2847.0,
            "content": "然后写大部分的文章天生都是把重点放到头和尾,",
            "speaker": 2
        },
        {
            "start": 2847.0,
            "end": 2850.0,
            "content": "比如说在这个对于股票分析师来说,",
            "speaker": 1
        },
        {
            "start": 2850.0,
            "end": 2851.0,
            "content": "二级市场,",
            "speaker": 1
        },
        {
            "start": 2851.0,
            "end": 2853.0,
            "content": "有时候我要去分析他这个earnings core,",
            "speaker": 1
        },
        {
            "start": 2853.0,
            "end": 2855.0,
            "content": "他并不是一篇文章,",
            "speaker": 1
        },
        {
            "start": 2855.0,
            "end": 2856.0,
            "content": "他是一个transcript,",
            "speaker": 1
        },
        {
            "start": 2856.0,
            "end": 2859.0,
            "content": "他是不应该有这样的一个权重的,",
            "speaker": 1
        },
        {
            "start": 2859.0,
            "end": 2861.0,
            "content": "所以说大模型在这种场景下,",
            "speaker": 1
        },
        {
            "start": 2861.0,
            "end": 2863.0,
            "content": "很多有时候一些企业的内部场景下,",
            "speaker": 1
        },
        {
            "start": 2863.0,
            "end": 2865.0,
            "content": "这个就会面临一个,",
            "speaker": 1
        },
        {
            "start": 2865.0,
            "end": 2866.0,
            "content": "就会有点挑战,",
            "speaker": 1
        },
        {
            "start": 2866.0,
            "end": 2869.0,
            "content": "这个是一个在prompt层面上就可以去解决的东西,",
            "speaker": 1
        },
        {
            "start": 2869.0,
            "end": 2871.0,
            "content": "那我觉得在这方面的问题,",
            "speaker": 2
        },
        {
            "start": 2871.0,
            "end": 2875.0,
            "content": "就是他跟lost in the middle还不大一样,",
            "speaker": 2
        },
        {
            "start": 2875.0,
            "end": 2876.0,
            "content": "lost in the middle,",
            "speaker": 2
        },
        {
            "start": 2876.0,
            "end": 2880.0,
            "content": "他就是这种观察的现象更多的是说,",
            "speaker": 2
        },
        {
            "start": 2880.0,
            "end": 2884.0,
            "content": "你的问题是比较generic,",
            "speaker": 2
        },
        {
            "start": 2884.0,
            "end": 2890.0,
            "content": "然后你所需要的信息很多时候就是来源于文章的头和尾,",
            "speaker": 2
        },
        {
            "start": 2890.0,
            "end": 2892.0,
            "content": "但是像刚刚你说的那种场景,",
            "speaker": 2
        },
        {
            "start": 2892.0,
            "end": 2896.0,
            "content": "很多时候是我们是需要对一个transcript中间一小段精准的提出来,",
            "speaker": 2
        },
        {
            "start": 2896.0,
            "end": 2903.0,
            "content": "这相当于是要就是模型有能力去对他的输入本身的,",
            "speaker": 2
        },
        {
            "start": 2903.0,
            "end": 2905.0,
            "content": "你给模型一个很长的输入,",
            "speaker": 2
        },
        {
            "start": 2905.0,
            "end": 2909.0,
            "content": "这些模型输入之中某一个片段的信息非常的重要,",
            "speaker": 2
        },
        {
            "start": 2909.0,
            "end": 2911.0,
            "content": "然后你希望这个模型可以提出来这些个片段,",
            "speaker": 2
        },
        {
            "start": 2911.0,
            "end": 2913.0,
            "content": "他能够识别并且提出来,",
            "speaker": 2
        },
        {
            "start": 2913.0,
            "end": 2915.0,
            "content": "至少我在用cloud的时候,",
            "speaker": 2
        },
        {
            "start": 2915.0,
            "end": 2916.0,
            "content": "我觉得还行,",
            "speaker": 2
        },
        {
            "start": 2916.0,
            "end": 2918.0,
            "content": "我觉得是对这方面经过了优化的,",
            "speaker": 2
        },
        {
            "start": 2919.0,
            "end": 2921.0,
            "content": "并且我觉得这个方面是可优化的,",
            "speaker": 2
        },
        {
            "start": 2921.0,
            "end": 2926.0,
            "content": "所以对于这种就是像会议机要R0 core transcript这种东西,",
            "speaker": 2
        },
        {
            "start": 2926.0,
            "end": 2928.0,
            "content": "其中间部分重要片段,",
            "speaker": 2
        },
        {
            "start": 2928.0,
            "end": 2930.0,
            "content": "我觉得这个东西是一个可以被解决的问题,",
            "speaker": 2
        },
        {
            "start": 2930.0,
            "end": 2931.0,
            "content": "明白,",
            "speaker": 2
        },
        {
            "start": 2931.0,
            "end": 2933.0,
            "content": "相信关注这个领域的同学都会知道,",
            "speaker": 1
        },
        {
            "start": 2933.0,
            "end": 2934.0,
            "content": "应该是上周吧,",
            "speaker": 1
        },
        {
            "start": 2934.0,
            "end": 2937.0,
            "content": "这个Meta发布了这个全新的Lama2,",
            "speaker": 1
        },
        {
            "start": 2937.0,
            "end": 2941.0,
            "content": "而且更重要是这个Lama2是可以商用的,",
            "speaker": 1
        },
        {
            "start": 2941.0,
            "end": 2945.0,
            "content": "如果你的用户量不超过7亿的用户,",
            "speaker": 1
        },
        {
            "start": 2945.0,
            "end": 2948.0,
            "content": "但我觉得其实这个对于大部分的公司来说都可以,",
            "speaker": 1
        },
        {
            "start": 2948.0,
            "end": 2949.0,
            "content": "已经足够适用了,",
            "speaker": 1
        },
        {
            "start": 2949.0,
            "end": 2952.0,
            "content": "我觉得已经是个挺高的一个门槛了,",
            "speaker": 1
        },
        {
            "start": 2952.0,
            "end": 2957.0,
            "content": "所以就是对于可能还没有来得及去深度研究Lama2的同学,",
            "speaker": 1
        },
        {
            "start": 2957.0,
            "end": 2959.0,
            "content": "可以给大家简单介绍一下,",
            "speaker": 1
        },
        {
            "start": 2959.0,
            "end": 2962.0,
            "content": "就是这一次比起第一代的Lama,",
            "speaker": 1
        },
        {
            "start": 2962.0,
            "end": 2965.0,
            "content": "让你自己觉得比较impressive的一些更新是什么?",
            "speaker": 1
        },
        {
            "start": 2965.0,
            "end": 2971.0,
            "content": "我觉得Lama2这次最重要的更新是他把enablement的部分,",
            "speaker": 2
        },
        {
            "start": 2971.0,
            "end": 2973.0,
            "content": "特别是你怎么要做RLHF,",
            "speaker": 2
        },
        {
            "start": 2973.0,
            "end": 2978.0,
            "content": "以及RLHF对于模型带来的比较精细的细颗粒度的影响,",
            "speaker": 2
        },
        {
            "start": 2978.0,
            "end": 2980.0,
            "content": "讲的还是比较清楚的,",
            "speaker": 2
        },
        {
            "start": 2980.0,
            "end": 2984.0,
            "content": "这个在Lama1的文章之中是完完全全没有讲的,",
            "speaker": 2
        },
        {
            "start": 2984.0,
            "end": 2988.0,
            "content": "基本上是Lama2的一个比较重点的内容是,",
            "speaker": 2
        },
        {
            "start": 2988.0,
            "end": 2991.0,
            "content": "他们的RLHF做了5个版本迭代,",
            "speaker": 2
        },
        {
            "start": 2991.0,
            "end": 2995.0,
            "content": "然后在这之前还有两次的SFT的迭代,",
            "speaker": 2
        },
        {
            "start": 2995.0,
            "end": 2998.0,
            "content": "就相当于他是先给你看了SFT,",
            "speaker": 2
        },
        {
            "start": 2998.0,
            "end": 3000.0,
            "content": "做完一遍之后效果提到什么地方,",
            "speaker": 2
        },
        {
            "start": 3000.0,
            "end": 3003.0,
            "content": "然后第二次SFT又提一点点,",
            "speaker": 2
        },
        {
            "start": 3003.0,
            "end": 3006.0,
            "content": "然后RLHF的时候有两种不同的算法,",
            "speaker": 2
        },
        {
            "start": 3006.0,
            "end": 3009.0,
            "content": "一种是Best of N,一种是PPO,",
            "speaker": 2
        },
        {
            "start": 3009.0,
            "end": 3011.0,
            "content": "PPO是完整的RL的方法,",
            "speaker": 2
        },
        {
            "start": 3011.0,
            "end": 3015.0,
            "content": "Best of N有点像SFT和RL之间的一种方法,",
            "speaker": 2
        },
        {
            "start": 3015.0,
            "end": 3019.0,
            "content": "他在RLHF5个版本迭代的时候,",
            "speaker": 2
        },
        {
            "start": 3019.0,
            "end": 3021.0,
            "content": "前三个版本用的是Best of N,",
            "speaker": 2
        },
        {
            "start": 3021.0,
            "end": 3023.0,
            "content": "到后两个版本的时候才用的PPO,",
            "speaker": 2
        },
        {
            "start": 3023.0,
            "end": 3026.0,
            "content": "就这样的精细化的路径,",
            "speaker": 2
        },
        {
            "start": 3026.0,
            "end": 3031.0,
            "content": "对于我觉得学术界或者开源界的启发,",
            "speaker": 2
        },
        {
            "start": 3031.0,
            "end": 3033.0,
            "content": "还是非常非常大的,",
            "speaker": 2
        },
        {
            "start": 3033.0,
            "end": 3038.0,
            "content": "基本上在Lama2做RLHF的这个report之前,",
            "speaker": 2
        },
        {
            "start": 3038.0,
            "end": 3042.0,
            "content": "在这方面的研究还是非常非常的少的,",
            "speaker": 2
        },
        {
            "start": 3042.0,
            "end": 3044.0,
            "content": "就会有一些,但是非常非常的少,",
            "speaker": 2
        },
        {
            "start": 3044.0,
            "end": 3047.0,
            "content": "也没有像Lama2这样子的惊喜,",
            "speaker": 2
        },
        {
            "start": 3047.0,
            "end": 3050.0,
            "content": "就相当于他把一个missing piece给补回来了,",
            "speaker": 2
        },
        {
            "start": 3050.0,
            "end": 3052.0,
            "content": "给拼起来了,",
            "speaker": 2
        },
        {
            "start": 3052.0,
            "end": 3055.0,
            "content": "我觉得这个是Lama2最重要的take away,",
            "speaker": 2
        },
        {
            "start": 3055.0,
            "end": 3060.0,
            "content": "然后Lama2当然你在实际跟他说的时候,",
            "speaker": 2
        },
        {
            "start": 3060.0,
            "end": 3062.0,
            "content": "他可能会过于安全的,",
            "speaker": 2
        },
        {
            "start": 3062.0,
            "end": 3064.0,
            "content": "就是你问他,",
            "speaker": 2
        },
        {
            "start": 3064.0,
            "end": 3069.0,
            "content": "你说一个程序员他会跑很多线程和进程,",
            "speaker": 2
        },
        {
            "start": 3069.0,
            "end": 3071.0,
            "content": "我如何kill掉一个进程,",
            "speaker": 2
        },
        {
            "start": 3071.0,
            "end": 3073.0,
            "content": "如何杀掉一个进程,",
            "speaker": 2
        },
        {
            "start": 3073.0,
            "end": 3075.0,
            "content": "这个kill也被认为是,",
            "speaker": 2
        },
        {
            "start": 3075.0,
            "end": 3077.0,
            "content": "其实你是杀一个程序,",
            "speaker": 2
        },
        {
            "start": 3077.0,
            "end": 3079.0,
            "content": "但是他会说我不能够杀人,",
            "speaker": 2
        },
        {
            "start": 3079.0,
            "end": 3083.0,
            "content": "他会有这样子的一个反馈,",
            "speaker": 2
        },
        {
            "start": 3083.0,
            "end": 3085.0,
            "content": "那就是安全可能做的有点过了头,",
            "speaker": 2
        },
        {
            "start": 3085.0,
            "end": 3089.0,
            "content": "我们现在倾向于认为他做安全做的有点过了头,",
            "speaker": 2
        },
        {
            "start": 3089.0,
            "end": 3092.0,
            "content": "但是他做安全做过头了也是有原因的,",
            "speaker": 2
        },
        {
            "start": 3092.0,
            "end": 3096.0,
            "content": "因为在去年好像是去年12月份的时候,",
            "speaker": 2
        },
        {
            "start": 3096.0,
            "end": 3099.0,
            "content": "他们发了一个模型叫Galactica,",
            "speaker": 2
        },
        {
            "start": 3099.0,
            "end": 3102.0,
            "content": "是专门做科学领域的帮你读论文的,",
            "speaker": 2
        },
        {
            "start": 3102.0,
            "end": 3104.0,
            "content": "然后制造很多论文信息的模型,",
            "speaker": 2
        },
        {
            "start": 3104.0,
            "end": 3108.0,
            "content": "这个模型就当时就没怎么做特别多的安全,",
            "speaker": 2
        },
        {
            "start": 3108.0,
            "end": 3110.0,
            "content": "于是上来之后各种胡说八道,",
            "speaker": 2
        },
        {
            "start": 3110.0,
            "end": 3112.0,
            "content": "然后上线两天就被喷下架了,",
            "speaker": 2
        },
        {
            "start": 3112.0,
            "end": 3114.0,
            "content": "所以他们这次吸取了教训,",
            "speaker": 2
        },
        {
            "start": 3114.0,
            "end": 3117.0,
            "content": "但是吸取的有点过头,",
            "speaker": 2
        },
        {
            "start": 3117.0,
            "end": 3120.0,
            "content": "我们觉得是这方面的原因,",
            "speaker": 2
        },
        {
            "start": 3120.0,
            "end": 3124.0,
            "content": "但我们觉得对于安全方面的一些measurement的话,",
            "speaker": 2
        },
        {
            "start": 3124.0,
            "end": 3127.0,
            "content": "就是过头比不做要好得多,",
            "speaker": 2
        },
        {
            "start": 3127.0,
            "end": 3129.0,
            "content": "就是宁可你做的过一些,",
            "speaker": 2
        },
        {
            "start": 3129.0,
            "end": 3130.0,
            "content": "因为做的过一些的话,",
            "speaker": 2
        },
        {
            "start": 3130.0,
            "end": 3133.0,
            "content": "你还可以在后期的版本迭代把它慢慢给调回来,",
            "speaker": 2
        },
        {
            "start": 3133.0,
            "end": 3138.0,
            "content": "但是就得有这样的一个意识,",
            "speaker": 2
        },
        {
            "start": 3138.0,
            "end": 3140.0,
            "content": "其实Galactica下架的时候,",
            "speaker": 2
        },
        {
            "start": 3140.0,
            "end": 3145.0,
            "content": "我在推特上面还跟OpenAI的head of policy",
            "speaker": 2
        },
        {
            "start": 3145.0,
            "end": 3149.0,
            "content": "有一些个讨论说,",
            "speaker": 2
        },
        {
            "start": 3149.0,
            "end": 3152.0,
            "content": "如果Meta在发布Galactica的时候,",
            "speaker": 2
        },
        {
            "start": 3152.0,
            "end": 3157.0,
            "content": "对于安全做得更重要一点的话,",
            "speaker": 2
        },
        {
            "start": 3157.0,
            "end": 3158.0,
            "content": "结局会不会不一样,",
            "speaker": 2
        },
        {
            "start": 3158.0,
            "end": 3159.0,
            "content": "然后Miles说,",
            "speaker": 2
        },
        {
            "start": 3159.0,
            "end": 3162.0,
            "content": "其实只要是有这方面的意识,",
            "speaker": 2
        },
        {
            "start": 3162.0,
            "end": 3165.0,
            "content": "然后documentation写得更加的明确一点,",
            "speaker": 2
        },
        {
            "start": 3165.0,
            "end": 3170.0,
            "content": "然后在这方面跟外界的这个沟通的过程之中,",
            "speaker": 2
        },
        {
            "start": 3170.0,
            "end": 3173.0,
            "content": "去展示一些对安全方面的努力,",
            "speaker": 2
        },
        {
            "start": 3173.0,
            "end": 3174.0,
            "content": "这样子的话,",
            "speaker": 2
        },
        {
            "start": 3174.0,
            "end": 3177.0,
            "content": "其实可能对公众的反馈也都会好很多,",
            "speaker": 2
        },
        {
            "start": 3177.0,
            "end": 3181.0,
            "content": "那显然Meta在这方面做了非常多的工作,",
            "speaker": 2
        },
        {
            "start": 3181.0,
            "end": 3182.0,
            "content": "我觉得是一个很好的事情,",
            "speaker": 2
        },
        {
            "start": 3182.0,
            "end": 3189.0,
            "content": "他们不仅仅是模型本身做了很多安全的相关工作,",
            "speaker": 2
        },
        {
            "start": 3189.0,
            "end": 3190.0,
            "content": "做过头了,",
            "speaker": 2
        },
        {
            "start": 3190.0,
            "end": 3193.0,
            "content": "然后同样的他们在他们的文档之中,",
            "speaker": 2
        },
        {
            "start": 3193.0,
            "end": 3194.0,
            "content": "网页之中,",
            "speaker": 2
        },
        {
            "start": 3194.0,
            "end": 3200.0,
            "content": "也强调了一些他们为了模型的无害化,",
            "speaker": 2
        },
        {
            "start": 3200.0,
            "end": 3201.0,
            "content": "做出来的努力,",
            "speaker": 2
        },
        {
            "start": 3201.0,
            "end": 3204.0,
            "content": "以及就要求用户也就遵循这方面的规则,",
            "speaker": 2
        },
        {
            "start": 3204.0,
            "end": 3209.0,
            "content": "我觉得这是一个朝着好的规则和约束的方向去发展,",
            "speaker": 2
        },
        {
            "start": 3209.0,
            "end": 3212.0,
            "content": "那其实我也大概看了一下他那个报告,",
            "speaker": 1
        },
        {
            "start": 3212.0,
            "end": 3215.0,
            "content": "然后其实Lama2其实在这个,",
            "speaker": 1
        },
        {
            "start": 3215.0,
            "end": 3217.0,
            "content": "他也增加了很多数据量,",
            "speaker": 1
        },
        {
            "start": 3217.0,
            "end": 3218.0,
            "content": "对吧,",
            "speaker": 1
        },
        {
            "start": 3218.0,
            "end": 3220.0,
            "content": "这个参数量也提高了很多,",
            "speaker": 1
        },
        {
            "start": 3220.0,
            "end": 3223.0,
            "content": "但他所提出出来的这些数据,",
            "speaker": 1
        },
        {
            "start": 3223.0,
            "end": 3227.0,
            "content": "使用的数据的情况也属于使用数据的方法上,",
            "speaker": 1
        },
        {
            "start": 3227.0,
            "end": 3229.0,
            "content": "你觉得有什么亮点,",
            "speaker": 1
        },
        {
            "start": 3229.0,
            "end": 3233.0,
            "content": "如果光是从机座模型的能力去看的话,",
            "speaker": 2
        },
        {
            "start": 3233.0,
            "end": 3236.0,
            "content": "那么就机座模型的能力分布以及提升,",
            "speaker": 2
        },
        {
            "start": 3236.0,
            "end": 3239.0,
            "content": "跟那么一区别并没有很大,",
            "speaker": 2
        },
        {
            "start": 3239.0,
            "end": 3242.0,
            "content": "就是这也是为什么我们认为那么去的大头是在,",
            "speaker": 2
        },
        {
            "start": 3242.0,
            "end": 3243.0,
            "content": "那么的方向,",
            "speaker": 2
        },
        {
            "start": 3243.0,
            "end": 3244.0,
            "content": "而不是给你的方向,",
            "speaker": 2
        },
        {
            "start": 3244.0,
            "end": 3246.0,
            "content": "所以你去比较那么去的机座模型,",
            "speaker": 2
        },
        {
            "start": 3247.0,
            "end": 3249.0,
            "content": "其实是差不多的高度相似,",
            "speaker": 2
        },
        {
            "start": 3249.0,
            "end": 3254.0,
            "content": "然后那么就这次并没有披露他们机座模型的数据组成,",
            "speaker": 2
        },
        {
            "start": 3254.0,
            "end": 3256.0,
            "content": "这件可以理解的事情,",
            "speaker": 2
        },
        {
            "start": 3256.0,
            "end": 3257.0,
            "content": "但是呢,",
            "speaker": 2
        },
        {
            "start": 3257.0,
            "end": 3259.0,
            "content": "他们在文章中也讲的,",
            "speaker": 2
        },
        {
            "start": 3259.0,
            "end": 3263.0,
            "content": "就是在他们的机座模型之中,",
            "speaker": 2
        },
        {
            "start": 3263.0,
            "end": 3268.0,
            "content": "就是就是减少了很多个人信息,",
            "speaker": 2
        },
        {
            "start": 3268.0,
            "end": 3270.0,
            "content": "就是就是为了保护个人信息,",
            "speaker": 2
        },
        {
            "start": 3270.0,
            "end": 3272.0,
            "content": "本来可能不小心加到,",
            "speaker": 2
        },
        {
            "start": 3272.0,
            "end": 3274.0,
            "content": "因为你在爬数据的时候真的会,",
            "speaker": 2
        },
        {
            "start": 3274.0,
            "end": 3278.0,
            "content": "就是就是在无意识的爬到很多,",
            "speaker": 2
        },
        {
            "start": 3278.0,
            "end": 3279.0,
            "content": "就是呃,",
            "speaker": 2
        },
        {
            "start": 3279.0,
            "end": 3281.0,
            "content": "被泄露的个人的信息啊,",
            "speaker": 2
        },
        {
            "start": 3281.0,
            "end": 3282.0,
            "content": "住址啊,",
            "speaker": 2
        },
        {
            "start": 3282.0,
            "end": 3283.0,
            "content": "这方面的东西,",
            "speaker": 2
        },
        {
            "start": 3283.0,
            "end": 3284.0,
            "content": "就你都不知道怎么卸的,",
            "speaker": 2
        },
        {
            "start": 3284.0,
            "end": 3286.0,
            "content": "而且还有就是各种各样的,",
            "speaker": 2
        },
        {
            "start": 3286.0,
            "end": 3287.0,
            "content": "因为网络就这样子的吧,",
            "speaker": 2
        },
        {
            "start": 3287.0,
            "end": 3288.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3288.0,
            "end": 3289.0,
            "content": "然后你就把它爬到了,",
            "speaker": 2
        },
        {
            "start": 3289.0,
            "end": 3291.0,
            "content": "然后他们应该是做了很大的力气,",
            "speaker": 2
        },
        {
            "start": 3291.0,
            "end": 3293.0,
            "content": "去把这部分的内容给清洗出去了,",
            "speaker": 2
        },
        {
            "start": 3293.0,
            "end": 3294.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3294.0,
            "end": 3295.0,
            "content": "对,",
            "speaker": 1
        },
        {
            "start": 3295.0,
            "end": 3296.0,
            "content": "嗯,",
            "speaker": 1
        },
        {
            "start": 3296.0,
            "end": 3297.0,
            "content": "这个还挺有意思,",
            "speaker": 1
        },
        {
            "start": 3297.0,
            "end": 3299.0,
            "content": "就是其实他们的机座能力并没有很大的,",
            "speaker": 1
        },
        {
            "start": 3299.0,
            "end": 3300.0,
            "content": "这个这个增强,",
            "speaker": 1
        },
        {
            "start": 3300.0,
            "end": 3301.0,
            "content": "嗯,",
            "speaker": 1
        },
        {
            "start": 3301.0,
            "end": 3302.0,
            "content": "对对,",
            "speaker": 2
        },
        {
            "start": 3302.0,
            "end": 3303.0,
            "content": "那么去的机座呢,",
            "speaker": 2
        },
        {
            "start": 3303.0,
            "end": 3304.0,
            "content": "其实你的这个模型,",
            "speaker": 2
        },
        {
            "start": 3304.0,
            "end": 3305.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3305.0,
            "end": 3307.0,
            "content": "你并没有显著超过那么旺,",
            "speaker": 2
        },
        {
            "start": 3307.0,
            "end": 3308.0,
            "content": "非常相似,",
            "speaker": 2
        },
        {
            "start": 3308.0,
            "end": 3309.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3309.0,
            "end": 3310.0,
            "content": "好一点点,",
            "speaker": 2
        },
        {
            "start": 3310.0,
            "end": 3311.0,
            "content": "就每每样都好一点点,",
            "speaker": 2
        },
        {
            "start": 3311.0,
            "end": 3312.0,
            "content": "但不是那种呃,",
            "speaker": 2
        },
        {
            "start": 3312.0,
            "end": 3313.0,
            "content": "严格增强,",
            "speaker": 2
        },
        {
            "start": 3313.0,
            "end": 3314.0,
            "content": "那所以我们会看到,",
            "speaker": 1
        },
        {
            "start": 3314.0,
            "end": 3316.0,
            "content": "那他会有所谓的这个,",
            "speaker": 1
        },
        {
            "start": 3316.0,
            "end": 3317.0,
            "content": "这个alignment text,",
            "speaker": 1
        },
        {
            "start": 3317.0,
            "end": 3318.0,
            "content": "呃,",
            "speaker": 1
        },
        {
            "start": 3318.0,
            "end": 3319.0,
            "content": "就是因为他在二来,",
            "speaker": 2
        },
        {
            "start": 3319.0,
            "end": 3321.0,
            "content": "你刚才提到他在二来美上去做了,",
            "speaker": 1
        },
        {
            "start": 3321.0,
            "end": 3323.0,
            "content": "应该有应该交了很多,",
            "speaker": 2
        },
        {
            "start": 3323.0,
            "end": 3324.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3324.0,
            "end": 3325.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3325.0,
            "end": 3326.0,
            "content": "有点过头,",
            "speaker": 2
        },
        {
            "start": 3326.0,
            "end": 3327.0,
            "content": "对对,",
            "speaker": 1
        },
        {
            "start": 3327.0,
            "end": 3328.0,
            "content": "那比如说他在那基座能力,",
            "speaker": 1
        },
        {
            "start": 3328.0,
            "end": 3329.0,
            "content": "就这个模型能力之外呢,",
            "speaker": 1
        },
        {
            "start": 3329.0,
            "end": 3330.0,
            "content": "就是你还靠什么,",
            "speaker": 1
        },
        {
            "start": 3330.0,
            "end": 3332.0,
            "content": "就是让他们能力上有提升的这个,",
            "speaker": 1
        },
        {
            "start": 3332.0,
            "end": 3333.0,
            "content": "对对对,",
            "speaker": 1
        },
        {
            "start": 3333.0,
            "end": 3334.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3334.0,
            "end": 3335.0,
            "content": "就是其实,",
            "speaker": 2
        },
        {
            "start": 3335.0,
            "end": 3337.0,
            "content": "其实他们也讲了很多,",
            "speaker": 2
        },
        {
            "start": 3337.0,
            "end": 3339.0,
            "content": "就是如果你在Name的时候,",
            "speaker": 2
        },
        {
            "start": 3339.0,
            "end": 3341.0,
            "content": "你在做RHF的时候,",
            "speaker": 2
        },
        {
            "start": 3341.0,
            "end": 3342.0,
            "content": "如果不加安全指甲,",
            "speaker": 2
        },
        {
            "start": 3342.0,
            "end": 3343.0,
            "content": "还要分的是的话,",
            "speaker": 2
        },
        {
            "start": 3343.0,
            "end": 3344.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3344.0,
            "end": 3346.0,
            "content": "这个模型的能力会有怎样的上升趋势,",
            "speaker": 2
        },
        {
            "start": 3346.0,
            "end": 3348.0,
            "content": "这个上升趋势也挺明显的,",
            "speaker": 2
        },
        {
            "start": 3348.0,
            "end": 3349.0,
            "content": "就意味着,",
            "speaker": 2
        },
        {
            "start": 3349.0,
            "end": 3350.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3350.0,
            "end": 3352.0,
            "content": "他也谈了很多,",
            "speaker": 2
        },
        {
            "start": 3352.0,
            "end": 3357.0,
            "content": "如果如何在RL阶段更好的把机座能力释放出来,",
            "speaker": 2
        },
        {
            "start": 3357.0,
            "end": 3359.0,
            "content": "这样的一些个方法,",
            "speaker": 2
        },
        {
            "start": 3359.0,
            "end": 3361.0,
            "content": "就是虽然说他的机座能力,",
            "speaker": 2
        },
        {
            "start": 3361.0,
            "end": 3364.0,
            "content": "跟那么一个机座能力变化不大,",
            "speaker": 2
        },
        {
            "start": 3364.0,
            "end": 3366.0,
            "content": "但是你怎么把它完整的释放出来,",
            "speaker": 2
        },
        {
            "start": 3366.0,
            "end": 3369.0,
            "content": "这个也是有很长的路要走的,",
            "speaker": 2
        },
        {
            "start": 3369.0,
            "end": 3374.0,
            "content": "那那么就我觉得核心是在如何去释放那么去,",
            "speaker": 2
        },
        {
            "start": 3374.0,
            "end": 3376.0,
            "content": "这个机座模型本身的能力,",
            "speaker": 2
        },
        {
            "start": 3376.0,
            "end": 3378.0,
            "content": "这个是他在做RL的,",
            "speaker": 2
        },
        {
            "start": 3378.0,
            "end": 3379.0,
            "content": "就是,",
            "speaker": 2
        },
        {
            "start": 3379.0,
            "end": 3380.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3380.0,
            "end": 3381.0,
            "content": "就是helpfulness,",
            "speaker": 2
        },
        {
            "start": 3381.0,
            "end": 3385.0,
            "content": "有有有有用心的RL里面的一个重点的内容,",
            "speaker": 2
        },
        {
            "start": 3385.0,
            "end": 3386.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3386.0,
            "end": 3387.0,
            "content": "那我想说,",
            "speaker": 1
        },
        {
            "start": 3387.0,
            "end": 3388.0,
            "content": "呃,",
            "speaker": 1
        },
        {
            "start": 3388.0,
            "end": 3389.0,
            "content": "在那在这个工业界,",
            "speaker": 1
        },
        {
            "start": 3389.0,
            "end": 3390.0,
            "content": "大家肯定最关注的就是,",
            "speaker": 1
        },
        {
            "start": 3390.0,
            "end": 3391.0,
            "content": "啊,",
            "speaker": 1
        },
        {
            "start": 3391.0,
            "end": 3392.0,
            "content": "他能够商用了,",
            "speaker": 1
        },
        {
            "start": 3392.0,
            "end": 3393.0,
            "content": "那在学术,",
            "speaker": 1
        },
        {
            "start": 3393.0,
            "end": 3395.0,
            "content": "从一个学术研究的这个角度的话,",
            "speaker": 1
        },
        {
            "start": 3395.0,
            "end": 3396.0,
            "content": "你看到这位拉玛兔了以后,",
            "speaker": 1
        },
        {
            "start": 3396.0,
            "end": 3398.0,
            "content": "你觉得他对于接下来很多学,",
            "speaker": 1
        },
        {
            "start": 3398.0,
            "end": 3400.0,
            "content": "这个学界来说有什么,",
            "speaker": 1
        },
        {
            "start": 3400.0,
            "end": 3401.0,
            "content": "啊,",
            "speaker": 1
        },
        {
            "start": 3401.0,
            "end": 3402.0,
            "content": "会有怎样的这个帮助,",
            "speaker": 1
        },
        {
            "start": 3402.0,
            "end": 3404.0,
            "content": "那可做的事情可实在是太多了,",
            "speaker": 2
        },
        {
            "start": 3404.0,
            "end": 3405.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3405.0,
            "end": 3406.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3406.0,
            "end": 3407.0,
            "content": "首先的话,",
            "speaker": 2
        },
        {
            "start": 3407.0,
            "end": 3408.0,
            "content": "哦,",
            "speaker": 2
        },
        {
            "start": 3408.0,
            "end": 3412.0,
            "content": "我们比较就是首先那么就我们其实我个人好,",
            "speaker": 2
        },
        {
            "start": 3412.0,
            "end": 3415.0,
            "content": "其实对经过了RLHF之后的,",
            "speaker": 2
        },
        {
            "start": 3415.0,
            "end": 3417.0,
            "content": "那么就这个模型兴趣要低于,",
            "speaker": 2
        },
        {
            "start": 3417.0,
            "end": 3419.0,
            "content": "就是那么就的这个原始的模型,",
            "speaker": 2
        },
        {
            "start": 3419.0,
            "end": 3420.0,
            "content": "这个就跟,",
            "speaker": 2
        },
        {
            "start": 3420.0,
            "end": 3421.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3421.0,
            "end": 3422.0,
            "content": "就是,",
            "speaker": 2
        },
        {
            "start": 3422.0,
            "end": 3424.0,
            "content": "因为因为这就买东西一样,",
            "speaker": 2
        },
        {
            "start": 3424.0,
            "end": 3426.0,
            "content": "你到底是选一个机装修的还是你自己装,",
            "speaker": 2
        },
        {
            "start": 3426.0,
            "end": 3427.0,
            "content": "啊,",
            "speaker": 2
        },
        {
            "start": 3427.0,
            "end": 3428.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3428.0,
            "end": 3429.0,
            "content": "那你是希望你自己装啊,",
            "speaker": 2
        },
        {
            "start": 3429.0,
            "end": 3430.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3430.0,
            "end": 3431.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3431.0,
            "end": 3434.0,
            "content": "所以我们对于基础基础模型也很很感兴趣,",
            "speaker": 2
        },
        {
            "start": 3434.0,
            "end": 3438.0,
            "content": "然后我们认为70币的这个基础模型还是有非常强的潜力的,",
            "speaker": 2
        },
        {
            "start": 3438.0,
            "end": 3439.0,
            "content": "然后呢,",
            "speaker": 2
        },
        {
            "start": 3439.0,
            "end": 3440.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3440.0,
            "end": 3444.0,
            "content": "我现在比较关注的是把这个70币的模型的能力朝着我想要的,",
            "speaker": 2
        },
        {
            "start": 3444.0,
            "end": 3445.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3445.0,
            "end": 3446.0,
            "content": "方向去发展,",
            "speaker": 2
        },
        {
            "start": 3446.0,
            "end": 3449.0,
            "content": "并且70币的现在的这个模型它可能代码稍微少一点,",
            "speaker": 2
        },
        {
            "start": 3449.0,
            "end": 3451.0,
            "content": "然后多语言稍微少一点,",
            "speaker": 2
        },
        {
            "start": 3451.0,
            "end": 3452.0,
            "content": "然后,",
            "speaker": 2
        },
        {
            "start": 3452.0,
            "end": 3453.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3453.0,
            "end": 3454.0,
            "content": "论文读的少了一点,",
            "speaker": 2
        },
        {
            "start": 3454.0,
            "end": 3455.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3455.0,
            "end": 3456.0,
            "content": "然后这方面的话,",
            "speaker": 2
        },
        {
            "start": 3456.0,
            "end": 3459.0,
            "content": "我们最近正在想什么样的方法把它这方面的能力给补上来,",
            "speaker": 2
        },
        {
            "start": 3459.0,
            "end": 3460.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3460.0,
            "end": 3463.0,
            "content": "然后这个是能力补全这样的一个事情,",
            "speaker": 2
        },
        {
            "start": 3463.0,
            "end": 3467.0,
            "content": "另外一个事情是怎么把这个那么的基础模型增加,",
            "speaker": 2
        },
        {
            "start": 3467.0,
            "end": 3468.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3468.0,
            "end": 3471.0,
            "content": "就是研究模型内部的工作的经理,",
            "speaker": 2
        },
        {
            "start": 3471.0,
            "end": 3474.0,
            "content": "因为也可以拿到模型的权重和模型的代码,",
            "speaker": 2
        },
        {
            "start": 3474.0,
            "end": 3475.0,
            "content": "这样子的话,",
            "speaker": 2
        },
        {
            "start": 3475.0,
            "end": 3476.0,
            "content": "就比如说模型,",
            "speaker": 2
        },
        {
            "start": 3476.0,
            "end": 3477.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3477.0,
            "end": 3481.0,
            "content": "有一个比较有意思的应用是精准的修改模型错误的信念,",
            "speaker": 2
        },
        {
            "start": 3481.0,
            "end": 3482.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3482.0,
            "end": 3483.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3483.0,
            "end": 3484.0,
            "content": "就如果模型,",
            "speaker": 2
        },
        {
            "start": 3484.0,
            "end": 3485.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3485.0,
            "end": 3486.0,
            "content": "就是如果在2024年,",
            "speaker": 2
        },
        {
            "start": 3486.0,
            "end": 3487.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3487.0,
            "end": 3488.0,
            "content": "美国重新大选,",
            "speaker": 2
        },
        {
            "start": 3488.0,
            "end": 3489.0,
            "content": "然后总统换人呢,",
            "speaker": 2
        },
        {
            "start": 3489.0,
            "end": 3491.0,
            "content": "但是模型的支持卡特的2023年,",
            "speaker": 2
        },
        {
            "start": 3491.0,
            "end": 3492.0,
            "content": "这个样子的话,",
            "speaker": 2
        },
        {
            "start": 3492.0,
            "end": 3493.0,
            "content": "他会认为,",
            "speaker": 2
        },
        {
            "start": 3493.0,
            "end": 3494.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3494.0,
            "end": 3496.0,
            "content": "2024年之后的总统是拜登,",
            "speaker": 2
        },
        {
            "start": 3496.0,
            "end": 3497.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3497.0,
            "end": 3498.0,
            "content": "或者说你问他,",
            "speaker": 2
        },
        {
            "start": 3498.0,
            "end": 3499.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3499.0,
            "end": 3500.0,
            "content": "现在的总统是谁,",
            "speaker": 2
        },
        {
            "start": 3500.0,
            "end": 3502.0,
            "content": "然后他可能会觉得现在总统是拜登,",
            "speaker": 2
        },
        {
            "start": 3502.0,
            "end": 3505.0,
            "content": "那你可能需要想要去精准的修改,",
            "speaker": 2
        },
        {
            "start": 3505.0,
            "end": 3506.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3506.0,
            "end": 3508.0,
            "content": "就是现在的总统这一项知识,",
            "speaker": 2
        },
        {
            "start": 3508.0,
            "end": 3509.0,
            "content": "但你不只是,",
            "speaker": 2
        },
        {
            "start": 3509.0,
            "end": 3511.0,
            "content": "但但你希望做到的事情是这个,",
            "speaker": 2
        },
        {
            "start": 3511.0,
            "end": 3513.0,
            "content": "当你修改这项之后,",
            "speaker": 2
        },
        {
            "start": 3513.0,
            "end": 3516.0,
            "content": "只要是跟总统有关的问题和总统有关的这个,",
            "speaker": 2
        },
        {
            "start": 3516.0,
            "end": 3517.0,
            "content": "他本来是一个网络结构呢,",
            "speaker": 2
        },
        {
            "start": 3517.0,
            "end": 3520.0,
            "content": "但你希望这个网络结构就可以同时发生变化,",
            "speaker": 2
        },
        {
            "start": 3520.0,
            "end": 3521.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3521.0,
            "end": 3522.0,
            "content": "怎么去修改这样子的模型,",
            "speaker": 2
        },
        {
            "start": 3522.0,
            "end": 3524.0,
            "content": "这件事一个非常有趣的应用,",
            "speaker": 2
        },
        {
            "start": 3524.0,
            "end": 3526.0,
            "content": "然后这这点,",
            "speaker": 2
        },
        {
            "start": 3526.0,
            "end": 3527.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3527.0,
            "end": 3530.0,
            "content": "我觉得可以有更多的研究和更多的突破,",
            "speaker": 2
        },
        {
            "start": 3530.0,
            "end": 3533.0,
            "content": "但是现在看起来的话有一些个研究,",
            "speaker": 2
        },
        {
            "start": 3533.0,
            "end": 3534.0,
            "content": "但这个方法,",
            "speaker": 2
        },
        {
            "start": 3534.0,
            "end": 3535.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3535.0,
            "end": 3536.0,
            "content": "并没有,",
            "speaker": 2
        },
        {
            "start": 3536.0,
            "end": 3537.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3537.0,
            "end": 3538.0,
            "content": "特别的完美,",
            "speaker": 2
        },
        {
            "start": 3538.0,
            "end": 3539.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3539.0,
            "end": 3541.0,
            "content": "但是那么就有经过了有签字的版本,",
            "speaker": 2
        },
        {
            "start": 3541.0,
            "end": 3543.0,
            "content": "就是签字的版本是经过恩爱之后的版本,",
            "speaker": 2
        },
        {
            "start": 3543.0,
            "end": 3546.0,
            "content": "他本身RHF会把一些个知识给覆盖掉,",
            "speaker": 2
        },
        {
            "start": 3546.0,
            "end": 3550.0,
            "content": "你觉得在跟这个ICML的这些个,",
            "speaker": 1
        },
        {
            "start": 3550.0,
            "end": 3551.0,
            "content": "呃,",
            "speaker": 1
        },
        {
            "start": 3551.0,
            "end": 3555.0,
            "content": "这个参会者交流过程中有哪一些你遇到有意思的一些,",
            "speaker": 1
        },
        {
            "start": 3555.0,
            "end": 3556.0,
            "content": "虽然说,",
            "speaker": 2
        },
        {
            "start": 3556.0,
            "end": 3557.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3557.0,
            "end": 3560.0,
            "content": "头部的大公司的选手们都会就是办各种各样的活动,",
            "speaker": 2
        },
        {
            "start": 3560.0,
            "end": 3561.0,
            "content": "但其实很多时候,",
            "speaker": 2
        },
        {
            "start": 3561.0,
            "end": 3562.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3562.0,
            "end": 3565.0,
            "content": "比较能够就是把人聚在一起的,",
            "speaker": 2
        },
        {
            "start": 3565.0,
            "end": 3570.0,
            "content": "或者说比如说你在任何一个活动上两个random的researcher,",
            "speaker": 2
        },
        {
            "start": 3570.0,
            "end": 3571.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3571.0,
            "end": 3574.0,
            "content": "然后就是不小心在吃饭的时候做了一桌,",
            "speaker": 2
        },
        {
            "start": 3574.0,
            "end": 3583.0,
            "content": "然后就是能够就是把人让两个人就是能够了解的还是一些个共同的兴趣和比较有意思的东西吧,",
            "speaker": 2
        },
        {
            "start": 3583.0,
            "end": 3584.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3584.0,
            "end": 3585.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3585.0,
            "end": 3586.0,
            "content": "我嗯,",
            "speaker": 2
        },
        {
            "start": 3586.0,
            "end": 3588.0,
            "content": "就是我前前天的话,",
            "speaker": 2
        },
        {
            "start": 3588.0,
            "end": 3589.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3589.0,
            "end": 3590.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3590.0,
            "end": 3593.0,
            "content": "跟一些个deep mind的researcher聊天,",
            "speaker": 2
        },
        {
            "start": 3593.0,
            "end": 3595.0,
            "content": "有一个topic非常的感兴趣,",
            "speaker": 2
        },
        {
            "start": 3595.0,
            "end": 3596.0,
            "content": "ok,",
            "speaker": 2
        },
        {
            "start": 3596.0,
            "end": 3598.0,
            "content": "叫做compression,",
            "speaker": 2
        },
        {
            "start": 3598.0,
            "end": 3599.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3599.0,
            "end": 3600.0,
            "content": "is all you need,",
            "speaker": 2
        },
        {
            "start": 3600.0,
            "end": 3601.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3601.0,
            "end": 3603.0,
            "content": "这个的就是这个的这个的提出是说,",
            "speaker": 2
        },
        {
            "start": 3603.0,
            "end": 3605.0,
            "content": "当你在训练神经网络的时候,",
            "speaker": 2
        },
        {
            "start": 3605.0,
            "end": 3607.0,
            "content": "你每次只是训练下一个词,",
            "speaker": 2
        },
        {
            "start": 3607.0,
            "end": 3609.0,
            "content": "然后你做的事情其实是无损压缩,",
            "speaker": 2
        },
        {
            "start": 3609.0,
            "end": 3612.0,
            "content": "就像相当于把你的信息全部压缩,",
            "speaker": 2
        },
        {
            "start": 3612.0,
            "end": 3613.0,
            "content": "在你的网络里面,",
            "speaker": 2
        },
        {
            "start": 3613.0,
            "end": 3615.0,
            "content": "然后这个的想法是,",
            "speaker": 2
        },
        {
            "start": 3615.0,
            "end": 3616.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3616.0,
            "end": 3617.0,
            "content": "jack ray,",
            "speaker": 2
        },
        {
            "start": 3617.0,
            "end": 3618.0,
            "content": "他是,",
            "speaker": 2
        },
        {
            "start": 3618.0,
            "end": 3619.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3619.0,
            "end": 3621.0,
            "content": "他本身是deep mind的研究员,",
            "speaker": 2
        },
        {
            "start": 3621.0,
            "end": 3622.0,
            "content": "后面跳槽去的openai,",
            "speaker": 2
        },
        {
            "start": 3622.0,
            "end": 3625.0,
            "content": "然后后面就是又又回到了deep mind,",
            "speaker": 2
        },
        {
            "start": 3625.0,
            "end": 3627.0,
            "content": "然后他在某次在,",
            "speaker": 2
        },
        {
            "start": 3627.0,
            "end": 3628.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3628.0,
            "end": 3632.0,
            "content": "就是斯坦福的一个课上讲的这样的一个想法,",
            "speaker": 2
        },
        {
            "start": 3632.0,
            "end": 3633.0,
            "content": "前天吃中饭的时候,",
            "speaker": 2
        },
        {
            "start": 3633.0,
            "end": 3634.0,
            "content": "我坐在旁边,",
            "speaker": 2
        },
        {
            "start": 3634.0,
            "end": 3635.0,
            "content": "我就问他,",
            "speaker": 2
        },
        {
            "start": 3635.0,
            "end": 3636.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3636.0,
            "end": 3637.0,
            "content": "就是关于,",
            "speaker": 2
        },
        {
            "start": 3637.0,
            "end": 3638.0,
            "content": "就是nosense compression,",
            "speaker": 2
        },
        {
            "start": 3638.0,
            "end": 3639.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3639.0,
            "end": 3641.0,
            "content": "相关的一些个想法,",
            "speaker": 2
        },
        {
            "start": 3641.0,
            "end": 3642.0,
            "content": "然后一些个结论,",
            "speaker": 2
        },
        {
            "start": 3642.0,
            "end": 3644.0,
            "content": "他跟scaling law相关的关系,",
            "speaker": 2
        },
        {
            "start": 3644.0,
            "end": 3646.0,
            "content": "以及nosense compression,",
            "speaker": 2
        },
        {
            "start": 3646.0,
            "end": 3647.0,
            "content": "为什么是,",
            "speaker": 2
        },
        {
            "start": 3647.0,
            "end": 3648.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3648.0,
            "end": 3649.0,
            "content": "为什么是无损的,",
            "speaker": 2
        },
        {
            "start": 3649.0,
            "end": 3650.0,
            "content": "而不是有损的,",
            "speaker": 2
        },
        {
            "start": 3650.0,
            "end": 3651.0,
            "content": "因为,",
            "speaker": 2
        },
        {
            "start": 3651.0,
            "end": 3652.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3652.0,
            "end": 3653.0,
            "content": "就是在他说这件事情之前,",
            "speaker": 2
        },
        {
            "start": 3653.0,
            "end": 3654.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3654.0,
            "end": 3656.0,
            "content": "大家觉得模型对于信息的压缩是有损压缩,",
            "speaker": 2
        },
        {
            "start": 3656.0,
            "end": 3658.0,
            "content": "那他说order是无损的压缩,",
            "speaker": 2
        },
        {
            "start": 3658.0,
            "end": 3659.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3659.0,
            "end": 3660.0,
            "content": "然后,",
            "speaker": 2
        },
        {
            "start": 3660.0,
            "end": 3661.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3661.0,
            "end": 3662.0,
            "content": "scaling,",
            "speaker": 2
        },
        {
            "start": 3662.0,
            "end": 3663.0,
            "content": "模型增大会对,",
            "speaker": 2
        },
        {
            "start": 3663.0,
            "end": 3664.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3664.0,
            "end": 3665.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3665.0,
            "end": 3667.0,
            "content": "对信息的压缩产生什么样的影响?",
            "speaker": 2
        },
        {
            "start": 3667.0,
            "end": 3668.0,
            "content": "然后,",
            "speaker": 2
        },
        {
            "start": 3669.0,
            "end": 3670.0,
            "content": "当时是怎样被发现的?",
            "speaker": 2
        },
        {
            "start": 3670.0,
            "end": 3671.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3671.0,
            "end": 3673.0,
            "content": "尤其下版本的scaling law现在指导,",
            "speaker": 2
        },
        {
            "start": 3673.0,
            "end": 3676.0,
            "content": "现在是大部分所有做大元模型的最,",
            "speaker": 2
        },
        {
            "start": 3676.0,
            "end": 3678.0,
            "content": "最重要指导方针,",
            "speaker": 2
        },
        {
            "start": 3678.0,
            "end": 3680.0,
            "content": "nama就是付贤的情形了,",
            "speaker": 2
        },
        {
            "start": 3680.0,
            "end": 3681.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3681.0,
            "end": 3682.0,
            "content": "然后他也谈了就是当时,",
            "speaker": 2
        },
        {
            "start": 3682.0,
            "end": 3683.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3683.0,
            "end": 3684.0,
            "content": "怎么去,",
            "speaker": 2
        },
        {
            "start": 3684.0,
            "end": 3685.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3685.0,
            "end": 3686.0,
            "content": "那当时就是,",
            "speaker": 2
        },
        {
            "start": 3686.0,
            "end": 3687.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3687.0,
            "end": 3689.0,
            "content": "找到情形的scaling law的一些个细节,",
            "speaker": 2
        },
        {
            "start": 3689.0,
            "end": 3692.0,
            "content": "因为情形的scaling law纠正了GP3.3的scaling law,",
            "speaker": 2
        },
        {
            "start": 3692.0,
            "end": 3693.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3693.0,
            "end": 3694.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3694.0,
            "end": 3695.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3695.0,
            "end": 3697.0,
            "content": "所以所以所以我觉得就是这些个讨论是非常非常的insightful的,",
            "speaker": 2
        },
        {
            "start": 3697.0,
            "end": 3698.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3698.0,
            "end": 3699.0,
            "content": "还有另外一位,",
            "speaker": 2
        },
        {
            "start": 3699.0,
            "end": 3700.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3700.0,
            "end": 3702.0,
            "content": "deep mind的researcher在讨论的是,",
            "speaker": 2
        },
        {
            "start": 3702.0,
            "end": 3703.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3703.0,
            "end": 3706.0,
            "content": "多智能体交互以及多个语言模型用强化学习的方法,",
            "speaker": 2
        },
        {
            "start": 3706.0,
            "end": 3707.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3707.0,
            "end": 3708.0,
            "content": "就多个agents,",
            "speaker": 2
        },
        {
            "start": 3708.0,
            "end": 3709.0,
            "content": "然后用强化学习,",
            "speaker": 2
        },
        {
            "start": 3709.0,
            "end": 3711.0,
            "content": "然后相互进步,",
            "speaker": 2
        },
        {
            "start": 3711.0,
            "end": 3712.0,
            "content": "这样的一些个,",
            "speaker": 2
        },
        {
            "start": 3712.0,
            "end": 3713.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3713.0,
            "end": 3715.0,
            "content": "想法和一些个就是呃,",
            "speaker": 2
        },
        {
            "start": 3715.0,
            "end": 3716.0,
            "content": "可以探索的内容,",
            "speaker": 2
        },
        {
            "start": 3716.0,
            "end": 3718.0,
            "content": "我觉得这些都非常的insightful,",
            "speaker": 2
        },
        {
            "start": 3718.0,
            "end": 3722.0,
            "content": "真的有很多的创新是这个发生在这个业界,",
            "speaker": 1
        },
        {
            "start": 3722.0,
            "end": 3724.0,
            "content": "所以像业界跟学界的这个结合,",
            "speaker": 1
        },
        {
            "start": 3724.0,
            "end": 3726.0,
            "content": "我觉得越来越越来越紧密,",
            "speaker": 1
        },
        {
            "start": 3726.0,
            "end": 3727.0,
            "content": "呃,",
            "speaker": 1
        },
        {
            "start": 3727.0,
            "end": 3730.0,
            "content": "每个researcher在完成了一个自己的这个研究之后,",
            "speaker": 1
        },
        {
            "start": 3730.0,
            "end": 3732.0,
            "content": "都会在寻找新的研究方向,",
            "speaker": 1
        },
        {
            "start": 3732.0,
            "end": 3734.0,
            "content": "在这个变化如此之快的AI这个领域,",
            "speaker": 1
        },
        {
            "start": 3734.0,
            "end": 3738.0,
            "content": "你自己会最关注哪几个方向会去深挖吗?",
            "speaker": 1
        },
        {
            "start": 3738.0,
            "end": 3740.0,
            "content": "我会倾向于把我的,",
            "speaker": 2
        },
        {
            "start": 3740.0,
            "end": 3741.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3741.0,
            "end": 3744.0,
            "content": "研究分成就是现在已经有比较好的解法,",
            "speaker": 2
        },
        {
            "start": 3744.0,
            "end": 3748.0,
            "content": "但是需要更加精细化和现在完全没有解法,",
            "speaker": 2
        },
        {
            "start": 3748.0,
            "end": 3749.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3749.0,
            "end": 3751.0,
            "content": "需要去探索这两个部分,",
            "speaker": 2
        },
        {
            "start": 3751.0,
            "end": 3754.0,
            "content": "那在在在这个已有解法,",
            "speaker": 2
        },
        {
            "start": 3754.0,
            "end": 3756.0,
            "content": "然后需要精细化这一类,",
            "speaker": 2
        },
        {
            "start": 3756.0,
            "end": 3759.0,
            "content": "我更加关注数据的组成,",
            "speaker": 2
        },
        {
            "start": 3759.0,
            "end": 3762.0,
            "content": "包括预训链数据组成和,",
            "speaker": 2
        },
        {
            "start": 3762.0,
            "end": 3763.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3763.0,
            "end": 3764.0,
            "content": "就是呃,",
            "speaker": 2
        },
        {
            "start": 3764.0,
            "end": 3766.0,
            "content": "微调反清理数据的组成,",
            "speaker": 2
        },
        {
            "start": 3766.0,
            "end": 3768.0,
            "content": "然后COT数据的组成,",
            "speaker": 2
        },
        {
            "start": 3768.0,
            "end": 3775.0,
            "content": "然后不同的数据组成对于模型能力平衡所带来的影响的一些个精细化调整,",
            "speaker": 2
        },
        {
            "start": 3775.0,
            "end": 3776.0,
            "content": "对,",
            "speaker": 2
        },
        {
            "start": 3776.0,
            "end": 3779.0,
            "content": "然后在这个的目标是希望找到,",
            "speaker": 2
        },
        {
            "start": 3780.0,
            "end": 3782.0,
            "content": "什么是最好的数据,",
            "speaker": 2
        },
        {
            "start": 3782.0,
            "end": 3783.0,
            "content": "使得,",
            "speaker": 2
        },
        {
            "start": 3783.0,
            "end": 3784.0,
            "content": "呃,",
            "speaker": 2
        },
        {
            "start": 3784.0,
            "end": 3787.0,
            "content": "你希望把那些不好的数据变成好的数据,",
            "speaker": 2
        },
        {
            "start": 3787.0,
            "end": 3793.0,
            "content": "然后好的数据比跟不好的数据的作用的区别是你好的数据和不好的数据,",
            "speaker": 2
        },
        {
            "start": 3793.0,
            "end": 3795.0,
            "content": "在你给模型塞数据的时候,",
            "speaker": 2
        },
        {
            "start": 3795.0,
            "end": 3797.0,
            "content": "模型都会得到提升,",
            "speaker": 2
        },
        {
            "start": 3797.0,
            "end": 3800.0,
            "content": "但是好的数据可以让模型提升的更快,",
            "speaker": 2
        },
        {
            "start": 3800.0,
            "end": 3801.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3801.0,
            "end": 3802.0,
            "content": "随着你数据的增多,",
            "speaker": 2
        },
        {
            "start": 3802.0,
            "end": 3809.0,
            "content": "好的数据使得模型能力增长的协力会比坏的数据使得模型能力增长学历更加的高一点,",
            "speaker": 2
        },
        {
            "start": 3809.0,
            "end": 3812.0,
            "content": "那如何去定位什么样的数据算是好数据,",
            "speaker": 2
        },
        {
            "start": 3812.0,
            "end": 3814.0,
            "content": "然后坏的数据也不是全部都坏,",
            "speaker": 2
        },
        {
            "start": 3814.0,
            "end": 3816.0,
            "content": "很多时候他们只是格式不对而已,",
            "speaker": 2
        },
        {
            "start": 3816.0,
            "end": 3819.0,
            "content": "那你怎么把那些个坏的数据变成好的数据,",
            "speaker": 2
        },
        {
            "start": 3819.0,
            "end": 3820.0,
            "content": "让模型能学,",
            "speaker": 2
        },
        {
            "start": 3820.0,
            "end": 3822.0,
            "content": "这个是我呃,",
            "speaker": 2
        },
        {
            "start": 3822.0,
            "end": 3824.0,
            "content": "比较关注的一个方面,",
            "speaker": 2
        },
        {
            "start": 3824.0,
            "end": 3826.0,
            "content": "然后就做数据这件事情,",
            "speaker": 2
        },
        {
            "start": 3826.0,
            "end": 3827.0,
            "content": "其实呃,",
            "speaker": 2
        },
        {
            "start": 3827.0,
            "end": 3829.0,
            "content": "很多地方都已经有比较成熟的方案了,",
            "speaker": 2
        },
        {
            "start": 3829.0,
            "end": 3831.0,
            "content": "所以它其实是在一个呃,",
            "speaker": 2
        },
        {
            "start": 3831.0,
            "end": 3832.0,
            "content": "已有的方案之上,",
            "speaker": 2
        },
        {
            "start": 3832.0,
            "end": 3834.0,
            "content": "怎么去把它做的更加的精细化,",
            "speaker": 2
        },
        {
            "start": 3834.0,
            "end": 3836.0,
            "content": "这样的一类研究的方向,",
            "speaker": 2
        },
        {
            "start": 3836.0,
            "end": 3839.0,
            "content": "那另外一个一类研究就是没有一个已有的方案,",
            "speaker": 2
        },
        {
            "start": 3839.0,
            "end": 3843.0,
            "content": "希望把它就是像把探索出来一个方案,",
            "speaker": 2
        },
        {
            "start": 3843.0,
            "end": 3844.0,
            "content": "这也是我在关注的,",
            "speaker": 2
        },
        {
            "start": 3844.0,
            "end": 3847.0,
            "content": "那我这边比较关注的就是呃,",
            "speaker": 2
        },
        {
            "start": 3847.0,
            "end": 3849.0,
            "content": "AI agents相关的方向,",
            "speaker": 2
        },
        {
            "start": 3849.0,
            "end": 3855.0,
            "content": "然后我特别关注的是把AI agents本身的数量和丰富程度增多,",
            "speaker": 2
        },
        {
            "start": 3855.0,
            "end": 3860.0,
            "content": "所以现在我们能够控制的AI agents可能就是在四五个这样的一个量级,",
            "speaker": 2
        },
        {
            "start": 3860.0,
            "end": 3864.0,
            "content": "那我就是前两天就昨天晚上跟呃,",
            "speaker": 2
        },
        {
            "start": 3864.0,
            "end": 3865.0,
            "content": "嗯,",
            "speaker": 2
        },
        {
            "start": 3865.0,
            "end": 3866.0,
            "content": "Samuel的同学聊天的时候,",
            "speaker": 2
        },
        {
            "start": 3866.0,
            "end": 3870.0,
            "content": "我们希望去关注你如何同时操纵超过1000个agent,",
            "speaker": 2
        },
        {
            "start": 3870.0,
            "end": 3871.0,
            "content": "哇,",
            "speaker": 2
        },
        {
            "start": 3871.0,
            "end": 3872.0,
            "content": "让他们呃,",
            "speaker": 2
        },
        {
            "start": 3872.0,
            "end": 3874.0,
            "content": "可以一起呃,",
            "speaker": 2
        },
        {
            "start": 3874.0,
            "end": 3876.0,
            "content": "协同呃,",
            "speaker": 2
        },
        {
            "start": 3876.0,
            "end": 3879.0,
            "content": "完成你给他们指定的任务,",
            "speaker": 2
        },
        {
            "start": 3879.0,
            "end": 3883.0,
            "content": "然后1000个AI agents怎么相互给feedback,",
            "speaker": 2
        },
        {
            "start": 3883.0,
            "end": 3886.0,
            "content": "就怎么做AI feedback at scale,",
            "speaker": 2
        },
        {
            "start": 3886.0,
            "end": 3892.0,
            "content": "然后这个scale的意思是说你的agent的数量和丰富程度变得非常的多,",
            "speaker": 2
        },
        {
            "start": 3892.0,
            "end": 3894.0,
            "content": "然后有些agent是actor,",
            "speaker": 2
        },
        {
            "start": 3894.0,
            "end": 3896.0,
            "content": "有些agent是critic,",
            "speaker": 2
        },
        {
            "start": 3896.0,
            "end": 3900.0,
            "content": "然后这个critic为这些个actor提供AI feedback,",
            "speaker": 2
        },
        {
            "start": 3900.0,
            "end": 3902.0,
            "content": "怎么在这个量级的呃,",
            "speaker": 2
        },
        {
            "start": 3902.0,
            "end": 3906.0,
            "content": "agents的时候使得他们的呃,",
            "speaker": 2
        },
        {
            "start": 3906.0,
            "end": 3908.0,
            "content": "feedback都是有效的,",
            "speaker": 2
        },
        {
            "start": 3908.0,
            "end": 3912.0,
            "content": "然后然后可以就是这一把把AI做成一个群体吧,",
            "speaker": 2
        },
        {
            "start": 3912.0,
            "end": 3914.0,
            "content": "AI agents它不是一个个体,",
            "speaker": 2
        },
        {
            "start": 3914.0,
            "end": 3916.0,
            "content": "它是一种种群,",
            "speaker": 2
        },
        {
            "start": 3916.0,
            "end": 3917.0,
            "content": "然后呃,",
            "speaker": 2
        },
        {
            "start": 3917.0,
            "end": 3919.0,
            "content": "人类作为一种种群,",
            "speaker": 2
        },
        {
            "start": 3919.0,
            "end": 3923.0,
            "content": "它的演化的过程是以生存为目标,",
            "speaker": 2
        },
        {
            "start": 3923.0,
            "end": 3926.0,
            "content": "自然选择AI作为一个呃,",
            "speaker": 2
        },
        {
            "start": 3926.0,
            "end": 3929.0,
            "content": "种群它的演化是以人类指定的目标为目标,",
            "speaker": 2
        },
        {
            "start": 3929.0,
            "end": 3933.0,
            "content": "然后让人类选择就怎么把自然选择改成人类选择,",
            "speaker": 2
        },
        {
            "start": 3933.0,
            "end": 3938.0,
            "content": "怎么把生存这个目标改成人类指定的另一任意目标,",
            "speaker": 2
        },
        {
            "start": 3938.0,
            "end": 3940.0,
            "content": "然后在总群的呃,",
            "speaker": 2
        },
        {
            "start": 3940.0,
            "end": 3942.0,
            "content": "范围内研究AI agents,",
            "speaker": 2
        },
        {
            "start": 3942.0,
            "end": 3944.0,
            "content": "这个是我比较呃,",
            "speaker": 2
        },
        {
            "start": 3944.0,
            "end": 3946.0,
            "content": "关注的下个话题,",
            "speaker": 2
        },
        {
            "start": 3946.0,
            "end": 3949.0,
            "content": "其实我昨天跟下面的朋友正在聊这个,",
            "speaker": 2
        },
        {
            "start": 3949.0,
            "end": 3951.0,
            "content": "我们觉得需要把九月份的时间全部空出来,",
            "speaker": 2
        },
        {
            "start": 3951.0,
            "end": 3952.0,
            "content": "专门搞这个,",
            "speaker": 2
        },
        {
            "start": 3952.0,
            "end": 3953.0,
            "content": "哇,",
            "speaker": 2
        },
        {
            "start": 3953.0,
            "end": 3955.0,
            "content": "这个听起来这个非常有意思的研究,",
            "speaker": 1
        },
        {
            "start": 3955.0,
            "end": 3960.0,
            "content": "就是说不定还会跟一些社会学的东西会有一定的这个结合,",
            "speaker": 1
        },
        {
            "start": 3960.0,
            "end": 3962.0,
            "content": "而且我们一直都想说AI,",
            "speaker": 1
        },
        {
            "start": 3962.0,
            "end": 3963.0,
            "content": "AI这工具,",
            "speaker": 1
        },
        {
            "start": 3963.0,
            "end": 3965.0,
            "content": "尤其有AI agents,",
            "speaker": 1
        },
        {
            "start": 3965.0,
            "end": 3968.0,
            "content": "我觉得真的是让这个一个人变成了一支队伍,",
            "speaker": 1
        },
        {
            "start": 3968.0,
            "end": 3971.0,
            "content": "我觉得甚至再往前更进一步去想的话,",
            "speaker": 1
        },
        {
            "start": 3971.0,
            "end": 3975.0,
            "content": "以后我们再去思考一个组织的形态的时候,",
            "speaker": 1
        },
        {
            "start": 3975.0,
            "end": 3977.0,
            "content": "可能都要发生很大的这个变化,",
            "speaker": 1
        },
        {
            "start": 3977.0,
            "end": 3979.0,
            "content": "比如我思考一个组织,",
            "speaker": 1
        },
        {
            "start": 3979.0,
            "end": 3981.0,
            "content": "现在想我要配备什么样的团队,",
            "speaker": 1
        },
        {
            "start": 3981.0,
            "end": 3982.0,
            "content": "什么样的人,",
            "speaker": 1
        },
        {
            "start": 3982.0,
            "end": 3983.0,
            "content": "可能现在变成了说,",
            "speaker": 1
        },
        {
            "start": 3983.0,
            "end": 3985.0,
            "content": "我先去设置好我的一个的agent,",
            "speaker": 1
        },
        {
            "start": 3985.0,
            "end": 3987.0,
            "content": "然后再去看这里面哪些要人再去补齐的,",
            "speaker": 1
        },
        {
            "start": 3987.0,
            "end": 3988.0,
            "content": "你的公司里面,",
            "speaker": 1
        },
        {
            "start": 3988.0,
            "end": 3991.0,
            "content": "假设你有所谓的这个agent作为你的员工,",
            "speaker": 1
        },
        {
            "start": 3991.0,
            "end": 3993.0,
            "content": "那如果你80%的工作都是有这些组织,",
            "speaker": 1
        },
        {
            "start": 3993.0,
            "end": 3997.0,
            "content": "我相信他们到时候会需要一个完全不一样的一个整个工具链,",
            "speaker": 1
        },
        {
            "start": 3997.0,
            "end": 4001.0,
            "content": "我觉得这个会是一个非常有深远影响的一个研究方向,",
            "speaker": 1
        },
        {
            "start": 4001.0,
            "end": 4004.0,
            "content": "当你有一个一支AI agents的一个团队的时候,",
            "speaker": 2
        },
        {
            "start": 4004.0,
            "end": 4006.0,
            "content": "你如何就是把已有的,",
            "speaker": 2
        },
        {
            "start": 4006.0,
            "end": 4011.0,
            "content": "就现在做那个团队组织架构有各种各样的社会学的实验,",
            "speaker": 2
        },
        {
            "start": 4011.0,
            "end": 4012.0,
            "content": "上课的实验,",
            "speaker": 2
        },
        {
            "start": 4012.0,
            "end": 4014.0,
            "content": "然后各种各样的结论,",
            "speaker": 2
        },
        {
            "start": 4014.0,
            "end": 4016.0,
            "content": "怎么把这种东西挪到AI的团队里面,",
            "speaker": 2
        },
        {
            "start": 4016.0,
            "end": 4018.0,
            "content": "我觉得这是一个非常化化学科,",
            "speaker": 2
        },
        {
            "start": 4018.0,
            "end": 4019.0,
            "content": "而且你想对,",
            "speaker": 2
        },
        {
            "start": 4019.0,
            "end": 4022.0,
            "content": "而且你想组织它自己也是在不断的进化的,",
            "speaker": 1
        },
        {
            "start": 4022.0,
            "end": 4025.0,
            "content": "十年前的这个Facebook的这个组织形式,",
            "speaker": 1
        },
        {
            "start": 4025.0,
            "end": 4027.0,
            "content": "跟他现在的文化各方都不一样,",
            "speaker": 1
        },
        {
            "start": 4027.0,
            "end": 4028.0,
            "content": "而且是,",
            "speaker": 1
        },
        {
            "start": 4028.0,
            "end": 4029.0,
            "content": "但他也可能未必是最好的,",
            "speaker": 1
        },
        {
            "start": 4029.0,
            "end": 4030.0,
            "content": "对吧,",
            "speaker": 1
        },
        {
            "start": 4030.0,
            "end": 4031.0,
            "content": "前经历了那么大的一个财源,",
            "speaker": 1
        },
        {
            "start": 4031.0,
            "end": 4033.0,
            "content": "说明他自己本身其实,",
            "speaker": 1
        },
        {
            "start": 4033.0,
            "end": 4035.0,
            "content": "那如果有更大的,",
            "speaker": 1
        },
        {
            "start": 4035.0,
            "end": 4036.0,
            "content": "更多是agent的话,",
            "speaker": 1
        },
        {
            "start": 4036.0,
            "end": 4038.0,
            "content": "就是组织会不会变得更加的,",
            "speaker": 1
        },
        {
            "start": 4038.0,
            "end": 4039.0,
            "content": "更加的智能,",
            "speaker": 1
        },
        {
            "start": 4039.0,
            "end": 4042.0,
            "content": "我们会更少的犯这些人类犯的这个组织管理上的一些,",
            "speaker": 1
        },
        {
            "start": 4042.0,
            "end": 4043.0,
            "content": "一些错误,",
            "speaker": 1
        },
        {
            "start": 4043.0,
            "end": 4046.0,
            "content": "我觉得这个都是非常非常有意思的一些方向,",
            "speaker": 1
        },
        {
            "start": 4046.0,
            "end": 4051.0,
            "content": "很多时候群体演化的方向是并没有一个特别好的预设的方向,",
            "speaker": 2
        },
        {
            "start": 4051.0,
            "end": 4053.0,
            "content": "只是在每一步的时候去找局部队友,",
            "speaker": 2
        },
        {
            "start": 4053.0,
            "end": 4055.0,
            "content": "群体无意识的现象,",
            "speaker": 2
        },
        {
            "start": 4055.0,
            "end": 4057.0,
            "content": "其实还是非常的严重的,",
            "speaker": 2
        },
        {
            "start": 4057.0,
            "end": 4059.0,
            "content": "很多时候一个比较大的群体做一个,",
            "speaker": 2
        },
        {
            "start": 4059.0,
            "end": 4062.0,
            "content": "一个比较重要的决策的时候,",
            "speaker": 2
        },
        {
            "start": 4062.0,
            "end": 4066.0,
            "content": "能不能为well informed randomness这方面,",
            "speaker": 2
        },
        {
            "start": 4066.0,
            "end": 4070.0,
            "content": "就是随机性在这方面play the role非常非常的多,",
            "speaker": 2
        },
        {
            "start": 4070.0,
            "end": 4071.0,
            "content": "所以,",
            "speaker": 2
        },
        {
            "start": 4071.0,
            "end": 4076.0,
            "content": "但是如果你可以在AI这样的一个群体性的agent scale上面,",
            "speaker": 2
        },
        {
            "start": 4076.0,
            "end": 4078.0,
            "content": "做这方面的研究的话,",
            "speaker": 2
        },
        {
            "start": 4078.0,
            "end": 4082.0,
            "content": "所以就可以对于那人类的这些个群体性的比较重要的研究的决策,",
            "speaker": 2
        },
        {
            "start": 4082.0,
            "end": 4085.0,
            "content": "应该也会有比较重要和深远的影响。",
            "speaker": 2
        },
        {
            "start": 4085.0,
            "end": 4088.0,
            "content": "很高兴傅瑶在这个百忙之中跟我们聊了这么长的时间,",
            "speaker": 1
        },
        {
            "start": 4088.0,
            "end": 4090.0,
            "content": "我觉得有非常非常多的这个insight,",
            "speaker": 1
        },
        {
            "start": 4090.0,
            "end": 4093.0,
            "content": "也让大家能够从一个侧面感受到了,",
            "speaker": 1
        },
        {
            "start": 4093.0,
            "end": 4097.0,
            "content": "在这个ICML这个人才和这个智慧的浓度,",
            "speaker": 1
        },
        {
            "start": 4097.0,
            "end": 4099.0,
            "content": "好,那谢谢傅瑶今天的时间,",
            "speaker": 1
        },
        {
            "start": 4099.0,
            "end": 4100.0,
            "content": "非常感谢。",
            "speaker": 1
        },
        {
            "start": 4100.0,
            "end": 4101.0,
            "content": "谢谢。",
            "speaker": 1
        },
        {
            "start": 4101.0,
            "end": 4104.0,
            "content": "以上就是这次跟傅瑶的全部访谈,",
            "speaker": 0
        },
        {
            "start": 4104.0,
            "end": 4106.0,
            "content": "不知你是否也像莫妮卡一样,",
            "speaker": 0
        },
        {
            "start": 4106.0,
            "end": 4108.0,
            "content": "觉得意犹未尽,",
            "speaker": 0
        },
        {
            "start": 4108.0,
            "end": 4109.0,
            "content": "未来的一个多月,",
            "speaker": 0
        },
        {
            "start": 4109.0,
            "end": 4111.0,
            "content": "莫妮卡还会在硅谷这边,",
            "speaker": 0
        },
        {
            "start": 4111.0,
            "end": 4114.0,
            "content": "与更多大模型最前沿的研究者,",
            "speaker": 0
        },
        {
            "start": 4114.0,
            "end": 4115.0,
            "content": "创业者,",
            "speaker": 0
        },
        {
            "start": 4115.0,
            "end": 4116.0,
            "content": "从业者交流,",
            "speaker": 0
        },
        {
            "start": 4116.0,
            "end": 4118.0,
            "content": "还有更多精彩的访谈,",
            "speaker": 0
        },
        {
            "start": 4118.0,
            "end": 4119.0,
            "content": "敬请期待,",
            "speaker": 0
        },
        {
            "start": 4119.0,
            "end": 4121.0,
            "content": "赶紧关注onboard。",
            "speaker": 0
        },
        {
            "start": 4121.0,
            "end": 4123.0,
            "content": "感谢大家的收听,",
            "speaker": 0
        },
        {
            "start": 4123.0,
            "end": 4125.0,
            "content": "如果你喜欢我们podcast的内容,",
            "speaker": 0
        },
        {
            "start": 4125.0,
            "end": 4128.0,
            "content": "欢迎你点赞并分享给可能感兴趣的朋友,",
            "speaker": 0
        },
        {
            "start": 4128.0,
            "end": 4131.0,
            "content": "有任何建议反馈都可以在评论区留言,",
            "speaker": 0
        },
        {
            "start": 4131.0,
            "end": 4133.0,
            "content": "我们都会很认真地看的,",
            "speaker": 0
        },
        {
            "start": 4133.0,
            "end": 4135.0,
            "content": "如果你在用apple podcast收听,",
            "speaker": 0
        },
        {
            "start": 4135.0,
            "end": 4138.0,
            "content": "也希望你花几秒钟给我们打个五星好评,",
            "speaker": 0
        },
        {
            "start": 4138.0,
            "end": 4140.0,
            "content": "让更多人了解到我们,",
            "speaker": 0
        },
        {
            "start": 4140.0,
            "end": 4141.0,
            "content": "我们下次再见了。",
            "speaker": 0
        }
    ],
    "summary": [
        {
            "start": 0,
            "content": "介绍"
        },
        {
            "start": 72,
            "content": "介绍傅瑶的研究背景"
        },
        {
            "start": 154,
            "content": "傅瑶分享在ICML做oral presentation的论文内容 "
        },
        {
            "start": 252,
            "content": "ICML会议情况介绍"
        },
        {
            "start": 357,
            "content": "Meta发布的Lama2模型更新情况介绍"
        },
        {
            "start": 521,
            "content": "傅瑶谈到和OpenAI研究员讨论compression is all you need的见解"
        },
        {
            "start": 677,
            "content": "多智能体交互讨论见解"
        },
        {
            "start": 754,
            "content": "傅瑶关注的数据组成研究方向 "
        },
        {
            "start": 889,
            "content": "傅瑶关注把语言模型作为agent的研究方向"
        },
        {
            "start": 1078,
            "content": "语言模型组成AI团队的应用和社会学结合讨论"
        },
        {
            "start": 1272,
            "content": "结束语"
        }
    ],
    "views": [
        {
            "content": "根据文本内容,反常识或者有尖锐态度的新观点包括:",
            "mark": false
        },
        {
            "content": "AI agents 未来可能会以群体形式存在,一个群体可能由上千个AI agents组成。这与现在只能控制几个AI agents形成鲜明对比。",
            "mark": false
        },
        {
            "content": "未来组织可能会由AI agents组成,这会改变组织的管理方式和运作逻辑。这与传统的组织管理有很大不同。",
            "mark": false
        },
        {
            "content": "数据的质量对模型性能有重大影响,找到高质量的数据至关重要。这与简单追求数据量增加有区别。 ",
            "mark": false
        },
        {
            "content": "模型内部表示的压缩具有无损特性。这改变了过去认为的有损压缩观点。",
            "mark": false
        },
        {
            "content": "通过强化学习训练出的模型不一定优于原始预训练模型。这与直接认为二次训练模型更强的看法不同。",
            "mark": false
        },
        {
            "content": "prompt engineering在实现各种AI agents中至关重要。这突破了仅依靠模型本身能力的传统看法。",
            "mark": false
        },
        {
            "content": "针对错误知识的精确修改能力对未来AI非常重要。这与一般方法的粗放修改形成对比。",
            "mark": false
        },
        {
            "content": "学术界的资源约束会促进方法创新,这有时反而优于工业界的资源优势。这对学术界的角色给出新的理解。",
            "mark": false
        }
    ],
    "origin": "web",
    "ctime": 1692671769,
    "utime": 1692672501
}
```

</p>
</details>


## Related Efforts

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A youtube-dl fork with additional features and fixes.

- [faster-whisper](https://github.com/guillaumekln/faster-whisper) - Faster Whisper transcription with CTranslate2.

- [pyannote-audio](https://github.com/pyannote/pyannote-audio) - Neural building blocks for speaker diarization: speech activity detection, speaker change detection, overlapped speech detection, speaker embedding.


## Maintainers

[@shixiangcap](https://github.com/shixiangcap)


## Contributing

Feel free to dive in! [Open an issue](https://github.com/shixiangcap/pickpod/issues/new) or submit PRs.


## License

[MIT](LICENSE) © shixiangcap
