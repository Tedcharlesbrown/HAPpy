# HAPpy: HAP Video Encoding Tool
<img src="https://github.com/Tedcharlesbrown/HAPpy/blob/main/GUI/assets/icon.png?raw=true" alt="HAPpy Icon" width="200"/>


[![License](https://img.shields.io/badge/Uses-FFmpeg-%23007808?logo=FFmpeg)](http://ffmpeg.org)
[![FFmpeg](https://img.shields.io/badge/License-GNU3.0-%23A42E2B?logo=gnu)](https://www.gnu.org/licenses/gpl-3.0.html#license-text)

HAPpy is a video encoding tool that wraps FFmpeg into a graphical user interface, designed specifically for the HAP codec.

## Features
- Intuitive GUI: Easily select and encode multiple videos with a few clicks.
- HAP Codec Support: Encode videos to the HAP format, ensuring optimal performance and quality.
- Custom Encoding Options: Choose between different encoding modes and codecs.

## Getting Started
### Installation
1. Navigate to the [Releases](https://github.com/tedcharlesbrown/HAPpy/releases/latest) section of the HAPpy GitHub repository.
2. Download the latest .exe release.
3. Run the downloaded .exe file to launch the HAPpy application.

## Usage
1. Launch the HAPpy application.
2. Drag and drop or select the videos you want to encode.
3. Press encode!
- Optional
  - By default, encoding destination is same as source
    - Or, create HAP folder in each destination directory
  - Choose a destination
  - Append HAP to version name *preserves version tags*
  - Advanced Options
    - Choose between `HAP`, `HAP ALPHA`, and `HAP Q`
    - Sizing, `Stretch` and `Pad`
      - The HAP codec must be divisible by 4
      - If the input video is not divisible by 4, the input will be stretched up or padded with black
    - Create Proxys **NOT YET IMPLEMENTED**
      - Will create 4 proxys at `1/2`, `1/4`, `1/8`, and `1/16` resolutions


## Why HAPpy?
- HAPpy provides a straightforward way to encode videos to the HAP format without the need to download and install other alternatives.
- HAPpy contains a pre-compiled version of FFmpeg with HAP included - so no searching for the correct version and no setting PATH variables.

## Warning!
- Use at your own risk. While this is a wrapper of FFmpeg, it has its limitations that comes with that.
- All resolutions should be divisible by 4 in both width and height.
  - The HAP codec must be divisible by 4, if the input video is not divisible by 4 in either direction - this app will either stretch or pad the output video to conform to that standard. (Changeable in the advanced settings)

## Why not NotchLC or DXV?
NotchLC and DXV are a proprietary codecs and has no plans on being shared outside of Notch and their own Media Encoder plugin. This means that in cannot be used in open source programs such as this one or FFmpeg. If this is something you need, and as it becomes more difficult to encode to NotchLC or DXV due to Adobe / Apple's silicone, I would recommend contacting Notch or Resolume.

## License
This software uses code of [FFmpeg](http://ffmpeg.org) licensed under the [GPLv3.0](https://www.gnu.org/licenses/gpl-3.0.html#license-text) and its source can be downloaded below

- [Windows](https://github.com/GyanD/codexffmpeg/releases/tag/2023-10-18-git-e7a6bba51a) from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/).
 
    Copyright (C) 2023  Ted Charles Brown

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

<!-- You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>. -->

## Special Thanks / Acknowledgments
[FFmpeg](https://github.com/FFmpeg/FFmpeg) - FFmpeg is a trademark of Fabric Bellard  
[Vidvox](https://github.com/Vidvox/hap) - Created HAP codec, originally written by Tom Butterworth and commissioned by VIDVOX, 2012.

## Support the project
If you find this software useful, please consider buying me a coffee.

[![Donate with PayPal](https://img.shields.io/badge/Donate-PayPal-%23003087?logo=paypal)](https://paypal.me/tedcharlesbrown?country.x=US&locale.x=en_US)
[![Donate with Venmo](https://img.shields.io/badge/Donate-Venmo-%23008CFF?logo=venmo)](https://account.venmo.com/u/TedCharlesBrown)
