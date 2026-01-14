from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# CORS aktivieren - erlaubt Zugriff von Wix/HTML-Seiten
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Später auf deine Domain beschränken
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- User Modell ---
class User(BaseModel):
    id: int
    name: str
    email: str | None = None

# ... rest bleibt gleich
# --- User Modell ---
class User(BaseModel):
    id: int
    name: str
    email: str | None = None


fake_users_db = [
    User(id=1, name="Alice Pagamory", email="alice@example.com"),
    User(id=2, name="Bob Solidarity", email="bob@example.com"),
]


# --- Pot (Topf) Modell ---
class Pot(BaseModel):
    id: int
    name: str
    description: str | None = None
    total_contributions: float = 0.0


fake_pots_db = [
    Pot(id=1, name="Gesundheitstopf", description="Für medizinische Notfälle", total_contributions=5000.0),
    Pot(id=2, name="Mobilitätstopf", description="Fahrzeugschäden und Reparaturen", total_contributions=3200.0),
]


# --- Basis-Endpoints ---
@app.get("/")
def read_root():
    return {"message": "Pagamory API läuft"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# --- User Endpoints ---
@app.get("/users", response_model=list[User])
def list_users():
    return fake_users_db


@app.get("/users/{user_id}", response_model=User | dict)
def get_user(user_id: int):
    for user in fake_users_db:
        if user.id == user_id:
            return user
    return {"error": "User not found"}


@app.post("/users", response_model=User)
def create_user(user: User):
    fake_users_db.append(user)
    return user


# --- Pot (Topf) Endpoints ---
@app.get("/pots", response_model=list[Pot])
def list_pots():
    """Gibt alle verfügbaren Solidartöpfe zurück"""
    return fake_pots_db


@app.get("/pots/{pot_id}", response_model=Pot | dict)
def get_pot(pot_id: int):
    """Gibt einen einzelnen Topf per ID zurück"""
    for pot in fake_pots_db:
        if pot.id == pot_id:
            return pot
    return {"error": "Pot not found"}


@app.post("/pots", response_model=Pot)
def create_pot(pot: Pot):
    """Erstellt einen neuen Solidartopf"""
    fake_pots_db.append(pot)
    return pot