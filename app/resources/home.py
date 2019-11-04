# -*- coding: utf-8 -*-
"""首页图标数据"""

from flask_restplus import Namespace, Resource

from app.controllers.home_c import HomeManager

ns = Namespace('home', description='源数据首页图表数据')
homeManager = HomeManager()


@ns.route('/summary')
class HomeSummary(Resource):

    def get(self):
        return homeManager.fetch_homepage_summary()


@ns.route('/tenement')
class HomeTenementInfo(Resource):

    def get(self):
        return homeManager.fetch_tenement_info()


@ns.route('/distribute')
class HomeDistibuteInfo(Resource):

    def get(self):
        return homeManager.fetch_distribute_info()


@ns.route('/aiImage')
class HomeAiImageInfo(Resource):

    def get(self):
        return homeManager.fetch_ai_image_info()


@ns.route('/aiTopic')
class HomeAiTopicInfo(Resource):

    def get(self):
        return homeManager.fetch_ai_topic_info()


@ns.route('/aiTopicCloud')
class HomeAiTopicCloud(Resource):

    def get(self):
        return homeManager.fetch_ai_topic_wordcloud()


@ns.route('/aiTagCloud')
class HomeAiTopicCloud(Resource):

    def get(self):
        return homeManager.fetch_ai_topic_tag_wordcloud()
