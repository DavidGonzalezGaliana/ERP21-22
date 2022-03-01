# -*- coding: utf-8 -*-
from datetime import date, timedelta
from odoo import models, fields, api
from datetime import datetime

from openerp import _
from openerp.exceptions import Warning

import random



class rapture(models.Model):
    _name = 'rapture.rapture'
    _description = 'rapture.rapture'

    name = fields.Char(string="Nombre", help='La ciudad contiene los distritos', default='Rapture')
    photo= fields.Image(max_width=100)

    external_influence   = fields.Integer(string="Porcentaje de influencia externa", readonly=True, help='Nivel de influencia hará que lleguen NPCs a Rapture pero otro paises se interesaran', default=0)
    science  = fields.Integer(string="Nivel de ciencia", readonly=True, help='Nivel de ciencia actual de Rapture', default=0)
    total_popolation = fields.Integer(string="Total de población", readonly=True, help='Numero total de la población de Rapture', default=0)
    sanity_opulation = fields.Integer(string="Locura de la población", readonly=True, help='Locura de la población de Rapture', default=0)
    player = fields.Many2one("res.partner", string="Jugador")

    total_oxygen = fields.Integer(string="Oxigeno total de la ciudad", readonly=True, default=0, help='Total de oxigeno de Rapture', compute='_calculate_total_oxygen')
    total_districts = fields.Integer(string="Cantidad de distritos", readonly=True, compute='_calculate_districts')

    districts = fields.One2many('rapture.district', 'rapture_district')


    districts_unavailable = fields.Many2many('rapture.district', compute='_get_districts_available')






    @api.depends('districts')
    def _get_districts_available(self):
        for b in self:
            b.districts_unavailable= b.districts.filtered(
                lambda w: w.defense <= 0
            )



    @api.depends('districts')
    def _calculate_districts(self):
        for r in self:
            r.total_districts=len(r.districts)



    @api.depends('districts')
    def _calculate_total_oxygen(self):
        for r in self:
            total_oxygen = 0
            total_popolation=0

            for d in r.districts:
                print("++++++++++++++++++++++++++")
                print("Total de oxigeno de la ciudad")
                print(d.name)
                print(d.total_oxygen_district)
                #r.total_oxygen+=d.total_oxygen_district

                total_oxygen+=d.total_oxygen_district



                print("++++++++++++++++++++++++++")
                print("Total de npcs de la ciudad")
                print(d.name)
                print(d.total_population_district)
                #r.total_popolation+=d.total_population_district
                total_popolation+=d.total_population_district
            r.total_oxygen=total_oxygen
            r.total_popolation=total_popolation



class player(models.Model):
    _name = 'res.partner'
   # _description = 'res.partner'
    _inherit = 'res.partner'

    is_player = fields.Boolean(default=False)
    #name = fields.Char(default="Andrew Ryan")
    photo= fields.Image(max_width=100)
    birthplace = fields.Char(default="Russian Empire")
    gender = fields.Char(default="Male")
    year_of_birth = fields.Date()

    health = fields.Integer(default=100)
    hunger = fields.Integer(default=100)
    sanity = fields.Integer(default=100)
    oxygen_consumption = fields.Integer(default=10)
    total_adam=fields.Integer(string="Total de Adam", readonly=True, help='Total de Adam del jugador', default=0, compute='_calculate_total_adam')
    
   
    big_daddys=fields.Many2many("rapture.big_daddy")

    city = fields.One2many('rapture.rapture','player', string="Ciudad" )


    def _getdrugs(self):
        all_drugs = self.env['rapture.plasmid'].search([]).ids

        random.shuffle(all_drugs)

        drugs=[]
        for i in range( 0, random.randint(0, 6)):
            drugs.append(all_drugs[i])
            print(all_drugs[i])
            print("se crea una droga")
            print(len(drugs))
        return drugs


    plasmids= fields.Many2many('rapture.plasmid', default=_getdrugs)
    district = fields.Many2many('rapture.district')


    @api.depends('big_daddys')
    def _calculate_total_adam(self):
            print("---------------------------------------")
            print("Se calcula el total de Adam del jugador")
            for r in self:
                print(r.name)
                print(r.big_daddys)
                total_adam=r.total_adam
                for d in r.big_daddys:
                    print("++++++++++++++++++++++++++")
                    print("Big Daddys ADAM")
                    total_adam+=d.total_adam_big_daddy
                r.total_adam=total_adam
                print(total_adam)


   


