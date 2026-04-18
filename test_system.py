#!/usr/bin/env python
"""
Test script to verify the GenAI Report Generation system is working correctly
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    try:
        from genai_reports import (
            Config, DataLoader, StatisticsGenerator,
            create_analyzer, PDFReportGenerator, ReportScheduler
        )
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    try:
        from genai_reports.config import Config
        
        print(f"  Project Root: {Config.PROJECT_ROOT}")
        print(f"  Data Dir: {Config.DATA_DIR}")
        print(f"  Box Dir: {Config.BOX_DIR}")
        print(f"  Key Dir: {Config.KEY_DIR}")
        print(f"  Reports Dir: {Config.REPORTS_DIR}")
        print(f"  LLM Provider: {Config.LLM_PROVIDER}")
        
        Config.ensure_directories()
        print("✓ Configuration validated and directories created")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_data_loader():
    """Test data loading"""
    print("\nTesting data loader...")
    try:
        from genai_reports.config import Config
        from genai_reports.data_loader import DataLoader
        
        loader = DataLoader(Config.DATA_DIR)
        
        count = loader.get_receipt_count()
        print(f"  Found {count} receipt files")
        
        if count == 0:
            print("⚠ No receipt data found (this is OK for initial setup)")
            return True
        
        # Try loading first few
        print("  Loading sample receipts...")
        receipts = loader.load_all_receipts()
        print(f"  Loaded {len(receipts)} valid receipts")
        print("✓ Data loader working")
        return True
    except Exception as e:
        print(f"✗ Data loader error: {e}")
        return False

def test_statistics():
    """Test statistics generation"""
    print("\nTesting statistics generator...")
    try:
        from genai_reports.config import Config
        from genai_reports.data_loader import DataLoader
        from genai_reports.statistics import StatisticsGenerator
        
        loader = DataLoader(Config.DATA_DIR)
        gen = StatisticsGenerator()
        
        receipts = loader.load_all_receipts()
        if not receipts:
            print("⚠ No receipts to analyze (this is OK for initial setup)")
            return True
        
        stats = gen.generate_all_statistics(receipts)
        print(f"  Generated statistics with {len(stats)} sections")
        print("✓ Statistics generator working")
        return True
    except Exception as e:
        print(f"✗ Statistics error: {e}")
        return False

def test_analyzer():
    """Test LLM analyzer"""
    print("\nTesting LLM analyzer...")
    try:
        from genai_reports.llm_analyzer import create_analyzer
        
        # Test with mock analyzer (no API keys needed)
        analyzer = create_analyzer("mock")
        print(f"  Created analyzer: {type(analyzer).__name__}")
        
        test_stats = {
            'total_receipts': 100,
            'financial_stats': {
                'sum': 1000.00,
                'average': 10.00,
                'min': 1.00,
                'max': 50.00,
            },
            'company_stats': {
                'total_unique_companies': 20,
            },
            'data_quality': {
                'field_completion_rates': {
                    'company': 95.0,
                }
            }
        }
        
        analysis = analyzer.analyze_statistics(test_stats)
        print(f"  Generated analysis ({len(analysis)} characters)")
        print("✓ Analyzer working")
        return True
    except Exception as e:
        print(f"✗ Analyzer error: {e}")
        return False

def test_pdf_generator():
    """Test PDF generator"""
    print("\nTesting PDF generator...")
    try:
        from genai_reports.config import Config
        from genai_reports.pdf_generator import PDFReportGenerator
        
        gen = PDFReportGenerator(Config.REPORTS_DIR)
        print("✓ PDF generator initialized")
        return True
    except ImportError:
        print("⚠ reportlab not installed (will be needed for PDF generation)")
        return True
    except Exception as e:
        print(f"✗ PDF generator error: {e}")
        return False

def test_scheduler():
    """Test scheduler"""
    print("\nTesting scheduler...")
    try:
        from genai_reports.scheduler import ReportScheduler
        
        scheduler = ReportScheduler()
        print(f"  Scheduler type: {type(scheduler).__name__}")
        status = scheduler.get_status()
        print(f"  Status: {status.get('message', 'Running' if status.get('running') else 'Stopped')}")
        print("✓ Scheduler initialized")
        return True
    except Exception as e:
        print(f"✗ Scheduler error: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("GenAI Report Generation System - Test Suite")
    print("="*60)
    
    tests = [
        test_imports,
        test_config,
        test_data_loader,
        test_statistics,
        test_analyzer,
        test_pdf_generator,
        test_scheduler,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"✗ Test failed with exception: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} passed")
    print("="*60)
    
    if passed == total:
        print("\n✓ All tests passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Set your LLM provider API key (optional)")
        print("  2. Run: python main.py --demo")
        print("  3. Check generated_reports/ for your PDF reports")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed.")
        print("Please resolve the issues above before using the system.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
