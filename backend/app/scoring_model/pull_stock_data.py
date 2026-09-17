from pathlib import Path
from app.services.yahoo import get_company_data

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data/returns"


cvx = get_company_data("cvx")

print(cvx)
