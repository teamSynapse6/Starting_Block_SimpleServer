from flask import Flask, jsonify, request, Response, json, send_from_directory
import os, random
from datetime import datetime

app = Flask(__name__)

# 'school_link.json' 파일에서 데이터 불러오기
with open('data/school_link.json', 'r', encoding='utf-8') as file:
    school_data = json.load(file)

# 'outschool_gara.json' 파일에서 데이터 불러오기
with open('data/outschool_gara.json', 'r', encoding='utf-8') as file:
    outschool_data = json.load(file)

def get_url_by_no(no):
    """
    주어진 번호에 해당하는 URL을 반환하는 함수
    """
    for school in school_data:
        if school['no'] == no:
            return school['url']
    return None

@app.route('/<int:no>/url', methods=['GET'])
def get_school_url(no):
    """
    주어진 학교 번호에 따라 URL을 반환하는 Flask 라우트
    """
    url = get_url_by_no(no)
    if url:
        return url  # JSON 대신 URL 문자열을 직접 반환
    else:
        return "URL not found for the provided number", 404

@app.route('/<int:no>/logo', methods=['GET'])
def get_school_logo(no):
    """
    주어진 학교 번호에 해당하는 로고 파일(SVG)을 반환하는 Flask 라우트
    """
    logo_path = f'data/school_logo/{no}.svg'
    if os.path.exists(logo_path):
        return send_from_directory('data/school_logo', f'{no}.svg')
    else:
        return "Logo not found for the provided number", 404


#교내지원사업_창업제도의 get, post메소드
@app.route('/<int:no>/system', methods=['GET'])
def get_system_data(no):
    """
    주어진 학교 번호에 해당하는 시스템 데이터(JSON)을 반환하는 Flask 라우트
    """
    system_path = f'data/oncampus_data/system/{no}.json'
    if os.path.exists(system_path):
        return send_from_directory('data/oncampus_data/system', f'{no}.json', mimetype='application/json; charset=utf-8')
    else:
        return "System data not found for the provided number", 404

@app.route('/<int:no>/system/ids', methods=['POST'])
def get_system_data_by_ids(no):
    # 요청에서 ID 목록을 받음
    requested_ids = request.json.get('ids', [])
    if not requested_ids:
        return jsonify({"error": "No IDs provided"}), 400

    # 시스템 데이터 파일 로드
    system_path = f'data/oncampus_data/system/{no}.json'
    if os.path.exists(system_path):
        with open(system_path, 'r', encoding='utf-8') as file:
            system_data = json.load(file)
        
        # 요청된 ID에 해당하는 데이터만 필터링
        filtered_data = [item for item in system_data if item.get('id') in requested_ids]

        return jsonify(filtered_data)
    else:
        return "System data not found for the provided number", 404
    



#교내지원사업_창업 강의의 get, post 메소드  
@app.route('/<int:no>/class', methods=['GET'])
def get_class_data(no):
    """
    주어진 학교 번호에 해당하는 클래스 데이터(JSON)를 반환하는 Flask 라우트
    """
    class_path = f'data/oncampus_data/class/{no}.json'
    if os.path.exists(class_path):
        return send_from_directory('data/oncampus_data/class', f'{no}.json', mimetype='application/json; charset=utf-8')
    else:
        return "Class data not found for the provided number", 404
    
@app.route('/<int:no>/class/ids', methods=['POST'])
def get_class_data_by_ids(no):
    # 요청에서 ID 목록을 받음
    requested_ids = request.json.get('ids', [])
    if not requested_ids:
        return jsonify({"error": "No IDs provided"}), 400

    # 클래스 데이터 파일 로드
    class_path = f'data/oncampus_data/class/{no}.json'
    if os.path.exists(class_path):
        with open(class_path, 'r', encoding='utf-8') as file:
            class_data = json.load(file)
        
        # 요청된 ID에 해당하는 데이터만 필터링
        filtered_data = [item for item in class_data if item.get('id') in requested_ids]

        return jsonify(filtered_data)
    else:
        return "Class data not found for the provided number", 404


