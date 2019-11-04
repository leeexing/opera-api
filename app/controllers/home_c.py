# -*- coding: utf-8 -*-
"""首页图标数据"""

from collections import Counter

import jieba
from flask_restplus import marshal

from app.models.tenement import Tenement
from app.public.base import BaseHandler
from app.public.fields import tenement_field
from app.public.enumtype import TenementIndustry
from app.util.connector import get_mongo_imagedata_connection

conn = get_mongo_imagedata_connection()
mongodb = conn.mainDatabase
cloud_wihte_list = []

class HomeManager(BaseHandler):

    def fetch_homepage_summary(self):
        """获取首页信息概要"""
        try:
            data = {}
            data['tenement'] = Tenement.query.count()
            data['ctImage'] = mongodb.Image.find({'ct': {'$exists': True}}).count()
            data['drImage'] = mongodb.Image.find({'dr.1' : {'$exists': 0}}).count()
            data['video'] = mongodb.Video.find().count()
            data['document'] = mongodb.Document.find().count()
            data['picture'] = mongodb.Picture.find().count()
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    def fetch_tenement_info(self):
        """获取租户信息"""
        try:
            data = []
            tenements = Tenement.query.all()
            tenements = marshal(tenements, tenement_field)
            for name, member in TenementIndustry.__members__.items():
                obj = {}
                obj['name'] = member.value
                obj['value'] = len(list(filter(lambda x: x['Industry'] == name.lower(), tenements)))
                data.append(obj)
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    def fetch_distribute_info(self):
        """待开发完善todo"""
        return self.Response.return_true_data()

    def fetch_ai_image_info(self):
        """获取AI智能推送<图库>概况"""
        try:
            images_total_count = self.mongo.brushing_image.find().count()
            images_used_count = self.mongo.brushing_image.find({'usages': {'$ne': 0}}).count()
            images_usage_total = list(self.mongo.brushing_image.aggregate([
                {'$group': {'_id': None, 'count': {'$sum': '$usages'}}}
            ]))[0]['count']
            echart_data = [
                {
                    'name': '未使用',
                    'value': images_total_count - images_used_count
                },
                {
                    'name': '已使用',
                    'value': images_used_count
                }
            ]
            data = {
                'echartData': echart_data,
                'imageUsageCount': images_usage_total
            }
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    def fetch_ai_topic_info(self):
        """获取AI智能推送<考题>概况"""
        try:
            topics_single_count = self.mongo.brushing_topic.find({'type': 1}).count()
            topics_multiple_count = self.mongo.brushing_topic.find({'type': 2}).count()
            topics_judge_count = self.mongo.brushing_topic.find({'type': 3}).count()
            data = [
                {
                    'name': '考题总量',
                    'value': sum([topics_single_count, topics_multiple_count, topics_judge_count])
                },
                {
                    'name': '单选题',
                    'value': topics_single_count
                },
                {
                    'name': '多选题',
                    'value': topics_multiple_count
                },
                {
                    'name': '判断题',
                    'value': topics_judge_count
                }
            ]
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    def fetch_ai_topic_wordcloud(self):
        """获取AI智能推送考题<题干>中的<词云>"""
        try:
            topic_text_list = list(self.mongo.brushing_topic.aggregate([
                {'$group': {'_id': None, 'text': {'$push': '$title'}}}
            ]))[0]['text']
            topic_text = ','.join(topic_text_list)
            topic_text_jieba = jieba.lcut(topic_text)
            topic_text_filter = filter(lambda x: len(x) >= 2 and x not in cloud_wihte_list, topic_text_jieba)
            topic_text_top20 = Counter(topic_text_filter).most_common(20)
            topic_text_top20_echart = list(map(lambda item: {'name': item[0], 'value': item[1]}, topic_text_top20))
            data = topic_text_top20_echart
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()

    def fetch_ai_topic_tag_wordcloud(self):
        """获取AI智能推送考题<知识点>中的<词云>"""
        try:
            tag_list = list(self.mongo.brushing_image.aggregate([
                {'$unwind': '$tags'},
                {'$group': {'_id': None, 'tags': {'$push': '$tags'}}}
            ]))[0]['tags']
            tag_text_list = list(map(lambda item: item['tag'], tag_list))
            tag_text_top20 = Counter(tag_text_list).most_common(20)
            tag_top20_echart = list(map(lambda item: {'name': item[0], 'value': item[1]}, tag_text_top20))
            data = tag_top20_echart
            return self.Response.return_true_data(data)
        except Exception as e:
            self.logger.error('Server Error: %s', str(e))
            return self.Response.return_server_error()