# Bibite Scripts
Scripts for editing bibites and save files for The Bibites game

## Official Game and community links

* [YouTube](https://www.youtube.com/c/TheBibitesDigitalLife)
* [itch.io](https://leocaussan.itch.io/the-bibites)
* [Reddit](https://www.reddit.com/r/TheBibites)

## Project setup

This section goes over the steps needed to setup this project on your machine and run the scripts or jupyter notebooks

### Prerequisites

Python 3.10 (may work on earlier versions too)

### Setup

Create a virtual environment before installing requirements

```commandline
python -m venv venv
```

Activate the virtual environment, on Windows do this:

```powershell
.\venv\Scripts\activate
```

On linux/macOS, do this:

```zsh
. venv/bin/activate
```

Install requirements

```commandline
python -m pip install -r requirements.txt
```

## Running jupyter lab

Jupyter lab is useful for visualizing data from a save file (see graph.ipynb)

To start, run this command:

```commandline
jupyter-lab
```

(you must install dependencies first, see setup section for details)

## Running scripts

Overview of current scripts

### Edit Bibite genes in a save file

This script makes a copy of the included save file with some genes modified for
all the Bibites.

```commandline
python edit_save.py
```

Currently this is hardcoded to edit the included save-file (`world_autosave_20220917102459.zip`),
but this can be customized by editing the `src` variable in the `main` function:

```python
    src = root / "world_autosave_20220917102459.zip"
```

Next you may customize the `new_genes` dict in the `main` function to the ones that
you'd like to change.

```python
            new_genes = {
                "BrainMutationSigma": random.uniform(0.15, 0.4),
                "BrainAverageMutation": random.uniform(1.5, 4.0),
            }
```

`random.uniform` is useful for specifying a range of values for the population, where each
Bibite gets a random value within this range.

This could also be a single value instead:

```python
            new_genes = {
                "Diet": 0.2,
            }
```