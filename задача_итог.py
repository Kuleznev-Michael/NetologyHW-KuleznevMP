import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import re

# Файл для хранения задач
TASKS_FILE = "tasks.txt"


class Task:
    def __init__(self, title, priority, isDone=False, id=None):
        self.id = id
        self.title = title
        self.priority = priority
        self.isDone = isDone

    def to_dict(self):
        # Преобразуем задачу в словарь
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "isDone": self.isDone
        }

    @classmethod
    def from_dict(cls, data):
        # Создаем задачу из словаря
        task_id = data["id"]
        if isinstance(task_id, str):
            # Пробуем преобразовать строку в число
            try:
                task_id = int(task_id)
            except ValueError:
                # Если это UUID или другая строка, генерируем новый числовой ID
                task_id = None

        return cls(
            id=task_id,
            title=data["title"],
            priority=data["priority"],
            isDone=data["isDone"]
        )


class TodoServer(BaseHTTPRequestHandler):
    tasks = []
    next_id = 1

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            try:
                with open(TASKS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = []

                    for task_data in data:
                        try:
                            task = Task.from_dict(task_data)
                            self.tasks.append(task)
                        except (KeyError, ValueError) as e:
                            print(f"Ошибка загрузки задачи: {e}, данные: {task_data}")
                            continue

                    # Поиск максимального уже существующего id
                    numeric_ids = []
                    for task in self.tasks:
                        if task.id is not None and isinstance(task.id, int):
                            numeric_ids.append(task.id)

                    if numeric_ids:
                        self.next_id = max(numeric_ids) + 1
                        print(f"Найден максимальный ID: {max(numeric_ids)}, следующий: {self.next_id}")
                    else:
                        self.next_id = 1
                        print("Не найдено числовых ID, начинаем с 1")

            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Ошибка загрузки файла: {e}")
                self.tasks = []
                self.next_id = 1
        else:
            print("Файл tasks.txt не найден, начинаем с пустого списка")
            self.tasks = []
            self.next_id = 1

    def save_tasks(self):
        # Сохраняем задачи в файл
        with open(TASKS_FILE, 'w', encoding='utf-8') as f:
            tasks_dict = [task.to_dict() for task in self.tasks]
            json.dump(tasks_dict, f, ensure_ascii=False, indent=2)

    def do_GET(self):
        # Обработка GET запросов
        parsed_path = urlparse(self.path)

        # Получение списка всех задач
        if parsed_path.path == "/tasks":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            tasks_dict = [task.to_dict() for task in self.tasks]
            response = json.dumps(tasks_dict, ensure_ascii=False).encode('utf-8')
            self.wfile.write(response)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        # Обработка POST запросов
        parsed_path = urlparse(self.path)

        # Создание новой задачи
        if parsed_path.path == "/tasks":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode('utf-8'))

                # Проверяем обязательные поля
                if 'title' not in data or 'priority' not in data:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = json.dumps({"error": "Title and priority are required"})
                    self.wfile.write(response.encode('utf-8'))
                    return

                # Проверяем валидность приоритета
                if data['priority'] not in ['low', 'normal', 'high']:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = json.dumps({"error": "Priority must be 'low', 'normal' or 'high'"})
                    self.wfile.write(response.encode('utf-8'))
                    return
                self.load_tasks() # Я не знаю как зачем и почему, но без этого не работает
                # next_id где-то откатывается до состояния при последнем запуске сервера
                # хотя это должно происходить только в самой load_tasks, и почему тогда её вызов всё чинит?

                new_task = Task(
                    id=self.next_id,
                    title=data['title'],
                    priority=data['priority'],
                    isDone=False
                )
                print(f"Создана задача с ID: {self.next_id}")
                self.next_id += 1

                self.tasks.append(new_task)
                self.save_tasks()

                # Отправляем ответ
                self.send_response(201)  # 201 Created
                self.send_header('Content-type', 'application/json')
                self.end_headers()

                response = json.dumps(new_task.to_dict(), ensure_ascii=False).encode('utf-8')
                self.wfile.write(response)

            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = json.dumps({"error": "Invalid JSON"})
                self.wfile.write(response.encode('utf-8'))

        # Отметка о выполнении задачи
        elif re.match(r"/tasks/\d+/complete", parsed_path.path):
            match = re.search(r"/tasks/(\d+)/complete", parsed_path.path)
            if match:
                task_id = int(match.group(1))  # ID как число

                # Поиск задачи с таким ID
                task_found = False
                for task in self.tasks:
                    if task.id == task_id:
                        task.isDone = True
                        task_found = True
                        self.save_tasks()
                        print(f"Задача {task_id} отмечена как выполненная")
                        break

                if task_found:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'')
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Task not found')
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Not Found')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def log_message(self, format, *args):
        print(f"{self.address_string()} - - [{self.log_date_time_string()}] {format % args}")


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TodoServer)

    TodoServer.load_tasks(TodoServer)

    print(f"Server running on port {port}")
    print(f"Tasks file: {TASKS_FILE}")
    print("Все ID будут числовыми (1, 2, 3, ...)")
    print("Endpoints:")
    print("  GET  /tasks - get all tasks")
    print("  POST /tasks - create new task (JSON body: title, priority)")
    print("  POST /tasks/{id}/complete - mark task as complete")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        httpd.server_close()


if __name__ == "__main__":
    run_server()