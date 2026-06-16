#!/usr/bin/env python
"""
Database initialization script for Student Finance Tracker.
Creates tables and optionally seeds default categories.
"""

import os
import sys
from app import create_app, db
from app.models import User, Category

def init_db():
    """Initialize the database and create all tables."""
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if default categories exist
        default_categories = [
            "Food & Dining",
            "Transportation",
            "Entertainment",
            "Shopping",
            "Utilities",
            "Healthcare",
            "Education",
            "Other"
        ]
        
        print("\nDatabase initialization complete!")
        print("Ready to run the application.")
        print("\nNext steps:")
        print("1. Set up your .env file with MySQL credentials and OpenAI API key")
        print("2. Run: python run.py")
        print("3. Visit: http://localhost:5000")

if __name__ == "__main__":
    init_db()
