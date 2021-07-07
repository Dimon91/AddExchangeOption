from enum import Enum, auto
from typing import Dict, List, Tuple

from lxml import etree as ET
from lxml.etree import Element

class TypeOfCompare(Enum):
    equal = auto()
    not_equal = auto()
    
    def tostring(self) -> str:
        if(self == self.equal):
            result = "Равно"
        elif (self == self.not_equal):
            result = "НеРавно"
        else:
            result = ""
        
        return result
    
    @classmethod
    def fromstring(cls, string: str):
        if(string == "Равно"):
            result = cls.equal
        elif(string == "НеРавно"):
            result = cls.not_equal
        else:
            result = None
        return result

class Rule:

    def __init__(self, rule_node):
        self.rule_node = rule_node
        self.name = rule_node.find('Наименование').text
        self.mode = rule_node.find("РеквизитРежимаВыгрузки").text
        self.exchangeRMQIsAvailable = False
        self.__filter_indent_len = 0
        self.__filternodes: List[Element] = []
        self.__filterparent: Element = None
        self.__filters_RMQ: Dict[str, TypeOfCompare] = {}
        filters = rule_node.find('ОтборПоСвойствамПланаОбмена')
        if(filters != None):
            self.__filters_in_group(filters)
        self.__filter_tail = '\n' + '\t' * self.__filter_indent_len
        self.__filter_end_tail = '\n' + '\t' * (self.__filter_indent_len - 1)

    def addfilternode_inline(self, filter: Tuple[str, TypeOfCompare]):

        filternode =  ET.SubElement(self.__filterparent, 'ЭлементОтбора')
        ET.SubElement(filternode, 'ЭтоСтрокаКонстанты').text = 'true'
        ET.SubElement(filternode, 'ТипСвойстваОбъекта').text = 'Строка'
        ET.SubElement(filternode, 'СвойствоПланаОбмена').text = 'ВариантВыгрузкиRMQ'
        ET.SubElement(filternode, 'ВидСравнения').text = filter[1].tostring()
        ET.SubElement(filternode, 'СвойствоОбъекта').text = filter[0]
        table = ET.SubElement(filternode, 'ТаблицаСвойствПланаОбмена')
        property = ET.SubElement(table, 'Свойство')
        ET.SubElement(property, 'Наименование').text = 'ВариантВыгрузкиRMQ' 
        ET.SubElement(property, 'Тип').text = 'Строка' 
        ET.SubElement(property, 'Вид').text = 'Реквизит' 

    def addfilternode(self, filter: Tuple[str, TypeOfCompare]):
        filtertext = self.__filtertext(filter[0], filter[1])
        filternode = ET.fromstring(filtertext)
        filternode.tail = self.__filter_end_tail
        self.__filterparent[-1].tail = self.__filter_tail
        self.__filterparent.append(filternode) 

    def __filters_in_group(self, group: Element):
        groupsFilters = group.findall('Группа')
        for subgroup in groupsFilters:
            self.__filters_in_group(subgroup)
        self.__filternodes = group.findall("ЭлементОтбора[СвойствоПланаОбмена = 'ВариантВыгрузкиRMQ']")
        if(len(self.__filternodes) > 0):
            self.exchangeRMQIsAvailable = True
            self.__filterparent = group            
            self.__filter_indent_len = len(group.tail)
            for filter in self.__filternodes:
                value = filter[4].text
                self.__filters_RMQ[value] = TypeOfCompare.fromstring(filter[3].text)
    
    def __filtertext(self, filtername: str, comparetype: TypeOfCompare) -> str:
        template = """[space]<ЭлементОтбора>
\t[space]<ЭтоСтрокаКонстанты>true</ЭтоСтрокаКонстанты>
\t[space]<ТипСвойстваОбъекта>Строка</ТипСвойстваОбъекта>
\t[space]<СвойствоПланаОбмена>ВариантВыгрузкиRMQ</СвойствоПланаОбмена>
\t[space]<ВидСравнения>[typeofcompare]</ВидСравнения>
\t[space]<СвойствоОбъекта>[name]</СвойствоОбъекта>
\t[space]<ТаблицаСвойствПланаОбмена>
\t\t[space]<Свойство>
\t\t\t[space]<Наименование>ВариантВыгрузкиRMQ</Наименование>
\t\t\t[space]<Тип>Строка</Тип>
\t\t\t[space]<Вид>Реквизит</Вид>
\t\t[space]</Свойство>
\t[space]</ТаблицаСвойствПланаОбмена>
[space]</ЭлементОтбора>"""

        space = '\t' * self.__filter_indent_len
        text = template.replace("[space]", space)
        text = text.replace("[name]", filtername)
        text = text.replace("[typeofcompare]", comparetype.tostring())

        return text
