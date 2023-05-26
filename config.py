
import logging
from logging.handlers import RotatingFileHandler
 
class Config(object):
    # 设置日志等级
    LOG_LEVEL = logging.DEBUG
 
 
class DevelopConfig(Config):
    """开发环境下的配置"""
    DEBUG = True
 
 
class ProductConfig(Config):
    """生成环境下的配置"""
    DEBUG = False
    LOG_LEVEL = logging.WARNING
 
 
class TestConfig(Config):
    """测试环境下的配置"""
    DEBUG = True
    TESTING = True
 
 
config = {
    "development": DevelopConfig,
    "production": ProductConfig,
    "testing": TestConfig,
}

def setup_log(config_name):
    """
    :param config_name: 传入日志等级
    :return:
    """
    # 设置日志的的等级
    logging.basicConfig(level=config[config_name].LOG_LEVEL)
    # 创建日志记录器，设置日志的保存路径和每个日志的大小和日志的总大小
    file_log_handler = RotatingFileHandler("static/mlog/log.log", maxBytes=1024 * 1024 * 100, backupCount=100)
    # 创建日志记录格式，日志等级，输出日志的文件名 行数 日志信息
    formatter = logging.Formatter("%(levelname)s %(filename)s: %(lineno)d %(message)s")
    # 为日志记录器设置记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flaks app使用的）加载日志记录器
    logging.getLogger().addHandler(file_log_handler)