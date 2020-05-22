from flask import Flask, request
import pandas as pd 
import sqlite3

app = Flask(__name__)

#--mendapatkan keseluruhan data employees
@app.route('/employee', methods=['GET'])
def get_emp():
    db_conn = sqlite3.connect("chinook.db")
    dt_emp = pd.read_sql_query("select (FirstName||' '||LastName) as FullName, Title, ReportsTo, BirthDate, HireDate, Address, City, State, Phone, Email from employees", db_conn)
    return(dt_emp.to_json())

#--mendapatkan total sales dari suatu type media di beberapa negara
@app.route('/media/<md_id>', methods=['GET'])
def get_track(md_id):
    db_conn = sqlite3.connect("chinook.db")
    dt_md_sales = pd.read_sql_query("SELECT inv.BillingCountry as Country, gnr.Name as Genre, md_typ.Name, SUM(inv.Total) as Total \
                                     FROM invoices as inv, invoice_items as inv_itm, tracks as trk, genres as gnr, media_types as md_typ \
                                     WHERE \
                                     inv.InvoiceId = inv_itm.InvoiceId \
                                     AND \
                                     inv_itm.TrackId = trk.TrackId \
                                     AND \
                                     trk.GenreId = gnr.GenreId \
                                     AND \
                                     trk.MediaTypeId = md_typ.MediaTypeId \
                                     AND \
                                     md_typ.MediaTypeId = %d \
                                     GROUP BY Genre \
                                     ORDER BY Total" %int(md_id), db_conn)
    dt_md_sales['Genre'] = dt_md_sales['Genre'].astype('category', errors='raise')                                 
    return(dt_md_sales.to_json())

#--mendapatkan total sales dari suatu negara
@app.route('/country/<country_nm>', methods=['GET'])
def get_genre(country_nm):
    db_conn = sqlite3.connect("chinook.db")
    dt_country_sales = pd.read_sql_query("SELECT inv.BillingCountry as Country, gnr.Name as Genre, md_typ.Name as Media_Nm, sum(inv.Total) as Total\
                                          FROM invoices as inv, invoice_items as inv_itm, tracks as trk, genres as gnr, media_types as md_typ \
                                          WHERE \
                                          inv.InvoiceId = inv_itm.InvoiceId \
                                          AND \
                                          inv_itm.TrackId = trk.TrackId \
                                          AND \
                                          trk.GenreId = gnr.GenreId \
                                          AND \
                                          trk.MediaTypeId = md_typ.MediaTypeId \
                                          AND \
                                          inv.BillingCountry = ? \
                                          GROUP BY Genre \
                                          ORDER BY Total DESC", db_conn, params=(country_nm,))

    dt_country_sales['Media_Nm'] = dt_country_sales['Media_Nm'].astype('category', errors='raise')
    return(dt_country_sales.to_json())   

#--mendapatkan total penjualan album
@app.route('/albums', methods=['GET'])
def get_album():
    db_conn = sqlite3.connect("chinook.db")
    dt_album = pd.read_sql_query("SELECT abm.Title as Album, art.Name as Artist, sum(inv.Total) as TotalSales, avg(inv.Total) as MeanSales\
                   FROM \
                   invoices as inv, invoice_items as inv_itm, tracks as trk, albums as abm, artists as art \
                   WHERE \
                   inv.InvoiceId = inv_itm.InvoiceId \
                   AND \
                   inv_itm.TrackId = trk.TrackId \
                   AND \
                   trk.AlbumId = abm.AlbumId \
                   AND \
                   abm.ArtistId = art.ArtistId \
                   GROUP BY abm.Title \
                   ORDER BY TotalSales DESC", db_conn)
    return(dt_album.to_json())

#--mendapatkan total sales per-employee
@app.route('/sales', methods=['GET'])
def get_sale():
    db_conn = sqlite3.connect("chinook.db")
    emp_sales = pd.read_sql_query("SELECT (emp.FirstName||' '||emp.LastName) as FullName, \
                                      sum(inv.Total) as TotalSales, inv.InvoiceDate as Period \
                                  FROM \
                                  employees as emp, customers as cst, invoices as inv \
                                  WHERE \
                                  emp.EmployeeId = cst.SupportRepId \
                                  AND \
                                  cst.CustomerId = inv.CustomerId \
                                  AND \
                                  emp.Title = 'Sales Support Agent' \
                                  GROUP BY FullName, inv.InvoiceDate", db_conn, parse_dates='Period')

    emp_sales['Period'] = pd.to_datetime(emp_sales['Period']).dt.to_period('M')
    dt_sales = pd.crosstab(index=emp_sales['Period'],
                           columns=emp_sales['FullName'],
                           values=emp_sales['TotalSales'],
                           aggfunc = 'sum').fillna(0)
    return(dt_sales.to_json())

#--mendapatkan total sales per-employee untuk setiap negara
@app.route('/empsales', methods=['GET'])
def get_empsales():
    db_conn = sqlite3.connect("chinook.db")
    emp_sales_count = pd.read_sql_query("SELECT (emp.FirstName||' '||emp.LastName) as FullName, \
                                      sum(inv.Total) as TotalSales, inv.BillingCountry as Country \
                                  FROM \
                                  employees as emp, customers as cst, invoices as inv \
                                  WHERE \
                                  emp.EmployeeId = +cst.SupportRepId \
                                  AND \
                                  cst.CustomerId = +inv.CustomerId \
                                  AND \
                                  emp.Title = 'Sales Support Agent' \
                                  GROUP BY BillingCountry \
                                  ORDER BY FullName, TotalSales", db_conn)

    dt_sales_count = emp_sales_count.fillna(0).stack()                               
    return(dt_sales_count.to_json())

if __name__ == '__main__':
     app.run(debug=True, port=5000)


