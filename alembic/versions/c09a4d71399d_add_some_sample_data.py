"""Add some sample data

Revision ID: c09a4d71399d
Revises: 1ea7e03e9d96
Create Date: 2020-09-22 23:43:27.133070

"""
from alembic import op
import sqlalchemy as sa
from auth.models import make_totp_secret
from auth.pwd_context import get_password_hash


# revision identifiers, used by Alembic.
revision = "c09a4d71399d"
down_revision = "1ea7e03e9d96"
branch_labels = None
depends_on = None

bind = op.get_bind()

Users = sa.Table(
    "user",
    sa.MetaData(),
    sa.Column("id", sa.Integer(), primary_key=True),
    sa.Column("username", sa.String()),
    sa.Column("password", sa.String()),
    sa.Column("totp_secret", sa.String()),
)


def upgrade():
    bind.execute(
        Users.insert().values(
            id=1337,
            username="icebreaker",
            password=get_password_hash("swordsfish"),
            totp_secret=make_totp_secret(),
        )
    )


def downgrade():
    bind.execute(Users.delete())
