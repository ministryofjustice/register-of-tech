# -*- coding: utf-8 -*-
from extended_choices import Choices


"""
Attempt at restricting relationships via code through a ManyToMany field
"""
RELATIONSHIPS = Choices(
    ('ONE_TO_ONE',  1, 'One to one'),
    ('ONE_TO_MANY',  2, 'One to many'),
    ('MANY_TO_ONE',  3, 'Many to one'),
    ('MANY_TO_MANY',  4, 'Many to Many'),
)
