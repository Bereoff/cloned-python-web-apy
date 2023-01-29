
from datetime import datetime

from blog.database import mongo

from .functions import prepare_slug


def get_all_posts(published: bool = True):
    posts = mongo.db.posts.find({"published": published})
    return posts.sort("date")


def get_post_by_slug(slug: str) -> dict:
    post = mongo.db.posts.find_one({"slug": slug})
    return post


def update_by_slug(slug: str, data: dict) -> dict:
    title = data.get("title")
    if mongo.db.posts.find_one({"slug": slug}).get("title") == title:
        return mongo.db.posts.find_one_and_update(
            {"slug": slug}, {"$set": data}
        )
    else:
        new_slug = prepare_slug(title)
        if mongo.db.posts.find_one({"slug": new_slug}):
            print("Post not updated! This post already exists!")
        else:
            data.update(
                {
                    "slug": new_slug
                }
            )
            return mongo.db.posts.find_one_and_update(
                {"slug": slug}, {"$set": data}
            )


def new_post(title: str, content: str, published: bool = True) -> str:
    try:
        slug = prepare_slug(title)

        if mongo.db.posts.find_one({"slug": slug}):
            print("Post not created! This post already exists!")
        else:

            mongo.db.posts.insert_one(
                {
                    "title": title,
                    "content": content,
                    "plublished": published,
                    "slug": slug,
                    "date": datetime.now(),
                }
            )
            print("Post created with sucess!")
            return slug
    except Exception as e:
        print(e)
