poetry install
poetry run python transform.py --size 100 100 --input images
poetry run python interpolation.py
