"""
Development Start Script for Vietnamese Legal AI Chatbot
Script Khởi động Phát triển cho Chatbot AI Pháp lý Việt Nam

Quick development environment setup and service startup.
Thiết lập nhanh môi trường phát triển và khởi động dịch vụ.
"""

import os
import sys
import subprocess
import time
import logging
import webbrowser
from pathlib import Path
from typing import List, Dict, Any
import threading
import signal

def setup_logging():
    """Setup logging for development script"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

class DevelopmentServer:
    """Development server manager for Vietnamese Legal AI Chatbot"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.processes = {}
        self.running = True
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info("Received shutdown signal. Stopping services...")
        self.stop_all_services()
        sys.exit(0)
    
    def check_environment(self) -> bool:
        """Check if development environment is properly configured"""
        self.logger.info("Checking development environment...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 8):
            self.logger.error("Python 3.8+ is required")
            return False
        
        # Check virtual environment
        if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            self.logger.warning("Not running in virtual environment")
        
        # Check required environment variables
        required_vars = [
            'OPENAI_API_KEY',
            'PINECONE_API_KEY',
            'PINECONE_ENVIRONMENT',
            'PINECONE_INDEX_NAME'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            self.logger.error(f"Missing environment variables: {missing_vars}")
            self.logger.info("Please check your .env file or set these variables")
            return False
        
        # Check if requirements are installed
        try:
            import fastapi
            import streamlit
            import pinecone
            import langchain
            self.logger.info("✅ All required packages are installed")
        except ImportError as e:
            self.logger.error(f"Missing required package: {e}")
            self.logger.info("Run: pip install -r requirements.txt")
            return False
        
        self.logger.info("✅ Development environment check passed")
        return True
    
    def install_dependencies(self) -> bool:
        """Install project dependencies"""
        self.logger.info("Installing dependencies...")
        
        try:
            # Upgrade pip
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], 
                         check=True, capture_output=True)
            
            # Install requirements
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                         check=True, capture_output=True)
            
            self.logger.info("✅ Dependencies installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install dependencies: {e}")
            return False
    
    def setup_directories(self):
        """Create necessary directories for development"""
        directories = [
            'logs',
            'data/documents',
            'data/processed',
            'data/temp',
            'uploads'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        self.logger.info("✅ Development directories created")
    
    def start_fastapi_server(self) -> bool:
        """Start FastAPI backend server"""
        self.logger.info("Starting FastAPI backend server...")
        
        try:
            # Change to app directory
            app_dir = Path(__file__).parent.parent / "app"
            
            # Start FastAPI with uvicorn
            cmd = [
                sys.executable, '-m', 'uvicorn',
                'main:app',
                '--host', '0.0.0.0',
                '--port', '8000',
                '--reload',
                '--reload-dir', str(app_dir),
                '--log-level', 'info'
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.processes['fastapi'] = process
            
            # Monitor process output in background
            threading.Thread(
                target=self._monitor_process_output,
                args=(process, 'FastAPI'),
                daemon=True
            ).start()
            
            # Wait for server to start
            time.sleep(3)
            
            if process.poll() is None:
                self.logger.info("✅ FastAPI server started on http://localhost:8000")
                return True
            else:
                self.logger.error("❌ Failed to start FastAPI server")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to start FastAPI server: {e}")
            return False
    
    def start_streamlit_app(self) -> bool:
        """Start Streamlit frontend application"""
        self.logger.info("Starting Streamlit frontend application...")
        
        try:
            # Change to app directory
            app_dir = Path(__file__).parent.parent / "app"
            
            # Start Streamlit
            cmd = [
                sys.executable, '-m', 'streamlit',
                'run', 'streamlit_app.py',
                '--server.port', '8501',
                '--server.address', '0.0.0.0',
                '--server.headless', 'false',
                '--browser.gatherUsageStats', 'false'
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=app_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            self.processes['streamlit'] = process
            
            # Monitor process output in background
            threading.Thread(
                target=self._monitor_process_output,
                args=(process, 'Streamlit'),
                daemon=True
            ).start()
            
            # Wait for server to start
            time.sleep(5)
            
            if process.poll() is None:
                self.logger.info("✅ Streamlit app started on http://localhost:8501")
                return True
            else:
                self.logger.error("❌ Failed to start Streamlit app")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to start Streamlit app: {e}")
            return False
    
    def _monitor_process_output(self, process, service_name):
        """Monitor process output and log it"""
        try:
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    self.logger.info(f"[{service_name}] {line.strip()}")
        except Exception as e:
            self.logger.error(f"Error monitoring {service_name}: {e}")
    
    def check_services_health(self) -> Dict[str, bool]:
        """Check health of running services"""
        health_status = {}
        
        # Check FastAPI
        try:
            import requests
            response = requests.get('http://localhost:8000/health', timeout=5)
            health_status['fastapi'] = response.status_code == 200
        except:
            health_status['fastapi'] = False
        
        # Check Streamlit (simple check if process is running)
        health_status['streamlit'] = (
            'streamlit' in self.processes and 
            self.processes['streamlit'].poll() is None
        )
        
        return health_status
    
    def open_browser_tabs(self):
        """Open browser tabs for development"""
        time.sleep(2)  # Wait for services to fully start
        
        urls = [
            'http://localhost:8501',  # Streamlit app
            'http://localhost:8000/docs',  # FastAPI docs
        ]
        
        for url in urls:
            try:
                webbrowser.open(url)
                time.sleep(1)
            except Exception as e:
                self.logger.warning(f"Could not open {url}: {e}")
    
    def stop_all_services(self):
        """Stop all running services"""
        self.logger.info("Stopping all services...")
        
        for service_name, process in self.processes.items():
            try:
                if process.poll() is None:
                    self.logger.info(f"Stopping {service_name}...")
                    process.terminate()
                    
                    # Wait for graceful shutdown
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        self.logger.warning(f"Force killing {service_name}")
                        process.kill()
                        
            except Exception as e:
                self.logger.error(f"Error stopping {service_name}: {e}")
        
        self.processes.clear()
        self.logger.info("✅ All services stopped")
    
    def start_development_environment(self, open_browser: bool = True):
        """Start complete development environment"""
        print("🚀 Vietnamese Legal AI Chatbot - Development Environment")
        print("=" * 60)
        
        # Check environment
        if not self.check_environment():
            self.logger.error("❌ Environment check failed")
            return False
        
        # Setup directories
        self.setup_directories()
        
        # Start FastAPI server
        if not self.start_fastapi_server():
            self.logger.error("❌ Failed to start FastAPI server")
            return False
        
        # Start Streamlit app
        if not self.start_streamlit_app():
            self.logger.error("❌ Failed to start Streamlit app")
            self.stop_all_services()
            return False
        
        # Open browser tabs
        if open_browser:
            self.open_browser_tabs()
        
        print("\n🎉 Development environment started successfully!")
        print("\n📋 Service URLs:")
        print("   • Streamlit App: http://localhost:8501")
        print("   • FastAPI Backend: http://localhost:8000")
        print("   • API Documentation: http://localhost:8000/docs")
        print("   • API Redoc: http://localhost:8000/redoc")
        print("\n💡 Tips:")
        print("   • Both services auto-reload on code changes")
        print("   • Check logs in the logs/ directory")
        print("   • Press Ctrl+C to stop all services")
        
        return True
    
    def monitor_services(self):
        """Monitor running services and restart if needed"""
        while self.running:
            try:
                time.sleep(30)  # Check every 30 seconds
                
                health = self.check_services_health()
                for service, is_healthy in health.items():
                    if not is_healthy and service in self.processes:
                        self.logger.warning(f"Service {service} is unhealthy, restarting...")
                        # TODO: Implement service restart logic
                        
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"Error monitoring services: {e}")

def main():
    """Main function for development script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Start Vietnamese Legal AI Chatbot development environment')
    parser.add_argument('--no-browser', action='store_true', help='Do not open browser tabs')
    parser.add_argument('--install-deps', action='store_true', help='Install dependencies before starting')
    parser.add_argument('--monitor', action='store_true', help='Monitor and restart services if needed')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    # Initialize development server
    dev_server = DevelopmentServer()
    
    try:
        # Install dependencies if requested
        if args.install_deps:
            if not dev_server.install_dependencies():
                sys.exit(1)
        
        # Start development environment
        if dev_server.start_development_environment(open_browser=not args.no_browser):
            # Monitor services if requested
            if args.monitor:
                dev_server.monitor_services()
            else:
                # Wait for keyboard interrupt
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass
        else:
            sys.exit(1)
            
    finally:
        dev_server.stop_all_services()

if __name__ == "__main__":
    main()
