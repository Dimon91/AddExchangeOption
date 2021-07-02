#!/usr/bin/python3
# coding: utf-8

import xml.etree.ElementTree as ET
from Rule import Rule


def main():
    tree = ET.parse('rules.xml')
    listGroup = tree.findall('ПравилаРегистрацииОбъектов/Группа')
    for group in listGroup:
        process_group(group)


def process_group(group):
    listGroup = group.findall('Группа')
    for subgroup in listGroup:
        process_group(subgroup)

    listRules = group.findall("Правило")
    for rule in listRules:
        process_rule(rule)


def process_rule(rule):

    rule_obj = Rule(rule)
    if(rule_obj.exchangeRMQIsAvailable):
        print(rule_obj.to_string(';'))

def filters_RMQ(rule):

    filters = rule.find('ОтборПоСвойствамПланаОбмена')

    listFilters = []

    if(filters != None):
        filters_in_group(filters, listFilters)

    return listFilters


def filters_in_group(group, listFilters):
    groupsFilters = group.findall('Группа')
    for subgroup in groupsFilters:
        filters_in_group(subgroup, listFilters)

    filters_RMQ = group.findall(
        "ЭлементОтбора[СвойствоПланаОбмена = 'ВариантВыгрузкиRMQ']")
    listFilters.extend(filters_RMQ)


if __name__ == "__main__":
    main()
