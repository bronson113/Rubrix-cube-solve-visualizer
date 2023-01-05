# Rubix's cube solve visualizer

Using pygame to render a rubrix cube!

## Setup

```bash
pip3 install -r requirements.txt
```


## Usage

To see the visualizations, run:
```bash
python3 "3D render.py"
```

To simulate effect of an algorithm, run:
```bash
python3 rubix.py
```
Then input your algorithm in the format `R U R' U' R' F R2 U' R' U' R U R' F'`

## Files

`3D render.py` - renders the cube in 3D using pygame

`rubix.py` - contains the rubix cube class and functions to replicate algorithms

## TODO

- [ ] Add solvers to the rubix cube class
- [ ] Visualize turning the cube:w