"""Database interactions"""

from sqlalchemy import Table, select
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


def get_db_engine(db_path: str) -> Engine:
    """Creates a new SQLAlchemy Engine instance from path

    Args:
        db_path (str): Path to SQLite database

    Returns:
        Engine: Connection to database
    """
    return create_engine(f"sqlite:///{db_path}", echo=False, future=True)


def get_model(model: str, engine: Engine):
    """Creates a Model class to bind for the model object

    Args:
        model (str): Model name to get
        engine (Engine): Connection to database

    Raises:
        KeyError: If model name is not supported

    Returns:
        Model: Model instance binded to database table
    """
    model_dict = {
        "payment_form": "cfdi_40_formas_pago",
        "unit_of_measure": "cfdi_40_claves_unidades",
    }

    try:
        table_name = model_dict[model.lower()]
    except KeyError as err:
        raise KeyError(f"Invalid model name: {model}") from err

    class Model(Base):
        """Common model class"""

        __table__ = Table(table_name, Base.metadata, autoload_with=engine)

    return Model


def get_record_scalars(model: str, db_path: str):
    """Connect to database and retrieve results as scalars

    Args:
        model (str): Model name of the object to retrieve
        db_path (str): Path to SQLite database

    Returns:
        ScalarResult: All table record objects
    """

    engine = get_db_engine(db_path)
    session = Session(engine)
    model_class = get_model(model, engine)
    results = select(model_class)
    return session.scalars(results)
