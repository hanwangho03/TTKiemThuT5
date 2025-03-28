from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)

# Giả lập danh sách công việc với tiến độ
tasks = [
    {"name": "Ví dụ task", "completed": False, "progress": 50}
]

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    tasks.append({"name": task, "completed": False, "progress": 0})
    return redirect('/')

@app.route('/delete/<int:index>')
def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return redirect('/')

@app.route('/update_status/<int:index>', methods=['POST'])
def update_status(index):
    data = request.get_json()
    if 0 <= index < len(tasks):
        tasks[index]['completed'] = data['completed']
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/update_progress/<int:index>', methods=['POST'])
def update_progress(index):
    data = request.get_json()
    if 0 <= index < len(tasks):
        new_progress = tasks[index]['progress'] + data['change']
        tasks[index]['progress'] = max(0, min(100, new_progress))  # Giới hạn 0-100
        return jsonify({"success": True})
    return jsonify({"success": False})
# Máy tính
@app.route('/calculator')
def calculator():
    return render_template('calculatorapp.html')
if __name__ == '__main__':
    app.run(debug=True)