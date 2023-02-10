from datetime import datetime

from blog.database import mongo
from flask import Flask
from flask_admin import Admin
from flask_admin.base import AdminIndexView
from flask_admin.contrib.pymongo import ModelView
from flask_simplelogin import login_required
from wtforms import fields, form, validators

from .utils.functions import prepare_slug

# decorate Flask-Admin view via Monkey Patching
AdminIndexView._handle_view = login_required(AdminIndexView._handle_view)
ModelView._handle_view = login_required(ModelView._handle_view)


class PostsForm(form.Form):
    title = fields.StringField("Title", [validators.data_required()])
    slug = fields.HiddenField("Slug")
    content = fields.TextAreaField("Content")
    published = fields.BooleanField("Published", default=True)


class AdminPosts(ModelView):
    column_list = ("title", "slug", "published", "date")
    form = PostsForm

    def on_model_change(self, form, post, is_created):

        post["slug"] = prepare_slug(post["title"])

        if mongo.db.posts.find_one({"slug": post["slug"]}):
            print("Post not created! This post already exists!")

        else:
            if is_created:
                post["date"] = datetime.now()


def configure(app):
    admin = Admin(
        app,
        name=app.config.get("TITLE"),
        template_mode="bootstrap4"
        )
    admin.add_view(AdminPosts(mongo.db.posts, "Posts"))
