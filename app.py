from flask import Flask, jsonify, request, Response, json, send_from_directory
import os, random
from datetime import datetime

app = Flask(__name__)

# 애플리케이션의 루트 디렉토리 기반으로 절대 경로 생성
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 'school_link.json' 파일에서 데이터 불러오기
school_link_path = os.path.join(BASE_DIR, 'data', 'school_link.json')
with open(school_link_path, 'r', encoding='utf-8') as file:
    school_data = json.load(file)

# 'outschool_gara.json' 파일에서 데이터 불러오기
outschool_gara_path = os.path.join(BASE_DIR, 'data', 'outschool_gara.json')
with open(outschool_gara_path, 'r', encoding='utf-8') as file:
    outschool_data = json.load(file)

@app.route('/<int:no>/logo', methods=['GET'])
def get_school_logo(no):
    logo_path = os.path.join(BASE_DIR, 'data', 'school_logo', f'{no}.svg')
    if os.path.exists(logo_path):
        return send_from_directory(os.path.join(BASE_DIR, 'data', 'school_logo'), f'{no}.svg')
    else:
        return "Logo not found for the provided number", 404

@app.route('/<int:no>/system', methods=['GET'])
def get_system_data(no):
    system_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'system', f'{no}.json')
    if os.path.exists(system_path):
        return send_from_directory(os.path.join(BASE_DIR, 'data', 'oncampus_data', 'system'), f'{no}.json', mimetype='application/json; charset=utf-8')
    else:
        return "System data not found for the provided number", 404

@app.route('/<int:no>/system/ids', methods=['POST'])
def get_system_data_by_ids(no):
    requested_ids = request.json.get('ids', [])
    if not requested_ids:
        return jsonify({"error": "No IDs provided"}), 400

    system_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'system', f'{no}.json')
    if os.path.exists(system_path):
        with open(system_path, 'r', encoding='utf-8') as file:
            system_data = json.load(file)
        filtered_data = [item for item in system_data if item.get('id') in requested_ids]
        return jsonify(filtered_data)
    else:
        return "System data not found for the provided number", 404

@app.route('/<int:no>/class', methods=['GET'])
def get_class_data(no):
    class_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'class', f'{no}.json')
    if os.path.exists(class_path):
        return send_from_directory(os.path.join(BASE_DIR, 'data', 'oncampus_data', 'class'), f'{no}.json', mimetype='application/json; charset=utf-8')
    else:
        return "Class data not found for the provided number", 404

@app.route('/<int:no>/class/ids', methods=['POST'])
def get_class_data_by_ids(no):
    requested_ids = request.json.get('ids', [])
    if not requested_ids:
        return jsonify({"error": "No IDs provided"}), 400

    class_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'class', f'{no}.json')
    if os.path.exists(class_path):
        with open(class_path, 'r', encoding='utf-8') as file:
            class_data = json.load(file)
        filtered_data = [item for item in class_data if item.get('id') in requested_ids]
        return jsonify(filtered_data)
    else:
        return "Class data not found for the provided number", 404

@app.route('/<int:no>/system/roadmapRec', methods=['POST'])
def getOnCampusRoadmapSystemRec(no):
    requested_types = request.json.get('type', [])

    system_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'system', f'{no}.json')
    if os.path.exists(system_path):
        with open(system_path, 'r', encoding='utf-8') as file:
            system_data = json.load(file)
        matching_items = [item for item in system_data if item.get('type') in requested_types]
        if matching_items:
            random_item = random.choice(matching_items)
            return jsonify(random_item)
        else:
            return jsonify({"error": "No matching system data found"}), 404
    else:
        return jsonify({"error": f"System data not found for the provided number {no}"}), 404

@app.route('/<int:no>/class/roadmapRec', methods=['GET'])
def getOnCampusRoadmapClassRec(no):
    class_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'class', f'{no}.json')
    if os.path.exists(class_path):
        with open(class_path, 'r', encoding='utf-8') as file:
            class_data = json.load(file)
        if class_data:
            random_item = random.choice(class_data)
            response = json.dumps(random_item, ensure_ascii=False, indent=4)
            return Response(response, mimetype="application/json; charset=utf-8")
        else:
            return jsonify({"error": "Class data is empty or not found"}), 404
    else:
        return jsonify({"error": "Class data not found for the provided number"}), 404

#교내지원사업_창업 지원 공고의 get, post 메소드
@app.route('/<int:no>/notify', methods=['GET'])
def get_notify_data(no):
    notify_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'notify', f'{no}.json')
    if os.path.exists(notify_path):
        return send_from_directory(os.path.join(BASE_DIR, 'data', 'oncampus_data', 'notify'), f'{no}.json', mimetype='application/json; charset=utf-8')
    else:
        return "Notify data not found for the provided number", 404

