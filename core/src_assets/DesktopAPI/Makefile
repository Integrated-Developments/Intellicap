# Makefile for building and running the DesktopAPI project

# Variables
PYTHON = python
FLASK_APP = desk_flask.py
GO_SRC = actions/go_components
RUST_SRC = actions/rust_components
C_SRC = actions/c_components
BIN_DIR = bin

.PHONY: all build test run clean

# Build all components
all: build-python build-go build-rust build-c

# Build Python components
build-python:
	@echo "Building Python components..."
	$(PYTHON) -m pip install -r requirements.txt

# Build Go components
build-go:
	@echo "Building Go components..."
	cd $(GO_SRC) && go build -o ../$(BIN_DIR)/go_component

# Build Rust components
build-rust:
	@echo "Building Rust components..."
	cd $(RUST_SRC) && cargo build --release

# Build C components
build-c:
	@echo "Building C components..."
	cd $(C_SRC) && gcc -o ../$(BIN_DIR)/c_component main.c

# Run the Flask app
run:
	@echo "Running Flask app..."
	$(PYTHON) $(FLASK_APP)

# Test all components
test:
	@echo "Running tests..."
	$(PYTHON) -m unittest discover

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(BIN_DIR)/*
