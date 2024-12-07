# Wakeify: A Teenager-Proof Alarm Clock
A Spotify playing tamper-proof alarm clock with snooze but no "off" button. Perfect for the tired teenager in your life!

<IMAGE>

## Equipment Needed
* A [Spotify Premium](https://www.spotify.com/) account, ideally ine dedicated to this device. Easy enough on a Family Plan.
* Raspberry Pi 3B+ or newer single board computer running Raspberry Pi OS. (This might work on a Raspberry Pi Zero 2 W but I have not tested it yet.)
* 1 to 3 SPST buttons, depending on functionality desired. 1 is required for the play/pause/snooze button, but 2 more can be added for previous and next buttons.
* (optional) 1 rotary encoder for volume control
* Various tools for electronics and building an enclosure as needed for this project
   
***A Note about compatibility***:  Wakeify would likely work on any Linux OS that runs on any hardware as long as you can wire up the GPIO or some alternative. It would likely require significant changes to the hardware interface code though, so beware!

## Installation and Setup Guide
### Rust
Install Rust as recommended here: https://www.rust-lang.org/tools/install

tl;dr: run `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
### Spotify Player
Install [spotify_player](https://github.com/aome510/spotify-player) using the [daemon option](https://github.com/aome510/spotify-player?tab=readme-ov-file#daemon). The instructions are a bit confusing so you can take my word for it and run:

 `cargo install spotify_player --features daemon,rodio-backend,sixel --locked`