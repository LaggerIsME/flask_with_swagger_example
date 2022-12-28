from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory, request
from marshmallow import Schema, fields

app = Flask(__name__, template_folder='swagger-ui/templates')


@app.route('/')
def hello_world():
    return 'Hello world'


spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)


@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


class ExampleResponseSchema(Schema):
    average_time = fields.Int()
    choices = fields.Int()


class ExampleListResponseSchema(Schema):
    user_list = fields.List(fields.Nested(ExampleResponseSchema))


class ToDoResponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()


class ToDoListResponseSchema(Schema):
    todo_list = fields.List(fields.Nested(ToDoResponseSchema))


@app.route('/example', methods=['POST'])
def example():
    """Post list of Users
            ---
            post:
                description: Post list of Users
                responses:
                    200:
                        description: Post list of Users
                        content:
                            application/json:
                                schema: ExampleListResponseSchema

        """
    average_time = request.form.get('average_time')
    choices = request.form.get('choices')
    example_data = [{'average_time':average_time}, {'choices':choices}]

    return ExampleListResponseSchema().dump({'user_list': example_data})


@app.route('/todo')
def todo():
    """Get list of Todo
        ---
        get:
            description: Get List of Todos
            responses:
                200:
                    description: Return a todo List
                    content:
                        application/json:
                            schema: ToDoListResponseSchema

    """
    dummy_data = [{
        'id': 1,
        'task': 'Finish this task',
        'status': False
    }, {
        'id': 2,
        'task': 'Finish this task',
        'status': True
    }]

    return ToDoListResponseSchema().dump({'todo_list': dummy_data})


@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger-ui/static', path)


with app.test_request_context():
    spec.path(view=todo)
    spec.path(view=example)


if __name__ == '__main__':
    app.run(debug=True)
