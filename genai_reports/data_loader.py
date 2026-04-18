"""
Data loader module for reading receipt data
"""

import json
import csv
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DataLoader:
    """Load and parse receipt data from CSV and JSON files"""
    
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.box_dir = data_dir / "box"
        self.key_dir = data_dir / "key"
    
    def load_all_receipts(self) -> List[Dict[str, Any]]:
        """Load all receipt data (boxes and key information)"""
        receipts = []
        
        key_files = sorted(self.key_dir.glob("*.json"))
        logger.info(f"Found {len(key_files)} receipt files")
        
        for key_file in key_files:
            receipt_id = key_file.stem
            receipt_data = self._load_receipt(receipt_id)
            if receipt_data:
                receipts.append(receipt_data)
        
        return receipts
    
    def _load_receipt(self, receipt_id: str) -> Optional[Dict[str, Any]]:
        """Load a single receipt's data"""
        try:
            key_file = self.key_dir / f"{receipt_id}.json"
            box_file = self.box_dir / f"{receipt_id}.csv"
            
            # Load key information
            with open(key_file, 'r', encoding='utf-8') as f:
                key_data = json.load(f)
            
            # Load bounding box data
            boxes = []
            if box_file.exists():
                with open(box_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    boxes = list(reader) if reader else []
            
            return {
                'id': receipt_id,
                'key_info': key_data,
                'boxes': boxes,
                'num_boxes': len(boxes)
            }
        except Exception as e:
            logger.warning(f"Failed to load receipt {receipt_id}: {str(e)}")
            return None
    
    def load_key_information(self) -> List[Dict[str, Any]]:
        """Load only key information from all receipts"""
        key_data = []
        
        for key_file in sorted(self.key_dir.glob("*.json")):
            try:
                with open(key_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    data['id'] = key_file.stem
                    key_data.append(data)
            except Exception as e:
                logger.warning(f"Failed to load {key_file}: {str(e)}")
        
        return key_data
    
    def get_receipt_count(self) -> int:
        """Get total number of receipts"""
        return len(list(self.key_dir.glob("*.json")))
    
    def extract_financial_data(self, receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract financial metrics from receipts"""
        totals = []
        companies = {}
        dates = []
        
        for receipt in receipts:
            key_info = receipt.get('key_info', {})
            
            # Extract total
            try:
                total = float(key_info.get('total', 0))
                totals.append(total)
            except (ValueError, TypeError):
                pass
            
            # Extract company
            company = key_info.get('company', 'Unknown')
            companies[company] = companies.get(company, 0) + 1
            
            # Extract date
            if key_info.get('date'):
                dates.append(key_info.get('date'))
        
        return {
            'totals': totals,
            'companies': companies,
            'dates': dates,
            'total_count': len(receipts),
            'unique_companies': len(companies),
        }
