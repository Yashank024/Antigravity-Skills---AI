#!/bin/bash

if [[ "$1" == "--help" ]]; then
  echo "Usage: ./setup-backend.sh [project_name] [framework]"
  echo "Frameworks: express, flask"
  exit 0
fi

PROJECT_NAME=$1
FRAMEWORK=$2

if [ -z "$PROJECT_NAME" ] || [ -z "$FRAMEWORK" ]; then
  echo "Missing arguments. Run with --help for usage."
  exit 1
fi

mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME" || exit 1

if [ "$FRAMEWORK" == "express" ]; then
  mkdir -p controllers services models routes config
  echo "Created Express project structure"
elif [ "$FRAMEWORK" == "flask" ]; then
  mkdir -p api/controllers api/services api/models core/config
  echo "Created Flask project structure"
else
  echo "Unknown framework"
fi
