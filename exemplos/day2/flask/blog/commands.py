import click
from blog.posts import (get_all_posts, get_post_by_slug, new_post,
                        update_by_slug)
from flask import Flask


@click.group()
def post():
    """Manage blog posts."""


@post.command()
@click.option("--title")
@click.option("--content")
def new(title, content):
    """Add new post to database"""
    try:
        if title and content:
            new = new_post(title, content)
            click.echo(f"New post created {new}")
        else:
            print(f'Title: {title} or Content {content} is missing.')
    except Exception as e:
        print(e)


@post.command("list")
def _list():
    """List all posts"""
    for post in get_all_posts():
        click.echo(post)
        click.echo("-" * 30)  # rich


@post.command()
@click.argument("slug")
def get(slug):
    """Get post by slug"""
    post = get_post_by_slug(slug)
    click.echo(post or "post not found")


@post.command()
@click.argument("slug")
@click.option("--content", default=None, type=str)
@click.option("--published", default=None, type=str)
def update(slug, content, published):
    """Update post by slug"""
    data = {}
    if content is not None:
        data["content"] = content
    if published is not None:
        data["published"] = published.lower() == "true"

    update_by_slug(slug, data)
    click.echo("Post updated")

# Todo - deletar ou despublicar um post


def configure(app: Flask):
    app.cli.add_command(post)
