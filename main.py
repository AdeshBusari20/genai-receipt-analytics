#!/usr/bin/env python
"""
Main entry point for GenAI Receipt Analytics Report Generation System

Usage:
    python main.py --weekly              # Generate weekly report
    python main.py --monthly             # Generate monthly report
    python main.py --scheduler           # Start automated scheduler
    python main.py --demo                # Run demo with sample data
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from genai_reports.config import Config
from genai_reports.data_loader import DataLoader
from genai_reports.statistics import StatisticsGenerator
from genai_reports.llm_analyzer import create_analyzer
from genai_reports.pdf_generator import PDFReportGenerator
from genai_reports.scheduler import ReportScheduler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE),
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)


class ReportGenerator:
    """Main report generation orchestrator"""
    
    def __init__(self):
        Config.ensure_directories()
        self.data_loader = DataLoader(Config.DATA_DIR)
        self.stats_generator = StatisticsGenerator()
        
        # Initialize PDF generator but don't fail if reportlab is missing
        try:
            self.pdf_generator = PDFReportGenerator(Config.REPORTS_DIR)
        except ImportError:
            logger.warning("PDF generator not available - reportlab not installed")
            self.pdf_generator = None
        
        self.analyzer = create_analyzer(
            Config.LLM_PROVIDER,
            api_key=Config.OPENAI_API_KEY if Config.LLM_PROVIDER == "openai" else Config.ANTHROPIC_API_KEY,
            model=Config.OPENAI_MODEL if Config.LLM_PROVIDER == "openai" else Config.ANTHROPIC_MODEL,
        )
    
    def generate_report(self, report_type: str = "weekly", context: str = "") -> Path:
        """Generate a complete report"""
        
        if not self.pdf_generator:
            print("\n✗ Error: reportlab library is not installed")
            print("   Install with: pip install reportlab")
            print("\nPlease run: pip install reportlab")
            raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")
        
        logger.info(f"Starting {report_type} report generation...")
        
        try:
            # Load data
            logger.info("Loading receipt data...")
            receipts = self.data_loader.load_all_receipts()
            logger.info(f"Loaded {len(receipts)} receipt records")
            
            # Generate statistics
            logger.info("Generating statistics...")
            statistics = self.stats_generator.generate_all_statistics(receipts)
            logger.info("Statistics generated successfully")
            
            # Get LLM analysis
            logger.info("Generating AI analysis...")
            analysis = self.analyzer.analyze_statistics(statistics, context)
            logger.info("AI analysis completed")
            
            # Generate PDF report
            logger.info("Creating PDF report...")
            title = f"{report_type.upper()} RECEIPT ANALYTICS REPORT - {datetime.now().strftime('%B %Y')}"
            report_path = self.pdf_generator.generate_report(
                title=title,
                statistics=statistics,
                analysis=analysis,
                report_type=report_type,
            )
            
            logger.info(f"Report generated successfully: {report_path}")
            print(f"\n✓ Report generated: {report_path}")
            return report_path
        
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}", exc_info=True)
            print(f"✗ Error generating report: {str(e)}")
            raise
    
    def generate_weekly_report(self) -> Path:
        """Generate weekly report"""
        context = "This is a weekly summary of receipt transactions. Focus on transaction trends and notable changes from the previous week."
        return self.generate_report("weekly", context)
    
    def generate_monthly_report(self) -> Path:
        """Generate monthly report"""
        context = "This is a monthly comprehensive analysis of receipt transactions. Include trends, patterns, and recommendations."
        return self.generate_report("monthly", context)
    
    def print_statistics_summary(self):
        """Print statistics summary to console"""
        logger.info("Loading receipt data...")
        receipts = self.data_loader.load_all_receipts()
        
        logger.info("Generating statistics...")
        statistics = self.stats_generator.generate_all_statistics(receipts)
        
        # Print summary
        print("\n" + "="*60)
        print("RECEIPT DATA STATISTICS SUMMARY")
        print("="*60)
        
        financial = statistics.get('financial_stats', {})
        company = statistics.get('company_stats', {})
        quality = statistics.get('data_quality', {})
        
        print(f"\nDataset Overview:")
        print(f"  Total Receipts: {statistics.get('total_receipts', 0):,}")
        print(f"  Generated: {statistics.get('timestamp', 'N/A')}")
        
        print(f"\nFinancial Summary:")
        print(f"  Total Amount: ${financial.get('sum', 0):,.2f}")
        print(f"  Average Per Receipt: ${financial.get('average', 0):,.2f}")
        print(f"  Median: ${financial.get('median', 0):,.2f}")
        print(f"  Range: ${financial.get('min', 0):,.2f} - ${financial.get('max', 0):,.2f}")
        print(f"  Std Dev: ${financial.get('std_dev', 0):,.2f}")
        
        print(f"\nCompany Information:")
        print(f"  Unique Companies: {company.get('total_unique_companies', 0)}")
        print(f"  Unique Addresses: {company.get('total_unique_addresses', 0)}")
        
        top_companies = company.get('top_companies', [])
        if top_companies:
            print(f"  Top 3 Companies:")
            for i, comp in enumerate(top_companies[:3], 1):
                print(f"    {i}. {comp['name']} ({comp['count']} transactions)")
        
        print(f"\nData Quality:")
        completion = quality.get('field_completion_rates', {})
        print(f"  Fully Complete Records: {quality.get('fully_complete_records', 0)}")
        print(f"  Field Completion Rates:")
        for field, rate in completion.items():
            print(f"    - {field.capitalize()}: {rate:.1f}%")
        
        print("="*60 + "\n")


def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(
        description="GenAI Receipt Analytics Report Generation System"
    )
    parser.add_argument(
        "--weekly",
        action="store_true",
        help="Generate a weekly report"
    )
    parser.add_argument(
        "--monthly",
        action="store_true",
        help="Generate a monthly report"
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print statistics summary to console"
    )
    parser.add_argument(
        "--scheduler",
        action="store_true",
        help="Start automated report scheduler"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run demo (generates both weekly and monthly reports)"
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "ollama", "mock"],
        help="LLM provider to use"
    )
    
    args = parser.parse_args()
    
    try:
        report_gen = ReportGenerator()
        
        if args.provider:
            Config.LLM_PROVIDER = args.provider
        
        if args.demo:
            print("\n🚀 Running GenAI Report Generator Demo...\n")
            print("Generating both weekly and monthly reports...\n")
            report_gen.generate_weekly_report()
            report_gen.generate_monthly_report()
            print("\n✓ Demo completed! Check the 'generated_reports' folder.\n")
        
        elif args.weekly:
            print("\n📊 Generating Weekly Report...\n")
            report_gen.generate_weekly_report()
        
        elif args.monthly:
            print("\n📊 Generating Monthly Report...\n")
            report_gen.generate_monthly_report()
        
        elif args.summary:
            report_gen.print_statistics_summary()
        
        elif args.scheduler:
            print("\n⏱️  Starting Report Scheduler...\n")
            scheduler = ReportScheduler()
            
            scheduler.schedule_weekly_report(
                report_gen.generate_weekly_report,
                day_of_week=Config.SCHEDULE_WEEKLY,
                time_str=Config.SCHEDULE_WEEKLY_TIME,
            )
            
            scheduler.schedule_monthly_report(
                report_gen.generate_monthly_report,
                day_of_month=Config.SCHEDULE_MONTHLY_DAY,
                time_str=Config.SCHEDULE_MONTHLY_TIME,
            )
            
            scheduler.start()
            
            print(f"Scheduler running. Press Ctrl+C to stop.\n")
            print(f"Scheduled jobs:")
            for job in scheduler.list_jobs():
                print(f"  - {job['name']} (Next run: {job['next_run']})")
            print()
            
            try:
                import time
                while scheduler.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nShutting down scheduler...")
                scheduler.stop()
                print("Scheduler stopped.")
        
        else:
            parser.print_help()
    
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        print(f"Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
