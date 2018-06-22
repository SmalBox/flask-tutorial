# __init__.py 
# Contain the application factory and tells python that
# the flaskr directory should be treated as a package

import os

from flask import Flask

def create_app(test_config=None):
	# create and configure the app
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_mapping(
		SECRET_KEY='dev',	
		DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
	)


	if test_config is None:
		# Load the instance config, if it exists, when not testing
		app.config.from_pyfile('config.py', silent=True)
	else:
		# Load the test config if passed in
		app.config.from_mapping(test_config)
	
	# ensure the instance folder exists
	try:
		os.makedirs(app.instance_path)
	except OSError:
		pass
	
	# a simple page that says hello
	@app.route('/hello')
	def hello():
		return 'Hello, World!'

	#Import and call this function from the factory
	from flaskr import db
	db.init_app(app)

	#import and register blueprint
	from flaskr import auth, blog
	app.register_blueprint(auth.bp)

	app.register_blueprint(blog.bp)

	# make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
	app.add_url_rule('/', endpoint='index')

	return app
