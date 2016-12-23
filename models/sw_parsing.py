#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re


# 解析show_version命令
def show_version(log):
    # f = open(r'C:\Users\nantian\Desktop\command_result\log.txt', 'r')
    show_version_list = []
    days = 0
    hours = 0
    minutes = 0
    for line in log.splitlines():
        if line:
            name_obj = re.search(r'.*(?=uptime)', line)
            if name_obj:
                name = name_obj.group(0).strip()
                day = re.search(r'(?<= )\d+ (?=day)', line)
                years = re.search(r'(?<= )\d+ (?=year)',line)
                month = re.search(r'(?<= )\d+ (?=month)',line)
                weeks = re.search(r'(?<= )\d+ (?=week)', line)
                hour = re.search(r'(?<= )\d+ (?=hour)', line)
                minute = re.search(r'(?<= )\d+ (?=minute)', line)
                if day:
                    days += int(day.group())
                if years:
                    days += int(years.group())*365
                if month:
                    days += int(month.group())*30
                if weeks:
                    days += int(weeks.group())*7
                if hour:
                    hours += int(hour.group())
                if minute:
                    minutes += int(minute.group())
                    continue
            system_image_obj = re.search(r'(?<=^system image file is ").*(?=")', line, re.IGNORECASE)
            if system_image_obj:
                system_image =system_image_obj.group().strip()
                continue

            config_register_obj = re.search(r'(?<=^Configuration register is ).*', line, re.IGNORECASE)
            if config_register_obj:
                config_register = config_register_obj.group().strip()
                continue
            kickstart_image_obj = re.search(r'(?<=^kickstart image file is: ).*', line, re.IGNORECASE)
            if kickstart_image_obj:
                kickstart_image = kickstart_image_obj.group().strip()
                continue
            memory_size_obj = re.search(r'(?<=with )\d+(?=K.*of memory)', line, re.IGNORECASE)
            if memory_size_obj:
                memory_size = int(memory_size_obj.group())/1024
                print memory_size
                continue
            bootflash_size_obj = re.search(r'(?<=bootflash:)\s+\d+(?= KB)', line, re.IGNORECASE)
            if bootflash_size_obj:
                bootflash_size = int(bootflash_size_obj.group().strip()) / 1024
                print bootflash_size
                continue
            software_obj = re.search(r'(?<=cisco).*?(?= Software)', line, re.IGNORECASE)
            if software_obj:
                software = software_obj.group().strip()
                soft_version_obj = re.search(r'(?<=Version)\s+([0-9\(.\)]+)SE', line, re.IGNORECASE)
                if soft_version_obj:
                    soft_version = soft_version_obj.group(0).strip()
                    continue
    show_version_list.append({'name':name,'days':days,'hours':hours,'minutes':minutes,'software':software,'soft_version':soft_version,'system_image':system_image,'kickstart_image':kickstart_image,'config_register':config_register,'memory_size':memory_size,'bootflash_size':bootflash_size})
    return show_version_list


# 解析show ip interface biref
def show_ip_int_biref():
    f = open(r'C:\Users\nantian\Desktop\command_result\log1.txt','r')
    alllines = f.readlines()
    f.close()
    interface = []
    ip_address = []
    ok = []
    method = []
    status = []
    protocol = []
    # 利用正则表达式获取需要信息的行
    for index ,line in enumerate(alllines):
        if index and len(line)>1:
            list = re.split('\s+', line)
            if list[-4] == 'administratively':
                list[-4] = list[-4]+' '+list[-3]
                list[-3] = list[-2]
                list[-2] = ''
            list.remove('')
            if '' in list:
                list.remove('')
            interface.append(list[0])
            ip_address.append(list[1])
            ok.append(list[2])
            method.append(list[3])
            status.append(list[4])
            protocol.append(list[5])
    interface_dict = {'interface': interface, 'ip_address': ip_address, 'ok': ok, 'method': method, 'status':status,'protocol':protocol}
    # print interface_dict
    return interface_dict
