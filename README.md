# Item Extractor

<!-- [![PyPI version](https://shields.io)](https://pypi.org)
[![Python versions](https://shields.io)](https://pypi.org) -->

lightweight feature extraction that turns natural-language into structured JSON of type tasks, events, todos, etc...

## Installation

Choose the installation method that fits your use case:

### 1. Standard Installation (Production / Inference)
If you only need to run existing agents, install the core package. This keeps the installation lightweight and bundles the standard **spaCy `en_core_web_md` model** automatically:
```bash
uv add item_extractor
# or via pip
pip install item_extractor
```

### 2. Notebook Installation (Development / Intent Classification Custom Agent Training)
If you want to use our interactive Jupyter Notebooks to design, benchmark, and train your own custom agent models, install the package with the `notebook` extra dependencies:
```bash
uv add "item_extractor[notebook]"
# or via pip
pip install "item_extractor[notebook]"
```

---

## 🚀 Quick Start (Core Library)

Use the built-in components to run an agent directly in your Python application:

```python
from item_extractor import extract

items = extract("Organize the garage")
print(response) # Returns Todo(title='Organize the garage', description='', type=<ItemType.TODO: 'todo'>, completed=False)
```

---

## 🧠 Creating Custom Intent Classification Agent Model

If you installed the package with the `[notebook]` extras, you can create and fine-tune your own agent architectures. 

1. Clone this repository to access the starter templates:
   ```bash
   git clone https://github.com/UnknwnDev/item-extractor.git
   cd item_extractor
   ```
2. Open `notebooks/create_custom_agent.ipynb` and follow the step-by-step guide to train your agent using spaCy embeddings, customize decision thresholds, and evaluate agent trajectories.



## 🛠️ Contribution & Local Setup

For developers looking to contribute to the codebase:

```bash
# Clone and sync all environment dependencies including notebook extras
git clone https://github.com/UnknwnDev/item-extractor.git
cd item_extractor
uv sync --extra notebook

# Run the test suite
uv run pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
