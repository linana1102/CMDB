#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xmlrpclib
import my_pexpect
import sw_parsing


def connect_create_server(create_model,fields_dict_list):
    url = '127.0.0.1:8069'
    db = 'test'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    for fields_dict in fields_dict_list:
        models.execute_kw(db,uid,password,create_model,'create',[fields_dict])


def connect_search_server(search_model,os_id_search_domain):
    url = '127.0.0.1:8069'
    db = 'test'
    username = 'admin'
    password = 'admin'
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
    uid = common.authenticate(db, username, password, {})
    models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return models.execute_kw(db,uid,password,search_model,'search',[os_id_search_domain],{'limit':1})


def create_network_management_ip(os_id):
    command = 'show version'
    fields_dict_list=[]
    child = my_pexpect.ssh_command(os_id.device_id.account_name,os_id.device_id.manage_ip,os_id.device_id.account_password,command)
    before = child.before
    show_version_list = sw_parsing.show_version(before)
    soft = show_version_list[0]['software']   # os_id_search_domain =[['software_id.name','like',soft],['device','=',os_id.device_id.id]]
    # search_model = 'cmdb.os_instance'
    # os_id = connect_search_server(search_model,os_id_search_domain)
    # print show_version_list[0]['name']

    fields_dict = {'os_id': os_id,'manage_ip':os_id.device_ide.manage_ip,'manage_interface':os_id.device_id.manage_interface}
    create_model = 'cmdb.network_management_ip'
    fields_dict_list.append(fields_dict)
    connect_create_server(create_model,fields_dict_list)


def create_interface(os_id):
    command = 'show ip interface brief'
    fields_dict_list = []
    child = my_pexpect.ssh_command(os_id.device_id.account_name, os_id.device_id.manage_ip,
                                   os_id.device_id.account_password, command)
    before = child.before
    show_ip_int_brief_list = sw_parsing.show_version(before)

    for i in len(show_ip_int_brief_list['interface']):
        fields_dict = {'name': show_ip_int_brief_list['interface'][i], 'os_id': os_id,
                       'ip_ids': show_ip_int_brief_list['ip_address'][i],
                       'link_status': show_ip_int_brief_list['status'][i],
                       'line_protocol_status': show_ip_int_brief_list['protocol'][i]}

        fields_dict_list.append(fields_dict)
    create_model = 'cmdb.interface'
    fields_dict_list.append(fields_dict)
    connect_create_server(create_model, fields_dict_list)

def create_xbar(os_id):
    pass