# Feedback and contributions

Use a GitHub issue for questions, reproducibility problems or a proposed improvement. Include your Python version, command, error output and relevant file/cell; omit credentials and personal data.

Before proposing a modeling change, state the feature availability assumptions, split strategy and comparison baseline. Keep historical notebook outputs separate from new runs, and avoid tuning on the held-out test set.

Run these checks from the repository root:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python train.py --output results-local
```

Document new results with their dataset hash, split, seed and package versions. Credit the original project team. Dataset provenance and redistribution terms remain to be clarified; see [data/README.md](data/README.md).
