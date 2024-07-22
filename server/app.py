from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
# 配置mysql 连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ez@localhost:3306/userdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭追踪修改的配置
# 做一个数据库手柄
db = SQLAlchemy(app)

# 在前端请求后端服务时，需要配置CORS
CORS(app)

# 创建user类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.Enum('male','female'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

# 接下来都是路由，命名规则按照题目中的要求
@app.route('/get_user_list', methods=['GET'])
def get_user():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'gender': user.gender
    } for user in users])

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
