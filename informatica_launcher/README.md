# 🚀 Informatica Quick Launcher

A simple desktop application for quick access to Informatica environments through Okta SSO.

## Features

- **Tabbed Interface**: Organize apps by category (Informatica environments, Other apps, etc.)
- **One-Click Access**: Launch any environment or app with a single click
- **Quick Logout**: One-click Okta logout button to switch environments cleanly
- **Custom Icons**: Each app can have its own icon
- **Daily Quiz**: Interactive quiz panel with medium-level analytical questions
- **Auto SSO**: Opens in browser with automatic Okta authentication
- **Access Logging**: Tracks which environments you access and when
- **Easy Configuration**: Add/modify environments via JSON config

## Requirements

- Python 3.7 or higher (Tkinter included)
- Windows OS
- Active Okta SSO account

## Installation

1. Ensure Python is installed:
   ```bash
   python --version
   ```

2. No additional packages needed! Tkinter comes with Python.

## Usage

### Quick Start

**Double-click `launcher.bat`** - That's it!

### Manual Start

```bash
cd informatica_launcher
python launcher.py
```

## Usage Workflow

### Switching Between Environments

Since Dev, QA, UAT, and Prod share the same Okta SSO:

1. **Click "Logout from Okta"** (pink button at top)
2. Wait for Okta logout page to complete
3. **Click your desired environment** (DEV, QA, etc.)
4. Browser opens and Okta SSO logs you in automatically

**Tip**: You only need to logout when switching environments. If you're returning to the same environment, just click the button directly.

### Daily Quiz

Click the **"Quiz"** tab to access the daily quiz:

1. **New Question Daily**: Fresh question every day (medium difficulty)
2. **Multiple Choice**: Click any answer to check if you're correct
3. **Instant Feedback**: 
   - Green = Correct answer
   - Red = Wrong answer
   - Correct answer always shown in green
4. **Show Answer**: Click to reveal the correct answer without guessing
5. **Question History**: Past 30 days of questions are tracked

The quiz fetches questions from the Open Trivia Database API, filtered to only include:
- **Science & Nature** - Scientific facts, biology, chemistry, physics
- **Geography** - Countries, capitals, landmarks, physical geography  
- **History** - Historical events, figures, dates
- **General Knowledge** - Broad educational topics

This filtering ensures you get analytical and educational questions (no entertainment, sports, or video game trivia). If the API is unavailable, it falls back to built-in educational questions.

## Configuration

Edit `config.json` to add or modify environments:

```json
{
  "okta_domain": "https://salesforce.okta.com/",
  "okta_logout_url": "https://salesforce.okta.com/login/signout",
  "categories": {
    "Informatica": [
      {
        "name": "Development",
        "shortName": "DEV",
        "type": "default",
        "url": "https://salesforce.okta.com/home/...",
        "description": "Development environment"
      }
    ],
    "Apps": [
      {
        "name": "Optum HSA",
        "shortName": "Optum HSA",
        "type": "default",
        "url": "https://salesforce.okta.com/home/...",
        "description": "HSA Account",
        "icon": "optum_logo.png"
      }
    ]
  }
}
```

### Config Options

- `okta_domain`: Your Okta domain URL
- `okta_logout_url`: URL to logout from Okta (default: `{okta_domain}/login/signout`)
- `categories`: Object containing category names as keys and arrays of apps/environments as values
  - Each category becomes a tab in the launcher
  - Items can have optional `icon` field pointing to a PNG file in the launcher folder

### Environment Types

- `dev` - Green button
- `qa` - Blue button
- `uat` - Orange button
- `prod` - Red button

### Adding New Environments or Apps

1. Go to your Okta portal
2. Right-click the app tile
3. Select "Copy link address"
4. Add new entry to the appropriate category in `config.json`
5. (Optional) Add a custom icon by placing a PNG file in the launcher folder and referencing it
6. Click "⟳ Reload Config" in the launcher

### Adding New Categories (Tabs)

Edit `config.json` and add a new category:

```json
"categories": {
  "Informatica": [...],
  "Apps": [...],
  "New Category": [
    {
      "name": "My App",
      "shortName": "APP",
      "type": "default",
      "url": "https://...",
      "description": "Description"
    }
  ]
}
```

## Tips

### Create Desktop Shortcut

1. Right-click `launcher.bat`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. (Optional) Right-click shortcut → Properties → Change Icon

### Pin to Taskbar

1. Create shortcut as above
2. Right-click shortcut
3. Select "Pin to taskbar"

### Keyboard Shortcuts (Coming Soon)

- Alt+1: Launch Dev
- Alt+2: Launch QA
- Alt+3: Launch UAT
- Alt+4: Launch Prod

## Troubleshooting

### "Python is not installed"

Download and install Python from [python.org](https://www.python.org/downloads/)

### "Config file not found"

Ensure `config.json` is in the same folder as `launcher.py`

### Links Don't Open

Check that your default browser is set correctly in Windows Settings

### SSO Not Working

The launcher opens URLs in your default browser. Make sure you're already logged into Okta in that browser, or it will prompt you to login.

### Quiz Not Loading

The quiz requires an internet connection to fetch questions. If the API is unavailable, it will use built-in fallback questions. Make sure `requests` library is installed:

```bash
pip install requests
```

### Quiz Shows Old Question

The quiz refreshes daily at midnight. To force a new question, delete `quiz_cache.json` and restart the launcher.

## Access Logs

The launcher creates `access_log.txt` to track your environment access:

```
2026-02-04 10:30:15 - Accessed: Development
2026-02-04 11:45:22 - Accessed: Quality Assurance
```

## Future Enhancements

- [ ] System tray integration
- [ ] Keyboard shortcuts
- [ ] Recent environments section
- [ ] Search/filter functionality
- [ ] Custom icons
- [ ] Dark mode
- [ ] Multi-app support (other Okta apps)

## Support

For issues or feature requests, contact your development team.

---

**Version**: 1.0  
**Created**: February 2026  
**Platform**: Windows with Python 3.7+
