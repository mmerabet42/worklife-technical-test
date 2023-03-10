"""3: Cascade all,delete for relationships

Revision ID: b70e4e1f8862
Revises: ffd12f1a3a13
Create Date: 2023-03-14 00:08:21.646992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b70e4e1f8862'
down_revision = 'ffd12f1a3a13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('balance_employee_id_fkey', 'balance', type_='foreignkey')
    op.drop_constraint('balance_vacation_type_id_fkey', 'balance', type_='foreignkey')
    op.create_foreign_key(None, 'balance', 'employee', ['employee_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'balance', 'vacation_type', ['vacation_type_id'], ['id'], ondelete='cascade')
    op.drop_constraint('vacation_employee_id_fkey', 'vacation', type_='foreignkey')
    op.drop_constraint('vacation_vacation_type_id_fkey', 'vacation', type_='foreignkey')
    op.create_foreign_key(None, 'vacation', 'vacation_type', ['vacation_type_id'], ['id'], ondelete='cascade')
    op.create_foreign_key(None, 'vacation', 'employee', ['employee_id'], ['id'], ondelete='cascade')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'vacation', type_='foreignkey')
    op.drop_constraint(None, 'vacation', type_='foreignkey')
    op.create_foreign_key('vacation_vacation_type_id_fkey', 'vacation', 'vacation_type', ['vacation_type_id'], ['id'])
    op.create_foreign_key('vacation_employee_id_fkey', 'vacation', 'employee', ['employee_id'], ['id'])
    op.drop_constraint(None, 'balance', type_='foreignkey')
    op.drop_constraint(None, 'balance', type_='foreignkey')
    op.create_foreign_key('balance_vacation_type_id_fkey', 'balance', 'vacation_type', ['vacation_type_id'], ['id'])
    op.create_foreign_key('balance_employee_id_fkey', 'balance', 'employee', ['employee_id'], ['id'])
    # ### end Alembic commands ###
