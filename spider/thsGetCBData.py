from urllib import request,parse
import json

url = 'http://www.iwencai.com/gateway/urp/v7/landing/getDataList'
headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
          'hexin-v':'A-7RzZL-AQaRy3ViIPcH0DRuNkW177J7xLNmzRi3WvGs-4BxgH8C-ZRDttPr'}
data = {'query':'可转债',
        'urp_sort_way':'desc',
        'urp_sort_index':'可转债@涨跌幅[20230203]',
        'page=1&perpage':'50',
        'condition':'[{\"indexName\":\"可转债@可转债简称\",\"indexProperties\":[],\"source\":\"new_parser\",\"type\":\"index\",\"indexPropertiesMap\":{},\"reportType\":\"null\",\"chunkedResult\":\"可转债\",\"valueType\":\"_可转债简称\",\"domain\":\"abs_可转债领域\",\"uiText\":\"可转债简称\",\"sonSize\":0,\"queryText\":\"可转债简称\",\"relatedSize\":0,\"tag\":\"可转债@可转债简称\"}]',
        'codelist':'',
        'indexnamelimit':'',
        'logid':'14effabd23c986f2cfd6c623b2e61fbd',
        'ret':'json_all',
        'sessionid':'2a596fee9fe52b7cecef815db5c5bcf1',
        'date_range[0]':'20230205',
        'iwc_token':'',
        'urp_use_sort':'1',
        'user_id':'Ths_iwencai_Xuangu_xvarwfx202pm0dw8h2naalt3d3b0iaip',
        'uuids[0]':'16775',
        'query_type':'conbond',
        'comp_id':'6467785',
        'business_cat':'soniu',
        'uuid':'16775'}
data = bytes(parse.urlencode(data),'utf-8')
req = request.Request(url, data=data, headers=headers, method='POST')
res = request.urlopen(req)
tmp_json = json.loads(res.read().decode('utf-8'))
data = tmp_json['answer']['components'][0]['data']['datas']
res = []
for item in data:
        tmp = {}
        tmp['转债代码']=item['可转债@可转债代码']
        tmp['转债简称']=item['可转债@可转债简称']
        tmp['上市日期']=item['可转债@上市日期']
        tmp['到期日']=item['可转债@到期日']
        tmp['网上发行申购价格']=item['可转债@网上发行申购价格']
        tmp['当前价格']=item['可转债@最新价']
        tmp['涨跌幅']=item['可转债@涨跌幅[20230203]']
        res.append(tmp)

print(res)