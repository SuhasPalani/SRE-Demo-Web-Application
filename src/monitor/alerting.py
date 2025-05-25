#!/usr/bin/env python3
"""
Alert management for SRE monitoring
"""

import smtplib
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

logger = logging.getLogger(__name__)

class AlertManager:
    def __init__(self):
        self.alert_history = []
        
    def send_alert(self, message, severity="info"):
        """Send alert via multiple channels"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'severity': severity
        }
        
        self.alert_history.append(alert)
        
        # Log the alert
        log_level = {
            'critical': logging.CRITICAL,
            'error': logging.ERROR,
            'warning': logging.WARNING,
            'info': logging.INFO
        }.get(severity, logging.INFO)
        
        logger.log(log_level, f"ALERT [{severity.upper()}]: {message}")
        
        # In a real environment, you would integrate with:
        # - Slack/Teams webhooks
        # - PagerDuty
        # - Email notifications
        # - SMS alerts
        
        self.log_to_file(alert)
        
    def log_to_file(self, alert):
        """Log alert to file for persistence"""
        try:
            with open('/app/logs/alerts.log', 'a') as f:
                f.write(json.dumps(alert) + '\n')
        except Exception as e:
            logger.error(f"Failed to log alert: {str(e)}")
    
    def get_recent_alerts(self, hours=24):
        """Get recent alerts for dashboard"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        return [
            alert for alert in self.alert_history
            if datetime.fromisoformat(alert['timestamp']).timestamp() > cutoff
        ]