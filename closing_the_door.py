import requests
import datetime
import time
from urllib.parse import unquote
import PySimpleGUI as sg
from haversine import haversine
import json
import playsound
import os
import threading

sg.theme('SystemDefault1')

# GUI 관련 변수
colcolor1 = 'grey30'
colcolor2 = 'grey30'
fontcolor = 'grey90'
fontcolor1 = 'grey90'
fontcolor2 = 'grey90'
recfontcolor = 'grey70'

eqrectimet = ('Noto Sans KR Bold', 12, 'bold')
eqdepthsizet = ('Noto Sans KR Bold', 20, 'bold')
eqexplaint = ('Noto Sans KR Bold', 15)
eqregiont = ('Noto Sans KR Bold', 20)
eqsint = ('Noto Sans KR Bold', 50, 'bold')
eqtimet = ('Noto Sans KR Bold', 13, 'bold')

recenteqrectimet = ('Noto Sans KR Bold', 10, 'bold')
recenteqdepthsizet = ('Noto Sans KR Bold', 14, 'bold')
recenteqexplaint = ('Noto Sans KR Bold', 12)
recenteqregiont = ('Noto Sans KR Bold', 17)
recenteqsint = ('Noto Sans KR Bold', 40, 'bold')
recenteqtimet = ('Noto Sans KR Bold', 12, 'bold')

elementlist1 = ['eqregionk', 'eqtimek', 'eqsink', 'col1k', 'm1k', 'eqsizek', 'eqdepthk', 'km1k', 'eqseck', 'sec1k', 'eqrectimek', 'col11k']
elementlist2 = ['recenteqregionk', 'recenteqtimek', 'recenteqsink', 'col2k', 'recenteqsizek', 'recenteqdepthk', 'km2k', 'recenteqrectimek', 'col21k']

textlist1 = ['eqregionk', 'eqtimek', 'eqsink', 'm1k', 'eqsizek', 'eqdepthk', 'km1k', 'eqseck', 'sec1k', 'eqrectimek']
textlist2 = ['recenteqregionk', 'recenteqtimek', 'recenteqsink', 'recenteqsizek', 'recenteqdepthk', 'km2k', 'recenteqrectimek']

# 작동 관련 변수
sindolist = ['Ⅰ', 'Ⅱ', 'Ⅲ', 'Ⅳ', 'Ⅴ', 'Ⅵ', 'Ⅶ', 'Ⅷ', 'Ⅸ', 'Ⅹ']
colorlist = ['white', 'a0e6ff', '92d050', 'FFFF00', 'FFC000', 'F00000', 'a32777', '632523', '4C2600', 'black']

eqregion = '현재 지진 정보가 없습니다.'
eqdepth = '0'
eqsize = '0.0'
eqtime = '0000/00/00 00:00:00'
eqsin = '⨉'
eqsec = 00
eqid = ''
curpos = (35.17, 129.06)
eqrectime = '0000/00/00 00:00:00 업데이트'

recenteqregion = '현재 지진 정보가 없습니다.'
recenteqdepth = '0'
recenteqsize = '0.0'
recenteqtime = '0000/00/00 00:00:00'
recenteqsin = '⨉'
recenteqrectime = '0000/00/00 00:00:00 업데이트'
recenteqid = ''

HeadLength = 4
MaxEqkStrLen = 60
MaxEqkInfoLen = 120
AreaNames = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]

eqinfo = [
            [sg.Text(eqregion, font=eqregiont, key='eqregionk', text_color=fontcolor, background_color=colcolor1)],
            [sg.Text(eqtime, font=eqtimet, key='eqtimek', text_color=fontcolor, background_color=colcolor1)]        
        ]
eqinfo2 = [
            [sg.Text(recenteqregion, font=recenteqregiont, key='recenteqregionk', text_color=fontcolor, background_color=colcolor2)],
            [sg.Text(recenteqtime, font=recenteqtimet, key='recenteqtimek', text_color=fontcolor, background_color=colcolor2)]        
        ]
col1 = [  [sg.Text(eqsin, font=eqsint, key='eqsink', text_color=fontcolor, background_color=colcolor1), sg.Column(eqinfo, key='col1k', background_color=colcolor1)],
            [sg.Text('M', font=eqexplaint, text_color=fontcolor, background_color=colcolor1, key='m1k'), sg.Text(eqsize, font=eqdepthsizet, key=('eqsizek'), text_color=fontcolor, background_color=colcolor1), sg.Text(eqdepth, font=eqdepthsizet, key='eqdepthk', text_color=fontcolor, background_color=colcolor1),sg.Text('KM', font=eqexplaint, text_color=fontcolor, background_color=colcolor1, key='km1k'), sg.Text(eqsec, font=eqdepthsizet, key='eqseck', text_color=fontcolor, background_color=colcolor1),sg.Text('초', font=eqexplaint, text_color=fontcolor, background_color=colcolor1, key='sec1k'), sg.Text(eqrectime, font=eqrectimet, key='eqrectimek', text_color=recfontcolor, background_color=colcolor1)]
        ]

