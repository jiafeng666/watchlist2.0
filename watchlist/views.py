import os
import sys
import click

from flask import render_template, request, url_for, flash, redirect
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movies


@app.route('/', methods=['GET', 'POST'])
def index():
    # 获取表单数据
    if request.method == 'POST':
        if not current_user.is_authenticated:   # 如果当前用户未认证
            return redirect(url_for('index'))

        title = request.form.get('title')  # 传入表单对应输入字段的name值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid Input!')  # 显示错误信息
            return redirect(url_for('index'))  # 重定向回主页

        movie = Movies.query.all()
        for m in movie:   # 判断是否已经存在
            if m.title == title:
                flash('Already Exits!')  # 显示错误信息
                return redirect(url_for('index'))  # 重定向回主页

        # 保存表单数据到数据库
        movie = Movies(title=title, year=year)
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交到数据库
        flash('Item Created!')
        return redirect(url_for('index'))

    # movies = Movies.query.all()  # 从数据库读取
    page = int(request.args.get('page', 1))   # 当前页数
    per_age = int(request.args.get('per_page', 10))  # 每页显示的条数
    paginate = Movies.query.paginate(page, per_age, error_out=False)   # error_out：是否打印错误信息
    movies = paginate.items   # 返回当前页的所有数据

    return render_template('index.html', movies=movies, paginate=paginate)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('Invalid Input.')
            return redirect(url_for('login'))

        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))

        flash('Invalid name or password.')    # 验证失败返回错误信息
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required   # 用于视图保护
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movies.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid Input!')
            return redirect(url_for('edit', movie_id=movie_id))

        movie.title = title  # 更新标题
        movie.year = year   # 更新年份
        db.session.commit()
        flash('Item Created!')
        return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)    # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def delete(movie_id):
    movie = Movies.query.get_or_404(movie_id)   # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()
    flash("Item Deleted!")
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 60:
            flash('Invalid name')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库对象，等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings success.')
        return redirect(url_for('index'))

    return render_template('settings.html')
