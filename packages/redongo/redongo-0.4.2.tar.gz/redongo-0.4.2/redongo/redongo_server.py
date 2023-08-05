import datetime
import logging
import logging.handlers
import os
import pymongo
import pytz
import redis
from redis.sentinel import Sentinel
from redis.exceptions import RedisError
import server_exceptions
import general_exceptions
import signal
import stoneredis
import sys
import time
import traceback
import utils
import redongo_client
import cipher_utils
import serializer_utils
import queue_utils
from optparse import OptionParser
from pymongo.errors import PyMongoError
from twisted.internet import reactor
from twisted.internet.error import ReactorNotRunning
from twisted.internet.task import LoopingCall
from pymongo.errors import BulkWriteError

try:
    from bson.objectid import ObjectId
    from bson.errors import InvalidId
    from bson.errors import InvalidDocument
except ImportError:
    from pymongo.objectid import ObjectId, InvalidId, InvalidDocument

try:
    import cPickle as pickle
except:
    import pickle

# LOGGER CONFIG
FACILITY = "local0"
logging.basicConfig()
logger = logging.getLogger()

formatter = logging.Formatter('PID:%(process)s %(filename)s %(funcName)s %(levelname)s %(message)s')

rs = None
options = None
args = None
run_stopped = False


class RedongoServer(object):
    def __init__(self, mode, *args, **kwargs):
        def __get_sk__():
            result = self.redis.get('redongo_sk')
            if not result:
                result = os.urandom(16)
                self.redis.set('redongo_sk', result)
            return result
        logger.info('Starting Redongo Server..')
        self.mode = mode
        self.create_redis_connection()
        self.keep_going = True
        self.redisQueue = options.redisQueue
        self.popSize = int(options.popSize)
        self.redisQueueSize = int(options.redisQueueSize)
        self.bulks = {}
        self.completed_bulks = set()
        self.objs = []
        self.cipher = cipher_utils.AESCipher(__get_sk__())
        disk_queue_load_time = time.time()
        logger.info('Loading disk queues...')
        self.disk_queue = queue_utils.Queue(queue_name=options.diskQueue)
        logger.info('Loading disk queue took {0}'.format(time.time() - disk_queue_load_time))
        ret_disk_queue_load_time = time.time()
        self.returned_disk_queue = queue_utils.Queue(queue_name='{0}_returned'.format(options.diskQueue))
        logger.info('Loading returned disk queue took {0}'.format(time.time() - ret_disk_queue_load_time))
        self.lock_key = '{0}_LOCK'.format(self.redisQueue)
        self.transaction_key = '{0}_TRANSACTION'.format(self.redisQueue)
        self.max_expiration_time = 60*60*24*30
        self.check_expired_transactions_gap = 300
        self.last_expiration_check = None
        self.redongo_client = redongo_client.RedongoSentinelClient(self.redis, self.redisQueue)
        self.last_empty_retrieval = None

    def create_redis_connection(self):
        if self.mode == 'Redis':
            self.redis = stoneredis.StoneRedis(options.redisIP, db=options.redisDB, port=options.redisPort, socket_connect_timeout=5, socket_timeout=5)
            self.redis.connect()
        else:
            SENTINEL_POOL = Sentinel(
                options.sentinelServers,
                socket_timeout=0.1,
                max_connections=1000,
            )

            self.redis = SENTINEL_POOL.master_for(
                options.sentinelName,
                redis_class=stoneredis.StoneRedis,
                socket_timeout=5,
                socket_connect_timeout=5,
            )

    def check_object(self, obj):
        if type(obj) != list or len(obj) != 2:
            raise server_exceptions.ObjectValidationError('Type not valid')

    def get_application_settings(self, application_name):
        return utils.get_application_settings(application_name, self.redis)

    def save_to_failed_queue(self, application_name, bulk):
        i = 0
        for obj, command, original_object in bulk['data']:
            self.redis.rpush('{0}_FAILED'.format(self.redisQueue), original_object)
            i += 1
        logger.warning('Moved {0} objects from application {1} to queue {2}_FAILED'.format(i, application_name, self.redisQueue))

    def check_expired_transactions(self):
        # Check if queue is up to date
        if self.last_empty_retrieval and self.last_empty_retrieval >= pytz.utc.localize(datetime.datetime.utcnow()) - datetime.timedelta(seconds=600):
            # Check if gap has passed since last check
            if not self.last_expiration_check or (pytz.utc.localize(datetime.datetime.utcnow()) - self.last_expiration_check).total_seconds() > self.check_expired_transactions_gap:
                queue_name = '{0}|*'.format(self.transaction_key)
                keys = self.redis.keys(queue_name)
                pipe = self.redis.pipeline()
                for k in keys:
                    pipe.ttl(k)
                settings_per_application = {}
                result = pipe.execute()
                ids_to_end = {}
                for key, time_result in zip(keys, result):
                    exp_key, application_name, obj_id = key.split('|')
                    if application_name not in settings_per_application:
                        settings_per_application[application_name] = self.get_application_settings(application_name)
                    if time_result <= self.max_expiration_time - settings_per_application[application_name]['transaction_expiration']:
                        ids_to_end.setdefault(application_name, set()).add(obj_id)
                for application_name, ids in ids_to_end.iteritems():
                    self.redongo_client.end_transaction(application_name, map(lambda x: {'_id': x}, ids))
                self.last_expiration_check = pytz.utc.localize(datetime.datetime.utcnow())

    def run(self):
        global run_stopped
        first_run = True
        try:
            logger.info('Running!')

            while self.keep_going:
                object_found = False

                lock = self.redis.wait_for_lock(self.lock_key, 60, auto_renewal=True)

                if first_run:
                    while self.returned_disk_queue._length > 0:
                        self.objs.append(self.returned_disk_queue.pop())
                        object_found = True
                    first_run = False
                    if object_found:
                        logger.info('Got {0} objects from returned disk queue {1}'.format(len(self.objs), self.returned_disk_queue._disk_queue_name))

                if self.disk_queue._length > 0:
                    for i in range(0, self.popSize):
                        if self.disk_queue._length:
                            self.objs.append(self.disk_queue.pop())
                            object_found = True
                        else:
                            break
                    logger.debug('Got {0} objects from disk queue {1}'.format(len(self.objs), self.disk_queue._disk_queue_name))
                else:
                    try:
                        self.objs.append(self.redis.blpop(self.redisQueue)[1])
                        object_found = True
                    except redis.TimeoutError:
                        pass
                    if object_found:
                        self.objs.extend(self.redis.multi_lpop(self.redisQueue, self.popSize-1))
                    logger.debug('Got {0} objects from redis queue {1}'.format(len(self.objs), self.redisQueue))

                if lock:
                    self.redis.release_lock(lock)

                if object_found:
                    while self.objs:
                        try:
                            orig_obj = self.objs.pop(0)
                            obj = pickle.loads(orig_obj)
                            try:
                                self.check_object(obj)
                                application_settings = self.get_application_settings(obj[0][0])
                            except (server_exceptions.ObjectValidationError, general_exceptions.ApplicationSettingsError), e:
                                logger.error('Discarding {0} object because of {1}'.format(obj[0], e))
                                continue
                            application_bulk = self.bulks.setdefault(obj[0][0], {'serializer': obj[0][1], 'data': []})
                            application_bulk.setdefault('inserted_date', datetime.datetime.utcnow())
                            application_bulk.update(application_settings)
                            ser = serializer_utils.serializer(obj[0][1])
                            obj_data = ser.loads(obj[1])
                            application_bulk['data'].append((self.normalize_object(obj_data), obj[0][2], orig_obj))
                        except (ValueError, TypeError, IndexError, ImportError, pickle.PickleError), e:
                            logger.error('Discarding {0} object because of {1}'.format(orig_obj, e))
                            continue
                else:
                    self.last_empty_retrieval = pytz.utc.localize(datetime.datetime.utcnow())

                while self.completed_bulks:
                    self.consume_application(self.completed_bulks.pop())

                self.check_expired_transactions()

            logger.info('Setting run_stopped to True')
            run_stopped = True

        except:
            logger.error('Stopping redongo because unexpected exception: {0}'.format(traceback.format_exc()))
            logger.info('Setting run_stopped to True')
            run_stopped = True
            stopApp()

    def back_to_disk(self):
        logger.info('Returning memory data to Disk Queue')
        objects_returned = 0
        for application_name, bulk in self.bulks.iteritems():
            for obj, command, original_object in bulk['data']:
                self.returned_disk_queue.push(original_object)
                objects_returned += 1
        logger.info('{0} objects returned to Disk Queue'.format(objects_returned))

    def get_mongo_collection(self, bulk):
        mongo_client = pymongo.MongoClient('mongodb://{0}:{1}@{2}:{3}/{4}'.format(bulk['mongo_user'], self.cipher.decrypt(bulk['mongo_password']), bulk['mongo_host'], bulk['mongo_port'], bulk['mongo_database']))
        mongo_db = mongo_client[bulk['mongo_database']]
        collection = mongo_db[bulk['mongo_collection']]
        return collection

    def normalize_object(self, obj):
        objectid_fields = obj.pop('objectid_fields', [])
        for f in objectid_fields:
            if obj.get(f, None):
                try:
                    obj[f] = ObjectId(obj[f])
                except InvalidId:
                    pass
                except TypeError:
                    pass

        return obj

    def handle_application_bulk(self, application_name):
        bulk = self.bulks[application_name]
        to_failed = []
        try:
            collection = self.get_mongo_collection(bulk)
        except (PyMongoError, InvalidDocument), e:
            logger.error('Not saving bulk {0} (moving to failed queue) from application {1} due to connection bad data: {2}'.format(bulk, application_name, e))
            self.save_to_failed_queue(application_name, bulk)
            return

        bulks_to_do = []
        while bulk['data']:
            obj, command, original_object = bulk['data'].pop(0)
            if not len(bulks_to_do) or bulks_to_do[-1][0][1] != command:
                bulks_to_do.append([])
            bulks_to_do[-1].append((obj, command, original_object))

        for bulk_to_do in bulks_to_do:
            failed = None
            current_command = bulk_to_do[0][1]
            # Execute command for all readed objects
            if current_command == 'save':
                failed = self.save_to_mongo(collection, bulk_to_do)
            elif current_command == 'add':
                failed = self.add_in_mongo(collection, bulk_to_do)
            elif current_command == 'end_transaction':
                failed = self.end_transaction(application_name, collection, bulk_to_do)
            elif current_command == 'add_to_transaction':
                failed = self.add_to_transaction(application_name, bulk_to_do)
            # Notify on failure
            if failed:
                to_failed += failed

        # If an error occurred, it notifies and inserts the required objects
        if to_failed:
            bulk['data'] = to_failed
            self.save_to_failed_queue(application_name, bulk)

    def add_to_transaction(self, application_name, objs):
        to_failed = []
        ids_to_save = {}
        for full_object in objs:
            obj = full_object[0]
            l = ids_to_save.setdefault(obj['_id'], [])
            l.append(pickle.dumps(full_object))
        for obj_id, l in ids_to_save.iteritems():
            queue_name = '{0}|{1}|{2}'.format(self.transaction_key, application_name, obj_id)
            try:
                self.redis.rpush(queue_name, *l)
                self.redis.expire(queue_name, self.max_expiration_time)
            except RedisError:
                logger.error('Fail adding in transaction {0}'.format(traceback.format_exc()))
                to_failed.append(full_object)
        # Return unadded objects and info
        return to_failed

    def end_transaction(self, application_name, collection, objs):
        to_failed = []
        final_objs = []
        for full_object in objs:
            try:
                obj = full_object[0]
                queue_name = '{0}|{1}|{2}'.format(self.transaction_key, application_name, obj['_id'])
                data = self.redis.lrange(queue_name, 0, self.redis.llen(queue_name))
                if data:
                    final_obj = {'_id': obj['_id']}
                    for obj_redis in data:
                        full_object_redis = pickle.loads(obj_redis)
                        self.combine_objects(final_obj, full_object_redis[0])
                    final_objs.append([final_obj, full_object_redis[1], full_object_redis[2]])
                self.redis.delete(queue_name)
            except RedisError:
                logger.error('Fail ending transaction {0}'.format(traceback.format_exc()))
                to_failed.append(full_object)

        if final_objs:
            self.save_to_mongo(collection, final_objs)
        return to_failed

    def combine_objects(self, final_object, new_object):
        for field, value in new_object.iteritems():
            if field == '_id':
                continue
            type_field = type(value)
            # Numeric and logical fields perform an addition (Complex number are not supported by mongo)
            if type_field is int or type_field is long or type_field is float:
                if field not in final_object:
                    final_object[field] = 0
                final_object[field] += value
            # List fields perform a concatenation
            elif type_field is list:
                if field not in final_object:
                    final_object[field] = []
                final_object[field].extend(value)
            # Dict fields will be treated as the original object
            elif type_field is dict:
                if field not in final_object:
                    final_object[field] = {}
                self.combine_objects(final_object[field], value)
            else:
                final_object[field] = value

    def save_to_mongo(self, collection, objs):
        to_insert = []
        to_update = []
        to_failed = []
        differents = set()
        while objs:
            full_object = objs.pop(0)
            if '_id' not in full_object[0]:
                to_insert.append(full_object)
            elif full_object[0]['_id'] not in differents:
                to_insert.append(full_object)
                differents.add(full_object[0]['_id'])
            else:
                to_update.append(full_object)

        # Bulk insert
        try:
            collection.insert_many(map(lambda x: x[0], to_insert))
        except BulkWriteError as bwe:
            to_update = to_insert[bwe.details['writeErrors'][0]['index']:] + to_update
        except (PyMongoError, InvalidDocument):
            logger.error('Fail saving to mongo {0}'.format(traceback.format_exc()))
            to_update = to_insert + to_update

        time.sleep(10)

        # One-to-one update
        while to_update:
            full_obj = to_update.pop(0)
            try:
                collection.update({'_id': full_obj[0]['_id']}, full_obj[0], upsert=True)
            except (PyMongoError, InvalidDocument):
                logger.error('Fail saving to mongo {0}'.format(traceback.format_exc()))
                to_failed.append(full_obj)

        # Return unsaved objects
        return to_failed

    def create_add_query(self, obj, previous_field='', query=None):
        if query is None:
            query = {}
        for field, value in obj.iteritems():
            if field == '_id':
                continue
            type_field = type(value)
            # Numeric and logical fields perform an addition (Complex number are not supported by mongo)
            if type_field is int or type_field is long or type_field is float or type_field is bool:  # type_field is complex:
                x = query.setdefault('$inc', {})
                x[previous_field + field] = value
            # String fields perform a set
            elif type_field is str:
                x = query.setdefault('$set', {})
                x[previous_field + field] = value
            # List fields perform a concatenation
            elif type_field is list:
                x = query.setdefault('$push', {})
                x[previous_field + field] = {'$each': value}
            # Dict fields will be treated as the original object
            elif type_field is dict:
                query = self.create_add_query(value, '{0}{1}.'.format(previous_field, field), query)
            else:
                query.setdefault('$set', {(previous_field + field): value})
        return query

    def add_in_mongo(self, collection, objs):
        to_failed = []
        # One-to-one update
        while objs:
            full_object = objs.pop(0)
            obj = full_object[0]
            try:
                collection.update({'_id': obj['_id']}, self.create_add_query(obj), upsert=True)
            except (PyMongoError, InvalidDocument):
                logger.error('Fail adding in mongo {0}'.format(traceback.format_exc()))
                to_failed.append(full_object)
        # Return unadded objects and info
        return to_failed

    def consume_application(self, application_name):
        # In case that check_completed_bulks reads while main thread was saving on previous iteration
        if application_name in self.bulks:
            self.handle_application_bulk(application_name)
            self.bulks.pop(application_name)

    def check_completed_bulks(self):
        try:
            for application_name, bulk in self.bulks.items():
                if len(bulk['data']) >= bulk['bulk_size'] or bulk['inserted_date'] + datetime.timedelta(seconds=bulk['bulk_expiration']) <= datetime.datetime.utcnow():
                    self.completed_bulks.add(application_name)
        except:
            stopApp()

    def check_redis_queue(self):
        try:
            if self.redis.llen(self.redisQueue) > self.redisQueueSize or self.disk_queue._length > 0:
                to_disk_queue = []
                object_found = False
                lock = self.redis.wait_for_lock(self.lock_key, 60, auto_renewal=True)
                while self.redis.llen(self.redisQueue) > self.redisQueueSize:
                    try:
                        to_disk_queue.append(self.redis.blpop(self.redisQueue)[1])
                        object_found = True
                    except redis.TimeoutError:
                        pass
                    if object_found:
                        to_disk_queue.extend(self.redis.multi_lpop(self.redisQueue, self.popSize-1))
                    self.save_to_disk_queue(to_disk_queue)
                self.redis.release_lock(lock)
        except redis.TimeoutError:
            pass

    def save_to_disk_queue(self, objs):
        while objs:
            obj = objs.pop(0)
            self.disk_queue.push(obj)

    def close_disk_queues(self):
        try:
            self.disk_queue.close()
        except:
            logger.error('Could not close disk queue {0}: {1}'.format(self.disk_queue._disk_queue_name, traceback.format_exc()))
        try:
            self.returned_disk_queue.close()
        except:
            logger.error('Could not close disk queue {0}: {1}'.format(self.returned_disk_queue._disk_queue_name, traceback.format_exc()))