@app.route('/<int:no>/system/roadmapRec', methods=['POST'])
def getOnCampusRoadmapSystemRec(no):
    # 클라이언트로부터 받은 type 배열
    requested_types = request.json.get('type', [])
    
    # 시스템 데이터 파일 로드
    system_path = f'data/oncampus_data/system/{no}.json'
    if os.path.exists(system_path):
        with open(system_path, 'r', encoding='utf-8') as file:
            system_data = json.load(file)
        
        # 요청된 type 배열과 일치하는 항목 필터링
        matching_items = [item for item in system_data if item.get('type') in requested_types]

        # 일치하는 항목이 있을 경우 무작위로 하나 선택하여 반환
        if matching_items:
            random_item = random.choice(matching_items)
            return jsonify(random_item)
        else:
            return jsonify({"error": "No matching system data found"}), 404
    else:
        return jsonify({"error": f"System data not found for the provided number {no}"}), 404

    

@app.route('/<int:no>/class/roadmapRec', methods=['GET'])
def getOnCampusRoadmapClassRec(no):
    class_path = f'data/oncampus_data/class/{no}.json'
    if os.path.exists(class_path):
        with open(class_path, 'r', encoding='utf-8') as file:
            class_data = json.load(file)
        
        # 데이터 리스트가 비어있지 않은 경우 무작위 항목 선택
        if class_data:
            random_item = random.choice(class_data)
            # ensure_ascii=False를 설정하여 아스키코드 변환 없이 JSON 응답 생성
            response = json.dumps(random_item, ensure_ascii=False, indent=4)
            return Response(response, mimetype="application/json; charset=utf-8")
        else:
            return jsonify({"error": "Class data is empty or not found"}), 404
    else:
        return jsonify({"error": "Class data not found for the provided number"}), 404
    

#교내지원사업_창업 지원 공고의 get, post 메소드    
@app.route('/<int:no>/notify', methods=['GET'])
def get_notify_data(no):
    """
    주어진 학교 번호에 해당하는 지원공고 데이터(JSON)를 반환하는 Flask 라우트
    """
    notify_path = f'data/oncampus_data/notify/{no}.json'
    if os.path.exists(notify_path):
        return send_from_directory('data/oncampus_data/notify', f'{no}.json', mimetype='application/json; charset=utf-8')
    else:
        return "Notify data not found for the provided number", 404
    

