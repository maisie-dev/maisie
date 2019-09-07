"""Add checksum

Revision ID: edd840572e9a
Revises: c18f4388a034
Create Date: 2019-08-25 19:10:18.698176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "edd840572e9a"
down_revision = "c18f4388a034"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("models", sa.Column("checksum", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("models", "checksum")
    # ### end Alembic commands ###