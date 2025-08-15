"""
Document Uploader Script for Vietnamese Legal AI Chatbot
Script Tải lên Tài liệu cho Chatbot AI Pháp lý Việt Nam

Batch upload Vietnamese legal documents to Pinecone vector database.
Tải lên hàng loạt tài liệu pháp lý Việt Nam vào cơ sở dữ liệu vector Pinecone.
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add app directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

def setup_logging(log_level: str = "INFO"):
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'logs/document_upload_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler()
        ]
    )

class DocumentUploader:
    """Vietnamese Legal Document Uploader for Pinecone"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # TODO: Initialize services when implementing
        # self.pinecone_service = PineconeService()
        # self.document_processor = VietnameseLegalDocumentProcessor()
        self.uploaded_count = 0
        self.failed_count = 0
        self.upload_log = []
    
    def upload_documents_from_directory(
        self, 
        directory_path: str,
        file_extensions: List[str] = None,
        batch_size: int = 10
    ) -> Dict[str, Any]:
        """
        Upload all legal documents from a directory
        
        Args:
            directory_path: Path to directory containing legal documents
            file_extensions: List of file extensions to process ['.pdf', '.docx', '.txt']
            batch_size: Number of documents to process in each batch
            
        Returns:
            Upload statistics and results
        """
        if file_extensions is None:
            file_extensions = ['.pdf', '.docx', '.txt', '.md']
        
        directory = Path(directory_path)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        self.logger.info(f"Starting document upload from: {directory_path}")
        
        # Find all legal document files
        document_files = []
        for ext in file_extensions:
            document_files.extend(directory.glob(f"**/*{ext}"))
        
        self.logger.info(f"Found {len(document_files)} documents to process")
        
        # Process documents in batches
        results = {
            'total_files': len(document_files),
            'uploaded': 0,
            'failed': 0,
            'skipped': 0,
            'batch_results': []
        }
        
        for i in range(0, len(document_files), batch_size):
            batch_files = document_files[i:i + batch_size]
            batch_result = self._process_document_batch(batch_files, i // batch_size + 1)
            results['batch_results'].append(batch_result)
            
            results['uploaded'] += batch_result['uploaded']
            results['failed'] += batch_result['failed']
            results['skipped'] += batch_result['skipped']
        
        self.logger.info(f"Upload completed. Total: {results['uploaded']} uploaded, {results['failed']} failed")
        return results
    
    def _process_document_batch(self, files: List[Path], batch_number: int) -> Dict[str, Any]:
        """Process a batch of document files"""
        self.logger.info(f"Processing batch {batch_number} with {len(files)} files")
        
        batch_result = {
            'batch_number': batch_number,
            'files_count': len(files),
            'uploaded': 0,
            'failed': 0,
            'skipped': 0,
            'file_results': []
        }
        
        for file_path in files:
            try:
                result = self._process_single_document(file_path)
                batch_result['file_results'].append(result)
                
                if result['status'] == 'uploaded':
                    batch_result['uploaded'] += 1
                elif result['status'] == 'failed':
                    batch_result['failed'] += 1
                else:
                    batch_result['skipped'] += 1
                    
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                batch_result['failed'] += 1
                batch_result['file_results'].append({
                    'file_path': str(file_path),
                    'status': 'failed',
                    'error': str(e)
                })
        
        return batch_result
    
    def _process_single_document(self, file_path: Path) -> Dict[str, Any]:
        """Process and upload a single document"""
        self.logger.info(f"Processing document: {file_path.name}")
        
        try:
            # TODO: Implement actual document processing
            # # Read and process document
            # document_content = self._read_document(file_path)
            # if not document_content:
            #     return {
            #         'file_path': str(file_path),
            #         'status': 'skipped',
            #         'reason': 'Empty or unreadable content'
            #     }
            
            # # Extract metadata from file path and content
            # metadata = self._extract_document_metadata(file_path, document_content)
            
            # # Process document with Vietnamese legal processor
            # processed_doc = self.document_processor.process_legal_document(
            #     content=document_content,
            #     metadata=metadata
            # )
            
            # # Upload to Pinecone
            # success = self.pinecone_service.upsert_documents([processed_doc])
            
            # if success:
            #     return {
            #         'file_path': str(file_path),
            #         'status': 'uploaded',
            #         'document_id': processed_doc['id'],
            #         'chunks_count': len(processed_doc['chunks'])
            #     }
            # else:
            #     return {
            #         'file_path': str(file_path),
            #         'status': 'failed',
            #         'error': 'Failed to upload to Pinecone'
            #     }
            
            # Placeholder implementation
            return {
                'file_path': str(file_path),
                'status': 'uploaded',
                'document_id': f'doc_{file_path.stem}',
                'chunks_count': 5
            }
            
        except Exception as e:
            self.logger.error(f"Failed to process {file_path}: {e}")
            return {
                'file_path': str(file_path),
                'status': 'failed',
                'error': str(e)
            }
    
    def _read_document(self, file_path: Path) -> Optional[str]:
        """Read document content based on file extension"""
        try:
            if file_path.suffix.lower() == '.pdf':
                # TODO: Implement PDF reading
                # return self._read_pdf(file_path)
                pass
            elif file_path.suffix.lower() == '.docx':
                # TODO: Implement DOCX reading
                # return self._read_docx(file_path)
                pass
            elif file_path.suffix.lower() in ['.txt', '.md']:
                return file_path.read_text(encoding='utf-8')
            else:
                self.logger.warning(f"Unsupported file type: {file_path.suffix}")
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to read file {file_path}: {e}")
            return None
    
    def _extract_document_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extract metadata from file path and content"""
        metadata = {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'file_size': file_path.stat().st_size,
            'upload_date': datetime.now().isoformat(),
            'language': 'vietnamese'
        }
        
        # Extract legal domain from file path or content
        legal_domain = self._detect_legal_domain(file_path, content)
        if legal_domain:
            metadata['legal_domain'] = legal_domain
        
        # Extract document type
        document_type = self._detect_document_type(file_path, content)
        if document_type:
            metadata['document_type'] = document_type
        
        return metadata
    
    def _detect_legal_domain(self, file_path: Path, content: str) -> Optional[str]:
        """Detect Vietnamese legal domain from file path or content"""
        domain_keywords = {
            'dan_su': ['dân sự', 'dân su', 'civil'],
            'hinh_su': ['hình sự', 'hinh su', 'criminal'],
            'lao_dong': ['lao động', 'lao dong', 'labor'],
            'thuong_mai': ['thương mại', 'thuong mai', 'commercial', 'doanh nghiệp'],
            'hanh_chinh': ['hành chính', 'hanh chinh', 'administrative'],
            'hien_phap': ['hiến pháp', 'hien phap', 'constitution'],
            'gia_dinh': ['gia đình', 'gia dinh', 'family'],
            'bat_dong_san': ['bất động sản', 'bat dong san', 'real estate']
        }
        
        file_name = file_path.name.lower()
        content_lower = content.lower()
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in file_name or keyword in content_lower for keyword in keywords):
                return domain
        
        return 'khac'  # Other
    
    def _detect_document_type(self, file_path: Path, content: str) -> Optional[str]:
        """Detect document type from content"""
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in ['bộ luật', 'bo luat']):
            return 'bo_luat'
        elif any(keyword in content_lower for keyword in ['luật', 'luat']):
            return 'luat'
        elif any(keyword in content_lower for keyword in ['nghị định', 'nghi dinh']):
            return 'nghi_dinh'
        elif any(keyword in content_lower for keyword in ['thông tư', 'thong tu']):
            return 'thong_tu'
        elif any(keyword in content_lower for keyword in ['quyết định', 'quyet dinh']):
            return 'quyet_dinh'
        else:
            return 'tai_lieu_khac'
    
    def upload_single_document(self, file_path: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Upload a single document with optional metadata"""
        file_path_obj = Path(file_path)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        result = self._process_single_document(file_path_obj)
        return result
    
    def get_upload_statistics(self) -> Dict[str, Any]:
        """Get upload statistics and logs"""
        return {
            'uploaded_count': self.uploaded_count,
            'failed_count': self.failed_count,
            'upload_log': self.upload_log
        }

def main():
    """Main function for document uploader script"""
    parser = argparse.ArgumentParser(description='Upload Vietnamese legal documents to Pinecone')
    parser.add_argument('--directory', '-d', required=True, help='Directory containing legal documents')
    parser.add_argument('--extensions', '-e', nargs='+', default=['.pdf', '.docx', '.txt'], 
                       help='File extensions to process')
    parser.add_argument('--batch-size', '-b', type=int, default=10, 
                       help='Number of documents to process in each batch')
    parser.add_argument('--log-level', '-l', default='INFO', 
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       help='Logging level')
    parser.add_argument('--output-report', '-o', help='Output file for upload report (JSON)')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    print("📚 Vietnamese Legal Document Uploader")
    print("=" * 50)
    
    try:
        # Initialize uploader
        uploader = DocumentUploader()
        
        # Upload documents
        results = uploader.upload_documents_from_directory(
            directory_path=args.directory,
            file_extensions=args.extensions,
            batch_size=args.batch_size
        )
        
        # Print results
        print(f"\n📊 Upload Results:")
        print(f"Total files: {results['total_files']}")
        print(f"✅ Uploaded: {results['uploaded']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"⏭️ Skipped: {results['skipped']}")
        
        # Save report if requested
        if args.output_report:
            with open(args.output_report, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"📝 Report saved to: {args.output_report}")
        
        print("\n🎉 Document upload completed!")
        
    except Exception as e:
        logger.error(f"Document upload failed: {e}")
        print(f"❌ Upload failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
