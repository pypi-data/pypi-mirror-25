import logging.config
import click
import logging
import numbers
import os.path
import cPickle as pickle
import time
import configparser
import sqlite3
import datetime
import json
import commentjson

import workflow
import cube
import hyper_optimizer

logging.basicConfig(level=logging.INFO,
                            format='%(levelname)s: %(asctime)s ::: %(name)s: %(message)s (%(filename)s:%(lineno)d)',
                                                datefmt='%Y-%m-%d %H:%M:%S')

# TODO: save to db: graph_args, main graph, important flag

def setup_logging(tg_chat, tg_token, disable_existing_loggers = True, debug_logging = False):
    if tg_chat is not None:
        tg_chat = int(tg_chat)

    logging_handlers = {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    }

    logging_level = 'DEBUG' if debug_logging else 'INFO'

    if tg_chat is not None:
        logging_handlers['telegram'] = {
            'class': 'telegram_handler.TelegramHandler',
            'token': tg_token,
            'chat_id': tg_chat,
            'level': 'CRITICAL',
            'formatter': 'telegram',
        }

    logging.config.dictConfig({
        'version': 1,
        'handlers': logging_handlers,
        "loggers": {
            "": {
                "level": logging_level,
                "handlers": ['console'] + (['telegram'] if tg_chat is not None else []),
                "propagate": "no"
            }
        },
        'formatters': {
            'console': {
                'format': '%(levelname)s: %(asctime)s ::: %(name)-10s: %(message)s (%(filename)s:%(lineno)d)',
            },
            'telegram': {
                'format': '%(message)s',
            }
        },
        'disable_existing_loggers': disable_existing_loggers,
    })

