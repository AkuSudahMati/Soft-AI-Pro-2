"""
API Client - Client untuk komunikasi dengan Flask Backend
Digunakan oleh Streamlit frontend untuk berkomunikasi dengan backend
"""

import urllib.request
import urllib.error
import json
from typing import Dict, Any, Optional, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    """Client untuk berkomunikasi dengan Flask API"""
    
    def __init__(self, base_url: str = 'http://127.0.0.1:5000'):
        """
        Initialize API Client
        
        Args:
            base_url: Base URL dari Flask API (default: localhost:5000)
        """
        self.base_url = base_url
        self.headers = {
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make HTTP request menggunakan urllib"""
        url = f'{self.base_url}{endpoint}'
        
        try:
            if method == 'GET':
                request = urllib.request.Request(url, headers=self.headers, method='GET')
                response = urllib.request.urlopen(request)
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data
                
            elif method == 'POST':
                request_data = json.dumps(data).encode('utf-8') if data else None
                request = urllib.request.Request(
                    url,
                    data=request_data,
                    headers=self.headers,
                    method='POST'
                )
                response = urllib.request.urlopen(request)
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data
                
            elif method == 'PUT':
                request_data = json.dumps(data).encode('utf-8') if data else None
                request = urllib.request.Request(
                    url,
                    data=request_data,
                    headers=self.headers,
                    method='PUT'
                )
                response = urllib.request.urlopen(request)
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data
                
            elif method == 'DELETE':
                request = urllib.request.Request(url, headers=self.headers, method='DELETE')
                response = urllib.request.urlopen(request)
                response_data = json.loads(response.read().decode('utf-8'))
                return response_data
        
        except urllib.error.URLError as e:
            logger.error(f"Connection error: {str(e)}")
            return {
                'success': False,
                'error': f'Connection error: {str(e)}'
            }
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {str(e)}")
            return {
                'success': False,
                'error': f'Invalid JSON response: {str(e)}'
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        
        # Fallback return for unknown methods
        return {
            'success': False,
            'error': f'Unknown HTTP method: {method}'
        }
    
    # ======================== PROJECT METHODS ========================
    
    def get_all_projects(self) -> Dict[str, Any]:
        """Ambil semua projects"""
        return self._make_request('GET', '/api/projects')
    
    def get_project(self, project_id: int) -> Dict[str, Any]:
        """Ambil detail project"""
        return self._make_request('GET', f'/api/projects/{project_id}')
    
    def create_project(self, 
                      name: str,
                      description: str,
                      project_type: str,
                      programming_language: str) -> Dict[str, Any]:
        """Buat project baru"""
        payload = {
            'name': name,
            'description': description,
            'project_type': project_type,
            'programming_language': programming_language
        }
        return self._make_request('POST', '/api/projects', payload)
    
    def update_project(self, 
                      project_id: int,
                      data: Dict[str, Any]) -> Dict[str, Any]:
        """Update project"""
        return self._make_request('PUT', f'/api/projects/{project_id}', data)
    
    def delete_project(self, project_id: int) -> Dict[str, Any]:
        """Hapus project"""
        return self._make_request('DELETE', f'/api/projects/{project_id}')
    
    def create_project_feature(self,
                               project_id: int,
                               name: str,
                               description: str = '',
                               priority: str = 'medium') -> Dict[str, Any]:
        """Tambah feature ke project"""
        payload: Dict[str, Any] = {
            'name': name,
            'description': description,
            'priority': priority
        }
        return self._make_request('POST', f'/api/projects/{project_id}/features', payload)

    def get_project_features(self, project_id: int) -> Dict[str, Any]:
        """Ambil semua fitur project"""
        return self._make_request('GET', f'/api/projects/{project_id}/features')

    def create_design_page(self,
                           project_id: int,
                           page_name: str,
                           page_url: str = '',
                           description: str = '',
                           page_number: int = 1) -> Dict[str, Any]:
        """Tambah design page ke project"""
        payload: Dict[str, Any] = {
            'page_name': page_name,
            'page_url': page_url,
            'description': description,
            'page_number': page_number
        }
        return self._make_request('POST', f'/api/projects/{project_id}/design-pages', payload)

    def save_project_credentials(self,
                                 project_id: int,
                                 api_keys: Dict[str, str],
                                 database: Dict[str, str],
                                 cloud_services: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Simpan kredensial project"""
        payload: Dict[str, Any] = {
            'api_keys': api_keys,
            'database': database,
            'cloud_services': cloud_services or {}
        }
        return self._make_request('POST', f'/api/projects/{project_id}/credentials', payload)

    def analyze_project(self,
                        project_id: int,
                        features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analisis project menggunakan Claude AI"""
        payload = {
            'features': features
        }
        return self._make_request('POST', f'/api/projects/{project_id}/analyze', payload)

    # ======================== FIGMA INTEGRATION METHODS ========================
    
    def fetch_figma_design(self, 
                          project_id: int,
                          figma_url: str,
                          figma_token: str) -> Dict[str, Any]:
        """Ambil design dari Figma"""
        payload = {
            'figma_url': figma_url,
            'figma_token': figma_token
        }
        return self._make_request('POST', f'/api/projects/{project_id}/figma/fetch', payload)
    
    def get_figma_components(self, project_id: int) -> Dict[str, Any]:
        """Ambil komponen Figma"""
        return self._make_request('GET', f'/api/projects/{project_id}/figma/components')
    
    # ======================== COMPONENT GENERATION METHODS ========================
    
    def generate_components(self,
                           project_id: int,
                           components: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate komponen dari design"""
        payload = {'components': components}
        return self._make_request('POST', f'/api/projects/{project_id}/components/generate', payload)
    
    # ======================== ML MODEL METHODS ========================
    
    def ml_predict(self, input_data: Any) -> Dict[str, Any]:
        """Lakukan prediksi ML"""
        payload = {'input_data': input_data}
        return self._make_request('POST', '/api/ml/predict', payload)
    
    def ml_train(self, training_data: Any) -> Dict[str, Any]:
        """Train ML model"""
        payload = {'training_data': training_data}
        return self._make_request('POST', '/api/ml/train', payload)
    
    # ======================== DATABASE METHODS ========================
    
    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute database query"""
        payload = {'query': query}
        return self._make_request('POST', '/api/database/query', payload)
    
    def backup_database(self) -> Dict[str, Any]:
        """Backup database"""
        return self._make_request('POST', '/api/database/backup')
    
    # ======================== HEALTH CHECK METHODS ========================
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        return self._make_request('GET', '/api/health')
    
    def get_status(self) -> Dict[str, Any]:
        """Get API status"""
        return self._make_request('GET', '/api/status')


# Create singleton instance
api_client = APIClient()

