# -*- coding: utf-8 -*-
# from odoo import http


# class Rapture(http.Controller):
#     @http.route('/rapture/rapture/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rapture/rapture/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('rapture.listing', {
#             'root': '/rapture/rapture',
#             'objects': http.request.env['rapture.rapture'].search([]),
#         })

#     @http.route('/rapture/rapture/objects/<model("rapture.rapture"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rapture.object', {
#             'object': obj
#         })