col2 = [  [sg.Text(recenteqsin, font=recenteqsint, key='recenteqsink', text_color=fontcolor, background_color=colcolor2), sg.Column(eqinfo2, background_color=colcolor2, key='col2k')],
            [sg.Text('M', font=recenteqexplaint, text_color=fontcolor, background_color=colcolor2, key='m2k'), sg.Text(recenteqsize, font=recenteqdepthsizet, text_color=fontcolor, key='recenteqsizek', background_color=colcolor2), sg.Text(recenteqdepth, text_color=fontcolor, font=recenteqdepthsizet, key='recenteqdepthk', background_color=colcolor2),sg.Text('KM', font=recenteqexplaint, text_color=fontcolor, background_color=colcolor2, key='km2k'), sg.Text(recenteqrectime, font=recenteqrectimet, key='recenteqrectimek', text_color=recfontcolor, background_color=colcolor2)]
        ]
layout = [
            [sg.Text("0000/00/00 00:00", font=eqtimet, key='timern', text_color=fontcolor, background_color='grey23')],
            [sg.Column(col1, element_justification='l', background_color=colcolor1, key='col11k', expand_x='true')],
            [sg.Column(col2, element_justification='l', background_color=colcolor2, key='col21k', expand_x='true')],
            [sg.VPush(background_color='grey23')]
         ]
window = sg.Window('Closing the Door', layout, resizable=True, background_color='grey23')

StationUpdate = True

def soundplay(music):
    t = threading.Thread(target=playsound.playsound, args=('./audio/'+music+'.wav',))
    t.start()

def geteqregion(phase, url):
    if phase == 2:
        try:
            response = requests.get(url + ".le", headers={"user-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)"}).get
            return response.json().get("info_ko", "")
        except Exception as e:
            print(e)
            with open("log.txt", "a") as log_file:
                log_file.write(str(datetime.datetime.utcnow()) + "\n")
                log_file.write(str(e) + "\n")
    else:
        try:
            response = requests.get(url + ".li", headers={"user-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)"}).get
            return response.json().get("info_ko", "")
        except Exception as e:
            print(e)
            with open("log.txt", "a") as log_file:
                log_file.write(str(datetime.datetime.utcnow()) + "\n")
                log_file.write(str(e) + "\n")

def changecolorelement1(color):
    if color != "grey30":
        if color in sindolist:
            if (sindolist.index(color)) < 5:
                colcolor1 = sindolist.index(color)
                fontcolor1 = 'black'
            else:
                colcolor1 = sindolist.index(color)
                fontcolor1 = 'white'
        else: 
            colcolor1 = 'black'
            fontcolor1 = 'white'
        for i, key in enumerate(textlist1):
            try:
                window[key].widget.master.configure(text_color=fontcolor1)
                window[key].widget.configure(text_color=fontcolor1)
            except:
                pass
    for i, key in enumerate(elementlist1):
        try:
            window[key].widget.master.configure(colcolor1)
            window[key].widget.configure(background=colcolor1)
        except:
            pass
                    
def changecolorelement2(color):
    if color != "grey30":
        if color in sindolist:
            if (sindolist.index(color)) < 5:
                colcolor2 = sindolist.index(color)
                fontcolor2 = 'black'
            else:
                colcolor2 = sindolist.index(color)
                fontcolor2 = 'white'
        else: 
            colcolor2 = 'black'
            fontcolor2 = 'white'
        for i, key in enumerate(textlist2):
            try:
                window[key].widget.master.configure(text_color=fontcolor2)
                window[key].widget.configure(text_color=fontcolor2)
            except:
                pass
    for i, key in enumerate(elementlist2):
        try:
            window[key].widget.master.configure(colcolor2)
            window[key].widget.configure(background=colcolor2)
        except:
            pass

changecolorelement1("grey30")
changecolorelement2("grey30")   

def byte_to_bin_str(val):
    return bin(val)[2:].zfill(8)

# 지진 핸들러

