# Installation & Troubleshooting Guide

## Quick Start

### 1. First, Run the Diagnostic
```bash
cd C:\Users\HP\OneDrive\Desktop\GENAIPROJECT
python diagnose.py
```

This will:
- Check your Python version
- List installed packages
- Automatically install missing packages

### 2. Then Run the Demo
```bash
python main.py --demo
```

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'reportlab'"

**Solution 1: Run the diagnostic script**
```bash
python diagnose.py
```

**Solution 2: Manual installation**
```bash
pip install --upgrade reportlab APScheduler
```

**Solution 3: Use Python explicitly**
```bash
python -m pip install reportlab APScheduler
```

### Error: "No module named 'genai_reports'"

Make sure you're in the correct directory:
```bash
cd C:\Users\HP\OneDrive\Desktop\GENAIPROJECT
```

Check the directory structure:
```bash
ls -la genai_reports/
```

### Verify Installation

Check if packages are installed:
```bash
python -c "import reportlab; print('reportlab: OK')"
python -c "import apscheduler; print('APScheduler: OK')"
python -c "from genai_reports import Config; print('genai_reports: OK')"
```

---

## Commands Reference

```bash
# Check Python version
python --version

# Check specific package
python -c "import reportlab; print(reportlab.__version__)"

# List installed packages
pip list

# Upgrade pip
python -m pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# Run system test
python test_system.py

# Run diagnostic
python diagnose.py

# Generate weekly report
python main.py --weekly

# Generate monthly report
python main.py --monthly

# Run demo (both reports)
python main.py --demo

# View statistics
python main.py --summary

# Start scheduler
python main.py --scheduler
```

---

## If Still Not Working

1. **Uninstall and reinstall:**
   ```bash
   pip uninstall reportlab APScheduler -y
   pip install reportlab APScheduler
   ```

2. **Check Python path:**
   ```bash
   python -c "import sys; print(sys.executable)"
   ```

3. **Install using full path:**
   ```bash
   C:\Users\HP\AppData\Local\Python\pythoncore-3.14-64\python.exe -m pip install reportlab APScheduler
   ```

4. **Run requirements.txt:**
   ```bash
   pip install -r requirements.txt
   ```

---

## File Structure

```
GENAIPROJECT/
├── main.py                    # Main entry point
├── test_system.py             # System test
├── diagnose.py               # Diagnostic script (new!)
├── requirements.txt
├── .env.example
├── genai_reports/            # Package directory
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── statistics.py
│   ├── llm_analyzer.py
│   ├── pdf_generator.py
│   └── scheduler.py
├── ICDAR-2019-SROIE/
│   └── data/
│       ├── box/
│       ├── key/
│       └── img/
└── generated_reports/        # Output folder (created automatically)
```

---

## Next Steps

1. Run `python diagnose.py` to auto-fix any issues
2. Run `python main.py --demo` to generate sample reports
3. Check `generated_reports/` folder for PDF files
4. Optional: Set up LLM API keys for better insights
