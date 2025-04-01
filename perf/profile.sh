poetry run python analysis.py


poetry shell
py-spy record -o ../docs/_static/flamegraph.svg -- python analysis.py


cd ..
snakeviz docs/_static/join_profile.prof
cd perf