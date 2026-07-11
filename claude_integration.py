"""
Claude AI Integration Module
Menghubungkan data Step 1 & Step 2 dengan Claude for analysis & optimization
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    from anthropic import Anthropic as AnthropicClient
    _anthropic_available: bool = True
except ImportError:
    AnthropicClient = None  # type: ignore
    _anthropic_available = False
    print("⚠️  Anthropic SDK not installed. Run: pip install anthropic")


class ClaudeAnalyzer:
    """Analyzer untuk menggunakan Claude AI untuk analisis project & features"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.client: Optional[Any] = None
        self.model = model or os.getenv("CLAUDE_MODEL", "claude-fable-5")
        self.api_key: Optional[str] = api_key
        self.init_client()
    
    def init_client(self) -> bool:
        """Initialize Claude client dengan API key dari parameter, environment atau .env"""
        try:
            if not _anthropic_available:
                print("❌ Anthropic SDK not installed!")
                return False
            
            if not self.api_key:
                # Cari API key dari .env file
                env_path = Path(".env")
                if env_path.exists():
                    with open(env_path, 'r') as f:
                        for line in f:
                            if line.startswith("CLAUDE_API_KEY="):
                                self.api_key = line.split("=")[1].strip()
                                break
            
            if not self.api_key:
                # Atau dari environment variable
                self.api_key = os.getenv("CLAUDE_API_KEY")
            
            if not self.api_key:
                print("❌ CLAUDE_API_KEY not found!")
                print("   Setup guide: CLAUDE_SETUP.md")
                return False
            
            # Import Anthropic only if available
            if _anthropic_available and AnthropicClient:
                self.client = AnthropicClient(api_key=self.api_key)
                print("✅ Claude client initialized successfully")
                print(f"   using model: {self.model}")
            return True
        
        except Exception as e:
            print(f"❌ Error initializing Claude: {str(e)}")
            return False
    
    def analyze_features(self, 
                        project_data: Dict[str, Any],
                        features: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analisis features menggunakan Claude AI
        
        Args:
            project_data: {name, description, project_type, programming_language}
            features: [{name, priority}, ...]
        
        Returns:
            {analysis, recommendations, optimized_features, file_path}
        """
        
        if not self.client:
            return {"error": "Claude client not initialized"}
        
        try:
            # Buat prompt untuk Claude
            prompt = self._create_analysis_prompt(project_data, features)
            
            print(f"🤖 Claude sedang menganalisis {len(features)} features...")
            
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract text safely from response
            response_text: str = ""
            if hasattr(message, 'content'):
                content = message.content
                if isinstance(content, list) and len(content) > 0:
                    first = content[0]
                    if isinstance(first, dict):
                        response_text = first.get('text', '') or first.get('content', '')
                    elif hasattr(first, 'text'):
                        response_text = str(first.text)
                    else:
                        response_text = str(first)
                elif isinstance(content, str):
                    response_text = content
            elif hasattr(message, 'completion'):
                response_text = str(message.completion)
            
            # Parse response
            result: Dict[str, Any] = {
                "project_name": project_data.get("name"),
                "project_type": project_data.get("project_type"),
                "features_count": len(features),
                "analysis": response_text,
                "timestamp": datetime.now().isoformat(),
                "model_used": self.model
            }
            
            # Save hasil ke file
            file_path = self._save_analysis(result, project_data)
            result["file_path"] = file_path
            
            print(f"✅ Analisis selesai! Tersimpan di: {file_path}")
            return result
        
        except Exception as e:
            return {"error": f"Error analyzing features: {str(e)}"}
    
    def _create_analysis_prompt(self, 
                               project_data: Dict[str, Any],
                               features: List[Dict[str, Any]]) -> str:
        """Create prompt untuk Claude analysis"""
        
        prompt = f"""
        Anda adalah senior software architect yang berpengalaman.
        
        ANALISIS PROJECT & FEATURES BERIKUT:
        ════════════════════════════════════
        
        PROJECT INFO:
        - Nama: {project_data.get('name')}
        - Tipe: {project_data.get('project_type')}
        - Bahasa: {project_data.get('programming_language')}
        - Deskripsi: {project_data.get('description', 'N/A')}
        
        FEATURES YANG DIRENCANAKAN:
        """
        
        for idx, feature in enumerate(features, 1):
            prompt += f"\n{idx}. {feature['name']} [Priority: {feature['priority']}]"
        
        prompt += f"""
        
        ANALISIS & REKOMENDASI:
        
        1. **REVIEW FITUR**:
           - Apakah fitur-fitur ini sesuai dengan tipe project?
           - Ada fitur yang hilang atau redundan?
           - Priority yang diberikan sudah optimal?
        
        2. **ISSUE & RISK**:
           - Potensi masalah teknis apa yang mungkin timbul?
           - Dependencies antar features?
           - Complexity assessment?
        
        3. **REKOMENDASI PERBAIKAN**:
           - Saran untuk menambah/mengurangi/mengubah features
           - Best practices untuk {project_data.get('project_type')}
           - Urutan development yang disarankan
        
        4. **ARCHITECTURE NOTES**:
           - Tech stack yang cocok untuk {project_data.get('programming_language')}
           - Pattern atau framework yang recommended
           - Scalability considerations
        
        Format respon dalam markdown yang rapi dan mudah dibaca.
        """
        
        return prompt
    
    def _save_analysis(self, 
                      result: Dict[str, Any],
                      project_data: Dict[str, Any]) -> str:
        """Save analysis result ke file"""
        
        try:
            # Buat folder untuk analysis jika belum ada
            analysis_dir = Path("analysis_results")
            analysis_dir.mkdir(exist_ok=True)
            
            # Generate filename
            project_name = project_data.get('name', 'project').replace(' ', '_')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"claude_analysis_{project_name}_{timestamp}.md"
            filepath = analysis_dir / filename
            
            # Buat content markdown
            content = f"""# Claude AI Analysis Report

## Project Information
- **Name**: {result['project_name']}
- **Type**: {result['project_type']}
- **Features Count**: {result['features_count']}
- **Analyzed on**: {result['timestamp']}
- **Model**: {result['model_used']}

## Analysis
{result['analysis']}

---
*Generated by Claude AI Integration*
"""
            
            # Save ke file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Juga save JSON version
            json_filename = f"claude_analysis_{project_name}_{timestamp}.json"
            json_filepath = analysis_dir / json_filename
            
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"   📄 Markdown: {filepath}")
            print(f"   📊 JSON: {json_filepath}")
            
            return str(filepath)
        
        except Exception as e:
            print(f"❌ Error saving analysis: {str(e)}")
            return ""
    
    def is_available(self) -> bool:
        """Check apakah Claude available & configured"""
        return self.client is not None and self.api_key is not None


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def analyze_step1_data(project_data: Dict[str, Any], 
                       features: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Quick function untuk analyze Step 1 data
    
    Usage:
        result = analyze_step1_data(
            project_data={'name': 'My App', 'project_type': 'Web', ...},
            features=[{'name': 'Auth', 'priority': 'High'}, ...]
        )
        print(result['file_path'])
    """
    
    analyzer = ClaudeAnalyzer()
    
    if not analyzer.is_available():
        return {
            "error": "Claude not configured",
            "message": "Please setup Claude API key first. See CLAUDE_SETUP.md"
        }
    
    return analyzer.analyze_features(project_data, features)


if __name__ == "__main__":
    # Test function
    print("=" * 60)
    print("🤖 Claude AI Integration Test")
    print("=" * 60)
    
    # Sample data
    sample_project = {
        "name": "E-Commerce Platform",
        "description": "Online marketplace dengan AI recommendation",
        "project_type": "Web Application",
        "programming_language": "Python"
    }
    
    sample_features = [
        {"name": "User Authentication", "priority": "High"},
        {"name": "Payment Gateway", "priority": "High"},
        {"name": "Product Catalog", "priority": "High"},
        {"name": "Shopping Cart", "priority": "Medium"},
        {"name": "AI Recommendation", "priority": "Medium"},
        {"name": "Order Management", "priority": "High"},
    ]
    
    # Run analysis
    result = analyze_step1_data(sample_project, sample_features)
    
    if "error" not in result:
        print(f"\n✅ Analysis complete!")
        print(f"📄 File: {result.get('file_path')}")
        print(f"\n📋 Summary:")
        print(result['analysis'][:500] + "...\n")
    else:
        print(f"\n❌ {result['error']}")
        print(f"📝 {result.get('message')}")
