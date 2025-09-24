#!/usr/bin/env python3
"""
数据库初始化脚本
用于单独测试和初始化数据库连接
"""

from re import S
import sys
import os
import logging
from pathlib import Path

from dotenv import load_dotenv
import pymysql
from sqlalchemy import create_engine, text

from quant.utils.logger import base_logger, SUCCESS

logger = base_logger.getChild("Database")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = PROJECT_ROOT / ".env"


def test_mysql_connection():
    """测试MySQL基础连接"""
    load_dotenv(ENV_FILE)

    try:
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
        )
        logger.log(SUCCESS, "MySQL基础连接成功")
        connection.close()
        return True
    except Exception as e:
        logger.error(f"MySQL基础连接失败: {e}")
        return False


def create_database_manually():
    """手动创建数据库"""
    load_dotenv(ENV_FILE)

    database_name = os.getenv("MYSQL_DATABASE", "Stock")

    try:
        # 连接到MySQL服务器（不指定数据库）
        connection = pymysql.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            port=int(os.getenv("MYSQL_PORT", 3306)),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
        )

        cursor = connection.cursor()

        # 检查数据库是否存在
        cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
        result = cursor.fetchone()

        if result is None:
            logger.info(f"创建数据库: {database_name}")
            cursor.execute(
                f"CREATE DATABASE `{database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
            logger.log(SUCCESS, "数据库创建成功")
        else:
            logger.log(SUCCESS, f"数据库 {database_name} 已存在")

        cursor.close()
        connection.close()
        return True

    except Exception as e:
        logger.error(f"创建数据库失败: {e}")
        return False


def test_sqlalchemy_connection():
    """测试SQLAlchemy连接"""
    try:
        from quant.utils.config import db_config

        # 测试连接到数据库
        engine = create_engine(db_config.get_connection_url(), echo=False)

        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.log(SUCCESS, "SQLAlchemy连接成功")

        engine.dispose()
        return True

    except Exception as e:
        logger.error(f"SQLAlchemy连接失败: {e}")
        return False


def initialize_database():
    """完整的数据库初始化"""
    try:
        from quant.utils.db import db_manager

        if db_manager is None:
            logger.error("数据库管理器初始化失败")
            return False

        if db_manager.test_connection():
            logger.log(SUCCESS, "数据库初始化成功")
            return True
        else:
            logger.error("数据库连接测试失败")
            return False

    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        return False


def main():
    """主函数"""
    logger.info("开始数据库初始化检查...")

    # 步骤1: 检查.env文件
    if not os.path.exists(".env"):
        logger.error("未找到.env配置文件")
        return False

    logger.log(SUCCESS, "找到.env配置文件")

    # 步骤2: 测试MySQL基础连接
    if not test_mysql_connection():
        logger.error("请检查MySQL服务是否运行以及配置是否正确")
        return False

    # 步骤3: 手动创建数据库
    if not create_database_manually():
        logger.error("数据库创建失败")
        return False

    # 步骤4: 测试SQLAlchemy连接
    if not test_sqlalchemy_connection():
        logger.error("SQLAlchemy连接失败")
        return False

    # 步骤5: 初始化数据库管理器
    if not initialize_database():
        logger.error("数据库管理器初始化失败")
        return False

    logger.info("🎉 数据库初始化完成！")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
