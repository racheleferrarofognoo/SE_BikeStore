from database import dao
from model import model

dao = dao.DAO()
model = model.Model()

print(dao.get_category())