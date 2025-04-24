#!/bin/bash
# Run from root directory
cd "$(dirname "$0")/.." || exit 1

# Define test configurations
declare -a TEST_NAMES=("rest_api" "database_query")

for TEST in "${TEST_NAMES[@]}"; do
  JMX_FILE="test/azure/${TEST}_test_plan.jmx"
  CSV_OUTPUT="results/azure/${TEST}_results.csv"
  HTML_OUTPUT_DIR="results/azure/${TEST}_html"

  echo "Running JMeter test for ${TEST}..."
  jmeter -n -t "$JMX_FILE" -l "$CSV_OUTPUT" &

  PIDS+=($!)
done

# Wait for all tests to complete
for PID in "${PIDS[@]}"; do
  wait $PID
done

echo "All JMeter tests completed."

# Generate HTML reports
for TEST in "${TEST_NAMES[@]}"; do
  CSV_OUTPUT="results/azure/${TEST}_results.csv"
  HTML_OUTPUT_DIR="results/azure/${TEST}_html"
  
  # Clean up old HTML report directory if it exists
  if [ -d "$HTML_OUTPUT_DIR" ]; then
    echo "Clearing old report directory: $HTML_OUTPUT_DIR"
    rm -rf "$HTML_OUTPUT_DIR"
  fi

  echo "Generating HTML report for ${TEST}..."
  jmeter -g "$CSV_OUTPUT" -o "$HTML_OUTPUT_DIR"
done

echo "Reports generated. Check the results/azure/ directory."