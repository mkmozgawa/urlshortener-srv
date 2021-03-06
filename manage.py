import flask.cli

from src import create_app, db
from src.api.models import Url

app = create_app()
cli = flask.cli.FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    cli()
