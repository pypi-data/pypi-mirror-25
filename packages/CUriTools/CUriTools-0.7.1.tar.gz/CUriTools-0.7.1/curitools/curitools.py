#!/usr/local/bin/python3.5
import os
import time
import codecs
import sys
import re
import click
from curitools.settings import Settings, MissingFileSettings
from curitools.setup_problems import SetupProblem
import curitools.requestpages.pages as rp
from requests.exceptions import HTTPError
import logging
import tempfile

@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-s', default=0, help='Submeter um problema')
@click.option('-d', is_flag=True, help='Debug output')
def uri(ctx, s, d):
    """Simple program to use with URI"""
    fp = None
    log_file_name = None
    if(d): 
        log_file = os.path.join(os.getcwd(), "curitools.log")
        logging.basicConfig(filename=log_file, format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.debug("The value of s: %s, d: %s", str(s), str(d))
        log_file_name = log_file
    else:
        fp = tempfile.NamedTemporaryFile()
        logging.basicConfig(filename=fp.name, format='%(levelname)s:%(message)s', level=logging.WARNING)
        log_file_name = fp.name


    settings = Settings() 
    try:
        user, password = settings.get_settings()
    except MissingFileSettings:
        logging.debug("Settings' file was not found")
        sys.exit()
    except:
        print("Some error has occured. Please check the file: %s" % log_file_name)

    ctx.obj = {}
    ctx.obj['settings'] = settings
    ctx.obj['log_file_name'] = log_file_name

    
    if s:
       logging.debug("S option was executed")
       session = get_session_login(user, password, log_file_name)
       sub = rp.SubmissionPage(session, s, language=settings.get_language())
       sub.run() 
   
    if(fp):
        fp.close()
    return 1 

@uri.command()
@click.pass_context
@click.option('-r', is_flag=True, help='Imprimir tabela de submissoes')
@click.option('-a', is_flag=True, help='Imprimir tabela de submissoes')
def view(ctx, r, a):
    """View some informations from URI"""
    
    user, password = ctx.obj["settings"].get_settings()
    session = get_session_login(user, password, ctx.obj["log_file_name"])
    if r:
       logging.debug("R option was executed")
       sub = rp.TabelaSubmissionPage(session)
       sub.run()
    if a:
       logging.debug("A option was executed")
       sub = rp.AcademicPage(session)
       sub.run()

@uri.command()
@click.option('-n', default=-1, help='Criar diretorio para submter um problema')
@click.pass_context
def c(ctx, n):
    """Create files and directories to start solving a problem"""
    logging.debug("C option was executed")
    if n > 0:
        cwd = os.getcwd()
        language = ctx.obj['settings'].get_language()
        template_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates")
        setup = SetupProblem(str(n), cwd, template_dir, language)
        setup.create_files()


def get_session_login(user, password, log_file_name):
    try:
        login = rp.LoginPage(user=user, password=password)
        login.run()
    except HTTPError:
        logging.debug("HTTP error")
        print("Some error has occured. Please check the file: %s" % log_file_name)
        return 0

    return login.get_session()


if __name__ == "__main__":
    uri(obj={})
