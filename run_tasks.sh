#!/bin/bash

# === CONFIGURATION ===
VENV_PATH="/home/pi/Lunch-Mail/.venv/bin/activate"
SCRIPT_PATH="/home/pi/Lunch-Mail/main.py"
LOG_DIR="/home/pi/Lunch-Mail/logs"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_OUT="$LOG_DIR/outputs/output_$TIMESTAMP.log"
LOG_ERR="$LOG_DIR/errors/error_$TIMESTAMP.log"
EMAIL="your_email@gmail.com"
HOSTNAME=$(hostname)

# === START TASK ===
echo "==== Task started at $(date) ====" | tee -a "$LOG_OUT" "$LOG_ERR"

# Activate virtual environment
if [[ -f "$VENV_PATH" ]]; then
    source "$VENV_PATH"
    echo "[INFO] Virtual environment activated." >> "$LOG_OUT"
else
    echo "[ERROR] Virtual environment not found: $VENV_PATH" | tee -a "$LOG_ERR"
    echo "Failed to activate virtual environment on $HOSTNAME at $(date)" | mail -s "Pi Task Error: Venv Missing" "$EMAIL"
    exit 1
fi

# Run Python script
echo "[INFO] Running Python script: $SCRIPT_PATH" >> "$LOG_OUT"
python "$SCRIPT_PATH" >> "$LOG_OUT" 2>> "$LOG_ERR"
SCRIPT_EXIT_CODE=$?

# === ERROR HANDLING ===
if [[ $SCRIPT_EXIT_CODE -ne 0 ]]; then
    echo "[ERROR] Script failed with exit code $SCRIPT_EXIT_CODE" | tee -a "$LOG_ERR"
    cat "$LOG_ERR" | mail -s "Pi Task Failed on $HOSTNAME" "$EMAIL"
else
    echo "[INFO] Script completed successfully." >> "$LOG_OUT"
fi

# === SHUTDOWN ===
echo "[INFO] Shutting down at $(date)" >> "$LOG_OUT"
sudo shutdown -h now
