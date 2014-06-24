PROJECT_DIRS := $(shell find . -type d |cut -d/ -f1| grep -v venv|grep -v test|grep -v .git|grep -v lost_and_found)

lint: $(PROJECT_DIRS)
	tests/lint_folders.sh $^
	@echo "linting complete"
