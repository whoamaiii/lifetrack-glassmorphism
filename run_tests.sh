#!/bin/bash

# Personal Life Tracker - Test Runner
# ===================================
#
# This script runs the test suite with various options.
#
# Usage:
#   ./run_tests.sh              # Run all tests with coverage
#   ./run_tests.sh unit         # Run only unit tests
#   ./run_tests.sh integration  # Run only integration tests
#   ./run_tests.sh quick        # Run tests without coverage
#   ./run_tests.sh specific <test_file>::<test_name>  # Run specific test
#   ./run_tests.sh watch        # Run tests in watch mode (requires pytest-watch)

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "🧪 Personal Life Tracker Test Suite"
echo "==================================="

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}❌ pytest is not installed${NC}"
    echo "Install it with: pip install pytest pytest-cov"
    exit 1
fi

# Parse command line arguments
MODE=${1:-"all"}

case $MODE in
    "all")
        echo -e "${GREEN}Running all tests with coverage...${NC}"
        pytest --cov=. --cov-report=html --cov-report=term-missing
        echo -e "\n${GREEN}✅ Coverage report generated in htmlcov/index.html${NC}"
        ;;
    
    "unit")
        echo -e "${GREEN}Running unit tests only...${NC}"
        pytest -m "not integration" -v
        ;;
    
    "integration")
        echo -e "${GREEN}Running integration tests only...${NC}"
        pytest -m integration -v
        ;;
    
    "quick")
        echo -e "${GREEN}Running tests without coverage...${NC}"
        pytest -v
        ;;
    
    "specific")
        if [ -z "$2" ]; then
            echo -e "${RED}Please specify test path${NC}"
            echo "Example: ./run_tests.sh specific tests/test_logic.py::TestConfigurationManagement::test_load_config_default"
            exit 1
        fi
        echo -e "${GREEN}Running specific test: $2${NC}"
        pytest -v "$2"
        ;;
    
    "watch")
        echo -e "${GREEN}Running tests in watch mode...${NC}"
        if ! command -v ptw &> /dev/null; then
            echo -e "${YELLOW}Installing pytest-watch...${NC}"
            pip install pytest-watch
        fi
        ptw -- -v
        ;;
    
    "debug")
        echo -e "${GREEN}Running tests with debugging enabled...${NC}"
        pytest -v --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb
        ;;
    
    "coverage")
        echo -e "${GREEN}Generating detailed coverage report...${NC}"
        pytest --cov=. --cov-report=html --cov-report=term-missing --cov-report=xml
        echo -e "\n${GREEN}Opening coverage report...${NC}"
        
        # Try to open the report in browser
        if command -v open &> /dev/null; then
            open htmlcov/index.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open htmlcov/index.html
        else
            echo "Coverage report available at: htmlcov/index.html"
        fi
        ;;
    
    *)
        echo -e "${RED}Unknown mode: $MODE${NC}"
        echo "Available modes:"
        echo "  all         - Run all tests with coverage (default)"
        echo "  unit        - Run unit tests only"
        echo "  integration - Run integration tests only"
        echo "  quick       - Run tests without coverage"
        echo "  specific    - Run specific test"
        echo "  watch       - Run tests in watch mode"
        echo "  debug       - Run tests with debugger"
        echo "  coverage    - Generate and open detailed coverage report"
        exit 1
        ;;
esac

# Show test statistics
echo -e "\n${YELLOW}Test Statistics:${NC}"
echo "Total test files: $(find tests -name "test_*.py" | wc -l)"
echo "Total test functions: $(grep -r "def test_" tests | wc -l)"

# Check for any TODO or FIXME in tests
TODO_COUNT=$(grep -r "TODO\|FIXME" tests 2>/dev/null | wc -l || echo "0")
if [ "$TODO_COUNT" -gt 0 ]; then
    echo -e "\n${YELLOW}⚠️  Found $TODO_COUNT TODO/FIXME comments in tests${NC}"
fi

echo -e "\n✨ Done!"