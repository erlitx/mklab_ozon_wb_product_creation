from odoo import api, exceptions, fields, models
import logging
import requests
import pprint
import json



class medicalsessionlines(models.Model):
    _name='medical.sessionline'
    name=fields.Char('Название')
    type=fields.Selection(
    [('char', 'Текст'),
     ('float', 'Число'), 
     ('many', 'Выбор из справочника'), 
     ('bin', 'Файл'), 
     ('date', 'Дата')    
    ],  default='char',  required=1,string='Тип данных')
    value_char=fields.Text('Текст')
    value_float=fields.Float('Число')
    value_many=fields.Many2many('sessionline.select',string='Выбор из справочника') #поставить домен на тип
    value_bin=fields.Binary('Файл')
    value_date=fields.Date('Дата')
    session_id=fields.Many2one('medical.session', string='Протокол')
    template_id=fields.Many2one('medical.session', string='Шаблон')
    tmp_name= fields.Char('Название')


    @api.multi
    def name_get(self):
        result=[]
        for s in self:
            res_txt=(s.name+': ' if s.name else '')
            if s.value_char:
               res_txt += s.value_char
            if s.value_float != 0:
                res_txt+=str(s.value_float)
            if s.value_many:
                for val in s.value_many:
                   res_txt+=val.name +', ' if val!=s.value_many[-1] else val.name
            if s.value_date:
                res_txt+=s.value_date       
            result.append((s.id, res_txt))    
        return result 
    

    @api.onchange('name', 'type', 'value_char','value_float','value_many','value_bin','value_date')
    def set_tmp_name(self):
        for s in self:
            res_txt=(s.name+': ' if s.name else '')
            if s.value_char:
               res_txt+=s.value_char
            if s.value_float!=0:
                res_txt+=str(s.value_float)
            if s.value_many:
                for val in s.value_many:
                   res_txt+=val.name +', ' if val!=s.value_many[-1] else val.name
            if s.value_date:
                res_txt+=s.value_date
            s.tmp_name = res_txt