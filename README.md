# Automated Receipt Analytics & GenAI Report Generation

AI-powered receipt analytics system that extracts structured data from scanned receipts, performs statistical analysis, and generates automated PDF reports using Generative AI and Large Language Models (LLMs).

## Features

- Automated weekly and monthly report generation
- Receipt data extraction and statistical analysis
- GenAI-powered insights and summaries
- PDF report generation
- Scheduler support for recurring reports
- Supports OpenAI, Anthropic, Ollama, and Mock providers

## Tech Stack

- Python
- LLMs / Generative AI
- PDF Generation
- Scheduling Automation
- Statistical Analysis

## Project Structure

```bash
.
├── main.py
├── requirements.txt
├── genai_reports/
│   ├── data_loader.py
│   ├── statistics.py
│   ├── llm_analyzer.py
│   ├── pdf_generator.py
│   └── scheduler.py
├── generated_reports/
└── data/
```

## Installation

```bash
git clone https://github.com/AdeshBusari20/genai-receipt-analytics.git
cd genai-receipt-analytics

pip install -r requirements.txt
```

## Usage

Generate weekly report:

```bash
python main.py --weekly
```

Generate monthly report:

```bash
python main.py --monthly
```

Run demo:

```bash
python main.py --demo
```

Start scheduler:

```bash
python main.py --scheduler
```

## Example Output

The system generates:

- Executive Summary
- Financial Statistics
- Merchant Insights
- AI-Generated Recommendations
- PDF Reports in `generated_reports/`

## Sample Results

- Processed 626+ receipt records
- Generated automated weekly and monthly PDF reports
- AI-powered analytics and summary generation

## Future Improvements

- Web dashboard
- Email report delivery
- Real-time analytics
- Advanced anomaly detection

### Contributors
- Adesh Busari
- Maruti Haval
- Disha Jadhav
- Ritu Jotawar

## License

MIT License
