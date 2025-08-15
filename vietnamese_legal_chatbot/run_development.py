#!/usr/bin/env python3
"""
Development Runner for Vietnamese Legal AI Chatbot
Script chạy phát triển cho Chatbot AI Pháp lý Việt Nam

This script starts both Streamlit frontend and FastAPI backend for development.
Script này khởi động cả frontend Streamlit và backend FastAPI cho phát triển.
"""

import os
import sys
import time
import signal
import subprocess
import threading
from pathlib import Path
import logging
from typing import List, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/development.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class VietnameseLegalChatbotRunner:
    """Main runner for the Vietnamese Legal AI Chatbot development environment"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.app_dir = self.project_root / "app"
        self.processes: List[subprocess.Popen] = []
        self.running = False
        
        # Ensure directories exist
        (self.project_root / "logs").mkdir(exist_ok=True)
        (self.project_root / "data" / "uploads").mkdir(parents=True, exist_ok=True)
        
    def check_dependencies(self) -> bool:
        """Check if all required dependencies are installed"""
        logger.info("🔍 Checking dependencies...")
        
        required_packages = [
            'streamlit', 'fastapi', 'uvicorn', 'openai', 
            'pinecone-client', 'langchain', 'underthesea'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"✅ {package} - OK")
            except ImportError:
                missing_packages.append(package)
                logger.warning(f"❌ {package} - Missing")
        
        if missing_packages:
            logger.error(f"Missing packages: {', '.join(missing_packages)}")
            logger.info("Run: pip install -r requirements.txt")
            return False
        
        logger.info("✅ All dependencies satisfied!")
        return True
    
    def check_environment(self) -> bool:
        """Check environment variables"""
        logger.info("🔍 Checking environment variables...")
        
        required_env_vars = [
            'OPENAI_API_KEY',
            'PINECONE_API_KEY', 
            'PINECONE_ENVIRONMENT',
            'PINECONE_INDEX_NAME'
        ]
        
        missing_vars = []
        
        for var in required_env_vars:
            if not os.getenv(var):
                missing_vars.append(var)
                logger.warning(f"❌ {var} - Not set")
            else:
                logger.info(f"✅ {var} - OK")
        
        if missing_vars:
            logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
            logger.info("Create .env file with required variables")
            return False
        
        logger.info("✅ Environment variables configured!")
        return True
    
    def start_backend(self) -> Optional[subprocess.Popen]:
        """Start FastAPI backend server"""
        logger.info("🚀 Starting FastAPI backend...")
        
        try:
            cmd = [
                sys.executable, "-m", "uvicorn",
                "app.main:app",
                "--host", "0.0.0.0",
                "--port", "8000",
                "--reload",
                "--log-level", "info",
                "--access-log"
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Start output monitoring thread
            threading.Thread(
                target=self._monitor_process_output,
                args=(process, "FastAPI"),
                daemon=True
            ).start()
            
            logger.info("✅ FastAPI backend started on http://localhost:8000")
            return process
            
        except Exception as e:
            logger.error(f"❌ Failed to start FastAPI backend: {e}")
            return None
    
    def start_frontend(self) -> Optional[subprocess.Popen]:
        """Start Streamlit frontend"""
        logger.info("🚀 Starting Streamlit frontend...")
        
        try:
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                "app/streamlit_app.py",
                "--server.port", "8501",
                "--server.address", "0.0.0.0",
                "--server.headless", "false",
                "--browser.gatherUsageStats", "false",
                "--theme.base", "light",
                "--theme.primaryColor", "#004B87",  # Vietnamese government blue
                "--theme.backgroundColor", "#FFFEF7",  # Vietnamese peace white
                "--theme.secondaryBackgroundColor", "#F8FAFC"
            ]
            
            process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Start output monitoring thread
            threading.Thread(
                target=self._monitor_process_output,
                args=(process, "Streamlit"),
                daemon=True
            ).start()
            
            logger.info("✅ Streamlit frontend started on http://localhost:8501")
            return process
            
        except Exception as e:
            logger.error(f"❌ Failed to start Streamlit frontend: {e}")
            return None
    
    def _monitor_process_output(self, process: subprocess.Popen, service_name: str):
        """Monitor process output and log it"""
        try:
            for line in iter(process.stdout.readline, ''):
                if line.strip():
                    logger.info(f"[{service_name}] {line.strip()}")
        except Exception as e:
            logger.error(f"Error monitoring {service_name}: {e}")
    
    def wait_for_services(self, timeout: int = 60) -> bool:
        """Wait for services to be ready"""
        logger.info("⏳ Waiting for services to be ready...")
        
        import requests
        from time import sleep
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Check FastAPI backend
                backend_response = requests.get("http://localhost:8000/health", timeout=5)
                if backend_response.status_code == 200:
                    logger.info("✅ FastAPI backend is ready")
                    
                    # Check Streamlit frontend
                    try:
                        frontend_response = requests.get("http://localhost:8501/_stcore/health", timeout=5)
                        if frontend_response.status_code == 200:
                            logger.info("✅ Streamlit frontend is ready")
                            return True
                    except requests.RequestException:
                        pass
                        
            except requests.RequestException:
                pass
            
            sleep(2)
        
        logger.error(f"❌ Services not ready after {timeout} seconds")
        return False
    
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def start(self):
        """Start the complete development environment"""
        logger.info("🏛️ Vietnamese Legal AI Chatbot - Development Environment")
        logger.info("🇻🇳 Hệ thống Tư vấn Pháp lý AI - Môi trường Phát triển")
        logger.info("=" * 60)
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Check prerequisites
        if not self.check_dependencies():
            sys.exit(1)
        
        if not self.check_environment():
            sys.exit(1)
        
        # Start services
        backend_process = self.start_backend()
        if not backend_process:
            logger.error("❌ Failed to start backend")
            sys.exit(1)
        
        self.processes.append(backend_process)
        
        # Wait a moment for backend to initialize
        time.sleep(3)
        
        frontend_process = self.start_frontend()
        if not frontend_process:
            logger.error("❌ Failed to start frontend")
            self.stop()
            sys.exit(1)
        
        self.processes.append(frontend_process)
        
        # Wait for services to be ready
        if not self.wait_for_services():
            logger.error("❌ Services failed to start properly")
            self.stop()
            sys.exit(1)
        
        self.running = True
        
        # Display startup information
        self.display_startup_info()
        
        # Keep the main thread alive and monitor processes
        try:
            while self.running:
                # Check if processes are still running
                for process in self.processes:
                    if process.poll() is not None:
                        logger.error(f"Process {process.pid} has died")
                        self.stop()
                        sys.exit(1)
                
                time.sleep(5)
                
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            self.stop()
    
    def display_startup_info(self):
        """Display startup information"""
        logger.info("🎉 Vietnamese Legal AI Chatbot is running!")
        logger.info("🇻🇳 Chatbot AI Pháp lý Việt Nam đã sẵn sàng!")
        logger.info("=" * 60)
        logger.info("📊 FastAPI Backend:  http://localhost:8000")
        logger.info("📊 API Documentation: http://localhost:8000/docs")
        logger.info("🖥️  Streamlit Frontend: http://localhost:8501")
        logger.info("📋 Health Check:     http://localhost:8000/health")
        logger.info("=" * 60)
        logger.info("🛡️  Government Compliance: Tuân thủ Thông tư 20/2018/TT-BTTTT")
        logger.info("⚖️  Legal Disclaimer: Chỉ mang tính chất tham khảo")
        logger.info("🏛️  Ministry: Bộ Tư pháp - Cục Pháp chế")
        logger.info("=" * 60)
        logger.info("Press Ctrl+C to stop all services")
        logger.info("Nhấn Ctrl+C để dừng tất cả dịch vụ")
    
    def stop(self):
        """Stop all processes"""
        logger.info("🛑 Stopping Vietnamese Legal AI Chatbot...")
        self.running = False
        
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=10)
                logger.info(f"✅ Process {process.pid} stopped")
            except subprocess.TimeoutExpired:
                logger.warning(f"⚠️ Force killing process {process.pid}")
                process.kill()
            except Exception as e:
                logger.error(f"❌ Error stopping process {process.pid}: {e}")
        
        logger.info("✅ All services stopped")

def main():
    """Main entry point"""
    runner = VietnameseLegalChatbotRunner()
    runner.start()

if __name__ == "__main__":
    main()
