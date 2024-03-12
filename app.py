from flask import Flask, request, jsonify
from models.meal import Meal
from database import db
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@127.0.0.1:3306/daily-diet'

db.init_app(app)

@app.route('/meal', methods=["POST"])
def create_meal():
  data = request.json
  name = data.get("name")
  description = data.get("description")
  date = data.get("date")
  fit = data.get("fit")

  if name and description and date:
    local_dt = datetime.strptime(date, "%d/%m/%Y %H:%M:%S")
    meal = Meal(name=name, description=description, date=local_dt, fit=fit)
    db.session.add(meal)
    db.session.commit()
    return jsonify({"message": "Refeicao cadastrada com sucesso"})

  return jsonify({"message": "Dados invalidos"}), 400

@app.route('/meals', methods=["GET"])
def list_meals():
  meals = Meal.query.all()
  
  meal_data = [meal.to_dict() for meal in meals]
  
  if meals:
    return meal_data
    
  return jsonify({"message": "Nenhuma refeicao cadastrada"}), 404

@app.route('/meal/<int:meal_id>', methods=["GET"])
def list_meal(meal_id):
  meal = Meal.query.get(meal_id)
  
  if meal:
    return meal.to_dict()

  return jsonify({"message": "Refeicao não encontrada"}), 404

@app.route('/meal/<int:meal_id>', methods=["PUT"])
def update_meal(meal_id):
  data = request.json
  meal = Meal.query.get(meal_id)
  
  if data.get("name") or data.get("description") or data.get("date"):
    local_dt = datetime.strptime(data.get("date"), "%d/%m/%Y %H:%M:%S")
    
    meal.name = data.get("name")
    meal.description = data.get("description")
    meal.date = local_dt
    db.session.commit()

    return jsonify({"message": f"Refeicao {meal_id} atualizada com sucesso"})

  return jsonify({"message": "Refeicao não encontrada"}), 404

@app.route('/meal/<int:meal_id>', methods=["DELETE"])
def delete_meal(meal_id):
  meal = Meal.query.get(meal_id)

  if meal:
    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": f"Refeicao {meal_id} deletada com sucesso"})

  return jsonify({"message": "Refeicao não encontrada"}), 404

if __name__ == '__main__':
  app.run(debug=True)