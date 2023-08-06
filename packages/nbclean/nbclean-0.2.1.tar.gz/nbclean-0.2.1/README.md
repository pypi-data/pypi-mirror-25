# nbclean
A collection of tools to preprocess, modify, and otherwise clean up Jupyter Notebooks.

## Installation
You can install `nbclean` with pip:

```bash
pip install nbclean
```

## Usage
You can use `nbclean` to "clean up" Jupyter notebooks. You can clear cell
outputs, cell content, or components of cell outputs. You can also replace
text in cells with new text of your choosing.

The primary feature of `nbclean` is the `NotebookCleaner` class, which performs
the above actions on a notebook according to tags that are in each cell's
metadata. For an example, see the [example notebook](examples/modify_notebooks.ipynb).
