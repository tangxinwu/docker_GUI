from abc import ABC, abstractmethod
import re


class JSONAttr:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        if value:
            instance.__dict__[self.storage_name] = value
            # return setattr(instance, self.storage_name, value)
        else:
            print("{}为空".format(self.storage_name))
            return self

    def __get__(self, instance, owner):
        return instance.__dict__[self.storage_name]
        # return getattr(instance, self.storage_name)


class Validted(ABC, JSONAttr):
    def __set__(self, instance, value):
        value = self.validte(instance, value)
        super().__set__(instance, value)

    @abstractmethod
    def validte(self, instance, value):
        """
        根据不同的属性设置不同的设置方法
        :return:
        """


class TitleValid(Validted):
    """
    设置title的属性值
    """
    def validte(self, instance, value):
        if value:
            modified_value = dict()
            modified_value.update({"text": value})
            return modified_value
        else:
            raise ValueError("标题不能为空")


class TooltipValid(Validted):
    """
    设置tooltip属性
    使用tooltip=True/Fasle开启
    默认显示模式{a} <br/>{b} : {c} ({d}%)
    """
    def validte(self, instance, value):
        if value is True:
            __temp_dict = dict()
            __temp_dict["trigger"] = "item"
            __temp_dict["formatter"] = "{a} <br/>{b} : {c} ({d}%)"
            return __temp_dict
        else:
            raise ValueError("tooltip参数必须是字典")


class LegendValid(Validted):
    """
    设置图列属性
    """
    def validte(self, instance, value):
        if isinstance(value, list):
            modified_value = dict()
            modified_value.update({"data": value})
            return modified_value
        else:
            raise ValueError("图例只能是列表")


class xAxisValid(Validted):
    """
    设置x轴属性
    """
    def validte(self, instance, value):
        if isinstance(value, list):
            modified_value = dict()
            modified_value.update({"data": value})
            return modified_value
        else:
            raise ValueError("x轴的属性只能是列表")


class yAxisValid(Validted):
    """
    设置y轴属性值
    """
    def validte(self, instance, value):
        if isinstance(value, list):
            modified_value = dict()
            modified_value.update({"data": value})
            return modified_value
        else:
            return {}


class SeriesValid(Validted):
    """
    设置series属性
    """
    def validte(self, instance, value):
        if isinstance(value, list):
            __temp = []
            for serie in value:
                if serie.__class__.__name__ == "SeriesBar":
                    __temp.append(eval(str(serie)))
                else:
                    raise ValueError("series属性必须是Series的实例")
            return __temp
        else:
            raise ValueError("series属性必须是列表类型")


class SeriesNameValid(Validted):
    """
    设置series name子属性
    """
    def validte(self, instance, value):
        if value:
            return value
        else:
            raise ValueError("名字不能为空")


class SeriesTypeValid(Validted):
    """
    设置Series Type子属性
    """
    def validte(self, instance, value):
        if value not in ("bar", "pie", ):
            raise ValueError("图标的类型不正确")
        else:
            return value


class SeriesDataValid(Validted):
    """
    设置 series Data子属性
    """
    def validte(self, instance, value):
        if isinstance(value, list):
            return value
        else:
            raise ValueError("data值必须是列表类型")


class SeriesPieValid(Validted):
    """
    验证饼状图的series属性是否正确
    """
    def validte(self, instance, value):
        if isinstance(value, list):
            __temp = []
            for serie in value:
                if serie.__class__.__name__ == "SeriesPie":
                    __temp.append(eval(str(serie)))
                else:
                    raise ValueError("series pie属性必须是SeriesPie的实例")
            return __temp
        else:
            raise ValueError("series pie属性必须是列表类型")


class SeriesPieDataValid(Validted):
    """
    验证传入pie的data格式是否正确
    应该传入元祖的列表[（value1，name1）,(value2, name2)]
    """
    def validte(self, instance, value):
        if isinstance(value, list):
            __temp_list = list()
            for i in value:
                if isinstance(i, tuple):
                    __temp_list.append({"value": i[0], "name": i[1]})
                else:
                    raise ValueError("value，name 类型错误")
            return __temp_list
        else:
            raise ValueError("Pie的data格式为[（value1，name1）,(value2, name2)]")


class SeriesPieRadiusValid(Validted):
    """
    设置饼状图的radius属性
    饼的圆的大小例如 55%
    """
    def validte(self, instance, value):
        if re.findall("^[0-9]+\%$", value):
            return value
        else:
            raise ValueError("Radius格式不正确")


class SeriesPieRoseTypeValid(Validted):
    """
    验证饼状图series属性下roseType属性值，
    可以改编饼显示的形态
    """
    def validte(self, instance, value):
        if value not in ("angle", ):
            raise ValueError("roseType参数不正确")
        else:
            return value
