import os
import shutil
import logging
from datetime import datetime
from pathlib import Path
from flask import current_app
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

class FileService:
    def delete_post_image(self, image_path: str, permanent: bool = False):
        """Delete image w/ recycle bin support"""
        if not image_path:
            return True
            
        upload_folder = current_app.config['UPLOAD_FOLDER']  # current_app HERE
        full_path = os.path.join(upload_folder, image_path)
        recycle_bin = os.path.join(upload_folder, 'recycle_bin')
        os.makedirs(recycle_bin, exist_ok=True)
        
        try:
            if not os.path.exists(full_path):
                logger.info(f"Image not found: {full_path}")
                return True
            
            if permanent:
                os.remove(full_path)
                logger.info(f"Permanently deleted: {full_path}")
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_name = secure_filename(Path(image_path).name)
                recycle_path = os.path.join(recycle_bin, f"{timestamp}_{safe_name}")
                shutil.move(full_path, recycle_path)
                logger.info(f"Moved to recycle: {full_path} -> {recycle_path}")
                return True
                
        except FileNotFoundError:
            logger.info(f"File already gone: {full_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete {full_path}: {str(e)}")
            return False
    
    def cleanup_recycle_bin(self, days_old: int = 7):
        """Production cron job"""
        upload_folder = current_app.config['UPLOAD_FOLDER']
        recycle_bin = os.path.join(upload_folder, 'recycle_bin')
        cutoff = datetime.now().timestamp() - (days_old * 86400)
        
        deleted = 0
        for file_path in Path(recycle_bin).glob("*"):
            if file_path.stat().st_mtime < cutoff:
                try:
                    file_path.unlink()
                    deleted += 1
                except Exception:
                    logger.error(f"Failed to cleanup: {file_path}")
        
        logger.info(f"Cleaned {deleted} files from recycle bin")
        return deleted

