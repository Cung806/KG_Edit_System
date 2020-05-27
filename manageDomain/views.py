from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse,JsonResponse
from manageDomain import models
import json
from django.contrib.auth.decorators import login_required


def add_domain(request):
    try:
        domain_name = request.POST.get('domain_name')
        relation_attr = request.POST.get('relation_attr')
        entity_attr = request.POST.get('entity_attr')
        d1 = models.DomainModel(domain_name=domain_name)
        d1.save()
        relation_attr_list = relation_attr.split(',')
        entity_attr_list = entity_attr.split(',')
        for r in relation_attr_list:
            relationmodel = models.relationModel(domain_name=d1, relation_label= r)
            relationmodel.save()
        for e in entity_attr_list:
            entitymodel = models.entityModel(domain_name=d1, entity_label= e)
            entitymodel.save()
        return HttpResponse("SUCCESS")
    except Exception as e:
        return HttpResponse("FAIL")


def delete_domain(request):
    if request.method == 'POST':
        domain_name = request.POST.get('domain_name')
        deletemodel = models.DomainModel.objects.filter(domain_name=domain_name)
        deletemodel.delete()
        return HttpResponse('SUCCESS')
    else:
        return HttpResponse('FAIL')


def update_domain(request):
    try:
        domain_new_name = request.POST.get('domain_new_name')
        domain_old_name = request.POST.get('domain_old_name')
        models.DomainModel.objects.filter(domain_name=domain_old_name).update(domain_name=domain_new_name)
        return HttpResponse('SUCCESS')
    except Exception as e:
        return HttpResponse('FAIL')


def update_entity_attr(request):
    try:
        domain_name = request.POST.get('domain_name')
        domainmodel = models.DomainModel.objects.filter(domain_name=domain_name)[0]
        entity_attr = request.POST.get('entity_attr')
        entity_attr_list = entity_attr.split(',')
        models.entityModel.objects.filter(domain_name=domainmodel).delete()
        for x in entity_attr_list:
            entitymodel = models.entityModel(domain_name=domainmodel, entity_label=x)
            entitymodel.save()
        return HttpResponse('SUCCESS')
    except Exception as e:
        return HttpResponse('FAIL')


def update_relation_attr(request):
    try:
        domain_name = request.POST.get('domain_name')
        domainmodel = models.DomainModel.objects.filter(domain_name=domain_name)[0]
        relation_attr = request.POST.get('relation_attr')
        relation_attr_list = relation_attr.split(',')
        models.entityModel.objects.filter(domain_name=domainmodel).delete()
        for x in relation_attr_list:
            relationmodel = models.relationModel(domain_name=domainmodel, relation_label=x)
            relationmodel.save()
        return HttpResponse('SUCCESS')
    except Exception as e:
        return HttpResponse('FAIL')


##获取实体属性和关系属性
##在知识图谱编辑里面用的（王志颖）
def get_label_list(request):
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
    la_re_json = {'entity_list': entity_list, 'relation_list': relation_list}
    json_result = json.dumps(la_re_json, ensure_ascii=False)
    return HttpResponse(json_result)


##获取实体属性和关系属性
##在知识图谱编辑里面用的（在领域管理里面用的）
def get_attr_list(request):
    domain_name = request.POST.get('domain_name')
    domainmodel = models.DomainModel.objects.filter(domain_name=domain_name)[0]
    result ={}
    entity_queryset = models.entityModel.objects.filter(domain_name=domainmodel)
    for x in entity_queryset:
        result[x.entity_label] = "entity"
    relation_queryset = models.relationModel.objects.filter(domain_name=domainmodel)
    for x in relation_queryset:
        result[x.relation_label] = "relation"
    json_result = json.dumps(result, ensure_ascii=False)
    return HttpResponse(json_result)


# @login_required
def get_domain_list(request):
    domain_list = []
    domain_qs = models.DomainModel.objects.all()
    for x in domain_qs:
        domain_list.append(x.domain_name)
    domain_json = {"domain_list": domain_list}
    domain_json = json.dumps(domain_json, ensure_ascii=False)
    return HttpResponse(domain_json)


def add_attr(request):
    domain_name = request.POST.get('domain_name')
    attr_type = request.POST.get('attr_type')
    attr_name = request.POST.get('attr_name')
    if len(attr_name)>0:
        domainmodel = models.DomainModel.objects.filter(domain_name=domain_name)[0]
        if attr_type == 'relation':
            relationmodel = models.relationModel(domain_name=domainmodel, relation_label=attr_name)
            relationmodel.save()
        if attr_type == 'entity':
            entitymodel = models.entityModel(domain_name=domainmodel, entity_label=attr_name)
            entitymodel.save()
        return HttpResponse('SUCCESS')
    else:
        return HttpResponse('FAIL')


# @login_required
def update_attr(request):
    domain_name = request.POST.get('domain_name')
    attr_type = request.POST.get('attr_type')
    attr_old_name = request.POST.get('attr_old_name')
    attr_new_name = request.POST.get('attr_new_name')
    if len(attr_new_name)>0 and len(attr_old_name)>0:
        domainmodel = models.DomainModel.objects.filter(domain_name=domain_name)[0]
        if attr_type == 'entity':
            models.entityModel.objects.filter(domain_name=domainmodel, entity_label=attr_old_name).update(entity_label=attr_new_name)
        if attr_type == 'relation':
            models.relationModel.objects.filter(domain_name=domainmodel, relation_label=attr_old_name).update(relation_label=attr_new_name)
        return HttpResponse('SUCCESS')
    else:
        return HttpResponse('FAIL')


def delete_attr(request):
    domain_name = request.POST.get('domain_name')
    attr_type = request.POST.get('attr_type')
    attr_name = request.POST.get('attr_name')
    try:
        domainmodel = models.DomainModel.objects.filter(domain_name=domain_name)[0]
        if attr_type == 'entity':
            models.entityModel.objects.filter(domain_name=domainmodel, entity_label=attr_name).delete()
        if attr_type == 'relation':
            models.relationModel.objects.filter(domain_name=domainmodel, relation_label=attr_name).delete()
        return HttpResponse('SUCCESS')
    except Exception:
        return HttpResponse('FAIL')
