from sqlmodel import Field, Session, SQLModel, create_engine
from testcontainers.mysql import MySqlContainer

TEST_DB_CMD = "mariadb -B --disable-column-names -p'test' -D'test' -e"


class Clients(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    pname: str = Field(..., max_length=255)
    login: str = Field(..., max_length=255)


class Domains(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(..., max_length=255)
    webspace_id: int
    cl_id: int = Field(default=None, foreign_key="clients.id")


class TestMariadb:
    __test__ = False

    def __init__(self):
        self.container = MySqlContainer("mariadb:latest")
        self.container.start()
        self.engine = create_engine(self.container.get_connection_url())

    def __create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def __insert_sample_data(self):
        with Session(self.engine) as session:
            client_b = Clients(pname="FIO", login="p-2342343")
            session.add(client_b)
            session.commit()

            main_domain = Domains(
                id=1184, name="gruzo.kz", webspace_id=0, cl_id=client_b.id
            )
            session.add(main_domain)

            subdomains = [
                Domains(
                    id=1185, name="sdfsd.gruzo.kz", webspace_id=1184, cl_id=client_b.id
                ),
                Domains(
                    id=1186,
                    name="pomogite.gruzo.kz",
                    webspace_id=1184,
                    cl_id=client_b.id,
                ),
                Domains(
                    id=1187, name="nodejs.gruzo.kz", webspace_id=1184, cl_id=client_b.id
                ),
                Domains(
                    id=1188,
                    name="virtualizor.gruzo.kz",
                    webspace_id=1184,
                    cl_id=client_b.id,
                ),
                Domains(
                    id=1189, name="wp.gruzo.kz", webspace_id=1184, cl_id=client_b.id
                ),
                Domains(
                    id=1190,
                    name="onebula.gruzo.kz",
                    webspace_id=1184,
                    cl_id=client_b.id,
                ),
                Domains(
                    id=1378, name="mxtest.gruzo.kz", webspace_id=1184, cl_id=client_b.id
                ),
                Domains(
                    id=1379, name="zone.gruzo.kz", webspace_id=1184, cl_id=client_b.id
                ),
                Domains(
                    id=1383, name="zless.gruzo.kz", webspace_id=1184, cl_id=client_b.id
                ),
            ]
            session.add_all(subdomains)
            session.commit()

    def populate_db(self):
        self.__create_db_and_tables()
        self.__insert_sample_data()
        return self

    def run_cmd(self, cmd: str) -> str:
        cmd_to_exec = f'sh -c "{cmd}"'
        return self.container.exec(cmd_to_exec).output.decode("utf-8")
