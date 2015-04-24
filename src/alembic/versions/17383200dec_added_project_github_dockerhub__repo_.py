"""Added Project.{github,dockerhub}_repo_exists columns

Revision ID: 17383200dec
Revises: 257ba619bb7
Create Date: 2015-04-24 10:18:01.486026

"""

# revision identifiers, used by Alembic.
revision = '17383200dec'
down_revision = '257ba619bb7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('dockerhub_repo_exists', sa.Boolean(), nullable=True))
    op.add_column('project', sa.Column('github_repo_exists', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'github_repo_exists')
    op.drop_column('project', 'dockerhub_repo_exists')
    ### end Alembic commands ###