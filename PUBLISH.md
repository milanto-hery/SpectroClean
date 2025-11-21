# PUBLISHING SpectroClean

## 1. Prepare
- Update `pyproject.toml` version
- Ensure tests pass: `pytest -q`

## 2. Build
```bash
python -m pip install --upgrade build twine
python -m build
```

## 3. TestPyPI (recommended)
```bash
python -m twine upload --repository testpypi dist/*
# Install from testpypi:
pip install -i https://test.pypi.org/simple/ SpectroClean
```

## 4. Publish to PyPI
```bash
python -m twine upload dist/*
```

## 5. Tips
- Use `twine check dist/*` to catch metadata issues
- Use a separate PyPI account for CI automation
- Add long_description_content_type = 'text/markdown' in pyproject if you use README badges
