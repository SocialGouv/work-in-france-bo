.PHONY: clean pylint

# Global tasks
# ============

clean:
	find . -type d -name "__pycache__" -depth -exec rm -rf '{}' \;

pylint:
	pipenv run pylint --rcfile='.pylintrc' --reports=no --output-format=colorized 'workinfrance';
