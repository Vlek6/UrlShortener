#!/bin/bash

# Run pre-commit hooks first
pre-commit run --all-files

# Check if pre-commit hooks passed (exit code 0)
if [ $? -eq 0 ]; then
    # If pre-commit passed, run Commitizen commit
    cz commit "$@"
else
    echo "Pre-commit hooks failed. Please fix the issues before committing."
    exit 1
fi