def handle_eqk(body, info_bytes, phase):
    data = body[-(MaxEqkStrLen * 8 + MaxEqkInfoLen):]
    eqk_str = unquote(info_bytes.decode('utf-8'))

    orig_lat = 30 + int(data[0:10], 2) / 100
    orig_lon = 124 + int(data[10:20], 2) / 100
    eqk_mag = int(data[20:27], 2) / 10
    eqk_dep = int(data[27:37], 2) / 10
    eqk_time = int(data[37:69], 2)
    eqk_id = "20" + str(int(data[69:95], 2))
    eqk_max = int(data[95:99], 2)
    eqk_max_area_str = data[99:116]
    eqk_max_area = [AreaNames[i] for i, bit in enumerate(eqk_max_area_str) if bit == '1']
    
    url2 = f"https://www.weather.go.kr/pews/data/{eqk_id}" # 지진 ID를 통한 발생위치 정보 수신을 위한 url

    # 지진 핸들링

    if eqid == eqk_id: # 현재 지진의 데이터 수정
        eqpos = (orig_lat, orig_lon)
        eqsec = format(haversine(eqpos, curpos, unit = 'km') / 3.75 - datetime.timestamp(datetime.now()) + eqk_time, ".0f")
        eqdepth = eqk_dep
        eqsize = eqk_mag
        eqtime = datetime.datetime.fromtimestamp(eqk_time).strftime('%Y/%m/%d %H:%M:%S')
        eqsin = eqk_max
        changecolorelement1(eqsin)
        eqid = eqk_id
        eqrectime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' ' + "업데이트"

        window['eqregionk'].update(eqregion)
        window['eqdepthk'].update(eqdepth)
        window['eqsizek'].update(eqsize)
        window['eqtimek'].update(eqtime)
        window['eqsink'].update(eqsin)
        window['eqrectimek'].update(eqrectime)

    elif recenteqid == eqk_id: # 최근 지진의 데이터 수정
        recenteqdepth = eqk_dep
        recenteqsize = datetime.datetime.fromtimestamp(eqk_time).strftime('%Y/%m/%d %H:%M:%S')
        recenteqtime = eqtime
        recenteqsin = eqk_max
        recenteqrectime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' ' + "업데이트"
        changecolorelement2(recenteqsin)

        window['recenteqregionk'].update(recenteqregion)
        window['recenteqdepthk'].update(recenteqdepth)
        window['recenteqsizek'].update(recenteqsize)
        window['recenteqtimek'].update(recenteqtime)
        window['recenteqsink'].update(recenteqsin)
        window['recenteqrectimek'].update(recenteqrectime)

    else: # 새로운 지진 업데이트
        if phase == 2:
            soundplay('eew')
        else:
            soundplay('earthquakeinfo')
        recenteqregion = eqregion
        recenteqdepth = eqdepth
        recenteqsize = eqsize
        recenteqtime = eqtime
        recenteqsin = eqsin
        recenteqrectime = eqrectime

        eqpos = (orig_lat, orig_lon)
        eqsec = format(haversine(eqpos, curpos, unit = 'km') / 3.75 - datetime.timestamp(datetime.now()) + eqk_time, ".0f")
        eqregion = geteqregion(phase, url2)
        eqdepth = eqk_dep
        eqsize = eqk_mag
        eqtime = datetime.datetime.fromtimestamp(eqk_time).strftime('%Y/%m/%d %H:%M:%S')
        eqsin = eqk_max
        changecolorelement1(eqsin)
        eqid = eqk_id
        eqrectime = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + ' ' + "업데이트"

        window['eqregionk'].update(eqregion)
        window['eqdepthk'].update(eqdepth)
        window['eqsizek'].update(eqsize)
        window['eqtimek'].update(eqtime)
        window['eqsink'].update(eqsin)
        window['eqrectimek'].update(eqrectime)

        window['recenteqregionk'].update(recenteqregion)
        window['recenteqdepthk'].update(recenteqdepth)
        window['recenteqsizek'].update(recenteqsize)
        window['recenteqtimek'].update(recenteqtime)
        window['recenteqsink'].update(recenteqsin)
        window['recenteqrectimek'].update(recenteqrectime)
        changecolorelement2(recenteqsin)

    print("위도:", orig_lat)
    print("경도:", orig_lon)
    print("규모:", eqk_mag)
    print("깊이:", eqk_dep)
    print("시각:", datetime.datetime.fromtimestamp(eqk_time).strftime('%Y-%m-%d %H:%M:%S'))
    print("ID:", eqk_id)
    print("설명:", eqk_str)
    print("최대 진도:", eqk_max)
    print("영향 지역:", ", ".join(eqk_max_area))
    
    if eqsec > 0 and eqsec != 0: # 카운트다운
        window['eqseck'].update(eqsec)
        if eqsec < 11:
            soundplay('countdown')
    elif eqsec != 0: 
        window['eqseck'].update('0')
        soundplay('reach')

