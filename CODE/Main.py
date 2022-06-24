#    this programs aim at requesting data market on blockchain.com via API and submit order
#    Copyright (C) 2021  BinderL binders@laposte.net

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#    The base URL to be used for all calls is
#    https://api.blockchain.com/v3/exchange

import json
from random import random
from functools import reduce

ROUND = 3
REWARD = 1





def get_options():
    with open("./CODE/in.json", "r") as _options:
        opt = json.load(_options)
    return opt



def deposit_round(opt):
    totalAccount = sum(opt["clusters_DAO"])
    tv_USD = opt["tv_USD"]
    deposited = []
    _deposit(deposited, tv_USD, 0, totalAccount)
    return deposited

def _deposit(deposited, tv_USD, _id=0, _total=0):
    rand = random()
    _compute_deposit(deposited, _id, rand, tv_USD) if rand > 0.5 else False
    return _deposit(deposited, tv_USD, _id+1, _total) if _id < _total else deposited

def _compute_deposit(_tab, _id, _rand, _tv_USD):
    _random = _rand *10 - int(_rand*10)
    _tab.append((_id, _random * _tv_USD/10))

def checkSum_tuple(_tuple):
    return reduce(lambda x,y:(x[0] + y[0], x[1]+y[1]), _tuple)

TV_DAO = [[],[],[]] 
TV_USD = []
 

def run(opt, stage=0, stage_max= 10): 
    deposited = deposit_round(opt)
    start_round( opt, deposited)
    tv_DAO, tv_USD = record(opt, TV_DAO, TV_USD)
    return opt if stage >= stage_max else run(opt, stage+1, stage_max)

def record(opt, tv_DAO, tv_USB):
    TV_DAO[0].append(opt["tv_DAO"][0])
    TV_DAO[1].append(opt["tv_DAO"][1])
    TV_DAO[2].append(opt["tv_DAO"][2])
    TV_USD.append(opt["tv_USD"])
    return tv_DAO, tv_USB


    

def mine(opt):
    _a, _b = compute_miningDistrib(opt["tv_USD"]) 
    opt["tv_USD"] = opt["tv_USD"] + _a * opt["tv_USD"] + _b
    


def start_round(opt, deposited, _round = 0):
    mine(opt)
    mine(opt)
    mine(opt) 
    return mint_shares(iter(deposited), opt)


def burn_round(opt, _deposited):
    opt["tv_USD"] = opt["tv_USD"] - checkSum_tuple(_deposited)[1]
    return mint_shares(iter(_deposited), opt)


def mint_shares(_it, opt):
    try:
        _value = _it.__next__()
        _id = _lookForDao(_value[0], iter(opt["clusters_DAO"]))
        _a, _b = compute_dynamicsDistrib(opt["tv_DAO"][_id], opt["tv_USD"], opt["clusters_DAO"][_id])
        opt["tv_DAO"][_id] = opt["tv_DAO"][_id] + _a * _value[1] + _b
        return mint_shares(_it, opt)
    except:
        return opt

def _lookForDao(_key, _it, count = 0, _id = 0):
    try:
        _value = _it.__next__()
        _value = _value + count
        return _id if _key - _value < 0 else _lookForDao( _key, _it, count + _value, _id + 1)
    except:
        return False

def compute_miningDistrib(_tv_USD):
    return coeffAffine((0, _tv_USD/100), (_tv_USD*100, 0))

def compute_dynamicsDistrib(_tv_DAO, _tv_USD, cluster_DAO):
    ptx = (0, _tv_DAO/_tv_USD + 1)
    pty = (_tv_USD, _tv_DAO/cluster_DAO)
    return coeffAffine(ptx, pty)

def coeffAffine(_ptx, _pty):
    a = (_pty[1] - _ptx[1])/(_pty[0] - _ptx[0])
    b = _pty[1] - a * _pty[0]
    return a, b





