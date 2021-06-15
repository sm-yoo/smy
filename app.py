from flask import Flask, render_template, request
from flaskext.mysql import MySQL

#Flask 객체 인스턴스 생성
app = Flask(__name__)

#db 설정ß
mysql = MySQL(app)
# config
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_DATABASE_USER'] = 'b3fe3c929ba6ff'
app.config['MYSQL_DATABASE_PASSWORD'] = 'b4f19d5a'
app.config['MYSQL_DATABASE_DB'] = 'heroku_5f42e4cb50eae7c'

# url 패턴 / 라우터 설정 - 데코레이터
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/regist')
def regist():
    # get을 통한 전달받은 데이터를 확인
    tidx = request.args.get('tidx')
    tname = request.args.get('tname')
    tsex = request.args.get('tsex')
    tmajor = request.args.get('tmajor')
    tcourse = request.args.get('tcourse')

    cur = mysql.get_db().cursor()
    cur.execute("use heroku_5f42e4cb50eae7c")
    if not tidx or not tname or not tsex or not tmajor or not tcourse:
        return render_template('index_regist.html')
    else:
        cur.execute(f"""
        insert into trainees(tidx, tname, tsex, tmajor, tcourse)
        values ("{tidx}","{tname}", "{tsex}","{tmajor}","{tcourse}");
        """)
        cur.execute('commit;')

        sql = cur.execute(f"""
        select * from trainees
        """)
        rows = cur.fetchall()[0]
        c1, c2, c3, c4, c5 = rows
        cur.close()

        # 사용자 보낼 데이터 정의
        data = {'tidx':c1, 'tname':c2, 'tsex':c3, 'tmajor':c4, 'tcourse':c5}
        print(data)

    return render_template('index_regist.html', data=data)

@app.route('/search')
def search():
    cur = mysql.get_db().cursor()
    cur.execute("use heroku_5f42e4cb50eae7c")

    sql = cur.execute(f"""
    select * 
    from trainees
    """)

    rows = cur.fetchall()
    data = rows
    print(data)

    filter1 = request.args.get('filter1')
    filter2 = request.args.get('filter2')

    if not filter1 and not filter2:
        filters = '1 = 1'
    elif filter1 and not filter2:
        filters = f'tname = "{filter1}"'
    elif not filter1 and filter2:
        filters = f'tcourse = "{filter2}"'
    else:
        filters = f'tname = "{filter1}" and tcourse = "{filter2}"'

    print(filters)

    sql = cur.execute(f"""
    select t1.tidx, t1.tname, t1.tsex, t1.tmajor, t1.tcourse
    , t2.tend_date
    from
    (
    select * 
    from trainees
    where {filters}
    ) t1
    join courses t2
    on (t1.tcourse = t2.tcourse);
    """)
    rows = cur.fetchall()
    cur.close()

    # 사용자 보낼 데이터 정의
    data = rows
    print(data)

    # return redirect(data)
    return render_template('index_search.html', data=data)

@app.route('/delete')
def delete():
    cur = mysql.get_db().cursor()
    cur.execute("use heroku_5f42e4cb50eae7c")
    sql = cur.execute(f"""
    select * 
    from trainees
    """)

    rows = cur.fetchall()
    data = rows

    filter = request.args.get('filter')
    print(filter)
    if filter:
        cur.execute(f"""
        delete from trainees
        where tidx = '{filter}'
        """)
        cur.execute('commit;')

    sql = cur.execute(f"""
    select * 
    from trainees
    """)
    rows = cur.fetchall()
    cur.close()
    data = rows
    print(data)

    return render_template('index_delete.html', data=data)

@app.route('/update')
def update():
    cur = mysql.get_db().cursor()
    cur.execute("use heroku_5f42e4cb50eae7c")
    sql = cur.execute(f"""
    select * 
    from courses
    """)
    rows = cur.fetchall()
    data = rows

    filter1 = request.args.get('filter1')
    filter2 = request.args.get('filter2')
    print(filter)
    if filter1 and filter2:
        cur.execute(f"""
        update courses set
        tend_date = '{filter2}'
        where tcourse = '{filter1}'
        """)
        cur.execute('commit;')


    sql = cur.execute(f"""
    select t1.tcourse, t1.tfullname, t1.tstart_date, t1.tend_date, count(t2.tidx) as cnt
    from courses t1
    left outer join trainees t2
    on (t1.tcourse = t2.tcourse)
    group by t1.tcourse, t1.tfullname, t1.tstart_date, t1.tend_date;
    """)
    rows = cur.fetchall()
    cur.close()
    data = rows
    print(data)

    return render_template('index_update.html', data=data)


# 메인 테스트
if __name__=="__main__":
    app.run(debug=True)