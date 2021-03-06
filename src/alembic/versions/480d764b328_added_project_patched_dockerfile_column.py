"""Added Project.patched_dockerfile column

Revision ID: 480d764b328
Revises: 11d6a165138
Create Date: 2015-04-27 22:41:21.777333

"""

# revision identifiers, used by Alembic.
revision = '480d764b328'
down_revision = '11d6a165138'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('patched_dockerfile', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'patched_dockerfile')
    ### end Alembic commands ###
