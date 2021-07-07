#!/usr/bin/python3
# coding: utf-8

from argparse import ArgumentParser
import argparse
from lxml import etree as ET
from typing import List
from Rule import Rule, TypeOfCompare


def main():    
    parser = create_argparser()
    namespace = parser.parse_args()    
    filein = namespace.file
    fileout = namespace.out
    optionname = namespace.name

    text = filein.read()
    filein.close()

    if(text == ''):
        raise Exception('Не удалось прочитать файл')
    
    tree = ET.fromstring(text)
    rulesroot = tree.find('ПравилаРегистрацииОбъектов')
    rules: List[Rule] = []
    process_group(rulesroot, rules)
    addOption(optionname, rules)
    outtext = ET.tostring(tree, encoding = 'unicode')
    if(fileout == None):
        print(outtext)
    else:
        fileout.write(outtext)
        fileout.close()


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


def create_argparser():
    parser = ArgumentParser(
        description = '''Программа добавляет настройку выгрузки в RMQ в правила регистрации'''
    )
    parser.add_argument('file',
        type = argparse.FileType('r', encoding = 'utf-8'),
        help = 'Путь к файлу XML с правилами регистрации',
        metavar = 'ПУТЬ')
    parser.add_argument('-o', '--out',
        type = argparse.FileType('w', encoding = 'utf-8'),
        help = 'Путь к файлу, в который будут сохранены измененные правила. Если не задан, текст правил будет направлен в стандартный вывод',
        metavar = 'ПУТЬ')
    parser.add_argument('-n', '--name', type = str, required = True,
        help = 'Имя варианта выгрузки в RMQ',
        metavar = 'ИМЯ')
    
    return parser


if __name__ == "__main__":
    main()
