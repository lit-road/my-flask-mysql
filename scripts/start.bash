#!/bin/bash

# Start the backend process
python3 ./server/app.py &

# Start the frontend process
pnpm run dev
