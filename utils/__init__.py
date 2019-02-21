from typing import List, Union
from .group import Group
from .group import amharic_ones


class Number2WordsConverter(object):
    def __init__(self, number: Union[float, int]):
        
        self.converter:Union[_Negative2WordsConverter, _Float2WordsConverter, _Integer2WordsConverter]
        
        if not( isinstance(number, float) or isinstance(number, int)):
            raise ValueError("Number required found: %s" % str(number))
        elif number < 0:
            self.converter = _Negative2WordsConverter(number)
        elif isinstance(number, int):
            self.converter = _Integer2WordsConverter(number)
        else:
            self.converter = _Float2WordsConverter(number)
        self.coma_separated = self.converter.coma_separated

    def to_words(self):
        return  self.converter.to_words().strip()
        
            


class _Integer2WordsConverter(object):
    def __init__(self, number: int):
        coma_separated_numbers: str = self.number2CommaSeperatedString(number)
        group_list: List[str] = coma_separated_numbers.split(",")
        groups: List[Group] = []
        for i in range(len(group_list), 0, -1):
            g = group_list[i - 1]
            g_index = len(group_list) - i
            group = Group(g, g_index)
            groups.append(Group(g, g_index))
        self.coma_separated = coma_separated_numbers
        self.groups = groups

    def to_words(self):
        output = ""
        for i in range(len(self.groups)):
            if len(self.groups[i].to_words()) > 0:
                output = self.groups[i].to_words()+" " + output
        return output.replace("  ", " ")

    def number2CommaSeperatedString(self, number: int) -> str:
        """Converts integer into comma seperated number	    

        Arguments:
            number {int} -- Integer to be converted
        Returns:
            str -- Comma separeted representation of the number
        """
        if int(number) != number:
            raise ValueError("Number should be integer")
        num_str = str(number)
        output = ""
        for i in range(len(num_str), -1, -3):
            if i < 3 and i > 0:

                if output == "":
                    output = num_str[:i]
                else:
                    output = num_str[:i] + "," + output
            elif i > 0:
                if output == "":
                    output = num_str[i - 3:i]
                else:
                    output = num_str[i - 3:i] + "," + output
            else:
                continue
        return output


class _Float2WordsConverter(object):
    def __init__(self, number: float):
        integer_part: int = int(number)

        float_part = str(number - integer_part)
        if number == integer_part:
            self.float_part = "0"
        else:
            index = float_part.find(".")
            if index != -1:
                self.float_part = float_part[index + 1:]

        coma_separated_numbers: str = self.int2CommaSeperatedString(
            integer_part)
        group_list: List[str] = coma_separated_numbers.split(",")
        groups: List[Group] = []
        for i in range(len(group_list), 0, -1):
            g = group_list[i - 1]
            g_index = len(group_list) - i
            group = Group(g, g_index)
            groups.append(Group(g, g_index))
        self.coma_separated = coma_separated_numbers+"."+str(self.float_part)
        self.int_groups = groups

    def to_words(self):
        output = ""
        for i in range(len(self.int_groups)):
            if len(self.int_groups[i].to_words()) > 0:
                output = self.int_groups[i].to_words()+" " + output
        integer_part = output.replace("  ", " ")
        if len(self.float_part) > 0:
            float_part = self.get_float_part_words().strip()
        else:
            float_part = ""

        if len(float_part) > 0:
            return integer_part.strip() + " ነጥብ " + float_part
        else:
            return integer_part

    def get_float_part_words(self):
        output = ""
        for i in range(len(self.float_part)):
            output += amharic_ones[int(self.float_part[i])] + " "
        return output

    def int2CommaSeperatedString(self, number: int) -> str:
        """Converts integer into comma seperated number	    

        Arguments:
            number {int} -- Integer to be converted
        Returns:
            str -- Comma separeted representation of the number
        """
        if int(number) != number:
            raise ValueError("Number should be integer")
        num_str = str(number)
        output = ""
        for i in range(len(num_str), -1, -3):
            if i < 3 and i > 0:

                if output == "":
                    output = num_str[:i]
                else:
                    output = num_str[:i] + "," + output
            elif i > 0:
                if output == "":
                    output = num_str[i - 3:i]
                else:
                    output = num_str[i - 3:i] + "," + output
            else:
                continue
        return output


class _Negative2WordsConverter(object):
    def __init__(self, number: Union[int, float]):
        self.converter:Union[_Integer2WordsConverter, _Float2WordsConverter]
        if isinstance(number, int):
            self.converter: _Integer2WordsConverter = _Integer2WordsConverter(
                number)
        elif isinstance(number, float):
            self.converter: _Float2WordsConverter = _Float2WordsConverter(number)
        self.coma_separated = self.converter.coma_separated
    def to_words(self):
        return "ነጌትቭ " + self.converter.to_words()
