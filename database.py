import sqlite3
import os
from typing import Dict, Any, List

class DatabaseManager:
    def __init__(self, db_path: str = "soft_ai_pro.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create projects table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                project_type TEXT,
                programming_language TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                model_path TEXT,
                design_path TEXT,
                streamlit_path TEXT,
                credentials_path TEXT,
                status TEXT DEFAULT 'created'
            )
        ''')

        # Create features table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'medium',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            )
        ''')

        # Create users table (for future expansion)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create design pages table for Figma designs (minimum 10 pages)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS design_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                page_name TEXT NOT NULL,
                page_url TEXT,
                description TEXT,
                page_number INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        conn.close()

    def save_project(self, project_data: Dict[str, Any]) -> int:
        """Save project data to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO projects (name, description, project_type, programming_language)
            VALUES (?, ?, ?, ?)
        ''', (
            project_data.get('name'),
            project_data.get('description'),
            project_data.get('project_type'),
            project_data.get('programming_language')
        ))

        project_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return project_id

    def get_projects(self) -> list:
        """Get all projects"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
        projects = cursor.fetchall()

        conn.close()
        return projects

    def update_project_model_path(self, project_id: int, model_path: str):
        """Update project with model path"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE projects SET model_path = ?, status = 'completed' WHERE id = ?
        ''', (model_path, project_id))

        conn.commit()
        conn.close()

    def update_project_design(self, project_id: int, design_path: str):
        """Update project with Figma design path"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE projects SET design_path = ? WHERE id = ?
        ''', (design_path, project_id))

        conn.commit()
        conn.close()

    def update_project_streamlit(self, project_id: int, app_path: str):
        """Update project with Streamlit app path"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE projects SET streamlit_path = ? WHERE id = ?
        ''', (app_path, project_id))

        conn.commit()
        conn.close()

    def update_project_credentials(self, project_id: int, credentials_path: str):
        """Update project with credentials path"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE projects SET credentials_path = ? WHERE id = ?
        ''', (credentials_path, project_id))

        conn.commit()
        conn.close()

    # ======================== FEATURES METHODS ========================

    def save_feature(self, project_id: int, feature_data: Dict[str, Any]) -> int:
        """Save a feature for a project"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO features (project_id, name, description, priority)
            VALUES (?, ?, ?, ?)
        ''', (
            project_id,
            feature_data.get('name'),
            feature_data.get('description', ''),
            feature_data.get('priority', 'medium')
        ))

        feature_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return feature_id

    def get_project_features(self, project_id: int) -> List[Dict[str, Any]]:
        """Get all features for a project"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM features WHERE project_id = ? ORDER BY created_at DESC
        ''', (project_id,))
        
        features = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return features

    def delete_feature(self, feature_id: int):
        """Delete a feature"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('DELETE FROM features WHERE id = ?', (feature_id,))
        conn.commit()
        conn.close()

    # ======================== DESIGN PAGES METHODS ========================

    def save_design_page(self, project_id: int, page_data: Dict[str, Any]) -> int:
        """Save a design page for a project"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO design_pages (project_id, page_name, page_url, description, page_number)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            project_id,
            page_data.get('page_name'),
            page_data.get('page_url', ''),
            page_data.get('description', ''),
            page_data.get('page_number', 1)
        ))

        page_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return page_id

    def get_design_pages(self, project_id: int) -> List[Dict[str, Any]]:
        """Get all design pages for a project"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM design_pages WHERE project_id = ? ORDER BY page_number ASC
        ''', (project_id,))
        
        pages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return pages

    def get_project(self, project_id: int) -> Dict[str, Any]:
        """Get a single project with full details"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = cursor.fetchone()
        conn.close()
        
        return dict(project) if project else None

    def get_all_projects(self) -> List[Dict[str, Any]]:
        """Get all projects"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
        projects = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return projects

    def delete_project(self, project_id: int) -> bool:
        """Delete a project and all related data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting project: {str(e)}")
            return False

    def update_project(self, project_id: int, update_data: Dict[str, Any]) -> bool:
        """Update project information"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Build dynamic update query
            set_clause = ', '.join([f"{key} = ?" for key in update_data.keys()])
            values = list(update_data.values()) + [project_id]
            
            cursor.execute(f'UPDATE projects SET {set_clause} WHERE id = ?', values)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating project: {str(e)}")
            return False

    def delete_design_page(self, page_id: int) -> bool:
        """Delete a design page"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM design_pages WHERE id = ?', (page_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting design page: {str(e)}")
            return False

    def search_projects(self, search_term: str) -> List[Dict[str, Any]]:
        """Search projects by name or description"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM projects 
                WHERE name LIKE ? OR description LIKE ?
                ORDER BY created_at DESC
            ''', (f'%{search_term}%', f'%{search_term}%'))
            
            projects = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return projects
        except Exception as e:
            print(f"Error searching projects: {str(e)}")
            return []

    def get_project_statistics(self, project_id: int) -> Dict[str, Any]:
        """Get statistics for a project"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get project info
            cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
            project = dict(cursor.fetchone()) if cursor.fetchone() else None
            
            # Count features
            cursor.execute('SELECT COUNT(*) as count FROM features WHERE project_id = ?', (project_id,))
            features_count = cursor.fetchone()[0]
            
            # Count design pages
            cursor.execute('SELECT COUNT(*) as count FROM design_pages WHERE project_id = ?', (project_id,))
            pages_count = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'project': project,
                'features_count': features_count,
                'design_pages_count': pages_count
            }
        except Exception as e:
            print(f"Error getting statistics: {str(e)}")
            return {}

    def query(self, sql_query: str) -> List[Dict[str, Any]]:
        """Execute custom database query"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(sql_query)
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            
            return results
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            return []

    def backup(self) -> str:
        """Create a backup of the database"""
        try:
            import shutil
            from datetime import datetime
            
            # Create backup directory if it doesn't exist
            backup_dir = "data/backups"
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)
            
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"soft_ai_db_backup_{timestamp}.db")
            
            # Copy database file
            shutil.copy(self.db_path, backup_path)
            
            return backup_path
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            return ""