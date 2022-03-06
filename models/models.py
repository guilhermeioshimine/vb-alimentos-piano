from peewee import *

db = SqliteDatabase('Gmaqui.db')

class BaseModel(Model):
    class Meta:
        database = db

class Report(BaseModel):
    report_data     = DateTimeField()
    recipe          = CharField()
    product1        = CharField()
    weight1         = DecimalField()
    product2        = CharField()
    weight2         = DecimalField()
    product3        = CharField()
    weight3         = DecimalField()
    product4        = CharField()
    weight4         = DecimalField()
    product5        = CharField()
    weight5         = DecimalField()
    product6        = CharField()
    weight6         = DecimalField()
    product7        = CharField()
    weight7         = DecimalField()
    product8        = CharField()
    weight8         = DecimalField()
    product9        = CharField()
    weight9         = DecimalField()
    product10        = CharField()
    weight10         = DecimalField()
    product11        = CharField()
    weight11         = DecimalField()
    product12        = CharField()
    weight12         = DecimalField()
    product13        = CharField()
    weight13         = DecimalField()
    product14        = CharField()
    weight14         = DecimalField()
    product15        = CharField()
    weight15         = DecimalField()
    sum1             = DecimalField()
    sum2             = DecimalField()

Report.create_table()