# -*- coding: utf-8 -*-

from odoo import http


class TestApi(http.Controller):

    @http.route("/api/test", methods=["GET"], type="http", auth="none", csrf=False)
    def test_endpoint(self):
        print("inside test_endpoint method")
        return "Hello from Test API!"

# class TestApi(http.Controller):
#
#     @http.route("/api/test", methods=["GET"], type="http", auth="none", csrf=False)
#     def test_endpoint(self):
#         print("inside test_endpoint method")
#         return "Hello from Test API!"

#     @http.route('/app_one/app_one/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('app_one.listing', {
#             'root': '/app_one/app_one',
#             'objects': http.request.env['app_one.app_one'].search([]),
#         })

#     @http.route('/app_one/app_one/objects/<model("app_one.app_one"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('app_one.object', {
#             'object': obj
#         })
