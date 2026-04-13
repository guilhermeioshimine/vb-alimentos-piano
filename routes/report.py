from flask import Blueprint, render_template, redirect, request
import sqlite3
from datetime import datetime
from models.models import *

report_bp = Blueprint('report', __name__)


@report_bp.route('/report')
def list_relatorio():
    report = Report.select().order_by(Report.report_data.desc()).limit(1000)
    reportList = []
    itemList = []
    for item in report:
        itemList = [item.id, item.report_data, item.recipe, item.product1, item.weight1, item.allotment1, item.product2, item.weight2, item.allotment2, item.product3, item.weight3, item.allotment3, item.product4, item.weight4, item.allotment4, item.product5, item.weight5, item.allotment5, item.product6, item.weight6, item.allotment6, item.product7,
                    item.weight7, item.allotment7, item.product8, item.weight8, item.allotment8, item.product9, item.weight9, item.allotment9, item.product10, item.weight10, item.allotment10, item.product11, item.weight11, item.allotment11, item.product12, item.weight12, item.allotment12, item.product13, item.weight13, item.allotment13, item.product14, item.weight14, item.allotment14, item.product15, item.weight15, item.allotment15, item.sum1, item.sum2]
        reportList.append(itemList)

    print(reportList)
    try:
        return render_template('report.html', titlePage='Dosagem - Piano', reports=reportList)
    except Exception as er:
        print(er)


@report_bp.route('/report_dosagens')
def list_dosagens():
    conn = sqlite3.connect('dosagem.db')
    cur = conn.cursor()
    cur.execute("SELECT id, receita, sequencia, codigo, produto, lote, unidade, peso, timestamp FROM dosagens ORDER BY timestamp DESC LIMIT 1000")
    rows = cur.fetchall()
    reportList = []
    for row in rows:
        # row: id, receita, sequencia, codigo, produto, lote, unidade, peso, timestamp
        ts = row[8]
        try:
            ts_dt = datetime.fromisoformat(ts)
        except Exception:
            ts_dt = ts
        item = [row[0], ts_dt, row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
        reportList.append(item)
    conn.close()
    try:
        return render_template('report_dosagens.html', titlePage='Dosagem Piano-PI', reports=reportList)
    except Exception as er:
        print(er)
