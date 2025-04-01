poetry install
poetry run python src/imgvisint/transform.py --size 100 100 --input images
poetry run python src/imgvisint/interpolation.py
