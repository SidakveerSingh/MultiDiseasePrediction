"""Routes package for MediScan API"""

from routes.heart import heart_bp
from routes.lung import lung_bp

__all__ = ['heart_bp', 'lung_bp']
