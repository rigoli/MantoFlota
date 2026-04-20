"""initial schema unidades y mantenimientos

Revision ID: 001_initial
Revises:
Create Date: 2026-04-19

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_initial"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "unidades",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("numero_economico", sa.String(length=64), nullable=False),
        sa.Column("placas", sa.String(length=32), nullable=False),
        sa.Column("marca", sa.String(length=128), nullable=False),
        sa.Column("modelo", sa.String(length=128), nullable=False),
        sa.Column("anio", sa.Integer(), nullable=False),
        sa.Column("tipo_vehiculo", sa.String(length=64), nullable=False),
        sa.Column("kilometraje_actual", sa.Integer(), nullable=False),
        sa.Column("estado", sa.String(length=20), nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_unidades_numero_economico"),
        "unidades",
        ["numero_economico"],
        unique=True,
    )
    op.create_index(
        op.f("ix_unidades_placas"), "unidades", ["placas"], unique=True
    )

    op.create_table(
        "mantenimientos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("unidad_id", sa.Integer(), nullable=False),
        sa.Column("tipo", sa.String(length=128), nullable=False),
        sa.Column("fecha_servicio", sa.Date(), nullable=False),
        sa.Column("kilometraje", sa.Integer(), nullable=False),
        sa.Column("costo", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("proveedor", sa.String(length=256), nullable=False),
        sa.Column("observaciones", sa.Text(), nullable=True),
        sa.Column("responsable", sa.String(length=128), nullable=False),
        sa.Column(
            "creado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "actualizado_en",
            sa.DateTime(timezone=True),
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["unidad_id"], ["unidades.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        mysql_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index(
        op.f("ix_mantenimientos_unidad_id"),
        "mantenimientos",
        ["unidad_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_mantenimientos_unidad_id"), table_name="mantenimientos")
    op.drop_table("mantenimientos")
    op.drop_index(op.f("ix_unidades_placas"), table_name="unidades")
    op.drop_index(op.f("ix_unidades_numero_economico"), table_name="unidades")
    op.drop_table("unidades")
