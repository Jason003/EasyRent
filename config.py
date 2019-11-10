import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "postgresql://jl5501:root@34.74.165.156/proj1part2"
    SQLALCHEMY_TRACK_MODIFICATIONS = False