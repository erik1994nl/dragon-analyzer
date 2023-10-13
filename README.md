# dragon-analyzer
Speed statistics of dragon boat sessions

# Using a Python environment
In your terminal navigate to your project folder
```python
pyenv install -v 3.11 # install python version
pyenv virtualenv 3.11 dragon-analyzer # creates a virtualenv, you can choose another name if you like
pyenv local dragon-analyzer # automatically use virtualenv when in this directory
```

# Install Poetry
We use Poetry to manage dependencies
If not already installed, run:
```
pip install poetry
```

To install all dependencies run:
```
poetry install
```