class district(models.Model):
    _name = 'rapture.district'
    _description = 'rapture.district'

    name = fields.Char()
    photo= fields.Image(max_width=300)

    defense = fields.Integer(string="Defensa", readonly=True, help='Defensa de la ciudad', default=500)

    space = fields.Selection([('small', 'Pequeño'),('medium','Medio'),('big','Grande')])
    sanity_population = fields.Integer(string="Locura de la población", readonly=True, help='Locura de la población de Rapture', default=0)

    #    space = fields.Float(random.random()*100, string="Total de oxigeno del distrito")
    total_oxygen_district = fields.Integer(string="Total de oxigeno del distrito", default=0,readonly=True)
    # total_topulation_district = fields.Integer(string="Poblacion del distrito", readonly=True, help='Capacidad del distrito en personas cambiar descripcion', default=0)
    total_population_district = fields.Integer(string="Total de la población", readonly=True, compute='_calculate_population')

    total_population_consumption = fields.Integer(string="Total de comsumo de Adam en el distrito", default=0, readonly=True, compute='_calculate_total_population_consumption')
    total_adam = fields.Integer(string="Adam", readonly=True, compute='_calculate_total_adam')

    total_adam_district = fields.Integer(string="Total de Adam del distrito", readonly=True, help='Total de Adam del distrito', default=0)

    
    @api.depends('npcs')
    def _calculate_population(self):
        for r in self:
            r.total_population_district=len(r.npcs)


    rapture_district = fields.Many2one("rapture.rapture", string="Ciudad",)
    npcs = fields.One2many('rapture.npc','npc_reside')
    player = fields.Many2one("res.partner")
    start= fields.Datetime(default=lambda self: fields.Datetime.now())
    time_to_end = fields.Datetime(string="Fecha de fin", compute='_calculate_time')
    widget_time = fields.Float(compute='_calculate_time_widget')
    state = fields.Selection([('preparation', 'Preparation'), ('inprogress', 'In Progress'), ('finished', 'Finished')],
                             default='preparation')


    @api.depends('npcs')
    def _calculate_total_population_consumption(self):
        print("_calculate_total_population_consumption")
        for r in self:
            total_population_consumption=0
            for n in r.npcs:
                print(r)
                total_population_consumption+=n.adam
            r.total_population_consumption=total_population_consumption

    @api.depends('time_to_end')
    def _calculate_time(self):
        for f in self:
            if f.start:

                variable=24-len(f.player.big_daddys)
                data = fields.Datetime.from_string(f.start)
                #print(data)
                #print(f.start)

                data=data+timedelta(hours=variable)
                f.time_to_end=fields.Datetime.to_string(data)
            else:
                f.time_to_end=False



    @api.depends('player')
    def _calculate_total_adam(self):
        for s in self:
            total_adam=0
            for p in s.player:
                total_adam=p.total_adam
            s.total_adam=total_adam

     




    @api.depends('widget_time')
    def _calculate_time_widget(self):
        for f in self:
            if f.start:
                start=fields.Datetime.from_string(f.start) 
                end=fields.Datetime.from_string(f.time_to_end)
                now = datetime.now()

            # print(start)
              #   print(end)
              #   print(now)
              #   print((end-start).total_seconds() / 60)

           
                time_to_complete = ((end-start).total_seconds() / 60)
                time = ((now-start).total_seconds() / 60)
               #  print(time_to_complete)
               #  print(time)
               #  print("resultado")
              #   print(time/time_to_complete)
                if((time/time_to_complete)<1):
                    f.write({'state': 'inprogress'})
                    f.widget_time= (time/time_to_complete)*100

                else:
                    f.write({'state': 'finished'})
                    f.widget_time= 100

            else:
                f.widget_time= 0
                
    @api.model
    def update_oxygen(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Se actualiza el oxigeno")

        distrits = self.env['rapture.district'].search([])

        for d in distrits:

            if(d.space=='small'):
                oxygen_space = 30

            if(d.space=='medium'):
                oxygen_space = 60
           
            if(d.space=='big'):
                 oxygen_space = 100


            print("Se actualiza el oxigeno :", d.name)
            print("Space :", d.space)
            total_all_oxygen_consum = d.total_population_district * 10
            print("Total consumo de la poblacion :",total_all_oxygen_consum)
            d.total_oxygen_district=(oxygen_space - total_all_oxygen_consum )



    @api.model
    def update_adam_consumption(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Se actualiza el la cantidad de ADAM")

        distrits = self.env['rapture.district'].search([])

        for d in distrits:
            print(d.name)
            print("Consumo de la poblacion")
            print("ESTOY AQUI?¿?¿?¿??¿?¿?¿?¿??¿?¿?¿?¿?¿?¿?¿?¿?¿?¿?")
            print(d.name)
            print(d.total_adam, "total de consumo:",d.total_population_consumption)
            total_adam=d.total_adam
            print(total_adam)
            #d.total_adam=total_adam-d.total_population_consumption
            d.total_adam_district=d.total_adam-d.total_population_consumption

            print("total",d.total_adam) 

    def _total_damaged(self):
        for b in self:
            total_damaged = 0
            for l in b.npcs:
                total_damaged+=l.damaged
            b.total_damaged_district=total_damaged


    total_damaged_district=fields.Integer(string="Total de daño", default=0 ,readonly=True, compute='_total_damaged')



class npc(models.Model):
    _name = 'rapture.npc'
    _description = 'rapture.npc'

    photo= fields.Image(max_width=130)
    def _name_generator(self):
        subnames=["Smith","Johnson"]
        name=["Aaren" ,"Zuzana" ]  
        return random.choice(subnames)+", "+random.choice(name)

        
    
    name = fields.Char(string="Nombre", default=_name_generator, readonly=True)

    health = fields.Integer(default=100 ,readonly=True)
    sanity = fields.Integer(default=100 ,readonly=True)
    oxygen_consumption = fields.Integer(default=10 ,readonly=True)
    gender = fields.Char(default="Male")
    npc_reside = fields.Many2one("rapture.district")


    def _rand_damage(self):
        return  random.randint(50, 1000) 

    damaged = fields.Integer(string="Damaged", default=_rand_damage ,readonly=True)


    def _quantity_adam_generator(self):
        return  random.randint(1, 100)

    adam= fields.Integer(default=_quantity_adam_generator ,readonly=True)

    #splicer = fields.Boolean(readonly=True, default=False) 
    splicer = fields.Boolean(string="Si el personaje supera un 80 de adicción al Adam se convertirá en un splicer", readonly=True, compute='_splicer_check')

    def _splicer_check(self):
        for npc in self:
            if (npc.adam >= 80):
                npc.splicer=True
            else:
               npc.splicer=False 



    @api.model
    def update_life_npc(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Se la vida de los npc")

        npcs = self.env['rapture.npc'].search([])
        for n in npcs:
            oxigen = n.npc_reside.total_oxygen_district
            print("Nombre", n.name)
            print("Distrito", n.npc_reside.name)
            print("Vida", n.health)
            print("Nivel del oxigeno", oxigen)


            if(oxigen<0):
                if(n.health>0):
                    n.health=n.health-10




   # adicciones = fields.Many2many('rapture.plasmid', default_getdrugs)

class plasmid(models.Model):
    _name = 'rapture.plasmid'
    _description = 'rapture.plasmid'

    name=fields.Char()



class generate_big_daddy(models.Model):
    _name = 'rapture.big_daddy'
    _description = 'rapture.big_daddy'





class big_daddy(models.Model):
    _name = 'rapture.big_daddy'
    _description = 'rapture.big_daddy'

    player=fields.Many2many("res.partner")
    is_premium = fields.Boolean(default=False)
    total_adam_big_daddy=fields.Integer(string="Adam", default=0 ,readonly=True, compute='_total_adam_big_daddy')
    health = fields.Integer(default=100)
    damaged = fields.Integer(default=100)

    
#aquí va las fotos y tal

    def _type_big_daddy_genertor(self):
            types=["Bouncer","Rosie","Rumbler","Alpha Series","Lancer"]
            return random.choice(types)
    
    name = fields.Char(string="Big Daddy Types", default= _type_big_daddy_genertor, readonly=True)



    def _assign_little_sister(self):
        all_little_sister = self.env['rapture.little_sister'].search([]).ids

        random.shuffle(all_little_sister)

        little_sister=[]
        for i in range( 1, random.randint(1, 3)):
            little_sister.append(all_little_sister[i])
            print(all_little_sister[i])
            print("se asigna una little sister")

        return little_sister

    little_sister= fields.Many2many('rapture.little_sister', default=_assign_little_sister)

    def _total_adam_big_daddy(self):
        for b in self:
            total_big_daddy_adam = 0
            for l in b.little_sister:
                total_big_daddy_adam+=l.adam
            b.total_adam_big_daddy=total_big_daddy_adam

            

class little_sister(models.Model):
    _name = 'rapture.little_sister'
    _description = 'rapture.little_sister'

    name=fields.Char()
    adam=fields.Integer(string="Adam", default=0 ,readonly=True)


    @api.model
    def update_adam_production(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Produccion de Adam en el modelo little_sister")
       
        big = self.env['rapture.big_daddy'].search([])
        for b in big:
            little = b.little_sister
            adam=0
            for l in little:
                print(l.name)
                adam+=10
            print("++++++++++++++++++++++KKAKAKAKAKAK++++++++++++++++++++++++++")
            print(adam)
            l.adam=adam


class res_partner_premium(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def apply_premium(self, health, damaged ):
       print("++++++++++++++++++++++res_partner_premium(models.Model)++++++++++++++++++++++")
      # id = self.env['rapture.big_daddy'].search([]).ids
       #print(id)

       self.big_daddys.create({"player":[self.id], "is_premium":True, "health":health, "damaged":damaged})

    

class product_premium(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    is_premium = fields.Boolean(default=False)
    health = fields.Integer()
    damaged  = fields.Integer()

    big_daddy = fields.Many2one('rapture.big_daddy')


class ventas_big_daddy(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    adam=fields.Integer(string="Adam", default=0 ,readonly=True)
    #big_daddy = fields.Many2one('rapture.big_daddy')
    premium_applied = fields.Boolean(default=False)


    def apply_premium(self):
        premium_products = self.order_line.filtered(lambda p: p.product_id.is_premium == True and self.premium_applied == False)
        for p in premium_products:
             self.partner_id.apply_premium(p.product_id.health, p.product_id.damaged)
        #self.premium_applied = True

    def write(self,values):
        super(ventas_big_daddy,self).write(values)
        self.apply_premium()

    @api.model
    def create(self,values):
        record = super(ventas_big_daddy,self).create(values)
        record.apply_premium()
        return record


#===========================================================================================================+

class npc_transient(models.TransientModel):
    _name = 'rapture.npc_transient'

    npc = fields.Many2one('rapture.npc')
    wizard = fields.Many2one('rapture.district_wizard')




class district_wizard(models.TransientModel):
    _name = 'rapture.district_wizard'
    _description = "district_wizard"

    name = fields.Char()
    photo= fields.Image(max_width=300)

    space = fields.Selection([('small', 'Pequeño'),('medium','Medio'),('big','Grande')])

    rapture_district = fields.Many2one("rapture.rapture", string="Ciudad")
    #npcs = fields.One2many('rapture.npc','npc_reside')
    npcs = fields.One2many('rapture.npc_transient','wizard')


    player = fields.Many2one("res.partner")
    start= fields.Datetime(default=lambda self: fields.Datetime.now())
    time_to_end = fields.Datetime(string="Fecha de fin", compute='_calculate_time')
    widget_time = fields.Float(compute='_calculate_time_widget')
    stateTime = fields.Selection([('preparation', 'Preparation'), ('inprogress', 'In Progress'), ('finished', 'Finished')],
                             default='preparation')


    @api.model
    def district_wizard_action(self):
        action = self.env.ref('rapture.district_wizard_action').read()[0]
        return action

    api.depends('npcs')
    def _calculate_population(self):
        for r in self:
            r.total_population_district=len(r.npcs)



    @api.depends('player')
    def _calculate_total_adam(self):
        for s in self:
            total_adam=0
            for p in s.player:
                total_adam=p.total_adam
            s.total_adam=total_adam


    @api.depends('time_to_end')
    def _calculate_time(self):
        for f in self:
            if f.start:

                variable=24-len(f.player.big_daddys)
                data = fields.Datetime.from_string(f.start)
                #print(data)
                #print(f.start)

                data=data+timedelta(hours=variable)
                f.time_to_end=fields.Datetime.to_string(data)
            else:
                f.time_to_end=False



    @api.depends('widget_time')
    def _calculate_time_widget(self):
        for f in self:
            if f.start:
                start=fields.Datetime.from_string(f.start) 
                end=fields.Datetime.from_string(f.time_to_end)
                now = datetime.now()
                time_to_complete = ((end-start).total_seconds() / 60)
                time = ((now-start).total_seconds() / 60)
    
                if((time/time_to_complete)<1):
                    f.write({'stateTime': 'inprogress'})
                    f.widget_time= (time/time_to_complete)*100

                else:
                    f.write({'stateTime': 'finished'})
                    f.widget_time= 100

            else:
                f.widget_time= 0
                




    @api.onchange('player')
    def _onchange_player(self):
        if self.player != False:
            city = self.player.city
            return {
                'domain': {
                    'rapture_district': [('id', 'in', city.ids)]
                }
            }






    state = fields.Selection([('part1','Parte 1'),('part2','Parte 2'),('part3','Parte 3'),('part4','Parte 4')], default = 'part1')


    def next(self):
        state = self.state
        if state == 'part1':
            if self.name != False and self.photo != False and self.space != False :
                self.state = 'part2'
            else:
                raise Warning(_('Completa todos los campos para continuar!'))
        elif state == 'part2':
            if self.player != False and self.rapture_district != False and len(self.npcs) > 0 :
                self.state = 'part3'
            else:
                raise Warning(_('Completa todos los campos para continuar!'))
        elif state == 'part3':
            self.state = 'part4'

        return {
            'name': 'Rapture district wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': dict(self._context, npcs_context=(self.npcs.npc).ids),
          
        }

    def previous(self):
        state = self.state
        if state == 'part2':
            self.state = 'part1'
        elif state == 'part3':
            self.state = 'part2'
        elif state == 'part4':
            self.state = 'part3'

        return {
            'name': 'Rapture distric wizard action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def create_district(self):
        for c in self:
            #npcs=[]
           # for p in c.player:
               #player=c.env['res.partner'].create({'name':p.name, 'is_player':True})
              # npcs.append(player.id)

            district = c.env['rapture.district'].create({'name':c.name, 
                                                        'photo':c.photo,
                                                        'space':c.space, 
                                                        'player':c.player.id,
                                                        'rapture_district':c.rapture_district.id,
                                                        'npcs':c._context['npcs_context']})
        return {
            'name': 'create_district',
            'type': 'ir.actions.act_window',
            'res_model': 'rapture.district',
            'res_id': district.id,
            'view_mode': 'form',
            'target': 'current',
        }


###########################################################################################################################################




class npc_wizard(models.TransientModel):
    _name = 'rapture.npc_wizard'
    _description = "npc_wizard"

    photo= fields.Image(max_width=130)       
    name = fields.Char(string="Nombre")
    gender = fields.Char(default="Male")



    def _default_reside(self):
        print(self._context)
        if('district_context' in self._context):
            print("_default_reside")
            print(self._context)
            district = self._context['district_context']
            return district

    npc_reside = fields.Many2one("rapture.district", default=_default_reside)


    def _quantity_adam_generator(self):
        return  random.randint(1, 100)

    adam= fields.Integer(default=_quantity_adam_generator ,readonly=True)
    splicer = fields.Boolean(string="Si el personaje supera un 80 de adicción al Adam se convertirá en un splicer", readonly=True, compute='_splicer_check')


    state = fields.Selection([('part1','Aspecto'),('part2','Residencia'),('part3','Atributos'),('part4','Resumen')], default = 'part1')




    def _splicer_check(self):
        for npc in self:
            if (npc.adam >= 80):
                npc.splicer=True
            else:
               npc.splicer=False 


    def next(self):
        state = self.state
        if state == 'part1':
            if self.name != False and self.photo != False :
                self.state = 'part2'
        elif state == 'part2':
            if self.npc_reside != False and self.gender != False :
                self.state = 'part3'
        elif state == 'part3':
            self.state = 'part4'

        return {
            'name': 'Rapture district npc action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context' : self._context
        }

    def previous(self):
        state = self.state
        if state == 'part2':
            self.state = 'part1'
        elif state == 'part3':
            self.state = 'part2'
        elif state == 'part4':
            self.state = 'part3'

        return {
            'name': 'Rapture distric npc action',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def create_npc(self):
        for n in self:
    
            npc = n.env['rapture.npc'].create({'name':n.name, 
                                                        'photo':n.photo,
                                                        'gender':n.gender, 
                                                        'npc_reside':n.npc_reside.id,
                                                        'adam':n.adam,
                                                        'splicer':n.splicer})



        return {
            'name': 'create_npc',
            'type': 'ir.actions.act_window',
            'res_model': 'rapture.npc',
            'res_id': npc.id,
            'view_mode': 'form',
            'target': 'current',
        }

################################################################################################33##3
##############################################################################################################


class distric_battle(models.TransientModel):
    _name = 'rapture.distric_battle_wizard'
    _description = "distric_battle"


    player = fields.Many2one("res.partner", string="Jugador")
    city = fields.Many2one("rapture.rapture", string="Ciudad")
    rapture_district = fields.Many2one("rapture.district", string="Distritos")
    
    total_damaged=fields.Integer(default=0 ,readonly=True, compute='_total_damaged', string="Damage")

    ganadorStr = fields.Char()

    @api.onchange('player')
    def _onchange_player(self):
        if self.player != False:
            city = self.player.city
            return {
                'domain': {
                    'city': [('id', 'in', city.ids)]
                }
            }

    @api.onchange('city')
    def _onchange_city(self):
        if self.city != False:
            district = self.city.districts
            return {
                'domain': {
                    'rapture_district': [('id', 'in', district.ids)]
                }
            }


    def _total_damaged(self):
        for b in self:
            for l in b.rapture_district:
                b.total_damaged=l.total_damaged_district



    player2 = fields.Many2one("res.partner", string="Jugador")
    city2 = fields.Many2one("rapture.rapture", string="Ciudad")
    rapture_district2 = fields.Many2one("rapture.district", string="Distritos")
    total_damaged2=fields.Integer(default=0 ,readonly=True, compute='_total_damaged2', string="Damage")
    

    @api.onchange('player2')
    def _onchange_player2(self):
        if self.player2 != False:
            city2 = self.player2.city
            return {
                'domain': {
                    'city2': [('id', 'in', city2.ids)]
                }
            }

    @api.onchange('city2')
    def _onchange_city2(self):
        if self.city2 != False:
            district2 = self.city2.districts
            return {
                'domain': {
                    'rapture_district2': [('id', 'in', district2.ids)]
                }
            }


    def _total_damaged2(self):
        for b in self:
            b.total_damaged2 = 0
            for l in b.rapture_district2:
                b.total_damaged2=l.total_damaged_district
                



    state = fields.Selection([('part1','Ciudad Atacante'),('part2','Ciudad Atacada'),('part3','Resumen'),('part4','Resultado de la batalla')], default = 'part1')


    winner_battle=fields.Integer(string="Total de daño", default=0 ,readonly=True, compute='_winner_battle')
    aplly_winner=fields.Integer(string="Ganador", default=0 ,readonly=True, compute='_aplly_winner')

    def _winner_battle(self):
        for f in self:
            f.winner_battle = 0
            if (f.total_damaged > f.total_damaged2):
                f.winner_battle = random.randint(0, 1)
            f.winner_battle =  random.randint(0, 3)


    def _aplly_winner(self):
        print("++++++++++++++++++++++++++")
        print("555555555555555555555555555555555555555555555555555555555555555555")
        for f in self:
            f.aplly_winner = 2
            if f.winner_battle == 1:
                for l in f.rapture_district2:
                    l.defense = f.total_damaged - l.defense 
                    f.aplly_winner = 1
                    f.ganadorStr= l.name
            else:
                for p in f.rapture_district:
                    p.defense =  f.total_damaged2 - p.defense
                    f.aplly_winner = 1
                    f.ganadorStr= p.name


    

    def next(self):
        state = self.state
        if state == 'part1':
                self.state = 'part2'
        elif state == 'part2':
                self.state = 'part3'
        elif state == 'part3':
            self.state = 'part4'

        return {
            'name': 'Rapture battle',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context' : self._context
        }
    
    def previous(self):
        state = self.state
        if state == 'part2':
            self.state = 'part1'
        elif state == 'part3':
            self.state = 'part2'
        elif state == 'part4':
            self.state = 'part3'

        return {
            'name': 'Rapture battle',
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
