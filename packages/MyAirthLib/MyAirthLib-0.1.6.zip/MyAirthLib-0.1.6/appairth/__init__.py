from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object("config")

from app.module_add.controllers import module_add

app.register_blueprint(module_add)