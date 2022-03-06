from flask import Blueprint, render_template, redirect, request
from models.models import *

report_bp = Blueprint('report', __name__)


@report_bp.route('/report')
def list_relatorio():
    report = Report.select().order_by(Report.report_data)
    reportList = []
    itemList = []
    for item in report:
        itemList = [item.id, item.report_data, item.recipe, item.product1, item.weight1, item.product2, item.weight2, item.product3, item.weight3, item.product4, item.weight4, item.product5, item.weight5, item.product6, item.weight6, item.product7,
                    item.weight7, item.product8, item.weight8, item.product9, item.weight9, item.product10, item.weight10, item.product11, item.weight11, item.product12, item.weight12, item.product13, item.weight13, item.product14, item.weight14, item.product15, item.weight15, item.sum1, item.sum2]
        reportList.append(itemList)

    print(reportList)
    try:
        return render_template('report.html', titlePage='Relatório', reports=reportList)
    except Exception as er:
        print(er)
