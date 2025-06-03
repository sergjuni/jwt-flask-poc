import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'você-precisa-mudar-isso'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'mude-esta-chave-jwt-tambem'
