"""
FastAPI Backend - Menghubungkan Frontend dengan Backend Services
Menyediakan REST API endpoints untuk komunikasi antara Streamlit Frontend dan Backend Services

Replacement untuk Flask dengan FastAPI (lebih cepat, modern, dan auto-docs)
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import json
import os
from pathlib import Path
import uvicorn

from project_manager import ProjectManager
from database import DatabaseManager
from figma_handler import FigmaHandler
from ml_model import MLModel
from claude_integration import ClaudeAnalyzer


# ======================== PYDANTIC MODELS (Request/Response validation) ========================

class ProjectCreate(BaseModel):
    name: str
    description: str
    project_type: str
    programming_language: str


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[str] = None
    programming_language: Optional[str] = None


class FeatureCreate(BaseModel):
    name: str
    description: Optional[str] = None
    priority: str = "medium"


class DesignPageCreate(BaseModel):
    page_name: str
    page_url: Optional[str] = None
    description: Optional[str] = None
    page_number: Optional[int] = None


class FigmaFetchRequest(BaseModel):
    figma_url: str
    figma_token: str


class MLPredictRequest(BaseModel):
    input_data: Dict[str, Any]


class MLTrainRequest(BaseModel):
    training_data: List[Dict[str, Any]]


class QueryRequest(BaseModel):
    query: str


class CredentialsCreate(BaseModel):
    api_keys: Dict[str, str]
    database: Dict[str, str]
    cloud_services: Optional[Dict[str, str]] = None


class AnalyzeRequest(BaseModel):
    features: List[FeatureCreate]


# ======================== INITIALIZE APP ========================

app = FastAPI(
    title="Soft AI Pro Backend API",
    description="REST API untuk Soft AI Pro - Project AI Generator",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
pm = ProjectManager()
db = DatabaseManager()
figma = FigmaHandler()
ml_model: MLModel = MLModel()


# ======================== HEALTH CHECK ENDPOINTS ========================

@app.get("/api/health")
async def health_check():
    """Check API health status"""
    return {
        "success": True,
        "message": "API is running",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/status")
async def api_status():
    """Get detailed API status"""
    return {
        "success": True,
        "api": "Soft AI Pro Backend API",
        "version": "1.0.0",
        "status": "operational",
        "framework": "FastAPI",
        "timestamp": datetime.now().isoformat()
    }


# ======================== PROJECT ENDPOINTS ========================

@app.get("/api/projects")
async def get_all_projects():
    """Ambil semua projects dari database"""
    try:
        projects: List[Dict[str, Any]] = db.get_all_projects()
        return {
            "success": True,
            "data": projects,
            "count": len(projects) if projects else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}")
async def get_project(project_id: int):
    """Ambil detail project tertentu"""
    try:
        project: Dict[str, Any] = db.get_project(project_id)
        if project:
            return {
                "success": True,
                "data": project
            }
        else:
            raise HTTPException(status_code=404, detail="Project tidak ditemukan")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects", status_code=201)
async def create_project(project: ProjectCreate):
    """Buat project baru"""
    try:
        data: Dict[str, Any] = project.model_dump()
        
        # Create project
        project_id: int = pm.create_new_project(data)
        
        return {
            "success": True,
            "message": "Project berhasil dibuat",
            "project_id": project_id,
            "data": {
                "id": project_id,
                **data,
                "created_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/projects/{project_id}")
async def update_project(project_id: int, project: ProjectUpdate):
    """Update project"""
    try:
        data: Dict[str, Any] = project.model_dump(exclude_unset=True)
        result: bool = db.update_project(project_id, data)
        
        if result:
            return {
                "success": True,
                "message": "Project berhasil diupdate",
                "data": data
            }
        else:
            raise HTTPException(status_code=404, detail="Project tidak ditemukan")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/projects/{project_id}")
async def delete_project(project_id: int):
    """Hapus project"""
    try:
        result: bool = db.delete_project(project_id)
        
        if result:
            return {
                "success": True,
                "message": "Project berhasil dihapus"
            }
        else:
            raise HTTPException(status_code=404, detail="Project tidak ditemukan")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ======================== FEATURES ENDPOINTS ========================

@app.get("/api/projects/{project_id}/features")
async def get_project_features(project_id: int):
    """Ambil semua features untuk sebuah project"""
    try:
        features: List[Dict[str, Any]] = db.get_project_features(project_id)
        return {
            "success": True,
            "data": features,
            "count": len(features) if features else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/features", status_code=201)
async def add_project_feature(project_id: int, feature: FeatureCreate):
    """Tambah feature ke project"""
    try:
        data: Dict[str, Any] = feature.model_dump()
        
        # Save feature
        feature_id: int = db.save_feature(project_id, data)
        
        return {
            "success": True,
            "message": "Feature berhasil ditambahkan",
            "feature_id": feature_id,
            "data": {
                "id": feature_id,
                "project_id": project_id,
                "name": data.get("name"),
                "description": data.get("description", ""),
                "priority": data.get("priority", "medium"),
                "created_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/projects/{project_id}/features/{feature_id}")
async def delete_project_feature(project_id: int, feature_id: int):
    """Hapus feature dari project"""
    try:
        db.delete_feature(feature_id)
        return {
            "success": True,
            "message": "Feature berhasil dihapus"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ======================== DESIGN PAGES ENDPOINTS ========================

@app.get("/api/projects/{project_id}/design-pages")
async def get_design_pages(project_id: int):
    """Ambil semua design pages untuk sebuah project"""
    try:
        pages: List[Dict[str, Any]] = db.get_design_pages(project_id)
        return {
            "success": True,
            "data": pages,
            "count": len(pages) if pages else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/design-pages", status_code=201)
async def add_design_page(project_id: int, page: DesignPageCreate):
    """Tambah design page ke project"""
    try:
        data: Dict[str, Any] = page.model_dump()
        
        # Get existing pages
        existing_pages: List[Dict[str, Any]] = db.get_design_pages(project_id)
        if len(existing_pages) >= 10:
            page_number: int = len(existing_pages) + 1
        else:
            page_number = data.get("page_number", len(existing_pages) + 1)
        
        data["page_number"] = page_number
        
        # Save design page
        page_id: int = db.save_design_page(project_id, data)
        
        return {
            "success": True,
            "message": "Design page berhasil ditambahkan",
            "page_id": page_id,
            "data": {
                "id": page_id,
                "project_id": project_id,
                "page_name": data.get("page_name"),
                "page_url": data.get("page_url", ""),
                "description": data.get("description", ""),
                "page_number": page_number,
                "created_at": datetime.now().isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/credentials", status_code=201)
async def save_project_credentials(project_id: int, credentials: CredentialsCreate):
    """Simpan kredensial dan konfigurasi project"""
    try:
        data: Dict[str, Any] = credentials.model_dump()
        success: bool = pm.save_user_credentials(data, project_id)
        if success:
            return {
                "success": True,
                "message": "Kredensial project berhasil disimpan",
                "data": data
            }
        else:
            raise HTTPException(status_code=500, detail="Gagal menyimpan kredensial project")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/projects/{project_id}/analyze")
async def analyze_project(project_id: int, request_data: AnalyzeRequest):
    """Analisis project dan fitur menggunakan Claude AI"""
    try:
        project: Dict[str, Any] = db.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project tidak ditemukan")

        api_key: Optional[str] = None
        credentials_path: Optional[str] = project.get("credentials_path")
        if credentials_path and os.path.exists(credentials_path):
            try:
                with open(credentials_path, 'r', encoding='utf-8') as f:
                    credentials_data = json.load(f)
                    api_key = credentials_data.get('api_keys', {}).get('claude')
            except Exception as e:
                print(f"Warning: unable to load project credentials: {e}")

        analyzer = ClaudeAnalyzer(api_key=api_key)
        result: Dict[str, Any] = analyzer.analyze_features(
            project_data=project,
            features=[feature.model_dump() for feature in request_data.features]
        )

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return {
            "success": True,
            "message": "Analisis project selesai",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ======================== FIGMA INTEGRATION ENDPOINTS ========================

@app.post("/api/projects/{project_id}/figma/fetch")
async def fetch_figma_design(project_id: int, request_data: FigmaFetchRequest):
    """Ambil design dari Figma"""
    try:
        # Fetch design from Figma
        design_data: Dict[str, Any] | None = pm.save_figma_design(
            request_data.figma_url,
            request_data.figma_token,
            project_id
        )
        
        if design_data:
            return {
                "success": True,
                "message": "Design berhasil diambil dari Figma",
                "data": design_data
            }
        else:
            raise HTTPException(status_code=400, detail="Gagal mengambil design dari Figma")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/figma/components")
async def get_figma_components(project_id: int):
    """Ambil komponen dari Figma design"""
    try:
        project_dir: Path = Path(os.getcwd()) / "projects" / f"project_{project_id}"
        design_file: Path = project_dir / "figma_design.json"
        
        if design_file.exists():
            with open(design_file, 'r') as f:
                design_data = json.load(f)
            
            return {
                "success": True,
                "data": design_data
            }
        else:
            raise HTTPException(status_code=404, detail="Design file tidak ditemukan")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ======================== COMPONENT GENERATION ENDPOINTS ========================

@app.post("/api/projects/{project_id}/components/generate")
async def generate_components(project_id: int, data: Dict[str, Any]):
    """Generate kode komponen dari design"""
    try:
        if "components" not in data:
            raise HTTPException(status_code=400, detail="components field diperlukan")
        
        # Generate code
        generated_code: str | None = pm.build_streamlit_app(data["components"], project_id)
        
        if generated_code:
            return {
                "success": True,
                "message": "Komponen berhasil digenerate",
                "code": generated_code
            }
        else:
            raise HTTPException(status_code=400, detail="Gagal generate komponen")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ======================== ML MODEL ENDPOINTS ========================

@app.post("/api/ml/predict")
async def ml_predict(request_data: MLPredictRequest):
    """Lakukan prediksi menggunakan ML model"""
    try:
        prediction: Dict[str, Any] = ml_model.predict(request_data.input_data)
        
        return {
            "success": True,
            "prediction": prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/ml/train")
async def ml_train(request_data: MLTrainRequest):
    """Train ML model dengan data baru"""
    try:
        result: Dict[str, Any] = ml_model.train(request_data.training_data)
        
        return {
            "success": True,
            "message": "Model berhasil dilatih",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ======================== DATABASE ENDPOINTS ========================

@app.post("/api/database/query")
async def execute_query(request_data: QueryRequest):
    """Execute custom database query"""
    try:
        result: List[Dict[str, Any]] = db.query(request_data.query)
        
        return {
            "success": True,
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/database/backup")
async def backup_database():
    """Backup database"""
    try:
        backup_path: str = db.backup()
        
        return {
            "success": True,
            "message": "Database berhasil dibackup",
            "backup_path": str(backup_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ======================== ERROR HANDLERS ========================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error"
        }
    )


# ======================== RUN APP ========================

if __name__ == "__main__":
    # Run FastAPI app dengan Uvicorn
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=5000,
        reload=True,
        log_level="info"
    )