def sigtermHandler():
    global rs
    global run_stopped
    rs.keep_going = False

    logger.info('Waiting for run_stopped')
    while not run_stopped:
        time.sleep(0.1)
    rs.back_to_disk()
    rs.close_disk_queues()
    logger.info('Exiting program!')


def stopApp():
    global run_stopped

    logger.info('Stopping app')
    try:
        reactor.stop()
    except ReactorNotRunning:
        run_stopped = True


def closeApp(signum, frame):
    logger.info('Received signal {0}'.format(signum))
    stopApp()


def validate(parser, options, required_options, silent=True):
    for required_option in filter(lambda x: x.__dict__['metavar'] in required_options, parser.option_list):
        if not getattr(options, required_option.dest):
            if not silent:
                logger.error('Option {0} not found'.format(required_option.metavar))
            return False
    return True


def validateRedisClient(parser, options):
    required_options = ['REDIS', 'REDIS_DB']
    return validate(parser, options, required_options, silent=False)


def validateSentinelClient(parser, options):
    required_options = ['SENTINEL_SERVERS', 'SENTINEL_NAME']
    return validate(parser, options, required_options, silent=False)


def validateArgs(parser, options):

    if validateRedisClient(parser, options):
        mode = 'Redis'
    elif validateSentinelClient(parser, options):
        mode = 'Sentinel'
    else:
        logger.error('Parameters for Redis connection not valid!\n\tUse -r HOST -d DB for Standard Redis mode\n\tUse -n GROUP NAME -S host1 port1 -S host2 port2 .. -S hostN:portN for Sentinel mode')
        sys.exit(-1)

    required_options = ['REDIS_QUEUE']

    if not validate(parser, options, required_options, silent=False):
        sys.exit(-1)

    return mode


