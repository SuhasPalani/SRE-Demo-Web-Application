#!/usr/bin/env python3
"""
Tests for monitoring components
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from monitor.health_checker import HealthChecker
from monitor.alerting import AlertManager

class TestHealthChecker(unittest.TestCase):
    def setUp(self):
        self.health_checker = HealthChecker()
        
    def test_default_config_loading(self):
        """Test that default config loads properly"""
        config = self.health_checker.get_default_config()
        self.assertIn('targets', config)
        self.assertIn('thresholds', config)
        
    @patch('requests.get')
    def test_health_check_success(self, mock_get):
        """Test successful health check"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'healthy'}
        mock_get.return_value = mock_response
        
        target = {'name': 'test', 'url': 'http://test:5000/health', 'timeout': 5, 'expected_status': 200}
        is_healthy, response_time, data = self.health_checker.check_service_health(target)
        
        self.assertTrue(is_healthy)
        self.assertIsNotNone(response_time)

class TestAlertManager(unittest.TestCase):
    def setUp(self):
        self.alert_manager = AlertManager()
        
    def test_send_alert(self):
        """Test alert sending"""
        self.alert_manager.send_alert("Test alert", "warning")
        self.assertEqual(len(self.alert_manager.alert_history), 1)
        self.assertEqual(self.alert_manager.alert_history[0]['severity'], 'warning')

if __name__ == '__main__':
    unittest.main()