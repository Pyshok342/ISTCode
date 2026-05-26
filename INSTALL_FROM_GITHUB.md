# Install from GitHub

After this project is pushed to a public GitHub repository, install it on any computer without Git:

```powershell
python -m pip install https://github.com/USERNAME/REPOSITORY/archive/refs/heads/main.zip
```

Or install with Git:

```powershell
python -m pip install git+https://github.com/USERNAME/REPOSITORY.git
```

Example:

```powershell
python -m pip install https://github.com/USERNAME/my_python_library/archive/refs/heads/main.zip
```

Test:

```powershell
python -c "from my_python_library import hello; print(hello('Alex'))"
```

Expected output:

```text
Hello, Alex!
```

## Push this project to GitHub

### Option A: GitHub CLI

Install GitHub CLI:

```powershell
winget install --id GitHub.cli
```

Login:

```powershell
gh auth login
```

If Git asks for author info:

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Commit and publish:

```powershell
cd "C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library"
git add .
git commit -m "Initial library scaffold"
gh repo create my_python_library --public --source . --remote origin --push
```

### Option B: GitHub website

Create a public empty repository on GitHub, then run:

```powershell
cd "C:\Users\Huawei\Desktop\маркетплейсы\Codex\my_python_library"
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git add .
git commit -m "Initial library scaffold"
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git branch -M main
git push -u origin main
```

## PyPI later

Install from PyPI would look like this:

```powershell
python -m pip install my-python-library
```

Before that, the package name must be unique on PyPI, and the package must be uploaded with:

```powershell
python -m build
python -m twine upload dist/*
```
