import unittest
import json
import os.path
import sys
import sdu_bkjws
import glob
import os

testDir = os.path.split(os.path.realpath(__file__))[0]


class TestStringMethods(unittest.TestCase):
    def setUp(self):
        if glob.glob(testDir + '/keys.json'):
            with open(testDir + '/keys.json', 'r', encoding='utf-8') as f:
                obj = json.load(f)
            student_id = obj['student_id']
            password = obj['password']
        else:
            student_id = os.environ['student_id']
            password = os.environ['password']
        self.sdu = sdu_bkjws.SduBkjws(student_id, password)

    def test_login(self):
        self.sdu.login()

    def test_detail(self):
        self.sdu.get_detail()
        self.assertIsInstance(self.sdu.detail, dict)

    def test_update_contact_info(self):
        self.sdu.update_contact_info()

    def test_lesson(self):
        lesson = self.sdu.lessons
        self.assertIsInstance(self.sdu.lessons, list)
        for key in ["lesson_num_long", "lesson_name", "lesson_num_short",
                    "credit", "school", "teacher", "weeks",
                    "days", "times", "place"]:
            for obj in lesson:
                self.assertIn(key, obj.keys())

    def test_past_score(self):
        raw = self.sdu.get_raw_past_score()
        past_score = self.sdu.get_past_score()
        for key in ['kch', 'kcm', 'kxh', 'xh', 'kssj', 'jsh', 'xnxq', 'xf', 'xs', 'kcsx', 'kscj']:
            for obj in past_score:
                self.assertIn(key, obj.keys())
        self.assertIsInstance(raw, dict)
        self.assertIsInstance(past_score, list)
        self.assertEqual(raw['object']['aaData'], past_score)

    def test_now_score(self):
        self.sdu.get_raw_now_score()
        self.sdu.get_now_score()

    def test_get_rank_with_query(self):
        score = self.sdu.get_now_score()
        if score:
            dic = {
                'lesson_num_long': score[0]['kch'],
                'lesson_num_short': score[0]['kxh'],
                'exam_time': score[0]['kssj']
            }
            search_list = [dic, dic]
            rank = self.sdu.get_rank_with_query(**dic)
            rank_list = self.sdu.get_multi_rank_with_query(search_list)
            self.assertIsInstance(rank, dict)
            self.assertIsInstance(rank_list, list)
            for key in ["lesson_num_long", "lesson_name", "lesson_num_short", "credit",
                        "rank", "score", "exam_time", "max_score", "min_score"]:
                self.assertIn(key, rank.keys())
                for obj in rank_list:
                    self.assertIn(key, obj.keys())

    def tearDown(self):
        self.sdu.session.close()


if __name__ == '__main__':
    unittest.main()
