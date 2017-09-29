import sys
import logging
import json
from datetime import datetime
import collections
from model import Market, Team, Deal, User

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

dbengine = create_engine('mysql+mysqlconnector://admin:ronaldo7@teamtrader.csywb8hubjmd.eu-west-2.rds.amazonaws.com/teamtrader')


SessionFactory = sessionmaker(bind=dbengine)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def marketsList(event, context):
    dbsession=SessionFactory()
    markets=dbsession.query(Market).all()
    json_data=[]
    for market in markets:
        d = collections.OrderedDict()
        d['id'] = market.id
        d['name'] = market.name
        d['marketopen']=market.marketopen.strftime('%Y-%m-%d')
        d['auctionclose']=market.auctionclose.strftime('%Y-%m-%d')
        json_data.append(d)

    # create a response
    response = {
        'statusCode': 200,
        'body': json.dumps(json_data)
    }

    return response

def marketsGet(event, context):
    dbsession=SessionFactory()
    id=event['pathParameters']['id']
    market=dbsession.query(Market).get(id)

    if market is None:
        return {'statusCode': 404}
    else:
        json_data = collections.OrderedDict()
        json_data['id'] = market.id
        json_data['Name'] = market.name
        json_data['marketopen']=market.marketopen.strftime('%Y-%m-%d')
        json_data['auctionclose']=market.auctionclose.strftime('%Y-%m-%d')

        # create a response
        return {'statusCode': 200, 'body': json.dumps(json_data)}
        
def marketsInsert(event, context):
    
    #validation
    if 'body' in event:
        body=json.loads(event['body'])
        if 'name' in body:
            name=body['name']
        else:
            return {'statusCode': 400, 'message': 'Name not provided'}
        
        if 'marketopen' in body:
            try:
                marketopen=datetime.strptime(body['marketopen'], '%Y-%m-%d')
            except ValueError:
                return {'statusCode': 400, 'message': 'Invalid market open date format'}

        if 'auctionclose' in body:
            if len(body['auctionclose']) > 0:
                try:
                    auctionclose=datetime.strptime(body['auctionclose'], '%Y-%m-%d')
                except ValueError:
                    return {'statusCode': 400, 'message': 'Invalid auction close date format'}
            else:
                auctionclose=None
    else:
        return {'statusCode': 400, 'message': 'No JSON body provided'}

    #save  
    dbsession=SessionFactory()
    try:  
        newMarket=Market(name=name, marketopen=marketopen, auctionclose = auctionclose)
        dbsession.add(newMarket)
        dbsession.commit()
        dbsession.close()
        return {'statusCode': 200}
    except:
        dbsession.rollback()
        dbsession.close()
        return {'statusCode': 400, 'message': 'SQL insert error'}

def marketsUpdate(event, context):
    
    #validation
    if 'body' in event:
        body=json.loads(event['body'])
        if 'name' in body:
            name=body['name']
        else:
            return {'statusCode': 400, 'message': 'Name not provided'}
        
        if 'marketopen' in body:
            try:
                marketopen=datetime.strptime(body['marketopen'], '%Y-%m-%d')
            except ValueError:
                return {'statusCode': 400, 'message': 'Invalid market open date format'}

        if 'auctionclose' in body:
            if len(body['auctionclose']) > 0:
                try:
                    auctionclose=datetime.strptime(body['auctionclose'], '%Y-%m-%d')
                except ValueError:
                    return {'statusCode': 400, 'message': 'Invalid auction close date format'}
            else:
                auctionclose=None
    else:
        return {'statusCode': 400, 'message': 'No JSON body provided'}

    #get id
    id=event['pathParameters']['id']
    #save  
    dbsession=SessionFactory()
    try:  
        market=dbsession.query(Market).get(id)
        if market is None:
            return {'statusCode': 404}
        market.name=name
        market.marketopen=marketopen
        market.auctionclose=auctionclose
        dbsession.add(market)
        dbsession.commit()
        dbsession.close()
        return {'statusCode': 200}
    except:
        dbsession.rollback()
        dbsession.close()
        return {'statusCode': 400, 'message': 'SQL update error'}

def teamsInsert(event, context):
    
    #validation
    if 'body' in event:
        body=json.loads(event['body'])

        if 'marketid' in body:
            try:
                marketid=int(body['marketid'])
            except ValueError:
                return {'statusCode': 400, 'message': 'Invalid market id'}
        else:
            return {'statusCode': 400, 'message': 'Market id not provided'}

        if 'name' in body:
            name=body['name']
        else:
            return {'statusCode': 400, 'message': 'Name not provided'}
        
        if 'numberofshares' in body:
            try:
                numberofshares=int(body['numberofshares'])
            except ValueError:
                return {'statusCode': 400, 'message': 'Invalid number of shares'}
        else:
            return {'statusCode': 400, 'message': 'Number of shares not provided'}

        auctionprice=None
        if 'auctionprice' in body:
            if len(body['auctionprice'])>0:
                try:
                    auctionprice=float(body['auctionprice'])
                except ValueError:
                    return {'statusCode': 400, 'message': 'Invalid auction price'}
        
        auctionuserid=None
        if 'auctionuserid' in body:
            if len(body['auctionuserid'])>0:
                try:
                    auctionuserid=int(body['auctionuserid'])
                except ValueError:
                    return {'statusCode': 400, 'message': 'Invalid auction user id'}

        lasttradedprice=None
        if 'lasttradedprice' in body:
            if len(body['lasttradedprice'])>0:
                try:
                    lasttradedprice=float(body['lasttradedprice'])
                except ValueError:
                    return {'statusCode': 400, 'message': 'Invalid last traded price'}

        bestbidprice=None
        if 'bestbidprice' in body:
            if len(body['bestbidprice'])>0:
                try:
                    bestbidprice=float(body['bestbidprice'])
                except ValueError:
                    return {'statusCode': 400, 'message': 'Invalid best bid price'}

        bestofferprice=None
        if 'bestofferprice' in body:
            if len(body['bestofferprice'])>0:
                try:
                    bestofferprice=float(body['bestofferprice'])
                except ValueError:
                    return {'statusCode': 400, 'message': 'Invalid best offer price'}

    else:
        return {'statusCode': 400, 'message': 'No JSON body provided'}

    #save  
    dbsession=SessionFactory()
    newTeam=Team(marketid=marketid, name=name, numberofshares=numberofshares, auctionprice=auctionprice, auctionuserid=auctionuserid, lasttradedprice=lasttradedprice, bestbidprice=bestbidprice, bestofferprice=bestofferprice)
    dbsession.add(newTeam)
    dbsession.commit()
    dbsession.close()
    return {'statusCode': 200}
    # except:
    #     return {'statusCode': 400, 'message': 'SQL insert error'}
    #     #dbsession.rollback()
    #     #dbsession.close()
        


# team get, list, add, update
# deal get, list, add, update 
# user get, add, update, login

#testing

#print(marketsGet({'pathParameters':{'id': 13}}, ''))
#print(marketsInsert('json.loads('{"body":{"name": "Champions League 2017-2018", "marketopen": "2017-10-01", "auctionclose": "2017-12-01"}}', ''))
# print(marketsUpdate({'pathParameters':{'id': 3}, 'body':{'name': 'Liverpool'}}, ''))
# print(marketsList({}, ''))
#
# print(teamsInsert(json.loads('{"body": {"marketid": "1","name": "Man Utd"}}'), ''))
# print('')