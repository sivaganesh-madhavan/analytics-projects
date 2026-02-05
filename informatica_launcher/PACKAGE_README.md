# Informatica Quick Launcher

A productivity tool for quick access to Informatica MDM environments, Okta apps, and daily learning through quizzes.

## What's Included

- **Quick Launcher**: One-click access to all Informatica environments
- **Okta Integration**: Automatic SSO authentication
- **App Shortcuts**: Quick links to Optum HSA and other apps
- **Daily Quiz**: Learn something new every day with analytical questions
- **Custom Icons**: Visual identification for each app

## Installation

### For First-Time Users:

1. **Install Python** (if not already installed):
   - Download from [python.org/downloads](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Restart your computer after installation

2. **Run Quick Start**:
   - Double-click `QUICK_START.bat`
   - This will install all dependencies and launch the app

### For Regular Use:

- Just double-click `launcher.bat` to start the application

## Features

### Tabs:
- **Informatica**: DEV, QA, UAT, UAT NEW, PERF, PROD environments
- **Apps**: Optum HSA and other company applications
- **Quiz**: Daily analytical quiz (Science, Geography, History, General Knowledge)

### Key Functions:
- One-click environment launch via Okta SSO
- Quick Okta logout for switching environments
- Daily quiz with instant feedback
- Question caching (same question all day)
- Visual indicators for correct/incorrect answers

## Usage Tips

1. **Launching Environments**:
   - Click any environment button
   - Browser opens with Okta SSO
   - You're logged in automatically

2. **Switching Environments**:
   - Click "Logout from Okta" button first
   - Wait for logout to complete
   - Then click the new environment

3. **Daily Quiz**:
   - Click "Quiz" tab
   - Read the question
   - Click any answer to check
   - Green = Correct, Red = Incorrect
   - New question appears every day

## Customization

### Adding New Environments:

1. Get the Okta URL:
   - Go to your Okta portal
   - Right-click the app tile
   - Select "Copy link address"

2. Edit `config.json`:
   - Add new entry to appropriate category
   - Save the file
   - Click "⟳ Reload" in the launcher

### Adding Custom Icons:

1. Place your PNG image in the launcher folder
2. Reference it in `config.json` with the `"icon"` field
3. Reload the launcher

## System Requirements

- Windows 10 or 11
- Python 3.7 or higher
- Internet connection
- Company Okta access

## Files

- `launcher.py` - Main application
- `launcher.bat` - Quick launch script
- `config.json` - Configuration for environments and apps
- `requirements.txt` - Python dependencies
- `informatica_logo.png` - Informatica icon
- `optum_logo.png` - Optum icon
- `quiz_cache.json` - Daily quiz cache (auto-generated)
- `access_log.txt` - Usage history (auto-generated)

## Troubleshooting

### Python Not Found
- Install Python from python.org
- Make sure "Add to PATH" was checked during installation

### Dependencies Not Installing
```bash
pip install pillow requests
```

### Quiz Not Loading
- Check internet connection
- Ensure `requests` library is installed

### Okta Not Working
- Make sure you're logged into Okta in your default browser
- Check that URLs in config.json are correct

## Support

For technical issues or questions, contact your IT administrator.

## Version

Version: 1.0  
Last Updated: February 2026
