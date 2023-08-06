# -*- coding: utf-8 -*-

from flask import _app_ctx_stack
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import NullPool


def _get_db_session_cls(url, poolclass=None, echo=False):
    """This will return session class to create session to the database.

    Note that this function doesn't return session object but session class.

    """
    eng = engine_from_config({
        'sqlalchemy.url': url,
        'sqlalchemy.poolclass': poolclass or NullPool,
        'sqlalchemy.echo': echo,
        'sqlalchemy.convert_unicode': True
    })

    Session = scoped_session(sessionmaker(bind=eng))

    return Session


def get_db_session():
    """This will return session object.

    Also this will register the session object and session class
    into the flask context.

    """
    ctx = _app_ctx_stack.top
    db_session = getattr(ctx, 'flachemy_db_session', None)
    if db_session is None:
        db_session_cls = getattr(ctx, 'flachemy_db_session_cls', None)
        if db_session_cls is None:
            db_session_cls = _get_db_session_cls(
                url=ctx.app.config['FLACHEMY_DATABASE_URI'],
                echo=ctx.app.config['FLACHEMY_ECHO'],
            )
            ctx.db_session_cls = db_session_cls
        db_session = db_session_cls()
        ctx.db_session = db_session
    return db_session


def init_app(app):
    """Initialized flask application object.

    app = flask.Flask(__name__)
    init_app(app)

    """
    app.teardown_appcontext(remove_db_session)


def remove_db_session(error=None):
    """Getting rid of database_session this library created"""
    db_session = getattr(_app_ctx_stack.top, 'flachemy_db_session', None)
    if db_session is not None:
        db_session.close()
    db_session_cls = getattr(_app_ctx_stack.top, 'flachemy_db_session_cls', None)
    if db_session_cls is not None:
        db_session_cls.remove()

