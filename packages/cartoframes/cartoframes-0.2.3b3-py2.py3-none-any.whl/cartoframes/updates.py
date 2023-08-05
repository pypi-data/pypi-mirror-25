"""Class for updating a cartoframe postgres table"""

class SQL(object):
    """class for building queries for syncing"""
    def __init__(self, cartoframe):
        """"""
        self.cframe = cartoframe

    def add_cols(self):
        """prototype methods for add columns to table/dataframe"""
        newcols = list(set(self.cframe.columns) -
                       set(self.cframe.last_state.columns))
        pgtypes = [pg_type(t, c) for t, c in zip(self.cframe[newcols].dtypes,
                                                 newcols)]
        addcol_temp = 'ADD COLUMN "{colname}" {pgtype}'
        addcols = [addcol_temp.format(colname=c,
                                      pgtype=p) for c, p in zip(newcols,
                                                                pgtypes)]
        query = '''
            ALTER TABLE "{tablename}"
            {addcols};
        '''.format(tablename=self.cframe.get_carto_tablename(),
                   addcols=addcols)
        return query

    def drop_cols(self):
        """Drops columns removed from dataframe"""
        oldcols = list(set(self.cframe.last_state.columns) -
                       set(self.cframe.columns))
        dropcol_temp = 'DROP COLUMN "{colname}"'
        dropcols = [dropcol_temp.format(colname=c) for c in oldcols]

        query = '''
            ALTER TABLE "{tablename}"
            {dropcols};
        '''.format(tablename=self.cframe.get_carto_tablename(),
                   dropcols=dropcols)

        return query

    def update_vals(self):
        """Update cells which have changed since last sync"""
        
        query = ('UPDATE "{tablename}" AS a '
                 'SET {setlist} '
                 'FROM {temptable} AS t '
                 'WHERE a.cartodb_id = t.id;')
        return query

def pg_type(dtype, colname):
    """Maps dataframe type to postgres type"""
    return dtype + colname 

