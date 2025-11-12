"""
Migration script to move data from the legacy `estado` table into the
new concrete estado_* tables (one table per concrete state).

This script is idempotent and safe to run multiple times. It performs the
following steps:

1. Ensures DB tables are created (calls init_db()).
2. If a legacy `estado` table exists, reads all rows from it.
3. For each legacy estado row, creates (if missing) a row in the matching
   concrete estado_* table based on canonical name mapping.
4. Updates referencing tables `evento_sismico`, `cambio_estado` and
   `serie_temporal` to populate the new polymorphic columns
   (estado_*_tipo, estado_*_id) and cache the canonical name/ambito.
5. Optionally drops the legacy `estado` table when run with `--drop-old`.

Usage:
    python migrate_estado_to_concrete.py [--drop-old]

Note: run this while the application is not mutating the DB, or run inside
a maintenance window. Always backup the DB before running.
"""

from __future__ import annotations
import argparse
import sys
import sqlalchemy
from sqlalchemy import text
from BDD.database import engine, SessionLocal, init_db
from BDD import orm_models

# Mapping of canonical display names to target ORM mapped classes
CANONICAL_TO_ORM = {
    'Auto-detectado': orm_models.EstadoAutoDetectado,
    'AutoDetectado': orm_models.EstadoAutoDetectado,
    'Auto-confirmado': orm_models.EstadoAutoConfirmado,
    'AutoConfirmado': orm_models.EstadoAutoConfirmado,
    'Pendiente de Cierre': orm_models.EstadoPendienteDeCierre,
    'PendienteDeCierre': orm_models.EstadoPendienteDeCierre,
    'Derivado': orm_models.EstadoDerivado,
    'Confirmado por Personal': orm_models.EstadoConfirmadoPorPersonal,
    'ConfirmadoPorPersonal': orm_models.EstadoConfirmadoPorPersonal,
    'Cerrado': orm_models.EstadoCerrado,
    'Rechazado': orm_models.EstadoRechazado,
    'Bloqueado en Revisión': orm_models.EstadoBloqueadoEnRevision,
    'BloqueadoEnRevision': orm_models.EstadoBloqueadoEnRevision,
    'Pendiente de Revisión': orm_models.EstadoPendienteDeRevision,
    'PendienteDeRevision': orm_models.EstadoPendienteDeRevision,
    'SinRevision': orm_models.EstadoSinRevision,
    'Sin Revisión': orm_models.EstadoSinRevision,
}


def table_exists(name: str) -> bool:
    insp = sqlalchemy.inspect(engine)
    return insp.has_table(name)


