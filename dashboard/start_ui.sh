#!/bin/bash
# Start the Chromium browser in kiosk mode pointing to the local dashboard
chromium-browser --kiosk --app=http://localhost:8000/static/index.html --disable-restore-session-state
