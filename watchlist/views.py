from watchlist import app,db
from flask import request,redirect,url_for,flash,render_template
from flask_login import current_user,login_user,logout_user,login_required
from watchlist.models import User,Ariticles




# 首页
@app.route('/',methods=['GET','POST'])
def index():
	movies = Ariticles.query.all()
	return render_template('index.html',movies=movies)


# 添加博文信息
@app.route('/movie/add',methods=['GET','POST'])
def add():
	if request.method == 'POST':
		if not current_user.is_authenticated:
			return redirect(url_for('index'))
		# 获取表单数据
		title = request.form.get('title')
		content = request.form.get('content')
		author = request.form.get('author')

		# 验证各字段不为空，并且title长度不大于60，pubdate长度不大于8
		if not title or not content or not author:
			flash('输入错误')	# 错误提示
			return redirect(url_for('add'))	# 重定向返回主页

		movie = Ariticles(title=title,content=content,author=author)	# 创建记录
		db.session.add(movie)	# 添加到数据库会话
		db.session.commit()	# 提交数据库会话
		flash('数据创建成功')
		return redirect(url_for('index'))

	movies = Ariticles.query.all()
	return render_template('add.html',movies=movies)


# 编辑博文信息页面
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
@login_required
def edit(movie_id):
	movie = Ariticles.query.get_or_404(movie_id)

	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']

		if not title or not content:
			flash('输入错误')
			return redirect(url_for('edit'),movie_id=movie_id)

		movie.title = title
		movie.content = content

		db.session.commit()
		flash('博文信息已经更新')
		return redirect(url_for('index'))
	return render_template('edit.html',movie=movie)


@app.route('/settings',methods=['GET','POST'])
@login_required
def settings():
	if request.method == 'POST':
		name = request.form['name']

		if not name or len(name)>20:
			flash('输入错误')
			return redirect(url_for('settings'))

		current_user.name = name
		db.session.commit()
		flash('设置name成功')
		return redirect(url_for('index'))

	return render_template('settings.html')

# 删除信息
@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
@login_required
def delete(movie_id):
	movie = Ariticles.query.get_or_404(movie_id)
	db.session.delete(movie)
	db.session.commit()
	flash('删除数据成功')
	return redirect(url_for('index'))


# 用户登录flask提供的login_user()函数
@app.route('/login',methods=['GET','POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if not username or not password:
			flash('输入错误')
			return redirect(url_for('login'))
		user = User.query.first()
		if username == user.username and user.validate_password(password):
			login_user(user)  # 登录用户
			flash('登录成功')
			return redirect(url_for('index'))   # 登录成功返回首页
		flash('用户名或密码出入错误')
		return redirect(url_for('login'))
	return render_template('login.html')


# 用户登出
@app.route('/logout')
def logout():
	logout_user()
	flash('退出登录')
	return redirect(url_for('index'))



