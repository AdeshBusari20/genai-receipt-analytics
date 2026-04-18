"""
Report scheduling module for automated recurring reports
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional
import time

logger = logging.getLogger(__name__)


class ReportScheduler:
    """Schedule automated report generation"""
    
    def __init__(self):
        self.is_running = False
        self.jobs = []
        self._init_scheduler()
    
    def _init_scheduler(self):
        """Initialize scheduler"""
        try:
            from apscheduler.schedulers.background import BackgroundScheduler
            from apscheduler.triggers.cron import CronTrigger
            
            self.BackgroundScheduler = BackgroundScheduler
            self.CronTrigger = CronTrigger
            self.scheduler = BackgroundScheduler()
        except ImportError:
            logger.warning("APScheduler not installed. Using simple scheduler.")
            self.scheduler = None
            self.BackgroundScheduler = None
            self.CronTrigger = None
    
    def schedule_weekly_report(
        self,
        report_func: Callable,
        day_of_week: str = "monday",
        time_str: str = "09:00"
    ) -> bool:
        """
        Schedule a weekly report
        
        Args:
            report_func: Function to call for report generation
            day_of_week: Day name (monday-sunday)
            time_str: Time in HH:MM format
        
        Returns:
            True if scheduled successfully
        """
        try:
            if not self.scheduler:
                logger.error("Scheduler not initialized")
                return False
            
            hour, minute = map(int, time_str.split(':'))
            day_map = {
                'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
                'friday': 4, 'saturday': 5, 'sunday': 6
            }
            day_num = day_map.get(day_of_week.lower(), 0)
            
            self.scheduler.add_job(
                report_func,
                self.CronTrigger(day_of_week=day_num, hour=hour, minute=minute),
                id=f'weekly_report_{datetime.now().timestamp()}',
                name=f'Weekly Report ({day_of_week} at {time_str})',
                replace_existing=False,
            )
            
            logger.info(f"Scheduled weekly report for {day_of_week} at {time_str}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to schedule weekly report: {str(e)}")
            return False
    
    def schedule_monthly_report(
        self,
        report_func: Callable,
        day_of_month: int = 1,
        time_str: str = "09:00"
    ) -> bool:
        """
        Schedule a monthly report
        
        Args:
            report_func: Function to call for report generation
            day_of_month: Day of month (1-31)
            time_str: Time in HH:MM format
        
        Returns:
            True if scheduled successfully
        """
        try:
            if not self.scheduler:
                logger.error("Scheduler not initialized")
                return False
            
            hour, minute = map(int, time_str.split(':'))
            
            self.scheduler.add_job(
                report_func,
                self.CronTrigger(day=day_of_month, hour=hour, minute=minute),
                id=f'monthly_report_{datetime.now().timestamp()}',
                name=f'Monthly Report (Day {day_of_month} at {time_str})',
                replace_existing=False,
            )
            
            logger.info(f"Scheduled monthly report for day {day_of_month} at {time_str}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to schedule monthly report: {str(e)}")
            return False
    
    def schedule_custom(
        self,
        report_func: Callable,
        cron_expression: str,
        name: str = "Custom Report"
    ) -> bool:
        """
        Schedule using a custom cron expression
        
        Args:
            report_func: Function to call
            cron_expression: Cron expression (field1 field2 field3 field4 field5)
            name: Job name
        
        Returns:
            True if scheduled successfully
        """
        try:
            if not self.scheduler:
                logger.error("Scheduler not initialized")
                return False
            
            parts = cron_expression.split()
            if len(parts) != 5:
                raise ValueError("Cron expression must have 5 fields")
            
            self.scheduler.add_job(
                report_func,
                self.CronTrigger(
                    minute=parts[0],
                    hour=parts[1],
                    day=parts[2],
                    month=parts[3],
                    day_of_week=parts[4],
                ),
                id=f'custom_report_{datetime.now().timestamp()}',
                name=name,
                replace_existing=False,
            )
            
            logger.info(f"Scheduled custom report: {name}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to schedule custom report: {str(e)}")
            return False
    
    def start(self) -> bool:
        """Start the scheduler"""
        try:
            if not self.scheduler:
                logger.error("Scheduler not initialized. Cannot start.")
                return False
            
            if self.is_running:
                logger.warning("Scheduler is already running")
                return True
            
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler started")
            return True
        
        except Exception as e:
            logger.error(f"Failed to start scheduler: {str(e)}")
            return False
    
    def stop(self) -> bool:
        """Stop the scheduler"""
        try:
            if not self.scheduler or not self.is_running:
                return False
            
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped")
            return True
        
        except Exception as e:
            logger.error(f"Failed to stop scheduler: {str(e)}")
            return False
    
    def list_jobs(self) -> list:
        """List all scheduled jobs"""
        if not self.scheduler:
            return []
        
        return [
            {
                'id': job.id,
                'name': job.name,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else 'None',
            }
            for job in self.scheduler.get_jobs()
        ]
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {
            'running': self.is_running,
            'jobs_count': len(self.list_jobs()),
            'jobs': self.list_jobs(),
        }


class SimpleScheduler:
    """Simple scheduler for testing without APScheduler"""
    
    def __init__(self):
        self.is_running = False
        self.jobs = []
    
    def schedule_weekly_report(
        self,
        report_func: Callable,
        day_of_week: str = "monday",
        time_str: str = "09:00"
    ) -> bool:
        """Schedule a weekly report (simple version)"""
        logger.info(f"Scheduled weekly report for {day_of_week} at {time_str} (manual scheduling required)")
        return True
    
    def schedule_monthly_report(
        self,
        report_func: Callable,
        day_of_month: int = 1,
        time_str: str = "09:00"
    ) -> bool:
        """Schedule a monthly report (simple version)"""
        logger.info(f"Scheduled monthly report for day {day_of_month} at {time_str} (manual scheduling required)")
        return True
    
    def start(self) -> bool:
        """Start scheduler"""
        logger.info("Simple scheduler does not auto-run. Call report functions manually.")
        return True
    
    def stop(self) -> bool:
        """Stop scheduler"""
        return True
    
    def get_status(self) -> dict:
        """Get scheduler status"""
        return {'running': False, 'message': 'Simple scheduler - manual invocation required'}
