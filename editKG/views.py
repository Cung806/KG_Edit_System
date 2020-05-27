from django.contrib.auth.decorators import login_required
import json
from py2neo import Graph
from django.http import HttpResponse,JsonResponse
from KG_django.settings import host_addr,user, password, encoding
from manageDomain import models
# Create your views here.

g = Graph(
        host_addr,
        user=user,
        password=password,encoding=encoding)


# @login_required
def get_entity(request):
    # 获取搜索关键词，返回搜索结果
    entity_name = request.POST.get('entity_name')
    if len(entity_name)==0:
        return HttpResponse('FAIL')
    try:
        domainname = request.session['domain_name']
        entity_list = []
        q = "match(p) where p.name =~'.*" + entity_name + ".*' and p.domain = '"+ domainname +"' return p"
        entity1 = g.run(q)
        entity1 = list(entity1)
        for x in entity1:
            entity_label = str(x.values()[0].labels)[1:]
            entityname = x.values()[0]['name']
            entity_list.append({"label": entity_label, "name": str(entityname)})
        entity_list = json.dumps(entity_list, ensure_ascii=False)
        entity_list = '{"0":' + entity_list + '}'
        entity_list = eval(entity_list)
        return JsonResponse(entity_list)
    except Exception as e:
        return HttpResponse('FAIL')


def get_neighbor(request):
    ##通过传入实体名称e_name和实体标签label,返回实体的邻居节点以及关系类型。
    entity_name= request.POST.get('entity_name')
    entity_label = request.POST.get('entity_label')
    domainname = request.session['domain_name']
    relation_label = request.POST.get('relation_label')
    if relation_label == 'ALL':
        q1 = 'match (p:' + entity_label + '{name:"' + entity_name + '", domain:"'+domainname+'"}) - [r]-> (c) return c,r'
        q2 = 'match (p) - [r]-> (c:' + entity_label + '{name:"' + entity_name + '", domain:"'+domainname+'"}) return p,r'
    else:
        q1 = 'match (p:' + entity_label + '{name:"' + entity_name + '", domain:"'+domainname+'"}) - [r:' + relation_label + '{name:"' + relation_label + '"}]-> (c) return c,r'
        q2 = 'match (p) -[r:' + relation_label + '{name:"' + relation_label + '"}]->  (c:' + entity_label + '{name:"' + entity_name + '", domain:"'+domainname+'"}) return p,r'
    ##逆向
    link_entity = g.run(q2)
    link_entity = list(link_entity)
    target_label = entity_label
    target_name = entity_name
    negative = []
    for e in link_entity:
        source_label = str(e.values()[0].labels)[1:]
        # source_label = dic1[source_label]
        source_name = e.values()[0]['name']
        relation = e.values()[1]['name']
        str1 = {"node": source_name, "type": source_label, "endpoint": target_name, "endpointtype": target_label,
                "value": relation}
        negative.append(str1)
    ##正向
    link_entity = g.run(q1)
    link_entity = list(link_entity)
    source_label = entity_label
    source_name = entity_name
    positive = []
    for e in link_entity:
        target_label = str(e.values()[0].labels)[1:]
        # target_label = dic1[target_label]
        target_name = e.values()[0]['name']
        relation = e.values()[1]['name']
        str1 = {"node": source_name, "type": source_label, "endpoint": target_name, "endpointtype": target_label,
                "value": relation}
        positive.append(str1)

    result = negative + positive
    if result ==[]:
        result =[{"node": entity_name, "type": entity_label, "endpoint":"无", "endpointtype":"无", "value":"无"}]
    result = json.dumps(result, ensure_ascii=False)
    result = '{"0":' + result + '}'
    result = eval(result)
    return JsonResponse(result)



def change_nodel_relation(request):
    domainname = request.session['domain_name']
    n_name = request.POST.get('n_name')
    n_label = request.POST.get('n_label')
    r_name = request.POST.get('r_name')
    m_name = request.POST.get('m_name')
    m_label = request.POST.get('m_label')
    new_n_name = request.POST.get('new_n_name')
    new_n_label = request.POST.get('new_n_label')
    new_r_name = request.POST.get('new_r_name')
    new_m_name = request.POST.get('new_m_name')
    new_m_label = request.POST.get('new_m_label')
    if len(new_n_name)==0 or len(new_m_name)==0:
        return HttpResponse('FAIL')
    q = 'match (n:'+n_label+'{name:"'+n_name+'", domain:"'+domainname+'"}) -[r_old:'+r_name+']->(m:'+m_label+'{name:"'+m_name+'", domain:"'+domainname+'"}) create (n)-[r_new:'+new_r_name+'{name:"'+new_r_name+'"}]->(m) delete r_old remove n:'+n_label+',m:'+m_label+' set n:'+new_n_label+',m:'+new_m_label+',n.name="'+new_n_name+'",m.name="'+new_m_name+'",n.domain="'+domainname+'",m.domain="'+domainname+'"'
    try:
        g.run(q)
        return HttpResponse("SUCCESS")
    except Exception as e:
        print(e)
        return HttpResponse("FAIL")


