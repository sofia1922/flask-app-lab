from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import select
from app.forms import RecipeForm
from app.utils import save_recipe_image
from app.recipes.models import Recipe, Category
from app import db

recipes_bp = Blueprint("recipes", __name__, template_folder="templates")


@recipes_bp.route('/')
def index():
    search = request.args.get("q", "")
    order = request.args.get("sort", "title")

    stmt = select(Recipe)

    if search:
        stmt = stmt.where(Recipe.title.ilike(f"%{search}%"))

    if order == "time":
        stmt = stmt.order_by(Recipe.cook_time)
    else:
        stmt = stmt.order_by(Recipe.title)

    recipes = db.session.scalars(stmt).all()

    return render_template(
        "recipes/index.html",
        recipes=recipes,
        search=search,
        order=order,
        title="Рецепти"
    )


@recipes_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = RecipeForm()

    categories = db.session.scalars(select(Category)).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():

        filename = save_recipe_image(form.image.data) if form.image.data else None

        recipe = Recipe(
            title=form.title.data,
            cook_time=form.cook_time.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            image=filename,
            category_id=form.category_id.data,
            user_id=current_user.id
        )

        db.session.add(recipe)
        db.session.commit()

        flash("Рецепт успішно створено!", "success")
        return redirect(url_for('recipes.index'))

    return render_template("recipes/create.html", form=form, title="Новий рецепт")


@recipes_bp.route('/<int:recipe_id>')
def detail(recipe_id):
    recipe = db.get_or_404(Recipe, recipe_id)
    return render_template("recipes/detail.html", recipe=recipe, title=recipe.title)


@recipes_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(recipe_id):
    recipe = db.get_or_404(Recipe, recipe_id)

    if recipe.user_id != current_user.id:
        flash("⛔ Ви не можете редагувати чужий рецепт!", "danger")
        return redirect(url_for("recipes.index"))

    form = RecipeForm(obj=recipe)

    categories = db.session.scalars(select(Category)).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]

    if form.validate_on_submit():

        if form.image.data:
            recipe.image = save_recipe_image(form.image.data)

        recipe.title = form.title.data
        recipe.cook_time = form.cook_time.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        recipe.category_id = form.category_id.data

        db.session.commit()

        flash("Рецепт оновлено!", "success")
        return redirect(url_for("recipes.detail", recipe_id=recipe.id))

    return render_template("recipes/edit.html", form=form, recipe=recipe, title="Редагування")


@recipes_bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete(recipe_id):
    recipe = db.get_or_404(Recipe, recipe_id)

    if recipe.user_id != current_user.id:
        flash("⛔ Ви не можете видаляти чужий рецепт!", "danger")
        return redirect(url_for("recipes.index"))

    db.session.delete(recipe)
    db.session.commit()

    flash("Рецепт видалено!", "info")
    return redirect(url_for("recipes.index"))
