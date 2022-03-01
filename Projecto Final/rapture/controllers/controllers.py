from odoo import http
import json
from odoo import tools
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



class banner_district_controller(http.Controller):
    @http.route('/rapture/disctrict_banner', auth='user', type='json')
    def banner(self):
        return {
            'html': """
                <style>
                .button-49,
                .button-49:after {
                width: 150px;
                height: 76px;
                line-height: 78px;
                font-size: 20px;
                font-family: 'Bebas Neue', sans-serif;
                background: linear-gradient(45deg, transparent 5%, #FF013C 5%);
                border: 0;
                color: #fff;
                letter-spacing: 3px;
                box-shadow: 6px 0px 0px #00E6F6;
                outline: transparent;
                position: relative;
                user-select: none;
                -webkit-user-select: none;
                touch-action: manipulation;
                }

                .button-49:after {
                --slice-0: inset(50% 50% 50% 50%);
                --slice-1: inset(80% -6px 0 0);
                --slice-2: inset(50% -6px 30% 0);
                --slice-3: inset(10% -6px 85% 0);
                --slice-4: inset(40% -6px 43% 0);
                --slice-5: inset(80% -6px 5% 0);
                
                content: 'ALTERNATE TEXT';
                display: block;
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(45deg, transparent 3%, #00E6F6 3%, #00E6F6 5%, #FF013C 5%);
                text-shadow: -3px -3px 0px #F8F005, 3px 3px 0px #00E6F6;
                clip-path: var(--slice-0);
                }

                .button-49:hover:after {
                animation: 1s glitch;
                animation-timing-function: steps(2, end);
                }

                @keyframes glitch {
                0% {
                    clip-path: var(--slice-1);
                    transform: translate(-20px, -10px);
                }
                10% {
                    clip-path: var(--slice-3);
                    transform: translate(10px, 10px);
                }
                20% {
                    clip-path: var(--slice-1);
                    transform: translate(-10px, 10px);
                }
                30% {
                    clip-path: var(--slice-3);
                    transform: translate(0px, 5px);
                }
                40% {
                    clip-path: var(--slice-2);
                    transform: translate(-5px, 0px);
                }
                50% {
                    clip-path: var(--slice-3);
                    transform: translate(5px, 0px);
                }
                60% {
                    clip-path: var(--slice-4);
                    transform: translate(5px, 10px);
                }
                70% {
                    clip-path: var(--slice-2);
                    transform: translate(-10px, 10px);
                }
                80% {
                    clip-path: var(--slice-5);
                    transform: translate(20px, -10px);
                }
                90% {
                    clip-path: var(--slice-1);
                    transform: translate(-10px, 0px);
                }
                100% {
                    clip-path: var(--slice-1);
                    transform: translate(0);
                }
                }

                @media (min-width: 768px) {
                .button-49,
                .button-49:after {
                    width: 200px;
                    height: 43px;
                    line-height: 44px;
                }
                }
                        }</style>

                <div class="rapture_banner" style="height: 450px; background-size:100%; background-image: url(/rapture/static/src/img/banner.gif)">
                    <div class="rapture_button" style="position: static; color:#fff;">
                        <a class="banner_button, button-49" type="action" data-reload-on-close="true" 
                        role="button" data-method="district_wizard_action" data-model="rapture.district_wizard">Crear distrito</a>
                </div>
                </div> """
        }
