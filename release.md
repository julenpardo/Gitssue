#### Steps for making a release


1. Edit `setup.py` with release tag.

2. Generate RST documentation:

  ```
  pandoc --from=markdown --to=rst --output=README.rst README.md
  ```

3. Build:

  ```
  python setup.py sdist
  ```

4. Upload Gitssue.egg-info/PKG-INFO to pypi.

5. Upload the release:

  ```
  twine upload -r pypi dist/Gitssue-<VERSION>.tar.gz
  ```
  