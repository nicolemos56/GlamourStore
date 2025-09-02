#!/usr/bin/env python3
"""
Script para remover ícones de estrela das categorias
"""
from app import app
from database import *
from models import *

def clean_category_names():
    with app.app_context():
        # Buscar todas as categorias
        categories = Category.query.all()
        
        for category in categories:
            # Remover vários tipos de ícones de estrela
            clean_name = category.name
            
            # Remover ícones de estrela comuns
            stars_to_remove = ['⭐', '★', '✨', '🌟', '*']
            for star in stars_to_remove:
                clean_name = clean_name.replace(star, '').strip()
            
            # Remover ícones HTML
            clean_name = clean_name.replace('&#9733;', '').strip()
            
            # Limpar espaços extras
            clean_name = ' '.join(clean_name.split())
            
            if clean_name != category.name:
                print(f"Alterando '{category.name}' para '{clean_name}'")
                category.name = clean_name
        
        # Salvar mudanças
        db.session.commit()
        print("Categorias limpas com sucesso!")

if __name__ == '__main__':
    clean_category_names()