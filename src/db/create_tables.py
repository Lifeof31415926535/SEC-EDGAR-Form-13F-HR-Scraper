import psycopg2

from src.config import DB_CONFIG


class TableCreator:
    def __init__(self,
                 name=DB_CONFIG['name'],
                 user=DB_CONFIG['user'],
                 password=DB_CONFIG['password'],
                 host=DB_CONFIG['host'],
                 port=DB_CONFIG['port']
                 ):
        self.connected = False

        try:
            self.conn = psycopg2.connect(
                database=name,
                user=user,
                password=password,
                host=host,
                port=port,
            )
            self.connected = True
        except Exception as exc:
            print("Failed to establish database connection.")
            print(exc)

    def create_all(self):
        if self.connected:
            self.create_source()
            self.create_filing()
            self.create_filing_info()

    def create_source(self):
        if not self.connected:
            return

        cur = self.conn.cursor()

        cur.execute(
            """
             CREATE TABLE source (
             id UUID PRIMARY KEY NOT NULL,
             company_name VARCHAR(127) NOT NULL,
             filing_date DATE NOT NULL,
             cik INT NOT NULL,
             file_name VARCHAR(255) NOT NULL,
             CONSTRAINT u_index UNIQUE(filing_date, file_name)
             ); 
            """
        )
        self.conn.commit()
        print("Database table 'source' created.")

    def create_filing(self):
        if not self.connected:
            return

        cur = self.conn.cursor()

        cur.execute(
            """
            CREATE TABLE filing (
                filing_id UUID PRIMARY KEY NOT NULL,
                source_id UUID NOT NULL,
                cik INT NOT NULL,
                company_name VARCHAR(127) NOT NULL,
                period_of_report VARCHAR (55) NOT NULL,
                UNIQUE(source_id),
                
                CONSTRAINT filing_source FOREIGN KEY (source_id)
                    REFERENCES source (id)
             );
            """
        )

        self.conn.commit()
        print("Database table 'filing' created.")

    def create_filing_info(self):
        if not self.connected:
            return

        cur = self.conn.cursor()

        cur.execute(
            """
            CREATE TABLE filing_info (
                filing_id UUID  NOT NULL,
                name_of_issuer VARCHAR(255) NOT NULL,
                cusip VARCHAR(55) NOT NULL,
                value INT NOT NULL,
                ssh_prnamt INT NOT NULL,
                ssh_prnamt_type VARCHAR (20) NOT NULL,
                va_sole INT NOT NULL,
                va_shared INT NOT NULL,
                va_none INT NOT NULL,
                put_call VARCHAR(10),
            
                CONSTRAINT filing_info_filing FOREIGN KEY (filing_id) 
                    REFERENCES filing (filing_id)
            );
            """
        )

        self.conn.commit()
        print("Database table 'filing_info' created.")
