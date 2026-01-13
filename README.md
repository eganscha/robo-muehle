# Robo Arm Mühle
## Setup
```sh
python3 -m venv venv && source venv/bin/activate
git clone https://github.com/frederik-uni/robo-muehle.git
cd robo-muehle
pip install -e .
```

or 

```sh
python3 -m venv venv && source venv/bin/activate
pip install git+https://github.com/frederik-uni/robo-muehle.git
```

## Usage
```sh
python3 -m muehle_game
```

## Test
```sh
pip install pytest
pytest
```

## Calibration
```sh
python -m piecewalker.calibration

usage: __main__.py [-h] [--path PATH] [--fixed_z]

Calibrates the positions of the game board. Creates a calibration_[idx].toml file inside of /configs/calibrations with a progressive index.

options:
  -h, --help   show this help message and exit
  --path PATH  Path where the calibration_[idx].toml file is stored. If none is provided, "/configs/calibration" will be used.
  --fixed_z    Do not calculate the z-value based off of the average of the calibration points. Instead, use a hard-coded z-value that will work for your particular board defined inside the
               "/configs/calibration/niryo_config.toml" file.
```