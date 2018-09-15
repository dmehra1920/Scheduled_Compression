# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import TemplateView
from .models import spm
from django.http import HttpResponse
import json
from django.http import HttpResponseRedirect



class FusionCharts:
    # constructorOptions = {}
    constructorTemplate = """
     <script type="text/javascript">
         FusionCharts.ready(function () {
             new FusionCharts(__constructorOptions__);
         });
     </script>"""
    renderTemplate = """
     <script type="text/javascript">
         FusionCharts.ready(function () {
             FusionCharts("__chartId__").render();
         });
     </script>
   """

    # constructor
    def __init__(self, type, id, width, height, renderAt, dataFormat, dataSource):
        self.constructorOptions = {}
        self.constructorOptions['type'] = type
        self.constructorOptions['id'] = id
        self.constructorOptions['width'] = width
        self.constructorOptions['height'] = height
        self.constructorOptions['renderAt'] = renderAt
        self.constructorOptions['dataFormat'] = dataFormat
        # dataSource = unicode(dataSource, errors='replace')
        self.constructorOptions['dataSource'] = dataSource

    # render the chart created
    # It prints a script and calls the FusionCharts javascript render method of created chart
    def render(self):
        self.readyJson = json.dumps(self.constructorOptions)
        self.readyJson = FusionCharts.constructorTemplate.replace('__constructorOptions__', self.readyJson)
        self.readyJson = self.readyJson + FusionCharts.renderTemplate.replace('__chartId__',
                                                                              self.constructorOptions['id'])
        self.readyJson = self.readyJson.replace('\\n', '')
        self.readyJson = self.readyJson.replace('\\t', '')

        if (self.constructorOptions['dataFormat'] == 'json'):
            self.readyJson = self.readyJson.replace('\\', '')
            self.readyJson = self.readyJson.replace('"{', "{")
            self.readyJson = self.readyJson.replace('}"', "}")

        return self.readyJson




class homepage(TemplateView):
    def get(self,request,**kwargs):
        return render(request,"home.html")



class display(TemplateView):
    def get(self,request,**kwargs):
        self.activity=request.GET['select']
        self.orignal_duration= request.GET['od']
        self.orignal_resources= request.GET['ors']
        self.orignal_cost= request.GET['oc']
        self.additional_resources=request.GET['adres']
        self.additional_cost=request.GET['ac']
        self.crash_duration_days = request.GET['cd']
        self.time_saved = request.GET['time']
        self.total_cost = request.GET['tc']
        s=spm(activity=self.activity,orignal_duration=self.orignal_duration,orignal_resources=self.orignal_resources, orignal_cost=self.orignal_cost,additional_resources=self.additional_resources, additional_cost=self.additional_cost, crash_duration_days= self.crash_duration_days, time_saved = self.time_saved, total_cost= self.total_cost )
        s.save()
        return render(request,'display.html',{'select':self.activity, 'od': self.orignal_duration, 'ors': self.orignal_resources, 'adres': self.additional_resources, 'oc': self.orignal_cost, 'ac': self.additional_cost,'cd': self.crash_duration_days, 'time': self.time_saved, 'tc': self.total_cost})


def save(request):
    values = spm.objects.all()
    dataSource = {}
    # setting chart cosmetics
    dataSource['chart'] = {
        "caption": "Scheduled Compression Analysis",
        "subCaption": "Total Cost Estimation",
        "xAxisName": "Activity",
        "yAxisName": "Total Cost",
	   "paletteColors": "#0075c2",
        "bgColor": "tomato",
        "borderAlpha": "20",
        "canvasBorderAlpha": "0",
        "usePlotGradientColor": "0",
        "plotBorderAlpha": "10",
        "placevaluesInside": "1",
        "rotatevalues": "1",
        "valueFontColor": "#ffffff",
        "showXAxisLine": "1",
        "xAxisLineColor": "#999999",
        "divlineColor": "#999999",
        "divLineDashed": "1",
        "showAlternateHGridColor": "0",
        "subcaptionFontBold": "0",
        "subcaptionFontSize": "14",
        "animation":"1",
        "animationDuration":"2",
    }

    dataSource['data'] = []
    # The data for the chart should be in an array wherein each element of the array is a JSON object as
    # `label` and `value` keys.
    # Iterate through the data in `Country` model and insert in to the `dataSource['data']` list.
    for key in spm.objects.all():
        data = {}
        data['label'] = key.activity
        data['value'] = key.total_cost
        dataSource['data'].append(data)

        # Create an object for the Column 2D chart using the FusionCharts class constructor
    column2D = FusionCharts("column2d", "ex1", "900", "400", "chart-1", "json", dataSource)
    # returning complete JavaScript and HTML code, which is used to generate chart in the browsers.
    return render(request,'result.html',{"values":values,"output":column2D.render()})