@app.route('/<int:no>/notify/ids', methods=['POST'])
def get_notify_data_by_ids(no):
    # 요청에서 ID 목록을 받음
    requested_ids = request.json.get('ids', [])
    if not requested_ids:
        return jsonify({"error": "No IDs provided"}), 400

    # 각 ID에 해당하는 파일을 찾아서 데이터를 모으는 작업
    notify_data = []  # 데이터를 저장할 빈 리스트

    for id in requested_ids:
        notify_path = f'data/oncampus_data/notify/{no}.json'
        if os.path.exists(notify_path):
            with open(notify_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                for item in data:
                    if item.get('id') == id:
                        notify_data.append(item)

    return jsonify(notify_data)

@app.route('/<int:no>/notify/filtered', methods=['POST'])
def get_notify_data_filtered(no):
    # 요청 본문에서 'type'과 'sorting' 받기
    requested_type = request.json.get('type', None)
    sorting = request.json.get('sorting', None)  # 정렬 조건 추가

    notify_path = f'data/oncampus_data/notify/{no}.json'
    # 파일 존재 확인 및 데이터 로드
    if os.path.exists(notify_path):
        with open(notify_path, 'r', encoding='utf-8') as file:
            notify_data = json.load(file)
        
        # 'type'이 '전체'일 경우 필터링 없이 모든 데이터 반환
        if requested_type == '전체':
            filtered_data = notify_data
        else:
            # 요청된 'type'에 해당하는 데이터 필터링
            filtered_data = [item for item in notify_data if item.get('type') == requested_type]

        # 정렬 로직
        if sorting == 'latest':
            # startdate 기준 오름차순 정렬 후, 동일한 경우 title로 오름차순 정렬
            filtered_data.sort(key=lambda x: (x['startdate'], x['title']))
        elif sorting == 'savedLot':
            # saved 기준 내림차순 정렬 후, 동일한 경우 title로 오름차순 정렬
            filtered_data.sort(key=lambda x: (-x['saved'], x['title']))

        return jsonify(filtered_data)
    else:
        return jsonify({"error": "Notify data not found for the provided number"}), 404

@app.route('/<int:no>/notify/search', methods=['POST'])
def get_notify_data_search(no):
    # 요청 본문에서 'type', 'sorting', 'keyword' 받기
    data = request.json
    requested_type = data.get('type', '전체')
    sorting = data.get('sorting', None)
    keyword = data.get('keyword', '')

    notify_path = f'data/oncampus_data/notify/{no}.json'
    # 파일 존재 확인 및 데이터 로드
    if os.path.exists(notify_path):
        with open(notify_path, 'r', encoding='utf-8') as file:
            notify_data = json.load(file)
        
        # 필터링 로직
        filtered_data = [
            item for item in notify_data
            if (requested_type == '전체' or item['type'] == requested_type) and
               (keyword.lower() in item['title'].lower() or keyword.lower() in item['content'].lower())
        ]

        # 정렬 로직
        if sorting == 'latest':
            # startdate 기준 오름차순 정렬 후, 동일한 경우 title로 오름차순 정렬
            filtered_data.sort(key=lambda x: (x['startdate'], x['title']))
        elif sorting == 'savedLot':
            # saved 기준 내림차순 정렬 후, 동일한 경우 title로 오름차순 정렬
            filtered_data.sort(key=lambda x: (-x['saved'], x['title']))

        return jsonify(filtered_data)
    else:
        return jsonify({"error": "Notify data not found for the provided number"}), 404
    
@app.route('/<int:no>/notify/roadmapRec', methods=['POST'])
def getOnCampusRoadmapRec(no):
    requested_types = request.json.get('types', [])
    
    # 교내지원사업 데이터 파일 로드
    notify_path = f'data/oncampus_data/notify/{no}.json'
    if os.path.exists(notify_path):
        with open(notify_path, 'r', encoding='utf-8') as file:
            notify_data = json.load(file)
        
        # 요청된 type에 해당하는 데이터만 필터링
        filtered_data = [item for item in notify_data if item.get('type') in requested_types]

        return jsonify(filtered_data)
    else:
        return jsonify({"error": f"Notify data not found for the provided number {no}"}), 404



#여기서부터 교외지원사업 데이터 부분

@app.route('/offcampus', methods=['GET'])
def get_offcampus_data():
    """
    'outschool_gara.json' 파일의 전체 데이터를 반환하는 Flask 라우트
    """
    json_data = json.dumps(outschool_data, ensure_ascii=False, indent=4)
    return Response(json_data, mimetype='application/json; charset=utf-8')


@app.route('/offcampus/ids', methods=['POST'])
def get_offcampus_data_by_ids():
    # 요청에서 ID 목록을 받음
    requested_ids = request.json.get('ids', [])
    if not requested_ids:
        return jsonify({"error": "No IDs provided"}), 400

    # 요청된 ID에 해당하는 데이터만 필터링
    filtered_data = [item for item in outschool_data if item.get('id') in requested_ids]

    return jsonify(filtered_data)


@app.route('/offcampus/filtered', methods=['POST'])
def get_offcampus_data_filter():
    # 요청에서 필터링 조건과 정렬 조건을 받음
    filter_conditions = request.json
    supporttype = filter_conditions.get('supporttype', '전체')
    region = filter_conditions.get('region', '전체')
    posttarget = filter_conditions.get('posttarget', '전체')  # 문자열로 받음
    sorting = filter_conditions.get('sorting', None)  # 정렬 조건 추가

    # 필터링된 데이터를 저장할 리스트
    filtered_data = []

    for item in outschool_data:
        if supporttype != '전체' and item['supporttype'] != supporttype:
            continue
        if region != '전체' and item['region'] != region:
            continue
        if posttarget != '전체' and posttarget not in item['posttarget']:
            continue
        filtered_data.append(item)

    # 정렬 로직
    if sorting == 'latest':
        # startdate 기준 오름차순 정렬 후, 동일한 경우 title로 오름차순 정렬
        filtered_data.sort(key=lambda x: (x['startdate'], x['title']))
    elif sorting == 'savedLot':
        # saved 기준 내림차순 정렬 후, 동일한 경우 title로 오름차순 정렬
        filtered_data.sort(key=lambda x: (-x['saved'], x['title']))

    return jsonify(filtered_data)

@app.route('/offcampus/search', methods=['POST'])
def get_offcampus_data_search():
    # 요청에서 필터링 조건, 정렬 조건, 그리고 검색 키워드를 받음
    filter_conditions = request.json
    supporttype = filter_conditions.get('supporttype', '전체')
    region = filter_conditions.get('region', '전체')
    posttarget = filter_conditions.get('posttarget', '전체')  # 문자열로 받음
    sorting = filter_conditions.get('sorting', None)  # 정렬 조건 추가
    keyword = filter_conditions.get('keyword', '')  # 검색 키워드 추가

    # 필터링된 데이터를 저장할 리스트
    filtered_data = []

    for item in outschool_data:
        if supporttype != '전체' and item['supporttype'] != supporttype:
            continue
        if region != '전체' and item['region'] != region:
            continue
        if posttarget != '전체' and posttarget not in item['posttarget']:
            continue
        # 키워드 검색 조건 추가: title 또는 content에 키워드가 포함되어야 함
        if keyword and (keyword.lower() not in item['title'].lower() and keyword.lower() not in item['content'].lower()):
            continue
        filtered_data.append(item)

    # 정렬 로직
    if sorting == 'latest':
        filtered_data.sort(key=lambda x: (x['startdate'], x['title']))
    elif sorting == 'savedLot':
        filtered_data.sort(key=lambda x: (-x['saved'], x['title']))

    return jsonify(filtered_data)




@app.route('/offcampus/popular', methods=['GET'])
def get_popular_search_terms():
    # 인기검색어
    file_path = 'data/offcampus_data/popular_search.json'
    
    # 파일 존재 여부 확인
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            # JSON 파일 로드
            popular_search_terms = json.load(file)
            # JSON 데이터를 ensure_ascii=False로 인코딩하여 반환
            return Response(json.dumps(popular_search_terms, ensure_ascii=False, indent=4), mimetype='application/json; charset=utf-8')
    else:
        return jsonify({"error": "File not found"}), 404
    

@app.route('/offcampus/roadmapRec', methods=['POST'])
def get_offcampus_roadmap_recommend():
    data = request.json
    posttarget_bool = data.get('posttarget', None)
    region = data.get('region', None)
    age = data.get('age', None)
    supporttypes = data.get('supporttype', [])

    filtered_data = []
    for item in outschool_data:
        # posttarget 필터링
        if posttarget_bool is not None:
            if posttarget_bool:
                # '예비창업자'를 제외하고 다른 대상이 하나라도 있으면 해당 항목 포함
                if '예비창업자' in item['posttarget'] and len(item['posttarget']) == 1:
                    continue
            else:
                # '예비창업자'만 포함된 데이터를 찾음
                if '예비창업자' not in item['posttarget']:
                    continue

        # region 필터링 - '전체' 또는 지정된 region과 일치할 때 포함
        if region and item['region'] != '전체' and item['region'] != region:
            continue

        # age 필터링
        if age and not (item['agestart'] <= age <= item['ageend']):
            continue

        # supporttype 필터링
        if supporttypes and not any(supporttype in item['supporttype'] for supporttype in supporttypes):
            continue

        filtered_data.append(item)

    return jsonify(filtered_data)


#여기서부터 창업지원단 데이터 부분

@app.route('/<int:no>/supportgroup/tablist', methods=['GET'])
def get_support_group_tablist(no):
    # support_group 파일 로드
    path = f'data/oncampus_data/support_group/{no}.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 고유 type 추출
        types = set(item['type'] for item in data)

        # 정렬 순서 정의
        order = ["멘토링", "동아리", "특강", "경진대회 및 캠프", "공간", "기타"]
        # 정렬 순서에 따라 types 정렬
        sorted_types = sorted(types, key=lambda x: order.index(x) if x in order else len(order))

        # 타입 이름만을 문자열 리스트로 변환
        return Response(json.dumps(sorted_types, ensure_ascii=False), mimetype='application/json; charset=utf-8')
    else:
        return "Support group data not found for the provided number", 404


@app.route('/<int:no>/supportgroup/<string:type_name>', methods=['GET'])
def get_support_group_by_type(no, type_name):
    # 타입명과 실제 타입의 매핑
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

    path = f'data/oncampus_data/support_group/{no}.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        filtered_data = [item for item in data if item['type'] == real_type]
        json_data = json.dumps(filtered_data, ensure_ascii=False, indent=4)
        return Response(json_data, mimetype='application/json; charset=utf-8')
    else:
        return "Support group data not found for the provided number", 404
    

# 여기서부터 시스템 데이터 부분
    
@app.route('/getUserNickName', methods=['POST'])
def get_user_nickname():
    # 클라이언트에서 전송한 닉네임 받기
    requested_nickname = request.json.get('nickname', None)
    
    # user_info.json 파일 위치 지정 및 파일 로드
    user_info_path = 'data/system_data/user_info.json'
    if os.path.exists(user_info_path):
        with open(user_info_path, 'r', encoding='utf-8') as file:
            user_info_data = json.load(file)
        
        # 파일 내 닉네임 리스트 검색
        existing_nicknames = [user['nickname'] for user in user_info_data['users']]
        if requested_nickname in existing_nicknames:
            # 닉네임이 리스트에 존재하면 False 반환
            return jsonify(False)
        else:
            # 닉네임이 리스트에 존재하지 않으면 True 반환
            return jsonify(True)
    else:
        return jsonify({"error": "User info file not found"}), 404


from flask import Response

@app.route('/createuserinfo', methods=['POST'])
def post_create_userinfo():
    nickname = request.json.get('nickname')
    kakaoUserID = request.json.get('kakaoUserID')  # kakaoUserID 받기
    if not nickname or kakaoUserID is None:
        return Response("Nickname and kakaoUserID are required", status=400)

    today = datetime.now().strftime('%y%m%d')
    userinfo_path = 'data/system_data/user_info.json'

    if not os.path.exists(userinfo_path) or os.stat(userinfo_path).st_size == 0:
        userinfo = {"users": []}
    else:
        with open(userinfo_path, 'r', encoding='utf-8') as file:
            userinfo = json.load(file)

    existing_user = next((user for user in userinfo['users'] if user.get('kakaoUserID') == kakaoUserID), None)
    if existing_user:
        # 기존 사용자의 닉네임 업데이트
        existing_user['nickname'] = nickname
        uuid = existing_user['uuid']  # 기존 사용자의 uuid 사용
    else:
        # 새 UUID 생성 및 저장
        today_users = [user for user in userinfo['users'] if user['uuid'].startswith(today)]
        next_number = len(today_users) + 1
        uuid = f'{today}{next_number:03d}'
        userinfo['users'].append({"uuid": uuid, "nickname": nickname, "kakaoUserID": kakaoUserID})

    # 파일 업데이트
    with open(userinfo_path, 'w', encoding='utf-8') as file:
        json.dump(userinfo, file, ensure_ascii=False, indent=4)

    # 수정된 부분: 생성되거나 업데이트된 사용자의 uuid 값만을 반환
    return Response(uuid, mimetype='text/plain')



@app.route('/changeNickName', methods=['POST'])
def get_change_usernickname():
    # 클라이언트로부터 uuid와 nickname 받기
    data = request.json
    uuid = data.get('uuid')
    new_nickname = data.get('nickname')
    
    # user_info.json 파일 위치 지정 및 로드
    user_info_path = 'data/system_data/user_info.json'
    if not os.path.exists(user_info_path):
        return jsonify({"error": "User info file not found"}), 404
    
    with open(user_info_path, 'r', encoding='utf-8') as file:
        user_info = json.load(file)
    
    # UUID에 해당하는 유저 찾기
    for user in user_info['users']:
        if user['uuid'] == uuid:
            # 기존 닉네임을 새로운 닉네임으로 업데이트
            user['nickname'] = new_nickname
            break
    else:
        return jsonify({"error": "User not found"}), 404

    # 변경된 데이터를 파일에 다시 쓰기
    with open(user_info_path, 'w', encoding='utf-8') as file:
        json.dump(user_info, file, ensure_ascii=False, indent=4)
    
    return jsonify({"success": True})

#Q&A 메소드
@app.route('/question/<question_id>', methods=['GET'])
def get_question_data(question_id):
    # 파일 경로 조합
    file_path = os.path.join('Q&A/question_data', f'{question_id}q.json')
    
    # 파일 존재 여부 확인 및 데이터 로드
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            question_data = json.load(file)
            # ensure_ascii=False를 설정하여 아스키 코드 변환 없이 JSON 응답 생성
            response = json.dumps(question_data, ensure_ascii=False, indent=4)
            return Response(response, mimetype="application/json; charset=utf-8"), 200
    else:
        # 에러 메시지도 아스키 코드 변환 없이 반환
        error_response = json.dumps({"error": "Question data not found"}, ensure_ascii=False)
        return Response(error_response, mimetype="application/json; charset=utf-8"), 404


# 질문 생성 및 업데이트 메소드
def update_question_data(file_path, new_data):
    if os.path.exists(file_path):
        with open(file_path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data.append(new_data)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
    else:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump([new_data], file, ensure_ascii=False, indent=4)

@app.route('/question/<question_id>/write', methods=['POST'])
def write_question_data(question_id):
    question_text = request.json.get('question')
    for_contact = request.json.get('forContact')
    user_uuid = request.json.get('uuid')
    user_name = request.json.get('nickname')
    # 클라이언트로부터 받은 profileNum 값을 처리
    profile_num = request.json.get('profileNum', 1)  # 기본값을 1로 설정

    # 파일 경로 조합
    file_path = os.path.join('Q&A/question_data', f'{question_id}q.json')
    
    # 새로운 qid 생성
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            last_qid = data[-1]['qid'] if data else f'{question_id}q000'
            qid_num = int(last_qid[-3:]) + 1  # 마지막 번호 + 1
    else:
        qid_num = 1  # 파일이 없으면 첫 번째 질문
    
    qid = f'{question_id}q{qid_num:03d}'
    
    # 현재 날짜
    today = datetime.now().strftime('%y%m%d')
    
    # 새로운 질문 데이터 생성
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
        "profileNum": profile_num  # 새로운 필드 추가
    }
    
    # 데이터 파일 업데이트
    update_question_data(file_path, new_question)
    
    # 생성된 qid 반환
    return jsonify({"qid": qid})

@app.route('/questionbyqid/<qid>', methods=['GET'])
def get_question_data_by_qid(qid):
    # 파일명에서 question_id 추출 (qid에서 마지막 'q'와 숫자 부분 제거)
    question_id = qid[:-4]  # '12401020001q002'의 경우 '12401020001' 추출
    file_name = f"{question_id}q.json"
    file_path = os.path.join('Q&A/question_data', file_name)
    
    # 파일 존재 여부 확인 및 데이터 로드
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            questions = json.load(file)
            # qid와 일치하는 질문 찾기
            question_data = next((item for item in questions if item['qid'] == qid), None)
            if question_data:
                # ensure_ascii=False를 설정하여 아스키 코드 변환 없이 JSON 응답 생성
                response = json.dumps(question_data, ensure_ascii=False, indent=4)
                return Response(response, mimetype="application/json; charset=utf-8")
            else:
                return jsonify({"error": "Question with given qid not found"}), 404
    else:
        return jsonify({"error": "Question data file not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
