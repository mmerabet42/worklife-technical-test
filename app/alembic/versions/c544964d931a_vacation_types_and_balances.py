"""Vacation Types and Balances

Revision ID: c544964d931a
Revises: f7186c348c68
Create Date: 2023-03-13 01:55:46.900773

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

import app

# revision identifiers, used by Alembic.
revision = 'c544964d931a'
down_revision = 'f7186c348c68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vacation_type',
    sa.Column('id', app.model.base.CustomUUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_vacation_type_id'), 'vacation_type', ['id'], unique=False)
    op.create_table('balance',
    sa.Column('id', app.model.base.CustomUUID(as_uuid=True), nullable=False),
    sa.Column('employee_id', app.model.base.CustomUUID(as_uuid=True), nullable=True),
    sa.Column('vacation_type_id', app.model.base.CustomUUID(as_uuid=True), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employee_id'], ['employee.id'], ),
    sa.ForeignKeyConstraint(['vacation_type_id'], ['vacation_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('employee_id', 'vacation_type_id')
    )
    op.create_index(op.f('ix_balance_id'), 'balance', ['id'], unique=False)
    op.add_column('vacation', sa.Column('vacation_type_id', app.model.base.CustomUUID(as_uuid=True), nullable=True))
    op.create_foreign_key(None, 'vacation', 'vacation_type', ['vacation_type_id'], ['id'])
    op.drop_column('vacation', 'vacation_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vacation', sa.Column('vacation_type', postgresql.ENUM('paid_leave', 'unpaid_leave', name='vacationtypes'), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'vacation', type_='foreignkey')
    op.drop_column('vacation', 'vacation_type_id')
    op.drop_index(op.f('ix_balance_id'), table_name='balance')
    op.drop_table('balance')
    op.drop_index(op.f('ix_vacation_type_id'), table_name='vacation_type')
    op.drop_table('vacation_type')
    # ### end Alembic commands ###
