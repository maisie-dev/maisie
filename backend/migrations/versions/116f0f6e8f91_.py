"""Initial database schema: incl. models and empty tables for users, projects and workspaces

Revision ID: 116f0f6e8f91
Revises: 
Create Date: 2019-03-24 18:17:07.183185

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "116f0f6e8f91"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "models",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "hyperparameters", postgresql.JSONB(astext_type=sa.Text()), nullable=True
        ),
        sa.Column("parameters", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("name", sa.String(length=40), nullable=True),
        sa.Column("path", sa.Text(), nullable=True),
        sa.Column("dataset_name", sa.String(length=120), nullable=True),
        sa.Column("dataset_description", sa.Text(), nullable=True),
        sa.Column("private", sa.Boolean(), nullable=True),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_model_hyperparameters",
        "models",
        ["hyperparameters"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_index(
        "ix_model_parameters",
        "models",
        ["parameters"],
        unique=False,
        postgresql_using="gin",
    )
    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "workspaces",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("workspaces")
    op.drop_table("users")
    op.drop_table("projects")
    op.drop_index("ix_model_parameters", table_name="models")
    op.drop_index("ix_model_hyperparameters", table_name="models")
    op.drop_table("models")
    # ### end Alembic commands ###