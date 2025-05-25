#!/usr/bin/env python3
"""
Health monitoring service for SRE demo
"""

import requests
import time
import logging
import json
import yaml
import os
import schedule
from datetime import datetime
from alerting import AlertManager
from metrics_collector import MetricsCollector
import docker

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HealthChecker:
    def __init__(self, config_path='/app/config/monitor_config.yml'):
        self.config = self.load_config(config_path)
        self.alert_manager = AlertManager()
        self.metrics_collector = MetricsCollector()
        self.docker_client = docker.from_env()
        self.consecutive_failures = 0
        
    def load_config(self, config_path):
        """Load monitoring configuration"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return self.get_default_config()
    
    def get_default_config(self):
        """Default configuration"""
        return {
            'targets': [
                {
                    'name': 'webapp',
                    'url': 'http://webapp:5000/health',
                    'timeout': 5,
                    'expected_status': 200
                }
            ],
            'thresholds': {
                'consecutive_failures': 3,
                'response_time_ms': 5000
            },
            'remediation': {
                'enabled': True,
                'restart_service': True
            }
        }
    
    def check_service_health(self, target):
        """Check health of a single service"""
        try:
            start_time = time.time()
            response = requests.get(
                target['url'], 
                timeout=target['timeout']
            )
            response_time = (time.time() - start_time) * 1000
            
            # Collect metrics
            self.metrics_collector.record_response_time(
                target['name'], response_time
            )
            
            if response.status_code == target['expected_status']:
                logger.info(f"✅ {target['name']} is healthy (Response time: {response_time:.2f}ms)")
                self.consecutive_failures = 0
                return True, response_time, response.json()
            else:
                logger.warning(f"❌ {target['name']} returned status {response.status_code}")
                return False, response_time, None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Failed to check {target['name']}: {str(e)}")
            return False, None, None
    
    def restart_service(self, service_name):
        """Restart a Docker service"""
        try:
            container = self.docker_client.containers.get(f"sre-demo_{service_name}_1")
            logger.info(f"Restarting container: {container.name}")
            container.restart()
            return True
        except docker.errors.NotFound:
            logger.error(f"Container not found: sre-demo_{service_name}_1")
            return False
        except Exception as e:
            logger.error(f"Failed to restart service {service_name}: {str(e)}")
            return False
    
    def perform_remediation(self, target):
        """Perform automated remediation"""
        if not self.config.get('remediation', {}).get('enabled', False):
            logger.info("Remediation is disabled")
            return
        
        if self.consecutive_failures >= self.config['thresholds']['consecutive_failures']:
            logger.warning(f"Performing remediation for {target['name']}")
            
            # Try to restart the service
            if self.config.get('remediation', {}).get('restart_service', False):
                if self.restart_service(target['name']):
                    self.alert_manager.send_alert(
                        f"Service {target['name']} restarted automatically",
                        "remediation"
                    )
                    self.consecutive_failures = 0
    
    def run_health_checks(self):
        """Run health checks for all targets"""
        logger.info("Running health checks...")
        
        all_healthy = True
        for target in self.config['targets']:
            is_healthy, response_time, data = self.check_service_health(target)
            
            if not is_healthy:
                all_healthy = False
                self.consecutive_failures += 1
                
                # Send alert if threshold reached
                if self.consecutive_failures >= self.config['thresholds']['consecutive_failures']:
                    self.alert_manager.send_alert(
                        f"Service {target['name']} has failed {self.consecutive_failures} consecutive times",
                        "critical"
                    )
                    
                    # Attempt remediation
                    self.perform_remediation(target)
            
            # Check response time threshold
            if response_time and response_time > self.config['thresholds']['response_time_ms']:
                self.alert_manager.send_alert(
                    f"Service {target['name']} response time is high: {response_time:.2f}ms",
                    "warning"
                )
        
        return all_healthy
    
    def start_monitoring(self):
        """Start the monitoring loop"""
        logger.info("Starting health monitoring service...")
        
        # Schedule regular health checks
        interval = int(os.getenv('CHECK_INTERVAL', 30))
        schedule.every(interval).seconds.do(self.run_health_checks)
        
        # Run metrics collection
        schedule.every(60).seconds.do(self.metrics_collector.collect_system_metrics)
        
        # Initial check
        self.run_health_checks()
        
        # Keep running
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    monitor = HealthChecker()
    monitor.start_monitoring()