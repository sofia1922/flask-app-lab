from flask import render_template, request, redirect, url_for, flash, abort, jsonify
from sqlalchemy import select
from app import db
from app.posts import post_bp
from app.posts.models import Post
from app.posts.forms import PostForm

@post_bp.route('/')
def all_posts():
    stmt = select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template('posts/all_posts.html', posts=posts, title="Усі пости")

@post_bp.route('/<int:id>')
def detail_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
    return render_template('posts/detail_post.html', post=post, title=post.title)

@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data
        )
        db.session.add(post)
        db.session.commit()
        flash("Пост успішно створено!", "success")
        return redirect(url_for("post_bp.all_posts"))
    return render_template("posts/add_post.html", form=form, page_title="Створити пост")

@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        flash("Пост оновлено успішно!", "success")
        return redirect(url_for('post_bp.detail_post', id=post.id))
    return render_template('posts/add_post.html', form=form, title="Редагування поста")

@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Пост видалено успішно!", "danger")
        return redirect(url_for('post_bp.all_posts'))
    return render_template('posts/delete_confirm.html', post=post)