class Main():
    def __init__(self):

        self.checkpoints_dir = config.get('cuber', 'checkpoints_dir', fallback = './checkpoints/')

        self.setup_db()


    def setup_db(self):
        path = os.path.abspath(self.checkpoints_dir)
        if not os.path.isdir(path):
            os.makedirs(path)

        db_file = os.path.join(self.checkpoints_dir, 'graphs.db')

        logging.info('DB: file: {}'.format(db_file))
        self.db_connect = sqlite3.connect(db_file)
        c = self.db_connect.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS graphs
                             (id INTEGER PRIMARY KEY, date text, file text, graph text, result text, comment text, start_time text, end_time text, status text)''')
        self.db_connect.commit()
        logging.info('DB: prepared')

    def db_register(self):
        c = self.db_connect.cursor()
        c.execute(
        '''
            INSERT INTO graphs (date, file, start_time, status, graph, comment) VALUES (?, ?, ?, ?, ?, ?)
        ''',
            (datetime.datetime.now().date().isoformat(), self.workflow_file, datetime.datetime.now().isoformat(), 'register', self.graph, self.comment)
        )
        self.db_id = c.lastrowid
        logging.info('Graph ID: {}'.format(self.db_id))
        self.db_connect.commit()
        logging.info('DB: registered')

    def db_update_status(self, status):
        c = self.db_connect.cursor()
        c.execute(
        '''
            UPDATE graphs SET status = ? WHERE id = ?
        ''',
            (status, self.db_id)
        )
        self.db_connect.commit()
        logging.info('DB: status updated to {}'.format(status))

    def db_update_comment(self, comment):
        c = self.db_connect.cursor()
        c.execute(
        '''
            UPDATE graphs SET comment = ? WHERE id = ?
        ''',
            (comment, self.db_id)
        )
        self.db_connect.commit()
        logging.info('DB: comment updated')

    def db_save_result(self, result):
        c = self.db_connect.cursor()
        c.execute(
        '''
            UPDATE graphs SET result = ?, end_time = ? WHERE id = ?
        ''',
            (result, datetime.datetime.now().isoformat(), self.db_id)
        )
        self.db_connect.commit()
        logging.info('DB: result saved')

    def db_show(self, filter_done = False):
        c = self.db_connect.cursor()
        res = c.execute(
        '''
            SELECT id, file, start_time, status, comment FROM graphs {}
        '''.format('WHERE status = "done"' if filter_done else ''),
        )
        for row in res:
            print '\t'.join(map(str, row))

    def db_show_detailed(self, db_id):
        c = self.db_connect.cursor()
        res = c.execute(
        '''
            SELECT id, graph, file, start_time, end_time, status, comment, result FROM graphs WHERE id = ?
        ''',
            (db_id, )
        )
        for row in res:
            print '\n'.join(map(str, row))

    def set_status_killed(self, graph_id):
        self.db_id = graph_id
        self.db_update_status('killed')

    def run_graph(self, workflow_file, full_result, comment, main, graph_args, disable_inmemory_cache, disable_file_cache):
        self.workflow_file = workflow_file
        self.comment = comment
        start_time = time.time()

        with open(workflow_file) as f:
            self.graph = f.read()

        self.db_register()

        message_delay = 60 * float(config.get('cuber', 'message_delay', fallback = 3))

        job_descritpion = '{}; {}'.format(workflow_file, self.comment)

        try:
            cube.Cube.checkpoints_dir = self.checkpoints_dir
            logging.info('Checkpoints dir: {}'.format(cube.Cube.checkpoints_dir))
            wf = workflow.Workflow(workflow_file, main = main, graph_args = graph_args)

            self.db_update_status('running')
            data = wf.run(disable_inmemory_cache = disable_inmemory_cache, disable_file_cache = disable_file_cache)

            res = '{}:\n'.format(workflow_file)
            for key, value in data.iteritems():
                if full_result or isinstance(value, str) or isinstance(value, numbers.Number):
                    res += '{}: {}\n'.format(key, value)
                else:
                    res += '{}: ...\n'.format(key)

            if time.time() - start_time >= message_delay:
                logging.critical('Calculation is done: {} (graph id: {})\n{}'.format(job_descritpion, self.db_id, res))
            else:
                logging.info('Calculation is done: {} (graph id: {})\n{}'.format(job_descritpion, self.db_id, res))
            self.db_save_result(res)
            self.db_update_status('done')
        except KeyboardInterrupt:
            if time.time() - start_time >= message_delay:
                logging.critical('Calculation is cancelled: {} (graph id: {})'.format(job_descritpion, self.db_id))
            else:
                logging.error('Calculation is cancelled: {} (graph id: {})'.format(job_descritpion, self.db_id))
            self.db_save_result('candelled')
            self.db_update_status('cancelled')
        except:
            import traceback
            traceback.print_exc()
            if time.time() - start_time >= message_delay:
                logging.critical('Calculation is failed: {} (graph id: {})'.format(job_descritpion, self.db_id))
            else:
                logging.error('Calculation is failed: {} (graph id: {})'.format(job_descritpion, self.db_id))
            self.db_update_status('failed')

config = None

@click.group()
@click.option('--logging', default = False, is_flag=True)
@click.option('--debug', default = False, is_flag=True)
def cli(logging, debug):
    global config
    config_file = '.cuber'
    config = configparser.ConfigParser()
    config.read(config_file)

    setup_logging(
        config.get('telegram', 'chat_id', fallback = None),
        config.get('telegram', 'token', fallback = None),
        disable_existing_loggers = not logging,
        debug_logging = debug,
    )

@cli.command()
def test_telegram():
    """
        Send telegram message with current config params
    """
    logging.critical('This is the test telegram message from cuber')

@cli.command()
@click.argument('workflow_file')
@click.option('--full_result', default = False, is_flag=True)
@click.option('--disable_inmemory_cache', default = False, is_flag=True)
@click.option('--disable_file_cache', default = False, is_flag=True)
@click.option('--comment', default = '')
@click.option('--main', default = 'main', help = 'Name of graph, that will be evaluated.')
@click.option('--graph_args', default = '{}', help = 'Json dict of params, that will be substituted at graph after `$` (`$alpha` and so on).')
def run(workflow_file, full_result, comment, main, graph_args, disable_inmemory_cache, disable_file_cache):
    """
        Runs the workflow file (graph)
    """
    Main().run_graph(workflow_file, full_result, 
        comment = comment, 
        disable_inmemory_cache = disable_inmemory_cache,
        disable_file_cache = disable_file_cache,    
        graph_args = json.loads(graph_args),
        main = main,
    )

@cli.command()
@click.argument('pickle_file')
def print_pickle(pickle_file):
    with open(pickle_file, 'rb') as f:
        data = pickle.load(f)
    print data

@cli.command()
@click.option('--opt_id', default = None)
@click.option('--iters', default = 20)
@click.option('--comment', default = '')
@click.argument('optimize_file', required=False)
def optimize(optimize_file, iters, comment, opt_id):
    """
        Creates a new optimization and starts it. If opt_id is specified, the passed optimization will be continued.
    """
    if opt_id is not None:
        ho = hyper_optimizer.HyperOptimizer(
                optimize_id = opt_id
            )
    else:
        with open(optimize_file) as f:
            optimize_json = f.read()
        optimize = commentjson.loads(optimize_json)

        with open(optimize['graph_file']) as f:
            graph = f.read()
        ho = hyper_optimizer.HyperOptimizer(
                graph = graph,
                optimization_params = optimize['params'],
                comment = comment,
            )
    result = ho.optimize(iters = iters)
    logging.info('optimisation result: {}'.format(result))

@cli.command()
@click.option('--opt_id', default = None, required = True)
@click.option('--point', default = None, required = True, help = 'JSON formatted string {var: value, ...}')
@click.option('--value', default = None, help = 'You may specify value of function at the point. Else the function will be evaluated.')
def optimize_add_point(opt_id, point, value):
    """
        Inserts users specified points to optimizer history. If you know attrs values, that prodice a good result, then this way you may suggest them to optimizer.
    """
    ho = hyper_optimizer.HyperOptimizer(
            optimize_id = opt_id
        )
    ho.add_point(json.loads(point), value)
    logging.info('Done')

@cli.command()
@click.option('--opt_id', default = None)
def optimize_show(opt_id):
    """
        Shows the optimizations or the optimization's result (if opt_id is specified).
    """
    db_connect = sqlite3.connect('optimizer.db')
    if opt_id is None:
        c = db_connect.cursor()
        res = c.execute(
        '''
            SELECT optimize_id, start_time, params, comment FROM optimizers
        ''',
        )
        for row in res:
            print '\t'.join(map(str, row))
    else:
        c = db_connect.cursor()
        res = c.execute(
        '''
            SELECT * FROM steps
            WHERE optimize_id = ?
        ''',
            (opt_id, )
        )
        for row in res:
            print '\t'.join(map(str, row))

@cli.command()
@click.option('--done', default = False, is_flag=True)
def show(done):
    """
        Shows the graphs run history.
    """
    Main().db_show(filter_done = done)

@cli.command()
@click.argument('graph_id')
def detailed(graph_id):
    """
        Shows details of one of history graphs.
    """
    Main().db_show_detailed(graph_id)

@cli.command()
@click.argument('graph_id')
def killed(graph_id):
    """
        Setup status 'killed' for graph. If you kill the process, it will not update status automatically, so it would be marked 'running'. 
    """
    Main().set_status_killed(graph_id)

@cli.command()
@click.argument('graph_id')
@click.option('--comment', required = True)
def update_comment(graph_id, comment):
    """
        Obviously, updates comment. 
    """
    m = Main()
    m.db_id = graph_id
    m.db_update_comment(comment)

if __name__ == '__main__':
    cli()