def main():
    global rs
    global options
    global args
    global logger

    parser = OptionParser(description='Startup options')
    parser.add_option('--redis', '-r', dest='redisIP', help='Redis server IP Address', metavar='REDIS')
    parser.add_option('--redisdb', '-d', dest='redisDB', help='Redis server DB', metavar='REDIS_DB')
    parser.add_option('--redisqueue', '-q', dest='redisQueue', help='Redis Queue', metavar='REDIS_QUEUE')
    parser.add_option('--popsize', '-p', dest='popSize', help='Redis Pop Size', metavar='REDIS_POP_SIZE', default=1000)
    parser.add_option('--port', '-P', dest='redisPort', help='Redis Port', metavar='REDIS_PORT', default=6379)
    parser.add_option('--sentinelservers', '-S', dest='sentinelServers', help='Sentinel Servers (-S host1 port1 -S host2 port2 .. -S hostN portN)', metavar='SENTINEL_SERVERS', action='append', nargs=2)
    parser.add_option('--sentinelname', '-n', dest='sentinelName', help='Sentinel Group Name', metavar='SENTINEL_NAME')
    parser.add_option('--queuesize', '-s', dest='redisQueueSize', help='Max Redis Queue Size', metavar='REDIS_QUEUE_SIZE', default=10000)
    parser.add_option('--diskqueue', '-Q', dest='diskQueue', help='Disk Queue', metavar='DISK_QUEUE', default='redongo_disk_queue')
    parser.add_option('--logger', '-L', dest='logger', help='Logger Usage', metavar='LOGGER_USAGE', default='1')
    parser.add_option('--log', '-l', dest='logLevel', help='Logger Level', metavar='LOG_LEVEL', default='debug')
    (options, args) = parser.parse_args()

    logger.setLevel(getattr(logging, options.logLevel.upper(), 'DEBUG'))

    mode = validateArgs(parser, options)

    # With this line the logs are sent to syslog.
    if options.logger != '0':
        handler = logging.handlers.SysLogHandler("/dev/log", FACILITY)
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    signal.signal(signal.SIGHUP, closeApp)
    signal.signal(signal.SIGTERM, closeApp)
    signal.signal(signal.SIGINT, closeApp)
    signal.signal(signal.SIGALRM, closeApp)

    # Handler for SIGTERM
    reactor.addSystemEventTrigger('before', 'shutdown', sigtermHandler)

    rs = RedongoServer(mode)

    lc = LoopingCall(rs.check_completed_bulks)
    lc.start(1, now=False)

    lc_redis_queue = LoopingCall(rs.check_redis_queue)
    lc_redis_queue.start(5, now=False)

    reactor.callInThread(rs.run)

    # Start the reactor
    reactor.run(installSignalHandlers=False)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(25)
