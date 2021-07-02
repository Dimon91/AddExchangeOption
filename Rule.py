from enum import Enum, auto

class TypeOfCompare(Enum):
    equal = auto()
    not_equal = auto()
    
    def to_string(self) -> str:
        if(self == self.equal):
            result = "Равно"
        elif (self == self.not_equal):
            result = "НеРавно"
        else:
            result = ""
        
        return result

class Rule:

    def __init__(self, rule_node):
        self.rule_node = rule_node
        self.name = rule_node.find('Наименование').text
        self.mode = rule_node.find("РеквизитРежимаВыгрузки").text
        self.filters_RMQ = []
        filters = rule_node.find('ОтборПоСвойствамПланаОбмена')
        if(filters != None):
            self.__filters_in_group(filters)
        self.exchangeRMQIsAvailable = (len(self.filters_RMQ) > 0)

    def to_string(self, delimiter = None):
        if(delimiter == None):
            delimiter = '\t'        
        fragments = [self.name, self.mode]
        if(self.exchangeRMQIsAvailable):
            for filter in self.filters_RMQ:
                keys = filter.keys()
                for key in keys:
                    fragments.append(key)
        return delimiter.join(fragments)
    
    def __filters_in_group(self, group):
        groupsFilters = group.findall('Группа')
        for subgroup in groupsFilters:
            self.__filters_in_group(subgroup)
        filters_RMQ = group.findall("ЭлементОтбора[СвойствоПланаОбмена = 'ВариантВыгрузкиRMQ']")
        for filter in filters_RMQ:
            value = filter[4].text
            comparison_type = filter[3].text
            pair = {value:comparison_type}
            self.filters_RMQ.append(pair)
    
    def add_filter(self, value, comparison_type: TypeOfCompare):
        pass


