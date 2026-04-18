"""
PDF Report Generator module
"""

import io
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import base64

logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """Generate PDF reports from statistics and LLM analysis"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.reportlab_available = False
        self._init_pdf_library()
    
    def _init_pdf_library(self):
        """Initialize PDF library"""
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter, A4
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
            
            self.colors = colors
            self.letter = letter
            self.A4 = A4
            self.SimpleDocTemplate = SimpleDocTemplate
            self.Table = Table
            self.TableStyle = TableStyle
            self.Paragraph = Paragraph
            self.Spacer = Spacer
            self.PageBreak = PageBreak
            self.getSampleStyleSheet = getSampleStyleSheet
            self.ParagraphStyle = ParagraphStyle
            self.inch = inch
            self.TA_CENTER = TA_CENTER
            self.TA_LEFT = TA_LEFT
            self.TA_RIGHT = TA_RIGHT
            self.TA_JUSTIFY = TA_JUSTIFY
            self.reportlab_available = True
            logger.info("reportlab library loaded successfully")
        except ImportError as e:
            self.reportlab_available = False
            logger.warning(f"reportlab not available: {e}. PDF reports will not be generated.")
            logger.info("Install with: pip install reportlab")
    
    def generate_report(
        self,
        title: str,
        statistics: Dict[str, Any],
        analysis: str,
        report_type: str = "summary"
    ) -> Path:
        """Generate a complete PDF report"""
        
        if not self.reportlab_available:
            logger.error("reportlab not available. Cannot generate PDF.")
            logger.info("Install with: pip install reportlab")
            raise ImportError("reportlab library is required for PDF generation. Install with: pip install reportlab")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.output_dir / f"{report_type}_report_{timestamp}.pdf"
        
        try:
            doc = self.SimpleDocTemplate(
                str(filename),
                pagesize=self.letter,
                rightMargin=0.75*self.inch,
                leftMargin=0.75*self.inch,
                topMargin=0.75*self.inch,
                bottomMargin=0.75*self.inch,
            )
            
            # Build story (content)
            story = []
            styles = self.getSampleStyleSheet()
            
            # Title
            title_style = self.ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=self.colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=self.TA_CENTER,
            )
            story.append(self.Paragraph(title, title_style))
            story.append(self.Spacer(1, 0.2*self.inch))
            
            # Metadata
            date_style = self.ParagraphStyle(
                'DateStyle',
                parent=styles['Normal'],
                fontSize=10,
                textColor=self.colors.grey,
                alignment=self.TA_CENTER,
            )
            story.append(self.Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                date_style
            ))
            story.append(self.Spacer(1, 0.3*self.inch))
            
            # Executive Summary Section
            story.append(self.Paragraph("Executive Summary", styles['Heading2']))
            story.append(self.Spacer(1, 0.1*self.inch))
            
            summary = self._create_executive_summary(statistics)
            story.append(self.Paragraph(summary, styles['Normal']))
            story.append(self.Spacer(1, 0.2*self.inch))
            
            # Statistics Tables
            story.append(self.PageBreak())
            story.append(self.Paragraph("Detailed Statistics", styles['Heading2']))
            story.append(self.Spacer(1, 0.1*self.inch))
            
            # Financial Statistics Table
            story.append(self.Paragraph("Financial Summary", styles['Heading3']))
            financial_table = self._create_financial_table(statistics)
            story.append(financial_table)
            story.append(self.Spacer(1, 0.2*self.inch))
            
            # Company Statistics Table
            story.append(self.Paragraph("Company & Merchant Data", styles['Heading3']))
            company_table = self._create_company_table(statistics)
            story.append(company_table)
            story.append(self.Spacer(1, 0.2*self.inch))
            
            # Data Quality Table
            story.append(self.Paragraph("Data Quality Assessment", styles['Heading3']))
            quality_table = self._create_quality_table(statistics)
            story.append(quality_table)
            story.append(self.Spacer(1, 0.3*self.inch))
            
            # AI Analysis Section
            story.append(self.PageBreak())
            story.append(self.Paragraph("AI-Powered Analysis & Insights", styles['Heading2']))
            story.append(self.Spacer(1, 0.1*self.inch))
            
            analysis_style = self.ParagraphStyle(
                'Analysis',
                parent=styles['Normal'],
                fontSize=10,
                leading=14,
            )
            
            # Format analysis text
            analysis_text = analysis.replace('\n', '<br/>')
            story.append(self.Paragraph(analysis_text, analysis_style))
            
            # Footer
            story.append(self.Spacer(1, 0.3*self.inch))
            footer_style = self.ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=8,
                textColor=self.colors.grey,
                alignment=self.TA_CENTER,
            )
            story.append(self.Paragraph(
                "This report was automatically generated by the GenAI Receipt Analytics System",
                footer_style
            ))
            
            # Build PDF
            doc.build(story)
            logger.info(f"PDF report generated: {filename}")
            return filename
        
        except Exception as e:
            logger.error(f"Error generating PDF: {str(e)}")
            raise
    
    def _create_executive_summary(self, statistics: Dict[str, Any]) -> str:
        """Create executive summary text"""
        financial = statistics.get('financial_stats', {})
        company = statistics.get('company_stats', {})
        quality = statistics.get('data_quality', {})
        
        summary = f"""
        <b>Dataset Overview:</b> This report analyzes {statistics.get('total_receipts', 0)} receipt transactions.<br/><br/>
        
        <b>Financial Performance:</b> Total transaction value of ${financial.get('sum', 0):,.2f} with an average per-receipt amount of ${financial.get('average', 0):,.2f}. Transaction values range from ${financial.get('min', 0):,.2f} to ${financial.get('max', 0):,.2f}.<br/><br/>
        
        <b>Business Activity:</b> Data covers {company.get('total_unique_companies', 0)} unique companies and {company.get('total_unique_addresses', 0)} unique locations, indicating {'diversified' if company.get('total_unique_companies', 0) > 20 else 'concentrated'} business operations.<br/><br/>
        
        <b>Data Quality:</b> {quality.get('fully_complete_records', 0)} records are fully complete with all required fields. Overall data completeness is strong across all fields.
        """
        return summary
    
    def _create_financial_table(self, statistics: Dict[str, Any]) -> 'Table':
        """Create financial statistics table"""
        financial = statistics.get('financial_stats', {})
        
        data = [
            ['Metric', 'Value'],
            ['Total Receipts', str(financial.get('count', 0))],
            ['Total Amount', f"${financial.get('sum', 0):,.2f}"],
            ['Average Per Receipt', f"${financial.get('average', 0):,.2f}"],
            ['Median', f"${financial.get('median', 0):,.2f}"],
            ['Minimum', f"${financial.get('min', 0):,.2f}"],
            ['Maximum', f"${financial.get('max', 0):,.2f}"],
            ['Standard Deviation', f"${financial.get('std_dev', 0):,.2f}"],
        ]
        
        table = self.Table(data, colWidths=[3*self.inch, 2*self.inch])
        table.setStyle(self.TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), self.colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, self.colors.black),
        ]))
        return table
    
    def _create_company_table(self, statistics: Dict[str, Any]) -> 'Table':
        """Create company statistics table"""
        company = statistics.get('company_stats', {})
        top_companies = company.get('top_companies', [])
        
        data = [
            ['Rank', 'Company', 'Count'],
        ]
        
        for idx, comp in enumerate(top_companies[:10], 1):
            name = comp.get('name', 'Unknown')[:40]  # Truncate long names
            count = comp.get('count', 0)
            data.append([str(idx), name, str(count)])
        
        if not top_companies:
            data.append(['—', 'No company data available', '—'])
        
        table = self.Table(data, colWidths=[0.8*self.inch, 3.7*self.inch, 0.8*self.inch])
        table.setStyle(self.TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), self.colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, self.colors.black),
        ]))
        return table
    
    def _create_quality_table(self, statistics: Dict[str, Any]) -> 'Table':
        """Create data quality table"""
        quality = statistics.get('data_quality', {})
        completion_rates = quality.get('field_completion_rates', {})
        
        data = [
            ['Field', 'Completion Rate'],
            ['Company', f"{completion_rates.get('company', 0):.1f}%"],
            ['Address', f"{completion_rates.get('address', 0):.1f}%"],
            ['Date', f"{completion_rates.get('date', 0):.1f}%"],
            ['Total', f"{completion_rates.get('total', 0):.1f}%"],
        ]
        
        table = self.Table(data, colWidths=[2.5*self.inch, 2.5*self.inch])
        table.setStyle(self.TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), self.colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), self.colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, self.colors.black),
        ]))
        return table
