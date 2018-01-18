from index import AttrModels

BAR_PARAMS = ("title", "tooltip", "legend", "xAxis", "yAxis", "series",)
SERIES_BAR_PARAMS = ("name", "data")
SERIES_PIE_PARAMS = ("name", "data", "radius", "roseType")


class SeriesBar:
    """
    设定 bar series类型的数据
    柱状图使用原始的类 其他的继承此类
    """
    name = AttrModels.SeriesNameValid("name")
    # type = AttrModels.SeriesTypeValid("type")
    data = AttrModels.SeriesDataValid("data")

    def __init__(self, **kwargs):
        self.type = "bar"
        for param in kwargs:
            if param not in SERIES_BAR_PARAMS:
                raise ValueError("没有{}参数".format(param))
        [self.__setattr__(param, kwargs.get(param, "")) for param in kwargs]

    def __str__(self):
        return str(vars(self))


class SeriesPie(SeriesBar):
    """
    设定饼状图的Series的数据属性
    """
    data = AttrModels.SeriesPieDataValid("data")
    radius = AttrModels.SeriesPieRadiusValid("radius")
    roseType = AttrModels.SeriesPieRoseTypeValid("roseType")

    def __init__(self, **kwargs):
        self.type = "pie"
        for param in kwargs:
            if param not in SERIES_PIE_PARAMS:
                raise ValueError("没有{}参数".format(param))
        [self.__setattr__(param, kwargs.get(param, "")) for param in kwargs]


class GenJSONBar:
    """
    生成能被前端解析的json数据，生成柱状图表
    GenJSONBar(title="",legend=[图列1, 图列2, 图列3],xAxis=[x轴属性1, x轴属性2]，
                yAxis=[y轴属性1, y轴属性2,y轴属性3], series=“series的实例”多个使用series1,series2
                )

    """
    title = AttrModels.TitleValid("title")
    tooltip = AttrModels.TooltipValid("tooltip")
    legend = AttrModels.LegendValid("legend")
    xAxis = AttrModels.xAxisValid("xAxis")
    yAxis = AttrModels.yAxisValid("yAxis")
    series = AttrModels.SeriesValid("series")

    def __init__(self, **kwargs):
        if "title" not in kwargs.keys():
            raise ValueError("标题不能为空")
        [self.__setattr__(param, kwargs.get(param)) for param in kwargs if not param.startswith("series")]
        series_list = [kwargs.get(param) for param in kwargs if param.startswith("series")]
        self.__setattr__("series", series_list)

    def __repr__(self):
        # print(vars(self))
        string = ""
        for k, v in vars(self).items():
            string = string + "(" + str(k) + "=" + str(v) + ")"
        return "{}{}".format(self.__class__.__name__, string)

    def gen(self):
        """
        返回最后的结果
        :return:
        """
        return self._params_check()

    def _params_check(self):
        """
        把空的没有设置的参数设置为空字典
        :return:
        """
        _check_data = vars(self)
        for i in BAR_PARAMS:
            if i not in _check_data.keys():
                _check_data.update({i: {}})
        return _check_data


class GenJSONPie:
    """
    GenJsonPie（series="instance of SeriesPie" 多个使用series1,series2）
    """
    series = AttrModels.SeriesPieValid("series")
    tooltip = AttrModels.TooltipValid("tooltip")

    def __init__(self, **kwargs):
        [self.__setattr__(param, kwargs.get(param)) for param in kwargs if not param.startswith("series")]
        series_list = [kwargs.get(param) for param in kwargs if param.startswith("series")]
        self.__setattr__("series", series_list)

    def gen(self):
        return vars(self)
