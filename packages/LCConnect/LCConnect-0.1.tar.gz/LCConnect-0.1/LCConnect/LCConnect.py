import requests



class  LCConnect(object):
    """Manage all API calls to LC. provide investor_id and api_key"""
    
    
    def __init__(self, investor_id, api_key):
        self.__investor_id = investor_id
        self.__version = 'v1'
        self.__header = {'Authorization' : api_key, 'Content-Type' : 'application/json'}
        self.__base_url = 'https://api.lendingclub.com/api/investor/{}/'.format(self.__version)
        self.__payload = {'showAll' : 'true'}
        
        
    def get_user_data(self, ending):
        """Query user specific data
           params: ending=the end of the api url
                   possible options: summary, availablecash, funds/pending,
                                     notes, detailednotes, portfolios, filters
           return: dict or None if failure"""
        ending = 'accounts/{}/'.format(self.__investor_id) + ending
        try:
            resp = requests.get(url=self.__base_url + ending,
                                headers=self.__header,
                                params=self.__payload)
            return resp.json()
        except Exception as e:
            print e
            return None
    
    
    def get_platform_loans(self):
        """Query current notes from the platform"""
        try:
            resp = requests.get(self.__base_url + 'loans/listing'.format(self.__version),
                                headers=self.__header,
                                params=self.__payload)
            return resp.json()['loans']
        except Exception as e:
            print e
            return None
    
    
    def submit_orders(self, portfolio_id, amount, loan_id_list):
        """Submit purchase order to LC.
           params: portfolio_id (int) for notes to be associated too.
                   amount (float) for amount to purchase
                   loan_id_list [int] for loan id's to buy"""
        url = srlf.__base_url + 'accounts/{}/orders'.format(self.__investor_id)
        orders = [{'loanId' : loan_id,
                   'requestedAmount' : amount,
                   'portfolioId' : portfolio_id} for loan_id in loan_id_list]
        payload = {'aid' : self.__investor_id, 'orders' : orders}
        try:
            resp = requests.post(url=url, headers=self.__header, json=payload)
            print 'Order Submitted for {} loans'.format(len(orders))
        except Exception as e:
            print e