def delete_relation(request):
    #单纯删除关系\
    domainname = request.session['domain_name']
    n_name = request.POST.get('n_name')
    n_label = request.POST.get('n_label')
    r_name = request.POST.get('r_name')
    m_name = request.POST.get('m_name')
    m_label = request.POST.get('m_label')
    if m_name =='无' and m_label =='无':    ##如果是孤立节点，就不能删除关系，返回删除关系失败
        return HttpResponse("RELATION_FAIL")
    else:
        q = 'match (n:'+n_label+'{name:"'+n_name+'", domain:"'+domainname+'"}) - [r:'+r_name+'] -> (m:'+m_label+'{name:"'+m_name+'", domain:"'+domainname+'"}) delete r'
    try:
        g.run(q)
        return HttpResponse("SUCCESS")
    except Exception as e:
        print(e)
        return HttpResponse("FAIL")


def delete_startnode(request):
    # 单纯起点实体及其相关关系\
    domainname = request.session['domain_name']
    n_name = request.POST.get('n_name')
    n_label = request.POST.get('n_label')
    r_name = request.POST.get('r_name')
    m_name = request.POST.get('m_name')
    m_label = request.POST.get('m_label')
    if m_name =='无' and m_label =='无':    ##如果是孤立节点，就只删除节点
        q = 'match (n:' + n_label + '{name:"' + n_name + '", domain:"' + domainname + '"}) delete n'
    else:
        q = 'match (n:' + n_label + '{name:"' + n_name + '", domain:"' + domainname + '"}) - [r:' + r_name + '] -> (m:' + m_label + '{name:"' + m_name + '", domain:"' + domainname + '"}) delete r,n'
    try:
        g.run(q)
        return HttpResponse("SUCCESS")
    except Exception as e:
        print(e)
        return HttpResponse("FAIL")


def delete_endnode(request):
    # 单纯删除关系\
    domainname = request.session['domain_name']
    n_name = request.POST.get('n_name')
    n_label = request.POST.get('n_label')
    r_name = request.POST.get('r_name')
    m_name = request.POST.get('m_name')
    m_label = request.POST.get('m_label')
    if m_name =="无" and m_label =="无":                ##如果是孤立点，则不能删除
        return HttpResponse('ENTITY_FAIL')
    q = 'match (n:' + n_label + '{name:"' + n_name + '", domain:"' + domainname + '"}) - [r:' + r_name + '] -> (m:' + m_label + '{name:"' + m_name + '", domain:"' + domainname + '"}) delete r,m'
    try:
        g.run(q)
        return HttpResponse("SUCCESS")
    except Exception as e:
        print(e)
        return HttpResponse("FAIL")



##获取实体属性和关系属性
##在知识图谱编辑里面用的（王志颖）
def get_label_list(request):
    domain_name = request.session['domain_name']
    domainmodel = models.DomainModel.objects.filter(domain_name=domain_name)[0]
    entity_list = []
    relation_list = []
    entity_queryset = models.entityModel.objects.filter(domain_name=domainmodel)
    for x in entity_queryset:
        entity_list.append(x.entity_label)
    relation_queryset = models.relationModel.objects.filter(domain_name=domainmodel)
    for x in relation_queryset:
        relation_list.append(x.relation_label)
    la_re_json = {'label_list': entity_list, 'relation_list': relation_list}
    json_result = json.dumps(la_re_json, ensure_ascii=False)
    return HttpResponse(json_result)


