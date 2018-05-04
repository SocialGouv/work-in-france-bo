.PHONY: clean pylint

# Global tasks
# ============

clean:
	docker exec -t wif_django find . -type d -name "__pycache__" -depth -exec rm -rf '{}' \;

pylint:
	docker exec -t wif_django pipenv run pylint --rcfile='.pylintrc' --reports=no --output-format=colorized 'workinfrance';
