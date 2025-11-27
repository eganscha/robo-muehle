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
