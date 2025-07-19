"""first

Revision ID: b2437a6523e3
Revises:
Create Date: 2022-10-28 09:35:00.424510

"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision = "b2437a6523e3"
down_revision = None
branch_labels = None
depends_on = None


def _create_updated_at_trigger() -> None:
    op.execute(
        """
    CREATE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS
    $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    )


def _timestamps() -> tuple[sa.Column, sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=func.now(),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
            server_default=func.now(),
            onupdate=func.current_timestamp(),
        ),
        sa.Column(
            "deleted_at",
            sa.TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )


def _create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, unique=False, nullable=False, index=True),
        sa.Column("email", sa.Text, unique=False, nullable=False, index=True),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("hashed_password", sa.Text),
        *_timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_user_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )
    # add default user
    op.execute(
        f"""
        INSERT INTO users (username, email, salt, hashed_password, created_at, updated_at)
        VALUES (
            'chiefaiuser@chiefai.com',
            'chiefaiuser@chiefai.com',
            '$2b$12$/inTEulyXCxuYwwqOg.o.O',
            '$2b$12$OF9AsAEX5L.fv8Zc6ZXviOfh4ufVfmeYMin6emwMqAt7yH.yc3Q.S',
            now(),
            now()
        )
        """
    )

def _create_events_table() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("event_uid", sa.Text, unique=False, nullable=False, index=True),  # UID
        sa.Column("user_id", sa.Integer, unique=False, nullable=False, index=True),  # Foreign key to users
        sa.Column("status", sa.Text, unique=False, nullable=False, index=True),  # STATUS
        sa.Column("summary", sa.Text, unique=False, nullable=False, index=False),  # SUMMARY
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),  # DTSTART
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),    # DTEND
        sa.Column("rrule", sa.Text, nullable=True),  # RRULE
        sa.Column("exdates", sa.ARRAY(sa.DateTime(timezone=True)), nullable=True),  # EXDATEs
        sa.Column("dtstamp", sa.DateTime(timezone=True), nullable=True),  # DTSTAMP
        sa.Column("event_created", sa.DateTime(timezone=True), nullable=True),  # CREATED
        sa.Column("last_modified", sa.DateTime(timezone=True), nullable=True),  # LAST-MODIFIED
        sa.Column("sequence", sa.Integer, nullable=True),  # SEQUENCE
        sa.Column("transp", sa.Text, nullable=True),  # TRANSP
        sa.Column("embedding", sa.ARRAY(sa.Float, dimensions=1), unique=False, nullable=True),  # VECTOR(1536)
        *_timestamps(),
    )
    op.execute(
        """
        CREATE TRIGGER update_event_modtime
            BEFORE UPDATE
            ON events
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    _create_updated_at_trigger()
    _create_users_table()
    _create_events_table()


def downgrade() -> None:
    op.drop_table("users")
    op.drop_table("events")
    op.execute("DROP FUNCTION update_updated_at_column")