def add_in_relation(request):
    n_name = request.POST.get('n_name')
    n_label = request.POST.get('n_label')
    r_name = request.POST.get('r_name')
    m_name = request.POST.get('m_name')
    m_label = request.POST.get('m_label')
    domain_name = request.session['domain_name']
    if len(n_name)==0 or len(n_label)==0:
        return HttpResponse('FAIL')
    if not get_node(n_name,n_label,domain_name):  ##如果终点实体不存在
        q1 = 'create (n:'+n_label+'{name:"'+n_name+'",domain:"'+domain_name+'"})'
        q2 = 'match (n:'+n_label+'{name:"'+n_name+'",domain:"'+domain_name+'"}),(m:'+m_label+'{name:"'+m_name+'",domain:"'+domain_name+'"}) create (n)-[r:'+r_name+'{name:"'+ r_name+'"}]->(m)'
        try:
            g.run(q1)
            g.run(q2)
            return HttpResponse("SUCCESS")
        except Exception as e:
            print(e)
            return HttpResponse("FAIL")
    elif get_node(n_name,n_label,domain_name):   ##如果终点实体已经存在的话,先判断是否存在 r_name的边，如果存在，则不执行q
        q_judge = 'match (n:' + n_label + '{name:"' + n_name + '",domain:"'+domain_name+'"}) - [r:'+r_name+'] -> (m:' + m_label + '{name:"' + m_name + '",domain:"'+domain_name+'"}) return r'
        q = 'match (n:' + n_label + '{name:"' + n_name + '",domain:"'+domain_name+'"}),(m:' + m_label + '{name:"' + m_name + '",domain:"'+domain_name+'"}) create (n)-[r:' + r_name + '{name:"' + r_name + '"}]->(m)'
        try:
            judge_result = g.run(q_judge)
            if len(list(judge_result))==0:
                g.run(q)
                return HttpResponse('SUCCESS')
            else:
                return HttpResponse('SUCCESS')
        except Exception as e:
            print(e)
            return HttpResponse("FAIL")
    else:
        return HttpResponse('FAIL')


def add_out_relation(request):
    n_name = request.POST.get('n_name')
    n_label = request.POST.get('n_label')
    r_name = request.POST.get('r_name')
    m_name = request.POST.get('m_name')
    m_label = request.POST.get('m_label')
    domain_name = request.session['domain_name']
    if len(m_name)==0 or len(m_label)==0:
        return HttpResponse('FAIL')
    if not get_node(m_name,m_label,domain_name):   ##如果终点实体不存在
        q1 = 'create (m:'+m_label+'{name:"'+m_name+'",domain:"'+domain_name+'"})'
        q2 = 'match (n:'+n_label+'{name:"'+n_name+'",domain:"'+domain_name+'"}),(m:'+m_label+'{name:"'+m_name+'",domain:"'+domain_name+'"}) create (n)-[r:'+r_name+'{name:"'+ r_name+'"}]->(m)'
        try:
            g.run(q1)
            g.run(q2)
            return HttpResponse("SUCCESS")
        except Exception as e:
            print(e)
            return HttpResponse("FAIL")
    elif get_node(m_name,m_label,domain_name):  ##如果终点实体已经存在的话,先判断是否存在 r_name的边，如果存在，则不执行q
        q_judge = 'match (n:' + n_label + '{name:"' + n_name + '",domain:"' + domain_name + '"}) - [r:' + r_name + '] -> (m:' + m_label + '{name:"' + m_name + '",domain:"' + domain_name + '"}) return r'
        q = 'match (n:' + n_label + '{name:"' + n_name + '",domain:"'+domain_name+'"}),(m:' + m_label + '{name:"' + m_name + '",domain:"'+domain_name+'"}) create (n)-[r:' + r_name + '{name:"' + r_name + '"}]->(m)'
        try:
            judge_result = g.run(q_judge)
            judge_result =list(judge_result)
            if len(judge_result)==0:
                g.run(q)
                return HttpResponse('SUCCESS')
            else:
                return HttpResponse('SUCCESS')
        except Exception as e:
            print(e)
            return HttpResponse("FAIL")
    else:
        return HttpResponse('FAIL')


def add_node(request):
    n_name = request.POST.get('entity_name')
    n_label = request.POST.get('entity_label')
    domain_name = request.session['domain_name']
    if len(n_name) ==0 or len(n_label)==0:   ##如果输入有为空的话，失败
        return  HttpResponse('FAIL')
    if get_node(n_name,n_label,domain_name):   ## 如果该节点已经存在
        return HttpResponse("NODE EXIST")
    else:
        q = 'create (m:' + n_label + '{name:"' + n_name + '",domain:"' + domain_name + '"})'
    try:
        g.run(q)
        return HttpResponse("SUCCESS")
    except Exception as e:
        return HttpResponse("FAIL")


def get_detail(request):
    n_name = request.POST.get('n_name')
    m_name = request.POST.get('m_name')
    return HttpResponse("暂无信息")



