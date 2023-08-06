import datetime

class Note(object):
    """Note class takes a json note format from LC and gen_attr holding clientId and clientName 
    and converts them to a Note object. 
    Note object also has class members string_values and string_columns_names for easy injection to db"""
    
    
    def __init__(self, note, gen_attr):
        for key, value in note.items():
            setattr(self, key, value)
        # gen_attr are clientId - int, clientName - str
        for key, value in gen_attr.items():
            setattr(self, key, value)
            
        self.data_types = {
          'accruedInterest' : 'FLOAT',
          'applicationType' : 'TEXT',
          'canBeTraded' : 'BOOL',
          'creditTrend' : 'TEXT',
          'currentPaymentStatus' : 'TEXT',
          'grade' : 'TEXT',
          'interestPending' : 'FLOAT',
          'interestRate' : 'FLOAT',
          'interestReceived' : 'FLOAT',
          'issueDate' : 'TIMESTAMP',
          'loanAmount' : 'INTEGER',
          'loanId' : 'INTEGER',
          'loanLength' : 'INTEGER',
          'loanStatus' : 'TEXT',
          'loanStatusDate' : 'TIMESTAMP',
          'nextPaymentDate' : 'TIMESTAMP',
          'noteAmount' : 'INTEGER',
          'noteId' : 'INTEGER',
          'orderDate' : 'TIMESTAMP',
          'orderId' : 'INTEGER',
          'paymentsReceived' : 'FLOAT',
          'portfolioId' : 'INTEGER',
          'portfolioName' : 'TEXT',
          'principalPending' : 'FLOAT',
          'principalReceived' : 'FLOAT',
          'purpose' : 'TEXT'}
    
        self.string_values = self.__create_string_values(note)

        self.string_columns_names = self.__create_string_columns_names(note)


    def __create_string_values(self, note):
        start_string = 'CURRENT_TIMESTAMP, ' + str(self.clientId) + ', ' + "'{}'".format(self.clientName)
        for key, value in sorted(note.items(), key=lambda a: a[0]):
            if self.data_types[key] == 'TEXT':
                start_string = start_string + ", '{}'".format(value)
            if self.data_types[key] == 'TIMESTAMP':
                epoch = self.__convert_to_epoch(value)
                start_string = start_string + ", to_timestamp({})".format(epoch)
            if self.data_types[key] in ['INTEGER', 'FLOAT', 'BOOL']:
                start_string = start_string + ", {}".format(value)
        
        return start_string


    def __create_string_columns_names(self, note):
        columns_names = sorted(note.keys())
        for name in ['clientName', 'clientId', 'dateUpdated']:
            columns_names.insert(0, name)
        
        return ', '.join('{}'.format(x) for x in columns_names)

    
    def __convert_to_epoch(self, value):
        epoch = (datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.000-07:00')).strftime('%s')
        
        return epoch




