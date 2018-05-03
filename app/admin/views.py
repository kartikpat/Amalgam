
from ..utilities import isLoggedIn
from . import admin

# @admin.route('/dashboard')
# def loadDashboard():
#     if isLoggedIn():
#         result = Dbhelper.findOne('User' , {"email":session['email']})
#         listOfProducts = result['products']
#         dic = {}
#         for product in listOfProducts:
#             dic[product] = getListOfUser(product)
#         return render_template('admin.html',dict=dic)
#     return redirect(url_for('auth.login'))
