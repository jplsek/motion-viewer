# Motion Viewer

A readonly and simple web ui for the [motion project](https://motion-project.github.io).

## Features

- **View the video recordings**
- View the stream

## Requirements

- A [fully running instance of Motion](https://motion-project.github.io/motion_guide.html).
- The `stream_localhost` option in motion must be set to `off`.
- The `target_dir` option must be specified. (Motion Viewer does not utilize Motion's database.)

## Install

Install `git docker`

```
git clone https://github.com/jplsek/motion-viewer
docker build -t motionviewer .
docker run -p 3000:3000 -e SERVER=http://motion.lan -v /:/motion --restart unless-stopped -d motionviewer
```

## Development

This requires a fully operational motion project already running.

If you want to use your server:

Install `sshfs`

```sh
mkdir motion
sshfs motion.lan:/ motion
```

Set up `.env` to your needs:

```
cp .env.example .env
```

Install `nodejs yarn`

Then:

```
yarn install
```

Now to start Motion Viewer:

```
yarn dev
```

### Linting and Code Style

```
yarn lint
```

## Notes

- Firefox does not work because they do not support the mkv video container.
- If the motion config changes, you must restart the client.
- This client may not read all of the config from motion properly (because I'm not utilizing that config key), so some stuff might break.

## FAQ

> How do I add authentication?

Proxy the app through a web server and set up Basic Authentication.

> How do I add TLS?

Proxy the app through a web server and set up TLS.

> Would you be willing to add more features to this?

Sure. I made this for my personal needs, but PRs are welcome. Check out [motionEye](https://github.com/ccrisan/motioneye) for a more feature rich client which may fit your needs.

# Motion Scripts

These scripts can be used to manage the videos recorded by Motion. These scripts are located in the `scripts` folder.

## Requirements

Dependencies:

```
python3 ffmpeg
```

Python packages:

```
python3-watchdog python3-wheel python3-setuptools
```

## Install

```
sudo python3 -m pip install .
```

This will also install a systemd service called `watch-motion-videos`.

## clean-motion-videos

This script removes videos under a certain duration.

It will read the motion config to get the value of `target_dir`, then check every video in the directory on whether it meets the duration criteria. If not, it will delete the video. If `--watch` is specified, it will instead check only for newly created videos.

```
usage: clean-motion-videos [-h] [-d] [-w] [-r ROOT] [-m MIN_DURATION]

Remove short videos.

optional arguments:
  -h, --help            show this help message and exit
  -d, --dry-run         Show what files would be deleted (default: False)
  -w, --watch           Watch the directory for new files (default: False)
  -r ROOT, --root ROOT  Set the root directory (default: /)
  -m MIN_DURATION, --min-duration MIN_DURATION
                        The minimum duration in seconds of the video required to keep (default: 2)
  -x MAX_SIZE, --max-size MAX_SIZE
                        The maximum size in gigabytes of total videos to keep (default: 50)
```