def migrate(drop_old: bool = False) -> int:
    init_db()  # ensure new tables exist

    if not table_exists('estado'):
        print('Legacy table `estado` not found; nothing to migrate.')
        return 0

    with SessionLocal() as session:
        conn = session.connection()

        # Helper: given nombre and ambito, find target ORM class and get-or-create
        def get_or_create_by_nombre_ambito(nombre: str, ambito: str):
            orm_cls = CANONICAL_TO_ORM.get(nombre)
            if orm_cls is None:
                # Fallback: try to match by simplified name
                key = (nombre or '').replace('-', '').replace(' ', '')
                for k, v in CANONICAL_TO_ORM.items():
                    if k.replace('-', '').replace(' ', '') == key:
                        orm_cls = v
                        break

            if orm_cls is None:
                return None

            # Try to find existing row by nombre + ambito to avoid duplicates
            exists = session.query(orm_cls).filter_by(nombre_estado=nombre, ambito=ambito).first()
            if exists:
                return exists

            new = orm_cls(nombre_estado=nombre, ambito=ambito)
            session.add(new)
            session.flush()
            print(f"Created {orm_cls.__tablename__} id={new.id} for estado ('{nombre}', ambito='{ambito}')")
            return new


        # Now update referencing tables. First ensure the DB has the new
        # polymorphic/cache columns — if not, add them (SQLite supports
        # ALTER TABLE ADD COLUMN). Then update rows using raw SQL so we do
        # not trigger ORM column-mismatch errors on older schemas.
        insp = sqlalchemy.inspect(engine)

        def ensure_column(table: str, column: str, coltype: str = 'TEXT'):
            if not insp.has_table(table):
                return
            cols = [c['name'] for c in insp.get_columns(table)]
            if column not in cols:
                print(f"Adding column {table}.{column} {coltype}")
                conn.execute(text(f'ALTER TABLE {table} ADD COLUMN {column} {coltype}'))

        # Ensure columns
        if insp.has_table('evento_sismico'):
            # Only ensure cached nombre/ambito columns; we will NOT add
            # polymorphic tipo/id columns as those are being removed.
            ensure_column('evento_sismico', 'estado_actual_nombre', 'TEXT')
            ensure_column('evento_sismico', 'estado_actual_ambito', 'TEXT')

        if insp.has_table('cambio_estado'):
            ensure_column('cambio_estado', 'estado_nombre', 'TEXT')
            ensure_column('cambio_estado', 'estado_ambito', 'TEXT')

        if insp.has_table('serie_temporal'):
            ensure_column('serie_temporal', 'estado_nombre', 'TEXT')
            ensure_column('serie_temporal', 'estado_ambito', 'TEXT')

        # Helper to update a row safely
        def update_table_row(table: str, pk: int, nombre_col: str, ambito_col: str, nombre_val, ambito_val):
            conn.execute(text(f"UPDATE {table} SET {nombre_col} = :nom, {ambito_col} = :amb WHERE id = :pk"),
                         {'nom': nombre_val, 'amb': ambito_val, 'pk': pk})

        # EventoSismico: legacy fk is estado_actual_id
        if insp.has_table('evento_sismico'):
            rows = conn.execute(text('SELECT id, estado_actual_id FROM evento_sismico')).mappings().all()
            for r in rows:
                old = r['estado_actual_id']
                if old is None:
                    continue
                legacy_row = conn.execute(text("SELECT nombre_estado, ambito FROM estado WHERE id = :id"), {'id': old}).mappings().first()
                if not legacy_row:
                    continue
                nombre = legacy_row['nombre_estado']
                ambito = legacy_row['ambito']
                target = get_or_create_by_nombre_ambito(nombre, ambito)
                if target is not None:
                    update_table_row('evento_sismico', r['id'], 'estado_actual_nombre', 'estado_actual_ambito', target.nombre_estado, target.ambito)
                else:
                    update_table_row('evento_sismico', r['id'], 'estado_actual_nombre', 'estado_actual_ambito', nombre, ambito)

        # CambioEstado: legacy fk is estado_id
        if insp.has_table('cambio_estado'):
            rows = conn.execute(text('SELECT id, estado_id FROM cambio_estado')).mappings().all()
            for r in rows:
                old = r['estado_id']
                if old is None:
                    continue
                legacy_row = conn.execute(text("SELECT nombre_estado, ambito FROM estado WHERE id = :id"), {'id': old}).mappings().first()
                if not legacy_row:
                    continue
                nombre = legacy_row['nombre_estado']
                ambito = legacy_row['ambito']
                target = get_or_create_by_nombre_ambito(nombre, ambito)
                if target is not None:
                    update_table_row('cambio_estado', r['id'], 'estado_nombre', 'estado_ambito', target.nombre_estado, target.ambito)
                else:
                    update_table_row('cambio_estado', r['id'], 'estado_nombre', 'estado_ambito', nombre, ambito)

        # SerieTemporal: legacy fk is estado_id
        if insp.has_table('serie_temporal'):
            rows = conn.execute(text('SELECT id, estado_id FROM serie_temporal')).mappings().all()
            for r in rows:
                old = r['estado_id']
                if old is None:
                    continue
                legacy_row = conn.execute(text("SELECT nombre_estado, ambito FROM estado WHERE id = :id"), {'id': old}).mappings().first()
                if not legacy_row:
                    continue
                nombre = legacy_row['nombre_estado']
                ambito = legacy_row['ambito']
                target = get_or_create_by_nombre_ambito(nombre, ambito)
                if target is not None:
                    update_table_row('serie_temporal', r['id'], 'estado_nombre', 'estado_ambito', target.nombre_estado, target.ambito)
                else:
                    update_table_row('serie_temporal', r['id'], 'estado_nombre', 'estado_ambito', nombre, ambito)

        session.flush()

        session.commit()

    if drop_old:
        # Careful: drop the old table
        with engine.connect() as conn:
            conn.execute(text('DROP TABLE IF EXISTS estado'))
            print('Dropped legacy table `estado`.')

    return 0


