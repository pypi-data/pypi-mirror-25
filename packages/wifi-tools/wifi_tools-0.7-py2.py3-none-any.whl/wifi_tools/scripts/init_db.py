# -*- coding: utf-8 -*-
#!/usr/bin/env python
import optparse

from sqlalchemy import create_engine

from wifi_tools import Base


def main():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    # from tesis.models import Ligand, Molecule

    usage = "usage: %prog -d {database_filename}"
    parser = optparse.OptionParser(usage)
    parser.add_option('-d', '--database_filename',
                      type='string',
                      default='wifi_tools.db')

    options, args = parser.parse_args()

    engine = create_engine('sqlite:///{0}'.format(options.database_filename), echo=False)
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    main()
