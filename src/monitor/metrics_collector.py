#!/usr/bin/env python3
"""
Metrics collection for monitoring
"""

import psutil
import time
import logging
from collections import defaultdict, deque
from datetime import datetime

logger = logging.getLogger(__name__)

class MetricsCollector:
    def __init__(self):
        self.response_times = defaultdict(lambda: deque(maxlen=100))
        self.system_metrics = deque(maxlen=100)
        
    def record_response_time(self, service, response_time_ms):
        """Record response time for a service"""
        self.response_times[service].append({
            'timestamp': datetime.now().isoformat(),
            'response_time': response_time_ms
        })
        
    def collect_system_metrics(self):
        """Collect system-level metrics"""
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent,
                'load_average': psutil.getloadavg()[0] if hasattr(psutil, 'getloadavg') else 0
            }
            
            self.system_metrics.append(metrics)
            logger.info(f"System metrics: CPU: {metrics['cpu_percent']}%, "
                       f"Memory: {metrics['memory_percent']}%, "
                       f"Disk: {metrics['disk_percent']}%")
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {str(e)}")
    
    def get_average_response_time(self, service, minutes=5):
        """Get average response time for a service"""
        if service not in self.response_times:
            return None
            
        cutoff = time.time() - (minutes * 60)
        recent_times = [
            rt['response_time'] for rt in self.response_times[service]
            if datetime.fromisoformat(rt['timestamp']).timestamp() > cutoff
        ]
        
        return sum(recent_times) / len(recent_times) if recent_times else None