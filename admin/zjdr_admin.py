#coding=utf-8

from zjdr import app
from flask import request
import logging

from flask import render_template
from zjdr.service import get_movies, get_movie_by_code, add_movie, update_movie, search_movies

from zjdr.domain import Movie

logger = logging.getLogger('zjdr.zjdr_admin')

@app.route('/zjdr/admin/movies', methods=['POST', 'GET'])
def movies():
	try:

		movies = get_movies()
		
		return render_template('admin_movies.html', movies=movies)

	except Exception, e:
		logger.warn("/zjdr/admin/movies error:"+str(e))

		return render_template('admin_movies.html')


@app.route('/zjdr/admin/movie/search', methods=['POST', 'GET'])
def movie_search():
	try:

		word = request.args.get('word', '')
		if None==word or ''==word:
			render_template('admin_movie_search.html')

		print word

		movies = search_movies(word)
		
		return render_template('admin_movie_search.html', movies=movies)

	except Exception, e:
		logger.warn("/zjdr/admin/movie/search error:"+str(e))

		return render_template('admin_movie_search.html')


@app.route('/zjdr/admin/movie', methods=['POST', 'GET'])
def movie():
	try:
		code = request.args.get('code', '')
		movie = get_movie_by_code(code)
		
		return render_template('admin_movie.html', movie=movie)

	except Exception, e:
		logger.warn("/zjdr/admin/movie error:"+str(e))

		return render_template('admin_movie.html')



@app.route('/zjdr/admin/movie/update', methods=['GET'])
def movie_update_page():
	try:
		code = request.args.get('code', '')
		movie = get_movie_by_code(code)
		
		return render_template('admin_movie_update.html', movie=movie)

	except Exception, e:
		logger.warn("/zjdr/admin/movie error:"+str(e))

		return render_template('admin_movie.html')


@app.route('/zjdr/admin/movie/update', methods=['POST'])
def movie_update():
	try:
		code = request.args.get('code', '')

		movie = get_movie_by_code(code)

		if None == movie:
			return render_template('admin_movie.html', movie=movie)	

		# print request.form

		movie.name = request.form['name']
		movie.e_name = request.form['e_name']
		movie.aliases = request.form['aliases']
		movie.season = request.form['season']
		movie.summary = request.form['summary']
		movie.pic_url = request.form['pic_url']
		movie.all_sets = request.form['all_sets']
		movie.now_set = request.form['now_set']
		movie.is_finished = ("on"==request.form['is_finished'])
		movie.begin_time = request.form['begin_time']
		movie.update_time = request.form['update_time']
		movie.update_type = request.form['update_type']
		movie.douban_url = request.form['douban_url']
		movie.youku_url = request.form['youku_url']

		update_movie(movie.code, movie)

		return render_template('admin_movie.html', movie=movie)
		
		return render_template('admin_movie.html', movie=movie)

	except Exception, e:
		logger.warn("/zjdr/admin/movie error:"+str(e))

		return render_template('admin_movie.html')


@app.route('/zjdr/admin/movie/add', methods=['GET'])
def movie_add_page():
	try:

		return render_template('admin_movie_add.html', movie=movie)

	except Exception, e:
		logger.warn("/zjdr/admin/movie/add error:"+str(e))

		return render_template('admin_movie_add.html')




@app.route('/zjdr/admin/movie/add', methods=['POST'])
def movie_add():
	try:
		print request.form

		code = request.form['code']

		movie = get_movie_by_code(code)
		if None != movie:
			return render_template('admin_movie.html', movie=movie)	

		movie = Movie()
		movie.code = code
		movie.name = request.form['name']
		movie.e_name = request.form['e_name']
		movie.aliases = request.form['aliases']
		movie.season = request.form['season']
		movie.summary = request.form['summary']
		movie.pic_url = request.form['pic_url']
		movie.all_sets = request.form['all_sets']
		movie.now_set = request.form['now_set']
		movie.is_finished = ("on"==request.form['is_finished'])
		movie.begin_time = request.form['begin_time']
		movie.update_time = request.form['update_time']
		movie.update_type = request.form['update_type']
		movie.douban_url = request.form['douban_url']
		movie.youku_url = request.form['youku_url']

		add_movie(movie.code, movie)

		return render_template('admin_movie.html', movie=movie)

	except Exception, e:
		logger.warn("/zjdr/admin/movie/add error:"+str(e))

		return render_template('admin_movie.html')