def drop_legacy_fk_columns():
    """Attempt to drop legacy FK columns from referencing tables.

    This operation may not be supported by older SQLite versions. We try
    a DROP COLUMN and if it fails we print instructions for manual
    cleanup.
    """
    with engine.connect() as conn:
        insp = sqlalchemy.inspect(engine)
        drops = []
        if insp.has_table('evento_sismico'):
            cols = [c['name'] for c in insp.get_columns('evento_sismico')]
            if 'estado_actual_id' in cols:
                drops.append(('evento_sismico', 'estado_actual_id'))
            if 'estado_actual_tipo' in cols:
                drops.append(('evento_sismico', 'estado_actual_tipo'))
        if insp.has_table('cambio_estado'):
            cols = [c['name'] for c in insp.get_columns('cambio_estado')]
            if 'estado_id' in cols:
                drops.append(('cambio_estado', 'estado_id'))
            if 'estado_tipo' in cols:
                drops.append(('cambio_estado', 'estado_tipo'))
        if insp.has_table('serie_temporal'):
            cols = [c['name'] for c in insp.get_columns('serie_temporal')]
            if 'estado_id' in cols:
                drops.append(('serie_temporal', 'estado_id'))
            if 'estado_tipo' in cols:
                drops.append(('serie_temporal', 'estado_tipo'))

        for table, col in drops:
            try:
                print(f"Attempting to drop column {table}.{col}")
                conn.execute(text(f'ALTER TABLE {table} DROP COLUMN {col}'))
                print(f"Dropped {table}.{col}")
            except Exception as e:
                print(f"Could not drop {table}.{col}: {e}")
                print("Manual migration required: sqlite may not support DROP COLUMN; consider recreating the table without the column.")


