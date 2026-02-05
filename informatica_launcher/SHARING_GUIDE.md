# How to Share Informatica Launcher

## Quick Sharing (5 minutes)

### Step 1: Create Package

**Option A - Manual:**
1. Copy these files into a new folder:
   - `launcher.py`
   - `launcher.bat`
   - `QUICK_START.bat`
   - `config.json`
   - `requirements.txt`
   - `README.md`
   - `PACKAGE_README.md`
   - `SETUP_INSTRUCTIONS.txt`
   - `informatica_logo.png`
   - `optum_logo.png`

**Option B - Automated:**
1. Run `CREATE_PACKAGE.bat`
2. It will create a folder with all necessary files

### Step 2: Zip the Folder
1. Right-click the folder
2. Send to → Compressed (zipped) folder
3. Name it: `InformaticaLauncher.zip`

### Step 3: Share
Send the ZIP file via:
- Email
- SharePoint
- Teams
- Shared drive

## What Recipients Need

### System Requirements:
- ✅ Windows 10/11
- ✅ Python 3.7+ ([Download](https://www.python.org/downloads/))
- ✅ Internet connection
- ✅ Company Okta access

### Setup Instructions for Recipients:
1. Extract the ZIP file
2. Run `QUICK_START.bat`
3. Wait for dependencies to install
4. Launcher opens automatically!

## Files Explanation

### Essential Files (Must Include):
- **launcher.py** - Main application code
- **launcher.bat** - Quick launch script
- **QUICK_START.bat** - First-time setup script
- **config.json** - Environment configuration
- **requirements.txt** - Python dependencies
- **PACKAGE_README.md** - User documentation
- **SETUP_INSTRUCTIONS.txt** - Quick reference
- **informatica_logo.png** - App icon
- **optum_logo.png** - Optum icon

### Files to EXCLUDE:
- ❌ `quiz_cache.json` (auto-generated)
- ❌ `access_log.txt` (personal usage log)
- ❌ `__pycache__/` (Python cache)
- ❌ Any `.pyc` files

## Email Template

```
Subject: Informatica Quick Launcher Tool

Hi Team,

I've created a productivity tool for quick access to Informatica environments and daily quizzes.

**What it does:**
- One-click launch to all Informatica environments (DEV, QA, UAT, PERF, PROD)
- Quick Okta logout for easy environment switching
- Access to Optum HSA and other apps
- Daily analytical quiz for learning

**Setup (5 minutes):**
1. Extract the attached ZIP file
2. Make sure Python is installed (python.org)
3. Run QUICK_START.bat
4. The launcher opens automatically!

**Usage:**
- Double-click launcher.bat to start
- Click any environment to launch via Okta SSO
- Check Quiz tab for daily questions

See PACKAGE_README.md for full documentation.

Let me know if you have any questions!
```

## Advanced Distribution

### Option 1: Standalone Executable (No Python Required)

Use PyInstaller to create an .exe:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=informatica_logo.ico launcher.py
```

Pros: No Python installation needed
Cons: Larger file size (~50MB)

### Option 2: Company SharePoint/Portal

1. Upload the entire folder to SharePoint
2. Share the link with access permissions
3. Users can download and extract

### Option 3: Git Repository

If your company uses Git:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push
```

## Customization Before Sharing

### Remove Personal Data:
1. Delete `quiz_cache.json` if it exists
2. Delete `access_log.txt` if it exists
3. Review `config.json` - remove any personal/test entries

### Add Company Branding:
1. Replace `informatica_logo.png` with company logo
2. Update header text in `launcher.py` if needed
3. Add company-specific instructions to README

## Support & Maintenance

### Version Updates:
When you improve the tool:
1. Update version number in PACKAGE_README.md
2. Add changelog notes
3. Re-package and share

### User Support:
Direct users to:
- SETUP_INSTRUCTIONS.txt for setup issues
- PACKAGE_README.md for usage questions
- Your IT team for Okta/access issues

## Security Notes

⚠️ **Important:**
- Never include credentials in config.json
- Okta handles all authentication
- No passwords are stored in the tool
- Each user uses their own Okta account

## File Size

Typical package size: ~100KB (without Python)
With Python (if bundled): ~50MB

Recommend: Share without Python, let users install it separately.