## 判断节点是否已经存在在知识图谱里面
def get_node(n_name,n_label,domain_name):
    q = 'match (n:'+n_label+'{name:"'+n_name+'",domain:"'+domain_name+'"}) return n'
    try:
        result = list(g.run(q))
        if len(result) ==0:
            return False
        else:
            return True
    except Exception as e:
        return False



###用作展示作用的接口，不需要登录获取session、# ，直接获取参数里面的domain_name
def get_entity_demo(request):
    # 获取搜索关键词，返回搜索结果
    entity_name = request.POST.get('entity_name')
    if len(entity_name)==0:
        return HttpResponse('FAIL')
    try:
        domainname = request.POST.get('domain_name')
        entity_list = []
        q = "match(p) where p.name =~'.*" + entity_name + ".*' and p.domain = '"+ domainname +"' return p"
        entity1 = g.run(q)
        entity1 = list(entity1)
        for x in entity1:
            entity_label = str(x.values()[0].labels)[1:]
            entityname = x.values()[0]['name']
            entity_list.append({"label": entity_label, "name": str(entityname)})
        entity_list = json.dumps(entity_list, ensure_ascii=False)
        entity_list = '{"0":' + entity_list + '}'
        entity_list = eval(entity_list)
        return JsonResponse(entity_list)
    except Exception as e:
        return HttpResponse('FAIL')


###用作展示作用的接口，不需要登录获取session、# ，直接获取参数里面的domain_name
def get_neighbor_demo(request):
    ##通过传入实体名称e_name和实体标签label,返回实体的邻居节点以及关系类型。
    entity_name= request.POST.get('entity_name')
    entity_label = request.POST.get('entity_label')
    domainname = request.POST.get('domain_name')
    relation_label = request.POST.get('relation_label')
    if relation_label == 'ALL':
        q1 = 'match (p:' + entity_label + '{name:"' + entity_name + '", domain:"'+domainname+'"}) - [r]-> (c) return c,r'
        q2 = 'match (p) - [r]-> (c:' + entity_label + '{name:"' + entity_name + '", domain:"'+domainname+'"}) return p,r'
    else:
        q1 = 'match (p:' + entity_label + '{name:"' + entity_name + '", domain:"'+domainname+'"}) - [r:' + relation_label + '{name:"' + relation_label + '"}]-> (c) return c,r'
        q2 = 'match (p) -[r:' + relation_label + '{name:"' + relation_label + '"}]->  (c:' + entity_label + '{name:"' + entity_name + '", domain:"'+domainname+'"}) return p,r'
    ##逆向
    link_entity = g.run(q2)
    link_entity = list(link_entity)
    target_label = entity_label
    target_name = entity_name
    negative = []
    for e in link_entity:
        source_label = str(e.values()[0].labels)[1:]
        # source_label = dic1[source_label]
        source_name = e.values()[0]['name']
        relation = e.values()[1]['name']
        str1 = {"node": source_name, "type": source_label, "endpoint": target_name, "endpointtype": target_label,
                "value": relation}
        negative.append(str1)
    ##正向
    link_entity = g.run(q1)
    link_entity = list(link_entity)
    source_label = entity_label
    source_name = entity_name
    positive = []
    for e in link_entity:
        target_label = str(e.values()[0].labels)[1:]
        # target_label = dic1[target_label]
        target_name = e.values()[0]['name']
        relation = e.values()[1]['name']
        str1 = {"node": source_name, "type": source_label, "endpoint": target_name, "endpointtype": target_label,
                "value": relation}
        positive.append(str1)

    result = negative + positive
    if result ==[]:
        result =[{"node": entity_name, "type": entity_label, "endpoint":"无", "endpointtype":"无", "value":"无"}]
    result = json.dumps(result, ensure_ascii=False)
    result = '{"0":' + result + '}'
    result = eval(result)
    return JsonResponse(result)



##获取实体属性和关系属性,###用作展示作用的接口，不需要登录获取session、# ，直接获取参数里面的domain_name
def get_label_list_demo(request):
    domain_name = request.POST.get('domain_name')
    domainmodel = models.DomainModel.objects.filter(domain_name=domain_name)[0]
    entity_list = []
    relation_list = []
    entity_queryset = models.entityModel.objects.filter(domain_name=domainmodel)
    for x in entity_queryset:
        entity_list.append(x.entity_label)
    relation_queryset = models.relationModel.objects.filter(domain_name=domainmodel)
    for x in relation_queryset:
        relation_list.append(x.relation_label)
    la_re_json = {'label_list': entity_list, 'relation_list': relation_list}
    json_result = json.dumps(la_re_json, ensure_ascii=False)
    return HttpResponse(json_result)