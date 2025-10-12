from typing import Union, List, Dict, Any, Tuple
import aiosqlite as sql


async def dict_to_db(path: str, data: Dict[str, List[Dict[str, Any]]]):
    """
    Sync an in-memory Python dictionary back to the SQLite database,
    replacing all rows in each table.

    Args:
        path (str): Path to the SQLite database file.
        data (Dict[str, List[Dict[str, Any]]]): Database contents as dictionary.
    """
    async with sql.connect(path) as db:
        for table, rows in data.items():
            if not rows:
                continue  # skip empty

            # clear table
            await db.execute(f"DELETE FROM {table}")

            # insert all rows
            columns = rows[0].keys()
            placeholders = ", ".join(["?"] * len(columns))
            col_names = ", ".join(columns)

            for row in rows:
                values = tuple(row[col] for col in columns)
                await db.execute(
                    f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})",
                    values
                )

        await db.commit()


class Database:
    def __init__(self, path: str):
        """
        Initialize the database helper.

        Args:
            path (str): Path to the SQLite database file. Defaults to "bot_data.db".
        """
        if not path:
            raise ValueError("Path is a required argument.")

        self.path = path


    # ---------- Table Management ----------
    async def create_table(self, name: str, columns: Union[List[str], Dict[str, str]]):
        """
        Create a table if it does not already exist.

        Args:
            name (str): Name of the table.
            columns (Union[List[str], Dict[str, str]]): Either a list of column definitions (as strings)
                or a dict mapping column names to definitions.
        """
        async with sql.connect(self.path) as db:
            if isinstance(columns, dict):
                columns_def = ', '.join([f"{col} {definition}" for col, definition in columns.items()])
            elif isinstance(columns, list):
                columns_def = ', '.join(columns)
            else:
                raise ValueError("columns must be a list or dict")

            await db.execute(f"CREATE TABLE IF NOT EXISTS {name} ({columns_def})")
            await db.commit()

    async def delete_table(self, name: str):
        """
        Delete a table if it exists.

        Args:
            name (str): Name of the table to drop.
        """
        async with sql.connect(self.path) as db:
            await db.execute(f"DROP TABLE IF EXISTS {name}")
            await db.commit()

    # ---------- CRUD Operations ----------
    async def insert(self, table: str, data: Dict[str, Any]):
        """
        Insert a new row into a table.

        Args:
            table (str): Table name.
            data (Dict[str, Any]): Dictionary mapping column names to values.
        """
        keys = ', '.join(data.keys())
        placeholders = ', '.join(["?" for _ in data])
        values = tuple(data.values())

        async with sql.connect(self.path) as db:
            await db.execute(
                f"INSERT INTO {table} ({keys}) VALUES ({placeholders})",
                values
            )
            await db.commit()

    async def update(self, table: str, updates: Dict[str, Any], where: str, params: Tuple[Any, ...]):
        """
        Update existing rows in a table.

        Args:
            table (str): Table name.
            updates (Dict[str, Any]): Dictionary mapping columns to new values.
            where (str): WHERE clause (without the 'WHERE' keyword).
            params (Tuple[Any, ...]): Parameters for the WHERE clause.
        """
        set_clause = ', '.join([f"{col} = ?" for col in updates.keys()])
        values = tuple(updates.values()) + params

        async with sql.connect(self.path) as db:
            await db.execute(
                f"UPDATE {table} SET {set_clause} WHERE {where}",
                values
            )
            await db.commit()

    async def delete(self, table: str, where: str, params: Tuple[Any, ...]):
        """
        Delete rows from a table.

        Args:
            table (str): Table name.
            where (str): WHERE clause (without the 'WHERE' keyword).
            params (Tuple[Any, ...]): Parameters for the WHERE clause.
        """
        async with sql.connect(self.path) as db:
            await db.execute(
                f"DELETE FROM {table} WHERE {where}",
                params
            )
            await db.commit()

    async def upsert(self, table: str, data: Dict[str, Any], conflict_column: str):
        """
        Insert or update a row depending on conflict.

        Args:
            table (str): Table name.
            data (Dict[str, Any]): Dictionary mapping column names to values.
            conflict_column (str): Column to check for conflict.
        """
        keys = ', '.join(data.keys())
        placeholders = ', '.join(["?" for _ in data])
        values = tuple(data.values())

        update_clause = ', '.join([f"{col}=excluded.{col}" for col in data.keys() if col != conflict_column])

        async with sql.connect(self.path) as db:
            await db.execute(
                f"""
                INSERT INTO {table} ({keys}) VALUES ({placeholders})
                ON CONFLICT({conflict_column}) DO UPDATE SET {update_clause}
                """,
                values
            )
            await db.commit()

    # ---------- Fetch Operations ----------
    async def fetchone(self, query: str, params: Tuple[Any, ...] = ()) -> Union[Dict[str, Any], None]:
        """
        Fetch a single row from a query.

        Args:
            query (str): SQL query to execute.
            params (Tuple[Any, ...], optional): Query parameters. Defaults to empty tuple.

        Returns:
            Dict[str, Any] | None: A single row as a dictionary, or None if no rows found.
        """
        async with sql.connect(self.path) as db:
            db.row_factory = sql.Row
            cursor = await db.execute(query, params)
            row = await cursor.fetchone()
            return dict(row) if row else None

    async def fetchall(self, query: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
        """
        Fetch all rows from a query.

        Args:
            query (str): SQL query to execute.
            params (Tuple[Any, ...], optional): Query parameters. Defaults to empty tuple.

        Returns:
            List[Dict[str, Any]]: A list of rows, each as a dictionary.
        """
        async with sql.connect(self.path) as db:
            db.row_factory = sql.Row
            cursor = await db.execute(query, params)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]

    # ---------- Utility ----------
    async def execute(self, query: str, params: Tuple[Any, ...] = ()):
        """
        Execute an arbitrary query with commit.

        Args:
            query (str): SQL query to execute.
            params (Tuple[Any, ...], optional): Query parameters. Defaults to empty tuple.
        """
        async with sql.connect(self.path) as db:
            await db.execute(query, params)
            await db.commit()

    async def executemany(self, query: str, seq_of_params: List[Tuple[Any, ...]]) -> None:
        """
        Execute the same query for multiple parameter sets with commit.

        Args:
            query (str): SQL query to execute.
            seq_of_params (list[Tuple[Any, ...]]): Sequence of parameters for each execution.
        """
        async with sql.connect(self.path) as db:
            await db.executemany(query, seq_of_params)
            await db.commit()


    async def to_dict(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Load an entire SQLite database into a Python dictionary.

        Returns:
            Dict[str, List[Dict[str, Any]]]: A dictionary where keys are table names
            and values are lists of rows (each row as a dict).
        """
        path = self.path

        db_dict: Dict[str, List[Dict[str, Any]]] = {}

        async with sql.connect(path) as db:
            db.row_factory = sql.Row

            # get all table names
            cursor = await db.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = await cursor.fetchall()

            for table in tables:
                table_name = table[0]
                cur = await db.execute(f"SELECT * FROM {table_name}")
                rows = await cur.fetchall()
                db_dict[table_name] = [dict(row) for row in rows]

        return db_dict
