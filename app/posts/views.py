import logging
from json import JSONDecodeError

from flask import Blueprint, render_template, request, abort
from app.posts.dao.posts_dao import PostsDAO
from app.posts.dao.comments_dao import CommentsDAO

posts_blueprint = Blueprint('posts_blueprint', __name__, template_folder='templates')
posts_dao = PostsDAO("data/posts.json")
comments_dao = CommentsDAO("data/comments.json")

logger = logging.getLogger("basic")


@posts_blueprint.route('/')
def posts_all():

    logger.debug("Запрошены все посты")
    try:
        posts = posts_dao.get_all()
        return render_template("index.html", posts=posts)
    except:
        return "Что-то пошло не так"


@posts_blueprint.route('/posts/<int:post_pk>/')
def posts_one(post_pk):

    logger.debug(f"Запрошены посты {post_pk}")

    try:
        post = posts_dao.get_by_pk(post_pk)
        comments = comments_dao.get_by_post_pk(post_pk)
    except (JSONDecodeError, FileNotFoundError) as error:
        return render_template("error.html", error=error)
    except BaseException as e:
        return render_template("error.html", error="неизвестная ошибка")

    else:
        if post is None:
            abort(404)
        number_of_comments = len(comments)
        return render_template("post.html", post=post, comments=comments, number_of_comments=number_of_comments)


@posts_blueprint.errorhandler(404)
def posts_error(e):
    return "Такой пост не найден", 404


@posts_blueprint.route('/search/')
def posts_search():
    return "Поиск по постам"


@posts_blueprint.route('/users/<username>/')
def posts_by_user(username):
    return "Поиск по пользователям"
