from flask import Flask, abort, request, jsonify
from flask import make_response

app = Flask(__name__)

#测试数据暂时存放处
tasks=[ {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }]

@app.route('/get_task/', methods=['GET'])
def get_task():
    if not request.args or 'id' not in request.args:
        # 没有指定id则返回全部
        return jsonify(tasks)
    # else:
        # task_id = request.args['id']
        # task = filter(lambda t: t['id'] == int(task_id), tasks)
        # return jsonify(tasks)
@app.route('/get_task/<int:task_id>', methods=['GET'])
def get_taskid(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    task=list(task)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})

#使404变成更好看的json格式
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


#POST创建
@app.route('/post/', methods=['POST'])
def create_task():
    print(request.json)
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201

#put更新
@app.route('/put/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    task=list(task)
    print(task)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    print(request.json)
    if 'title' not in request.json and type(request.json['title']) != 'unicode':
        abort(400)
    if 'description' not in request.json and type(request.json['description']) is not 'unicode':
        abort(400)
    if 'done' not in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})
#删除delete
@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    task=list(task)
    if len(task) == 0:
        abort(404)
    print('-----------------------')
    tasks.remove(task[0])
    return jsonify({'result': True})



if __name__ == '__main__':
    app.run()
