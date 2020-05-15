from flask import Flask, request
import pandas as pd 
import sqlite3

app = Flask(__name__)

#--mendapatkan keseluruhan data employees
@app.route('/emp', methods=['GET'])
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
    return(dt_md_sales.to_json())

#--mendapatkan total sales dari suatu negara
@app.route('/country/<nama>', methods=['GET'])
def get_genre(nama):
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
                                          ORDER BY Total DESC", db_conn, params=(nama,))
    return(dt_country_sales.to_json())    


if __name__ == '__main__':
     app.run(debug=True, port=5000)


