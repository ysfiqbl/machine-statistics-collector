"""create statistics and emails tables

Revision ID: 18c94242195f
Revises: 
Create Date: 2017-12-15 19:37:51.085509

"""
import datetime
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '18c94242195f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    statistics_table = op.create_table('statistics',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('ip', sa.String(15), nullable=False),
        sa.Column('response', sa.String(150)),
        sa.Column('created_on', sa.DateTime(), default=datetime.datetime.now),
        sa.Column('updated_on', sa.DateTime(), onupdate=datetime.datetime.now)
    )

    emails_table = op.create_table('emails',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('to', sa.String(50), nullable=False),
        sa.Column('sender', sa.String(50), nullable=False),
        sa.Column('message', sa.String(200)),
        sa.Column('status', sa.Integer),
        sa.Column('retry_count', sa.Integer, default=0),
        sa.Column('created_on', sa.DateTime(), default=datetime.datetime.now),
        sa.Column('updated_on', sa.DateTime(), onupdate=datetime.datetime.now)
    )

    op.bulk_insert(statistics_table, [
        {'ip': '172.24.0.2', 'response': '{"disk":7.3,"cpu":100.0,"memory":56.2}'},
        {'ip': '172.24.0.3', 'response': '{"disk":7.3,"cpu":100.0,"memory":56.2}'},
        {'ip': '172.24.0.4', 'response': '{"disk":7.3,"cpu":100.0,"memory":56.2}'},
        {'ip': '172.24.0.5', 'response': '{"disk":7.3,"cpu":100.0,"memory":56.2}'},
        {'ip': '172.24.0.6', 'response': '{"disk":7.3,"cpu":100.0,"memory":56.2}'}
    ])

    op.bulk_insert(emails_table, [
        {'to': 'ysf.iqbl@gmail.com', 'sender': 'noreply@mstats.com', 'message': 'No alerts for 172.24.0.2 on 2017-Dec-11 @ 17:00 PST', 'status': 1 },
        {'to': 'ysf.iqbl@gmail.com', 'sender': 'noreply@mstats.com', 'message': 'No alerts for 172.24.0.2 on 2017-Dec-11 @ 17:00 PST', 'status': 2 },
        {'to': 'ysf.iqbl@gmail.com', 'sender': 'noreply@mstats.com', 'message': 'No alerts for 172.24.0.2 on 2017-Dec-11 @ 17:00 PST', 'status': 3 },
        {'to': 'ysf.iqbl@gmail.com', 'sender': 'noreply@mstats.com', 'message': 'No alerts for 172.24.0.2 on 2017-Dec-11 @ 17:00 PST', 'status': 4, 'retry_count': 4 },
        {'to': 'ysf.iqbl@gmail.com', 'sender': 'noreply@mstats.com', 'message': 'No alerts for 172.24.0.2 on 2017-Dec-11 @ 17:00 PST', 'status': 4, 'retry_count': 5 }
    ])
    

def downgrade():
    op.drop_table('statistics')
    op.drop_table('emails')
