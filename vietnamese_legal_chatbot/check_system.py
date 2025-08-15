#!/usr/bin/env python3
"""
System Check and Initialization for Vietnamese Legal AI Chatbot
Kiểm tra và Khởi tạo Hệ thống cho Chatbot AI Pháp lý Việt Nam

This script checks system requirements and initializes the Vietnamese Legal AI Chatbot.
Script này kiểm tra yêu cầu hệ thống và khởi tạo Chatbot AI Pháp lý Việt Nam.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import platform

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class VietnameseLegalSystemInitializer:
    """System initializer for Vietnamese Legal AI Chatbot"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.requirements_met = True
        self.errors = []
        self.warnings = []
        
    def check_python_version(self) -> bool:
        """Check Python version compatibility"""
        logger.info("🐍 Checking Python version...")
        
        version = sys.version_info
        required_version = (3, 11)
        
        if version >= required_version:
            logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
            return True
        else:
            error_msg = f"❌ Python {version.major}.{version.minor} - Requires Python {required_version[0]}.{required_version[1]}+"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return False
    
    def check_dependencies(self) -> bool:
        """Check if all required packages are installed"""
        logger.info("📦 Checking Python dependencies...")
        
        required_packages = [
            ('streamlit', '1.28.0'),
            ('fastapi', '0.104.0'),
            ('uvicorn', '0.24.0'),
            ('openai', '1.6.0'),
            ('pinecone-client', '2.2.4'),
            ('langchain', '0.0.348'),
            ('underthesea', '6.7.0'),
            ('pandas', '2.1.0'),
            ('pydantic', '2.5.0'),
            ('requests', '2.31.0')
        ]
        
        missing_packages = []
        outdated_packages = []
        
        for package_name, min_version in required_packages:
            try:
                # Import package
                package = __import__(package_name.replace('-', '_'))
                
                # Check version if available
                if hasattr(package, '__version__'):
                    installed_version = package.__version__
                    logger.info(f"✅ {package_name} {installed_version}")
                    
                    # Compare versions (simplified)
                    if self._compare_versions(installed_version, min_version) < 0:
                        outdated_packages.append(f"{package_name} (installed: {installed_version}, required: {min_version}+)")
                else:
                    logger.info(f"✅ {package_name} - Installed")
                    
            except ImportError:
                missing_packages.append(package_name)
                logger.error(f"❌ {package_name} - Not installed")
        
        if missing_packages:
            error_msg = f"Missing packages: {', '.join(missing_packages)}"
            self.errors.append(error_msg)
            logger.error(f"❌ {error_msg}")
            logger.info("💡 Install with: pip install -r requirements.txt")
        
        if outdated_packages:
            warning_msg = f"Outdated packages: {', '.join(outdated_packages)}"
            self.warnings.append(warning_msg)
            logger.warning(f"⚠️ {warning_msg}")
            logger.info("💡 Update with: pip install --upgrade -r requirements.txt")
        
        return len(missing_packages) == 0
    
    def check_environment_variables(self) -> bool:
        """Check required environment variables"""
        logger.info("🔑 Checking environment variables...")
        
        required_vars = [
            ('OPENAI_API_KEY', 'OpenAI API key for GPT models'),
            ('PINECONE_API_KEY', 'Pinecone API key for vector database'),
            ('PINECONE_ENVIRONMENT', 'Pinecone environment (e.g., us-east-1-aws)'),
            ('PINECONE_INDEX_NAME', 'Pinecone index name for Vietnamese legal docs')
        ]
        
        missing_vars = []
        
        for var_name, description in required_vars:
            value = os.getenv(var_name)
            if value:
                # Mask sensitive values
                display_value = f"{value[:8]}..." if len(value) > 8 else "***"
                logger.info(f"✅ {var_name} = {display_value}")
            else:
                missing_vars.append(f"{var_name} ({description})")
                logger.error(f"❌ {var_name} - Not set")
        
        if missing_vars:
            error_msg = "Missing environment variables"
            self.errors.append(error_msg)
            logger.error(f"❌ {error_msg}:")
            for var in missing_vars:
                logger.error(f"   - {var}")
            logger.info("💡 Copy .env.example to .env and fill in your API keys")
            return False
        
        return True
    
    def check_directories(self) -> bool:
        """Check and create required directories"""
        logger.info("📁 Checking directory structure...")
        
        required_dirs = [
            'logs',
            'data/uploads',
            'data/temp', 
            'data/documents',
            'app/models',
            'app/services',
            'app/utils',
            'scripts',
            'tests'
        ]
        
        created_dirs = []
        
        for dir_path in required_dirs:
            full_path = self.project_root / dir_path
            if not full_path.exists():
                full_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(dir_path)
                logger.info(f"📁 Created directory: {dir_path}")
            else:
                logger.info(f"✅ Directory exists: {dir_path}")
        
        if created_dirs:
            logger.info(f"📁 Created {len(created_dirs)} missing directories")
        
        return True
    
    def check_api_connectivity(self) -> bool:
        """Check connectivity to external APIs"""
        logger.info("🌐 Checking API connectivity...")
        
        checks_passed = True
        
        # Check OpenAI API
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                import openai
                openai.api_key = openai_key
                
                # Simple API test
                response = openai.Model.list()
                logger.info("✅ OpenAI API - Connected")
                
            except Exception as e:
                warning_msg = f"OpenAI API connection failed: {str(e)}"
                self.warnings.append(warning_msg)
                logger.warning(f"⚠️ {warning_msg}")
        
        # Check Pinecone API
        pinecone_key = os.getenv('PINECONE_API_KEY')
        pinecone_env = os.getenv('PINECONE_ENVIRONMENT')
        
        if pinecone_key and pinecone_env:
            try:
                import pinecone
                pinecone.init(api_key=pinecone_key, environment=pinecone_env)
                
                # List indexes
                indexes = pinecone.list_indexes()
                logger.info("✅ Pinecone API - Connected")
                
            except Exception as e:
                warning_msg = f"Pinecone API connection failed: {str(e)}"
                self.warnings.append(warning_msg)
                logger.warning(f"⚠️ {warning_msg}")
        
        return checks_passed
    
    def check_ports(self) -> bool:
        """Check if required ports are available"""
        logger.info("🔌 Checking port availability...")
        
        required_ports = [
            (8000, 'FastAPI Backend'),
            (8501, 'Streamlit Frontend'),
            (6379, 'Redis Cache'),
            (5432, 'PostgreSQL Database')
        ]
        
        import socket
        
        for port, service in required_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                logger.warning(f"⚠️ Port {port} ({service}) - Already in use")
                self.warnings.append(f"Port {port} is in use")
            else:
                logger.info(f"✅ Port {port} ({service}) - Available")
        
        return True
    
    def initialize_sample_data(self) -> bool:
        """Initialize sample Vietnamese legal data"""
        logger.info("📚 Initializing sample legal data...")
        
        sample_documents = [
            {
                "title": "Bộ luật Dân sự 2015",
                "type": "law",
                "domain": "dan_su",
                "content": "Bộ luật này quy định về các quan hệ dân sự phát sinh trong lĩnh vực dân sự..."
            },
            {
                "title": "Luật Lao động 2019", 
                "type": "law",
                "domain": "lao_dong",
                "content": "Luật này quy định về quyền, nghĩa vụ, trách nhiệm của người lao động..."
            },
            {
                "title": "Luật Hôn nhân và Gia đình 2014",
                "type": "law", 
                "domain": "gia_dinh",
                "content": "Luật này quy định về hôn nhân và gia đình; quyền, nghĩa vụ, trách nhiệm..."
            }
        ]
        
        sample_data_path = self.project_root / 'data' / 'sample_legal_docs.json'
        
        try:
            with open(sample_data_path, 'w', encoding='utf-8') as f:
                json.dump(sample_documents, f, ensure_ascii=False, indent=2)
            
            logger.info(f"📚 Sample legal documents created: {sample_data_path}")
            return True
            
        except Exception as e:
            error_msg = f"Failed to create sample data: {str(e)}"
            self.errors.append(error_msg)
            logger.error(f"❌ {error_msg}")
            return False
    
    def create_config_files(self) -> bool:
        """Create necessary configuration files"""
        logger.info("⚙️ Creating configuration files...")
        
        # Create .env if it doesn't exist
        env_file = self.project_root / '.env'
        env_example = self.project_root / '.env.example'
        
        if not env_file.exists() and env_example.exists():
            try:
                import shutil
                shutil.copy2(env_example, env_file)
                logger.info("📝 Created .env file from .env.example")
                logger.warning("⚠️ Please edit .env file with your API keys")
                self.warnings.append("Edit .env file with your API keys")
            except Exception as e:
                error_msg = f"Failed to create .env file: {str(e)}"
                self.errors.append(error_msg)
                logger.error(f"❌ {error_msg}")
                return False
        
        return True
    
    def run_system_check(self) -> bool:
        """Run complete system check"""
        logger.info("🏛️ Vietnamese Legal AI Chatbot - System Check")
        logger.info("🇻🇳 Chatbot AI Pháp lý Việt Nam - Kiểm tra Hệ thống")
        logger.info("=" * 60)
        
        checks = [
            self.check_python_version,
            self.check_directories,
            self.check_dependencies,
            self.check_environment_variables,
            self.create_config_files,
            self.check_ports,
            self.initialize_sample_data,
        ]
        
        for check in checks:
            try:
                if not check():
                    self.requirements_met = False
            except Exception as e:
                error_msg = f"System check failed: {str(e)}"
                self.errors.append(error_msg)
                logger.error(f"❌ {error_msg}")
                self.requirements_met = False
        
        # Try API connectivity (non-blocking)
        try:
            self.check_api_connectivity()
        except Exception as e:
            logger.warning(f"⚠️ API connectivity check failed: {str(e)}")
        
        return self.requirements_met
    
    def display_results(self):
        """Display system check results"""
        logger.info("=" * 60)
        
        if self.requirements_met:
            logger.info("🎉 System check completed successfully!")
            logger.info("✅ Vietnamese Legal AI Chatbot is ready to run")
            logger.info("")
            logger.info("Next steps:")
            logger.info("1. Edit .env file with your API keys")
            logger.info("2. Run: python run_development.py")
            logger.info("3. Access frontend: http://localhost:8501")
            logger.info("4. Access API docs: http://localhost:8000/docs")
        else:
            logger.error("❌ System check failed!")
            logger.error("Please fix the following issues:")
            for error in self.errors:
                logger.error(f"   - {error}")
        
        if self.warnings:
            logger.warning("⚠️ Warnings:")
            for warning in self.warnings:
                logger.warning(f"   - {warning}")
        
        logger.info("=" * 60)
        return self.requirements_met
    
    def _compare_versions(self, version1: str, version2: str) -> int:
        """Compare two version strings (simplified)"""
        def normalize(v):
            return [int(x) for x in v.split('.') if x.isdigit()]
        
        v1_parts = normalize(version1)
        v2_parts = normalize(version2)
        
        # Pad with zeros
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        if v1_parts < v2_parts:
            return -1
        elif v1_parts > v2_parts:
            return 1
        else:
            return 0

def main():
    """Main entry point"""
    initializer = VietnameseLegalSystemInitializer()
    
    try:
        success = initializer.run_system_check()
        initializer.display_results()
        
        if success:
            print("\n🚀 Ready to start Vietnamese Legal AI Chatbot!")
            print("Run: python run_development.py")
            sys.exit(0)
        else:
            print("\n❌ Please fix the issues above before proceeding.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("\n⏹️ System check interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error during system check: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
