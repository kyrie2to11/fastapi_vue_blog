from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 导入项目的Base模型
from app.db.base import Base
target_metadata = Base.metadata

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# 从环境变量或配置文件获取数据库连接URL
config.set_main_option("sqlalchemy.url", "postgresql://postgres:postgres@localhost:5432/blog_db")

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 配置target_metadata为项目的Base.metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. 由用户手动执行命令后，可通过此模式生成迁移脚本。
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    此模式用于实际执行数据库迁移，需确保Alembic能连接数据库。
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if __name__ == "__main__":
    if context.is_offline_mode():
        run_migrations_offline()
    else:
        run_migrations_online()
