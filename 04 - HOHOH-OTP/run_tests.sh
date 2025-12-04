#!/bin/bash
echo "================================"
echo "Running HOHOH-OTP Test Suite"
echo "================================"
cd "$(dirname "$0")"
python -m pytest

