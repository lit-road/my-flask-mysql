from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ez@localhost:3306/userdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭追踪修改的配置
db = SQLAlchemy(app)

CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.Enum('male','female'), nullable=False)

    # Q: What is __repr__?
    # A: __repr__ is a special method in Python that is called by the repr() built-in function to get a string representation of the object for debugging. If the __repr__ method is not defined for an object, the default implementation is used which returns a string in the format <__main__.ClassName object at 0x0000021D2A1A4E80>.
    def __repr__(self):
        return '<User %r>' % self.name

# @app.route('/user', methods=['GET'])
@app.route('/get_user_list', methods=['GET'])
def get_user():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'gender': user.gender
    } for user in users])

# @app.route('/user/add', methods=['POST'])
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    user = User(name=data['name'], gender=data['gender'])
    db.session.add(user)
    # 成功新增資料後，必須執行 db.session.commit() 才會將資料寫入資料庫
    db.session.commit()
    return jsonify({
        'message': 'User added successfully',
    })

# @app.route('/user/update/<int:id>', methods=['PUT'])
@app.route('/edit_user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    data = request.json
    if user is None:
        return jsonify({
            'message': 'User not found',
        }), 404
    user.name = data['name']
    user.gender = data['gender']
    db.session.commit()
    return jsonify({
        'message': 'User updated successfully',
    })

@app.route('/user/delete/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user is None:
        return jsonify({
            'message': 'User not found',
        }), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        'message': 'User deleted successfully',
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000, host='0.0.0.0')
