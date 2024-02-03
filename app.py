from flask import Flask, jsonify, request, Response, json, send_from_directory
import os

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


#여기서부터 교외지원사업 데이터 부분

@app.route('/offcampus', methods=['GET'])
def get_offcampus_data():
    """
    'outschool_gara.json' 파일의 전체 데이터를 반환하는 Flask 라우트
    """
    response = jsonify(outschool_data)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/offcampus/ids', methods=['POST'])
def get_offcampus_data_by_ids():
    # 요청에서 ID 목록을 받음
    requested_ids = request.json.get('ids', [])
    if not requested_ids:
        return jsonify({"error": "No IDs provided"}), 400

    # 요청된 ID에 해당하는 데이터만 필터링
    filtered_data = [item for item in outschool_data if item.get('id') in requested_ids]

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


if __name__ == '__main__':
    app.run(debug=True)