def handle_stn(stn_body, bin_body):
    stn_lat = [30 + int(stn_body[i:i+10], 2) / 100 for i in range(0, len(stn_body), 20)]
    stn_lon = [120 + int(stn_body[i+10:i+20], 2) / 100 for i in range(0, len(stn_body), 20)]

    print("관측소 수:", len(stn_lat))

    if len(stn_lat) < 99:
        # 재시도
        return

    mmi_data = parse_mmi(bin_body)

    print("관측소 현재 최대, 최소 진도:", max(mmi_data), min(mmi_data))

    mmi_data = [v for v in mmi_data if v > 1]
    if mmi_data:
        print("진도 목록:", ", ".join(map(str, mmi_data)))

    if len(stn_lat) >= 99:
        # 얻은 관측소 수가 충분하여 다음 업데이트 대기
        global StationUpdate
        StationUpdate = False

def parse_mmi(data):
    mmi_data = []

    mmi_body = data.split("11111111")[0][8:]
    for i in range(0, len(mmi_body), 4):
        mmi_data.append(int(mmi_body[i:i+4], 2))

    return mmi_data

def main():
    while True:
        timern = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        prev_bin_time = ''
        tide = 1000
        next_sync_time = datetime.datetime.min
        event, values = window.read(timeout=10)
        window.refresh()
        window['timern'].update(timern)
        if event == sg.WIN_CLOSED:
            break
        else:
            try:
                bin_time = (datetime.datetime.utcnow() - datetime.timedelta(milliseconds=tide)).strftime("%Y%m%d%H%M%S")
                if prev_bin_time == bin_time:
                    continue
                prev_bin_time = bin_time

                print(bin_time)

                url = f"https://www.weather.go.kr/pews/data/{bin_time}"

                response = requests.get(url + ".b", headers={"user-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)"})
                bytes_data = response.content

                # 시간 동기화
                if datetime.datetime.utcnow() >= next_sync_time:
                    next_sync_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=10.0)

                    st_str = response.headers.get("ST")
                    if st_str and st_str.strip() and st_str.isdigit():
                        server_time = float(st_str)
                        tide = int(time.time() * 1000) - server_time * 1000 + 1000
                        print("동기화:", tide)

                if bytes_data and len(bytes_data) > MaxEqkStrLen:
                    header = ''.join([byte_to_bin_str(byte_val) for byte_val in bytes_data[:HeadLength]])
                    body = byte_to_bin_str(bytes_data[0]) + ''.join([byte_to_bin_str(byte_val) for byte_val in bytes_data[HeadLength:]])

                    global StationUpdate
                    StationUpdate = StationUpdate or (header[0] == '1')

                    phase = 0
                    if header[1] == '0':
                        phase = 1
                    elif header[1] == '1' and header[2] == '0':
                        phase = 2
                    elif header[2] == '1':
                        phase = 3
                    else:
                        phase = 4

                    if phase > 1:
                        if not os.path.exists("bin"):
                            os.makedirs("bin")

                        with open(f"bin/{bin_time}.b", "wb") as file:
                            file.write(bytes_data)

                        info_bytes = bytes_data[-MaxEqkStrLen:]
                        handle_eqk(body, info_bytes, phase)

                    if StationUpdate:
                        stn_bytes = requests.get(url + ".s", headers={"user-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)"}).content

                        if not os.path.exists("bin"):
                            os.makedirs("bin")

                        with open(f"bin/{bin_time}.s", "wb") as file:
                            file.write(stn_bytes)

                        stn_body = ''.join([byte_to_bin_str(byte_val) for byte_val in stn_bytes])
                        handle_stn(stn_body, body)
                    else:
                        mmi_data = parse_mmi(body)

                        if max(mmi_data) >= 2:
                            print("관측소 현재 최대, 최소 진도:", max(mmi_data), min(mmi_data))
                            mmi_data = [v for v in mmi_data if v > 1]
                            if mmi_data:
                                print("진도 목록:", ", ".join(map(str, mmi_data)))
                            if not os.path.exists("bin"):
                                os.makedirs("bin")
                            with open(f"bin/{bin_time}.b", "wb") as file:
                                file.write(bytes_data)
            except Exception as e:
                print(e)
                with open("log.txt", "a") as log_file:
                    log_file.write(str(datetime.datetime.utcnow()) + "\n")
                    log_file.write(str(e) + "\n")
        while timern == datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'): 
            continue

if __name__ == "__main__":
    main()