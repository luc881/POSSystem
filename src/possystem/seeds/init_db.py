# possystem/scripts/init_db.py

from sqlalchemy.orm import Session
from possystem.db.session import SessionLocal

from possystem.seeds.seed_permissions import seed_permissions
from possystem.seeds.seed_roles import seed_roles
from possystem.seeds.seed_superuser import seed_superuser

def init_db():
    """Ejecuta todos los seeders del proyecto en orden correcto."""
    db: Session = SessionLocal()
    try:
        print("🔹 Iniciando seeding de permisos...")
        seed_permissions(db)

        print("🔹 Iniciando seeding de roles...")
        seed_roles(db)

        print("🔹 Creando superusuario...")
        seed_superuser(db)

        print("🎉 Base de datos inicializada correctamente.")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