@app.route('/<int:no>/notify/ids', methods=['POST'])
def get_notify_data_by_ids(no):
    requested_ids = request.json.get('ids', [])
    if not requested_ids:
        return jsonify({"error": "No IDs provided"}), 400

    notify_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'notify', f'{no}.json')
    if os.path.exists(notify_path):
        with open(notify_path, 'r', encoding='utf-8') as file:
            notify_data = json.load(file)
        notify_data_filtered = [item for item in notify_data if item.get('id') in requested_ids]
        return jsonify(notify_data_filtered)
    else:
        return "Notify data not found for the provided number", 404

@app.route('/<int:no>/notify/filtered', methods=['POST'])
def get_notify_data_filtered(no):
    requested_type = request.json.get('type', None)
    sorting = request.json.get('sorting', None)

    notify_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'notify', f'{no}.json')
    if os.path.exists(notify_path):
        with open(notify_path, 'r', encoding='utf-8') as file:
            notify_data = json.load(file)
        if requested_type == '전체':
            filtered_data = notify_data
        else:
            filtered_data = [item for item in notify_data if item.get('type') == requested_type]

        if sorting == 'latest':
            filtered_data.sort(key=lambda x: (x['startdate'], x['title']))
        elif sorting == 'savedLot':
            filtered_data.sort(key=lambda x: (-x['saved'], x['title']))

        return jsonify(filtered_data)
    else:
        return jsonify({"error": "Notify data not found for the provided number"}), 404

@app.route('/<int:no>/notify/search', methods=['POST'])
def get_notify_data_search(no):
    data = request.json
    requested_type = data.get('type', '전체')
    sorting = data.get('sorting', None)
    keyword = data.get('keyword', '')

    notify_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'notify', f'{no}.json')
    if os.path.exists(notify_path):
        with open(notify_path, 'r', encoding='utf-8') as file:
            notify_data = json.load(file)
        filtered_data = [
            item for item in notify_data
            if (requested_type == '전체' or item['type'] == requested_type) and
               (keyword.lower() in item['title'].lower() or keyword.lower() in item['content'].lower())
        ]

        if sorting == 'latest':
            filtered_data.sort(key=lambda x: (x['startdate'], x['title']))
        elif sorting == 'savedLot':
            filtered_data.sort(key=lambda x: (-x['saved'], x['title']))

        return jsonify(filtered_data)
    else:
        return jsonify({"error": "Notify data not found for the provided number"}), 404

