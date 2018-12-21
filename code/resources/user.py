import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
	parser = reqparse.RequestParser()

	parser.add_argument(
			'username', required=True, help="Username is required"
		)
	parser.add_argument(
			'password', required=True, help="Password is required"
		)

	def post(self):
		
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		data = UserRegister.parser.parse_args()

		if UserModel.find_by_username(data['username']):
			return {"message": "User %s already exists" %(data['username'])}

		query = "INSERT INTO users values (NULL, ?, ?)"
		cursor.execute(query, (data['username'], data['password'],)), 400
			
		connection.commit()
		connection.close()

		return {"message": "User is successfully registered."}, 201


