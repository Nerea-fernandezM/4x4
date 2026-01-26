import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Crear conexión a la base de datos PostgreSQL"""
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    conn = psycopg2.connect(database_url, cursor_factory=RealDictCursor)
    return conn

def read_used():
    """Leer categorías usadas de la base de datos"""
    result = {"D": [], "O": []}
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT difficulty, title, words FROM used_categories")
        rows = cur.fetchall()
        
        for row in rows:
            words = row['words'].split(',')
            title = row['title']
            result[row['difficulty']].append({title: words})
    finally:
        cur.close()
        conn.close()
    
    return result

def read_words(used):
    """Leer categorías disponibles que no han sido usadas"""
    result = {"D": [], "O": []}
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT difficulty, title, words FROM categories")
        rows = cur.fetchall()
        
        # Obtener títulos usados
        used_titles = {"D": set(), "O": set()}
        for difficulty in used:
            for item in used[difficulty]:
                used_titles[difficulty].update(item.keys())
        
        for row in rows:
            words = row['words'].split(',')
            title = row['title']
            
            if title not in used_titles[row['difficulty']]:
                result[row['difficulty']].append({title: words})
    finally:
        cur.close()
        conn.close()
    
    return result

def clean_used():
    """Limpiar la tabla de categorías usadas"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM used_categories")
        conn.commit()
    finally:
        cur.close()
        conn.close()

def save_used_category(difficulty, title, words):
    """Guardar una categoría como usada"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        words_str = ','.join(words)
        cur.execute(
            "INSERT INTO used_categories (difficulty, title, words) VALUES (%s, %s, %s)",
            (difficulty, title, words_str)
        )
        conn.commit()
    finally:
        cur.close()
        conn.close()

def save_current_game(words_dict):
    """
    Guardar el juego actual en la base de datos.
    words_dict contiene exactamente 4 categorías con sus palabras.
    Ejemplo: {'portmanteau words': ['BRUNCH', 'MOTEL', ...], ...}
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Limpiar juego anterior (eliminar la única fila si existe)
        cur.execute("DELETE FROM current_game")
        
        # Convertir el diccionario a una lista ordenada
        categories = list(words_dict.items())
        
        # Insertar el nuevo juego como UNA SOLA FILA con 4 categorías
        cur.execute("""
            INSERT INTO current_game 
            (category1_name, category1_words,
             category2_name, category2_words,
             category3_name, category3_words,
             category4_name, category4_words)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            categories[0][0], ','.join(categories[0][1]),
            categories[1][0], ','.join(categories[1][1]),
            categories[2][0], ','.join(categories[2][1]),
            categories[3][0], ','.join(categories[3][1])
        ))
        
        conn.commit()
    finally:
        cur.close()
        conn.close()

def read_current_game():
    """
    Leer el juego actual desde la base de datos.
    Retorna un diccionario con 4 categorías.
    """
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT category1_name, category1_words,
                   category2_name, category2_words,
                   category3_name, category3_words,
                   category4_name, category4_words
            FROM current_game 
            LIMIT 1
        """)
        row = cur.fetchone()
        
        if not row:
            return {}
        
        # Reconstruir el diccionario desde la fila única
        result = {
            row['category1_name']: row['category1_words'].split(','),
            row['category2_name']: row['category2_words'].split(','),
            row['category3_name']: row['category3_words'].split(','),
            row['category4_name']: row['category4_words'].split(',')
        }
        
        return result
    finally:
        cur.close()
        conn.close()