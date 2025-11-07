from flask import render_template, request, redirect, url_for, flash, abort
from app import db
from app.posts import post_bp
from app.posts.models import Post
from app.posts.forms import PostForm
from flask import jsonify

@post_bp.route('/')
def all_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template('posts/all_posts.html', posts=posts, title="Усі пости")

@post_bp.route('/<int:id>')
def detail_post(id):
    post = Post.query.get_or_404(id)
    return render_template('posts/detail_post.html', post=post, title=post.title)

@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

   

        post = Post(title=title, content=content)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post_bp.all_posts'))

    return render_template("posts/add_post.html", form=form, page_title="Create Post")

@post_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)
    form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        db.session.commit()
        flash("Post updated successfully", "success")
        return redirect(url_for('post_bp.detail_post', id=post.id))
    return render_template('posts/add_post.html', form=form, title="Edit Post")

@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted successfully", "danger")
        return redirect(url_for('post_bp.all_posts'))
    return render_template('posts/delete_confirm.html', post=post)