@app.route('/offcampus', methods=['GET'])
def get_offcampus_data():
    outschool_gara_path = os.path.join(BASE_DIR, 'data', 'outschool_gara.json')
    if os.path.exists(outschool_gara_path):
        with open(outschool_gara_path, 'r', encoding='utf-8') as file:
            outschool_data = json.load(file)
        return Response(json.dumps(outschool_data, ensure_ascii=False, indent=4), mimetype='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Outschool data file not found"}), 404

@app.route('/offcampus/ids', methods=['POST'])
def get_offcampus_data_by_ids():
    requested_ids = request.json.get('ids', [])
    if not requested_ids:
        return jsonify({"error": "No IDs provided"}), 400

    outschool_gara_path = os.path.join(BASE_DIR, 'data', 'outschool_gara.json')
    if os.path.exists(outschool_gara_path):
        with open(outschool_gara_path, 'r', encoding='utf-8') as file:
            outschool_data = json.load(file)
        filtered_data = [item for item in outschool_data if item.get('id') in requested_ids]
        return jsonify(filtered_data)
    else:
        return jsonify({"error": "Outschool data file not found"}), 404

@app.route('/offcampus/filtered', methods=['POST'])
def get_offcampus_data_filter():
    filter_conditions = request.json
    supporttype = filter_conditions.get('supporttype', '전체')
    region = filter_conditions.get('region', '전체')
    posttarget = filter_conditions.get('posttarget', '전체')
    sorting = filter_conditions.get('sorting', None)

    outschool_gara_path = os.path.join(BASE_DIR, 'data', 'outschool_gara.json')
    if os.path.exists(outschool_gara_path):
        with open(outschool_gara_path, 'r', encoding='utf-8') as file:
            outschool_data = json.load(file)
        filtered_data = [item for item in outschool_data if
                          (supporttype == '전체' or item['supporttype'] == supporttype) and
                          (region == '전체' or item['region'] == region) and
                          (posttarget == '전체' or posttarget in item['posttarget'])]

        if sorting == 'latest':
            filtered_data.sort(key=lambda x: (x['startdate'], x['title']))
        elif sorting == 'savedLot':
            filtered_data.sort(key=lambda x: (-x['saved'], x['title']))

        return jsonify(filtered_data)
    else:
        return jsonify({"error": "Outschool data file not found"}), 404

@app.route('/offcampus/search', methods=['POST'])
def get_offcampus_data_search():
    filter_conditions = request.json
    supporttype = filter_conditions.get('supporttype', '전체')
    region = filter_conditions.get('region', '전체')
    posttarget = filter_conditions.get('posttarget', '전체')
    sorting = filter_conditions.get('sorting', None)
    keyword = filter_conditions.get('keyword', '')

    outschool_gara_path = os.path.join(BASE_DIR, 'data', 'outschool_gara.json')
    if os.path.exists(outschool_gara_path):
        with open(outschool_gara_path, 'r', encoding='utf-8') as file:
            outschool_data = json.load(file)
        filtered_data = [
            item for item in outschool_data
            if (supporttype == '전체' or item['supporttype'] == supporttype) and
               (region == '전체' or item['region'] == region) and
               (posttarget == '전체' or posttarget in item['posttarget']) and
               (keyword.lower() in item['title'].lower() or keyword.lower() in item['content'].lower())
        ]

        if sorting == 'latest':
            filtered_data.sort(key=lambda x: (x['startdate'], x['title']))
        elif sorting == 'savedLot':
            filtered_data.sort(key=lambda x: (-x['saved'], x['title']))

        return jsonify(filtered_data)
    else:
        return jsonify({"error": "Outschool data file not found"}), 404

@app.route('/offcampus/popular', methods=['GET'])
def get_popular_search_terms():
    popular_search_path = os.path.join(BASE_DIR, 'data', 'offcampus_data', 'popular_search.json')
    if os.path.exists(popular_search_path):
        with open(popular_search_path, 'r', encoding='utf-8') as file:
            popular_search_terms = json.load(file)
        return Response(json.dumps(popular_search_terms, ensure_ascii=False, indent=4), mimetype='application/json; charset=utf-8')
    else:
        return jsonify({"error": "Popular search terms file not found"}), 404

@app.route('/offcampus/roadmapRec', methods=['POST'])
def get_offcampus_roadmap_recommend():
    data = request.json
    posttarget_bool = data.get('posttarget', None)
    region = data.get('region', None)
    age = data.get('age', None)
    supporttypes = data.get('supporttype', [])

    outschool_gara_path = os.path.join(BASE_DIR, 'data', 'outschool_gara.json')
    if os.path.exists(outschool_gara_path):
        with open(outschool_gara_path, 'r', encoding='utf-8') as file:
            outschool_data = json.load(file)
        filtered_data = [
            item for item in outschool_data
            if ((posttarget_bool is None or (posttarget_bool and '예비창업자' not in item['posttarget']) or
                 (not posttarget_bool and '예비창업자' in item['posttarget'])) and
                (region is None or item['region'] == region) and
                (age is None or (item['agestart'] <= age <= item['ageend'])) and
                (not supporttypes or any(supporttype in item['supporttype'] for supporttype in supporttypes)))
        ]
        return jsonify(filtered_data)
    else:
        return jsonify({"error": "Outschool data file not found"}), 404

@app.route('/<int:no>/supportgroup/tablist', methods=['GET'])
def get_support_group_tablist(no):
    support_group_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'support_group', f'{no}.json')
    if os.path.exists(support_group_path):
        with open(support_group_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        types = set(item['type'] for item in data)
        order = ["멘토링", "동아리", "특강", "경진대회 및 캠프", "공간", "기타"]
        sorted_types = sorted(types, key=lambda x: order.index(x) if x in order else len(order))
        return Response(json.dumps(sorted_types, ensure_ascii=False), mimetype='application/json; charset=utf-8')
    else:
        return "Support group data not found for the provided number", 404

@app.route('/<int:no>/supportgroup/<string:type_name>', methods=['GET'])
def get_support_group_by_type(no, type_name):
    type_mapping = {
        "mentoring": "멘토링",
        "club": "동아리",
        "lecture": "특강",
        "competition": "경진대회 및 캠프",
        "space": "공간",
        "etc": "기타"
    }
    real_type = type_mapping.get(type_name)
    if not real_type:
        return "Invalid type", 400

    support_group_path = os.path.join(BASE_DIR, 'data', 'oncampus_data', 'support_group', f'{no}.json')
    if os.path.exists(support_group_path):
        with open(support_group_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        filtered_data = [item for item in data if item['type'] == real_type]
        return Response(json.dumps(filtered_data, ensure_ascii=False, indent=4), mimetype='application/json; charset=utf-8')
    else:
        return "Support group data not found for the provided number", 404


# 여기서부터 시스템 데이터 부분

@app.route('/getUserNickName', methods=['POST'])
def get_user_nickname():
    requested_nickname = request.json.get('nickname', None)
    user_info_path = os.path.join(BASE_DIR, 'data', 'system_data', 'user_info.json')
    if os.path.exists(user_info_path):
        with open(user_info_path, 'r', encoding='utf-8') as file:
            user_info_data = json.load(file)
        existing_nicknames = [user['nickname'] for user in user_info_data['users']]
        return jsonify(not requested_nickname in existing_nicknames)
    else:
        return jsonify({"error": "User info file not found"}), 404

@app.route('/createuserinfo', methods=['POST'])
def post_create_userinfo():
    nickname = request.json.get('nickname')
    kakaoUserID = request.json.get('kakaoUserID')
    if not nickname or kakaoUserID is None:
        return Response("Nickname and kakaoUserID are required", status=400)
    userinfo_path = os.path.join(BASE_DIR, 'data', 'system_data', 'user_info.json')
    if os.path.exists(userinfo_path) and os.stat(userinfo_path).st_size != 0:
        with open(userinfo_path, 'r', encoding='utf-8') as file:
            userinfo = json.load(file)
    else:
        userinfo = {"users": []}
    existing_user = next((user for user in userinfo['users'] if user.get('kakaoUserID') == kakaoUserID), None)
    if existing_user:
        existing_user['nickname'] = nickname
    else:
        uuid = f"{datetime.now().strftime('%y%m%d')}{len(userinfo['users'])+1:03d}"
        userinfo['users'].append({"uuid": uuid, "nickname": nickname, "kakaoUserID": kakaoUserID})
    with open(userinfo_path, 'w', encoding='utf-8') as file:
        json.dump(userinfo, file, ensure_ascii=False, indent=4)
    return Response(uuid if existing_user else userinfo['users'][-1]['uuid'], mimetype='text/plain')

@app.route('/changeNickName', methods=['POST'])
def get_change_usernickname():
    data = request.json
    uuid = data.get('uuid')
    new_nickname = data.get('nickname')
    user_info_path = os.path.join(BASE_DIR, 'data', 'system_data', 'user_info.json')
    if not os.path.exists(user_info_path):
        return jsonify({"error": "User info file not found"}), 404
    with open(user_info_path, 'r', encoding='utf-8') as file:
        user_info = json.load(file)
    user = next((user for user in user_info['users'] if user['uuid'] == uuid), None)
    if user:
        user['nickname'] = new_nickname
        with open(user_info_path, 'w', encoding='utf-8') as file:
            json.dump(user_info, file, ensure_ascii=False, indent=4)
        return jsonify({"success": True})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/question/<question_id>', methods=['GET'])
def get_question_data(question_id):
    file_path = os.path.join(BASE_DIR, 'Q&A', 'question_data', f'{question_id}q.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            question_data = json.load(file)
        return Response(json.dumps(question_data, ensure_ascii=False, indent=4), mimetype="application/json; charset=utf-8")
    else:
        return jsonify({"error": "Question data not found"}), 404

# 이후에 있는 /question/<question_id>/write, /questionbyqid/<qid> 등의 라우트도 비슷한 방식으로 파일 경로를 `os.path.join`을 사용하여 수정해 주세요. 

# 질문 생성 및 업데이트 메소드
@app.route('/question/<question_id>/write', methods=['POST'])
def write_question_data(question_id):
    question_text = request.json.get('question')
    for_contact = request.json.get('forContact')
    user_uuid = request.json.get('uuid')
    user_name = request.json.get('nickname')
    profile_num = request.json.get('profileNum', 1)  # 기본값을 1로 설정

    file_path = os.path.join(BASE_DIR, 'Q&A', 'question_data', f'{question_id}q.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            last_qid = data[-1]['qid'] if data else f'{question_id}q000'
            qid_num = int(last_qid[-3:]) + 1
    else:
        qid_num = 1

    qid = f'{question_id}q{qid_num:03d}'
    today = datetime.now().strftime('%y%m%d')
    new_question = {
        "userUUID": user_uuid,
        "userName": user_name,
        "qid": qid,
        "question": question_text,
        "date": today,
        "forContact": for_contact,
        "like": 0,
        "answerCount": 0,
        "contactAnswer": False,
        "profileNum": profile_num
    }

    if os.path.exists(file_path):
        with open(file_path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data.append(new_question)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
    else:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([new_question], file, ensure_ascii=False, indent=4)

    return jsonify({"qid": qid})

@app.route('/questionbyqid/<qid>', methods=['GET'])
def get_question_data_by_qid(qid):
    question_id = qid[:-4]
    file_path = os.path.join(BASE_DIR, 'Q&A', 'question_data', f'{question_id}q.json')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            questions = json.load(file)
            question_data = next((item for item in questions if item['qid'] == qid), None)
            if question_data:
                return Response(json.dumps(question_data, ensure_ascii=False, indent=4), mimetype="application/json; charset=utf-8")
            else:
                return jsonify({"error": "Question with given qid not found"}), 404
    else:
        return jsonify({"error": "Question data file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