def recreate_table_excluding_columns(tables_to_exclude: dict):
    """Recreate tables excluding the listed columns.

    tables_to_exclude: mapping table_name -> list of column names to remove
    This will:
      - back up the DB file
      - for each table: create a temporary table with same columns except the excluded ones
      - copy data from old -> temp
      - drop old table and rename temp to original

    WARNING: this operation will lose foreign key constraints and indexes on
    the recreated tables and should be run with caution. We already create a
    backup before proceeding.
    """
    # Determine DB file path for backup
    try:
        from BDD.database import engine
        db_path = engine.url.database
    except Exception:
        print("Could not determine DB file path for backup; aborting recreate operation.")
        return

    import shutil, time
    backup_path = f"{db_path}.backup.{int(time.time())}"
    try:
        shutil.copyfile(db_path, backup_path)
        print(f"Backup created at {backup_path}")
    except Exception as e:
        print(f"Failed to create backup: {e}")
        return

    conn = engine.connect()
    insp = sqlalchemy.inspect(engine)

    # We must temporarily disable foreign keys while we recreate tables
    conn.execute(text("PRAGMA foreign_keys=OFF"))

    for table, exclude_cols in tables_to_exclude.items():
        if not insp.has_table(table):
            print(f"Table {table} not found, skipping")
            continue

        cols_info = conn.execute(text(f"PRAGMA table_info('{table}')")).mappings().all()
        cols_keep = [c for c in cols_info if c['name'] not in exclude_cols]
        if not cols_keep:
            print(f"No columns left for table {table} after exclusion; skipping")
            continue

        # Collect foreign keys and indices to reapply (only those that do not
        # reference excluded columns)
        fk_rows = conn.execute(text(f"PRAGMA foreign_key_list('{table}')")).mappings().all()
        # Group fk rows by 'id' for multi-column FKs
        fk_groups = {}
        for fk in fk_rows:
            fk_id = fk['id']
            fk_groups.setdefault(fk_id, []).append(fk)

        fks_to_apply = []
        for fk_id, rows in fk_groups.items():
            from_cols = [r['from'] for r in rows]
            to_table = rows[0]['table']
            to_cols = [r['to'] for r in rows]
            on_update = rows[0].get('on_update')
            on_delete = rows[0].get('on_delete')
            # skip if any from column is excluded
            if any(c in exclude_cols for c in from_cols):
                continue
            fks_to_apply.append((from_cols, to_table, to_cols, on_update, on_delete))

        # Collect indexes
        index_list = conn.execute(text(f"PRAGMA index_list('{table}')")).mappings().all()
        indexes_to_apply = []
        for idx in index_list:
            idx_name = idx['name']
            unique = bool(idx['unique'])
            # Get index columns
            idx_info = conn.execute(text(f"PRAGMA index_info('{idx_name}')")).mappings().all()
            idx_cols = [r['name'] for r in idx_info]
            # Skip if any index column will be removed
            if any(c in exclude_cols for c in idx_cols):
                continue
            indexes_to_apply.append((idx_name, idx_cols, unique))

        # Build CREATE TABLE SQL with retained columns and applicable foreign keys
        col_defs = []
        pk_cols = []
        for c in cols_keep:
            name = c['name']
            typ = c['type'] or 'TEXT'
            notnull = ' NOT NULL' if c['notnull'] else ''
            dflt = f" DEFAULT {c['dflt_value']}" if c['dflt_value'] is not None else ''
            col_def = f"{name} {typ}{notnull}{dflt}"
            # If single PK column, mark inline
            if c['pk'] and c['name'] and sum(1 for x in cols_keep if x['pk']) == 1:
                col_def += ' PRIMARY KEY'
            col_defs.append(col_def)
            if c['pk']:
                pk_cols.append(name)

        table_level_pk = ''
        if len(pk_cols) > 1:
            table_level_pk = f", PRIMARY KEY ({', '.join(pk_cols)})"

        # Build FK clauses
        fk_clauses = []
        for (from_cols, to_table, to_cols, on_update, on_delete) in fks_to_apply:
            frm = ', '.join(from_cols)
            to = ', '.join(to_cols)
            clause = f"FOREIGN KEY ({frm}) REFERENCES {to_table} ({to})"
            if on_update and on_update.strip().upper() != '':
                clause += f" ON UPDATE {on_update}"
            if on_delete and on_delete.strip().upper() != '':
                clause += f" ON DELETE {on_delete}"
            fk_clauses.append(clause)

        all_clauses = col_defs[:]
        if table_level_pk:
            all_clauses.append(table_level_pk.lstrip(', '))
        all_clauses.extend(fk_clauses)

        tmp_name = f"{table}__new"
        create_sql = f"CREATE TABLE {tmp_name} ({', '.join(all_clauses)});"
        print(f"Creating temporary table {tmp_name} for {table}")
        conn.execute(text(create_sql))

        # Copy data
        cols_list = ', '.join([c['name'] for c in cols_keep])
        copy_sql = f"INSERT INTO {tmp_name} ({cols_list}) SELECT {cols_list} FROM {table};"
        conn.execute(text(copy_sql))

        # Drop old and rename
        conn.execute(text(f"DROP TABLE {table};"))
        conn.execute(text(f"ALTER TABLE {tmp_name} RENAME TO {table};"))
        print(f"Recreated {table} without columns: {exclude_cols}")

        # Recreate indexes
        for idx_name, idx_cols, unique in indexes_to_apply:
            cols_sql = ', '.join(idx_cols)
            uq = 'UNIQUE ' if unique else ''
            # Use same index name; if it collides, sqlite will error but that's unlikely
            create_idx = f"CREATE {uq}INDEX {idx_name} ON {table} ({cols_sql});"
            try:
                conn.execute(text(create_idx))
            except Exception as e:
                print(f"Could not recreate index {idx_name} on {table}: {e}")

    conn.execute(text("PRAGMA foreign_keys=ON"))
    conn.close()

    print('Migration finished successfully.')
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--drop-old', action='store_true', help='Drop legacy `estado` table after migration')
    parser.add_argument('--drop-legacy-fks', action='store_true', help='Attempt to drop legacy FK/tipo columns (may not be supported by SQLite)')
    parser.add_argument('--recreate-drop', action='store_true', help='Recreate referencing tables to remove legacy fk/id columns (destructive; backup will be created)')
    args = parser.parse_args()
    try:
        rc = migrate(drop_old=args.drop_old) or 0
        if args.drop_legacy_fks:
            drop_legacy_fk_columns()
        if args.recreate_drop:
            # tables -> columns to remove
            tables = {
                'evento_sismico': ['estado_actual_id', 'estado_actual_tipo'],
                'cambio_estado': ['estado_id', 'estado_tipo'],
                'serie_temporal': ['estado_id', 'estado_tipo'],
            }
            recreate_table_excluding_columns(tables)
        sys.exit(rc)
    except Exception as e:
        print('Migration failed:', e)
        raise
