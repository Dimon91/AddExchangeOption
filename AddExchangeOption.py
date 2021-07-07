#!/usr/bin/python3
# coding: utf-8

from lxml import etree as ET
from typing import List
from Rule import Rule, TypeOfCompare


def main():    
    text = ''
    with(open('rules.xml', 'r', encoding='utf-8')) as f:
        text = f.read()        
    if(text == ''):
        raise Exception('Не удалось открыть файл')
    
    tree = ET.fromstring(text)
    rulesroot = tree.find('ПравилаРегистрацииОбъектов')
    rules: List[Rule] = []
    process_group(rulesroot, rules)
    for rule in rules:
        rule.addfilternode(("НовыйФильтр", TypeOfCompare.not_equal))
    
    with(open('result.xml', 'w', encoding='utf-8')) as f:
        outtext = ET.tostring(tree, encoding = 'unicode')
        f.write(outtext)


def process_group(group, rules: List[Rule]):
    listGroup = group.findall('Группа')
    for subgroup in listGroup:
        process_group(subgroup, rules)
    listRules = group.findall("Правило")
    for rule in listRules:
        rule_obj = Rule(rule)
        if(rule_obj.exchangeRMQIsAvailable):
            rules.append(rule_obj)


def addOption(name: str, rules: List[Rule]):
    for rule in rules:
        rule.addfilternode((name, TypeOfCompare.not_equal))


if __name__ == "__main__":
    main()
