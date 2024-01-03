import requests
import datetime
import pytz
import time
from urllib.parse import unquote
import PySimpleGUI as sg
from haversine import haversine
import json
import playsound
import os
import threading
from bs4 import BeautifulSoup

# GUI 관련 변수

sg.theme('SystemDefault1')

eqrectimet = ('Noto Sans KR Bold', 12, 'bold')
eqdepthsizet = ('Noto Sans KR Bold', 20, 'bold')
eqexplaint = ('Noto Sans KR Bold', 15)
eqregiont = ('Noto Sans KR SemiBold', 25)
eqsint = ('Noto Sans KR Bold', 65, 'bold')
eqtimet = ('Noto Sans KR Medium', 13)
timernt = ('Noto Sans KR Bold', 13)

recenteqrectimet = ('Noto Sans KR Bold', 10, 'bold')
recenteqdepthsizet = ('Noto Sans KR SemiBold', 14, 'bold')
recenteqexplaint = ('Noto Sans KR Bold', 12)
recenteqregiont = ('Noto Sans KR SemiBold', 17)
recenteqsint = ('Noto Sans KR Bold', 40, 'bold')
recenteqtimet = ('Noto Sans KR Bold', 12, 'bold')

elementlist = ['eqsin', 'eqregion', 'eqtime', 'eqsize', 'eqdepth', 'eqsec', 'eqrectime', 'colm', 'col']
textlist = ['eqsin', 'eqregion', 'eqtime', 'eqsize', 'eqdepth', 'eqsec', 'eqrectime']
# 작동 관련 변수
sindolist = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
colorlist = ['ffffff', 'a0e6ff', '92d050', 'FFFF00', 'FFC000', 'F00000', 'a32777', '632523', '4C2600', '000000']
sindoromaji = ['Ⅰ','Ⅱ','Ⅲ','Ⅳ','Ⅴ','Ⅵ','Ⅶ','Ⅷ','Ⅸ','Ⅹ']

eqlat = []
eqlon = []
eqregion = []
eqdepth = []
eqsize = []
eqtime = []
eqsin = []
eqsec = []
eqid = []
eqrectime = []
eqsource = []
errorhappened = False
doneparsing = True
neweqdata = False
eqexist = False
rectime = "00:00:00 갱신"
lastfilename = ''

lastnuridata = 0
curpos = (35.17, 129.06)
HeadLength = 4
MaxEqkStrLen = 60
MaxEqkInfoLen = 120
AreaNames = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", "세종", "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남", "제주"]

layout = [
    [sg.Text("0000/00/00 00:00", font=timernt, key='timern', text_color='grey90', background_color='grey23'), sg.Text("00:00:00 갱신", font=timernt, key='rectime', text_color='grey70', background_color='grey23')],
    [sg.Column([
        [sg.vtop(sg.Text('⨉', font=eqsint, key='eqsin'+str(1), text_color='grey90', background_color='grey30',pad=(0,0))),
        sg.Column([
            [sg.Text('현재 지진 정보가 없습니다.', font=eqregiont, key='eqregion'+str(1), text_color='grey90', background_color='grey30',pad=(0,0))],
            [sg.Text('0000/00/00 00:00:00', font=eqtimet, key='eqtime'+str(1), text_color='grey90', background_color='grey30',pad=(0,0)), sg.Text('00:00:00 수신', font=eqtimet, key='eqrectime'+str(1), text_color='grey70', background_color='grey30',pad=(0,0))],
            [sg.Text('M 0.0', font=recenteqdepthsizet, text_color='grey90', key='eqsize'+str(1), background_color='grey30',pad=(0,0)), sg.Text('0 KM', text_color='grey90', font=recenteqdepthsizet, key='eqdepth'+str(1), background_color='grey30',pad=(0,0)), sg.Text('0 초', font=recenteqdepthsizet, key='eqsec' + str(1), text_color='grey90', background_color='grey30',pad=(0,0))]],
            element_justification='l', background_color='grey30', key='colm'+str(1),pad=(0,0))],
        ]
        , element_justification='l', background_color='grey30', key='col'+str(1),  vertical_alignment='t', expand_x='true',pad=(0,0))],
    [[sg.Column([
        [sg.vtop(sg.Text('⨉', font=recenteqsint, key='eqsin'+str(i+2), text_color='grey90', background_color='grey30',pad=(0,0))),
        sg.Column([
            [sg.Text('현재 지진 정보가 없습니다.', font=recenteqregiont, key='eqregion'+str(i+2), text_color='grey90', background_color='grey30',pad=(0,0))],
            [sg.Text('0000/00/00 00:00:00', font=eqtimet, key='eqtime'+str(i+2), text_color='grey90', background_color='grey30',pad=(0,0)), sg.Text('00:00:00 수신', font=eqtimet, key='eqrectime'+str(i+2), text_color='grey70', background_color='grey30',pad=(0,0)), sg.Text('M 0.0', font=recenteqdepthsizet, text_color='grey90', key='eqsize'+str(i+2), background_color='grey30',pad=(0,0)), sg.Text('0 KM', text_color='grey90', font=recenteqdepthsizet, key='eqdepth'+str(i+2), background_color='grey30',pad=(0,0)), sg.Text('0 초', font=recenteqdepthsizet, key='eqsec' + str(i+2), text_color='grey90', background_color='grey30',pad=(0,0))]],
            element_justification='l', background_color='grey30', key='colm'+str(i+2))]]
        , element_justification='l', background_color='grey30', key='col'+str(i+2), expand_x='true',pad=(0,0)), [sg.Column((), size=(0,2), background_color='grey23')]] for i in range (5)]
]

window = sg.Window('Closing the Door', layout, resizable=True, background_color='grey23')
event, values = window.read(timeout=10)

StationUpdate = True

def soundplay(music):
    t = threading.Thread(target=playsound.playsound, args=('./audio/'+music+'.wav',))
    t.start()

def geteqregion(phase, url):
    print(phase)
    if phase == 2:
        try:
            response = requests.get(url + ".le", headers={"user-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)"})
            return (response.json()).get("info_ko", "")
        except Exception as e:
            print(e)
            with open("log.txt", "a") as log_file:
                log_file.write(str(datetime.datetime.utcnow()) + "\n")
                log_file.write(str(e) + "\n")
    else:
        try:
            response = requests.get(url + ".li", headers={"user-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)"})
            return (response.json()).get("info_ko", "")
        except Exception as e:
            print(e)
            with open("log.txt", "a") as log_file:
                log_file.write(str(datetime.datetime.utcnow()) + "\n")
                log_file.write(str(e) + "\n")

def guiupdate():
    for i in range(len(eqrectime)):
        if (eqsource[i] == 'PEWS' and int(eqsin[i]) < 5) or (eqsource[i] != 'PEWS' and sindoromaji.index(eqsin[i]) < 5):
            if eqsource[i] == 'PEWS':
                colcolor1 = '#'+colorlist[eqsin[i]-1]
            else:
                colcolor1 = '#'+colorlist[sindoromaji.index(eqsin[i])]
            fontcolor1 = 'black'
        else:
            fontcolor1 = 'white'
        if (eqsource[i] == 'PEWS' and int(eqsin[i]) > 10) or (eqsource[i] != 'PEWS' and eqsin[i] not in sindoromaji):
            fontcolor1 = 'white'
            colcolor1 = 'black'
        window['eqsin' + str(i+1)].update(background_color=colcolor1)
        window['eqsin' + str(i+1)].update(text_color=fontcolor1)
        if isinstance(eqsin[i], int):
            window['eqsin'+str(i+1)].update(sindoromaji[eqsin[i]])
        else:
            window['eqsin'+str(i+1)].update(eqsin[i])
        window['eqregion'+str(i+1)].update(eqregion[i])
        window['eqtime'+str(i+1)].update(eqtime[i])
        window['eqsize'+str(i+1)].update('M ' + str(eqsize[i]))
        window['eqdepth'+str(i+1)].update(str(eqdepth[i]) + " KM")
        window['eqsec'+str(i+1)].update(str(eqsec[i]) + " 초")
        window['eqrectime'+str(i+1)].update(str(eqrectime[i]))

for i in range(6):
        for x in range(len(elementlist)):
            elementname = elementlist[x]+str(i+1)
            window[elementname].ParentRowFrame.config(background='grey30')
            window[elementname].widget.configure(background='grey30')

def byte_to_bin_str(val):
    return bin(val)[2:].zfill(8)

# 지진 핸들러
# 3 = 일반정보 2 = 신속정보

def kmaeqkparse(first):
    global lastnuridata
    url = ''
    if first == True:
        url = 'https://www.weather.go.kr/w/eqk-vol/search/korea.do?schOption=&xls=0&startTm=2023-12-01&endTm=' + datetime.datetime.now().strftime('%Y-%m-%d') + '&startSize=&endSize=&startLat=&endLat=&startLon=&endLon=&lat=&lon=&dist=&keyword=&dpType=a'
    else:
        url = 'https://www.weather.go.kr/w/eqk-vol/search/korea.do?schOption=&xls=0&startTm=2023-12-01&endTm=' + datetime.datetime.now().strftime('%Y-%m-%d') + '&startSize=&endSize=2&startLat=&endLat=&startLon=&endLon=&lat=&lon=&dist=&keyword=&dpType=a'
    try:
        response = requests.get(url, timeout=1)
    except:
        return
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='eqk-search-table')
    rows = table.find('tbody').find_all('tr')
    i = 0
    if first == True:
        for row in rows[:6]:  # 첫 번째에서 여섯 번째까지의 행만 추출
            columns = row.find_all('td')
            eqsec.append(0)
            eqtime.append(columns[1].text.strip())
            eqsize.append(columns[2].text.strip())
            eqdepth.append(columns[3].text.strip())
            eqsin.append(columns[4].text.strip())
            eqlat.append(columns[5].text.strip())
            eqlon.append(columns[6].text.strip())
            eqregion.append(columns[7].text.strip())
            eqid.append(columns[0].text.strip())
            eqsource.append('weathergokr')
            eqrectime.append(datetime.datetime.now().strftime('%H:%M:%S') + ' ' + "수신")
        url = 'https://www.weather.go.kr/w/eqk-vol/search/korea.do?schOption=&xls=0&startTm=2023-12-01&endTm=' + datetime.datetime.now().strftime('%Y-%m-%d') + '&startSize=&endSize=2&startLat=&endLat=&startLon=&endLon=&lat=&lon=&dist=&keyword=&dpType=a'
        lastnuridata = str(int(columns[0].text.strip())+6)
    else:
        for row in rows[:1]:  # 첫 번째에서 첫 번째까지의 행만 추출
            columns = row.find_all('td')
            if lastnuridata == columns[0].text.strip() or (eqtime.index(columns[1].text.strip()) == eqsize.index(columns[2].text.strip()) == eqdepth.index(columns[3].text.strip()) == eqsin.index(columns[4].text.strip()) == eqlat.index(columns[5].text.strip()) == eqlon.index(columns[6].text.strip()) == eqregion.index(columns[7].text.strip())) : # 내가 더러워서 못해먹겠네
                lastnuridata = (columns[0].text.strip())
                break
            else:
                soundplay('earthquakeinfo')
                eqsec.insert(0, 0)
                eqtime.insert(0, columns[1].text.strip())
                eqsize.insert(0, columns[2].text.strip())
                eqdepth.insert(0, columns[3].text.strip())
                eqsin.insert(0, columns[4].text.strip())
                eqlat.insert(0, columns[5].text.strip())
                eqlon.insert(0, columns[6].text.strip())
                eqregion.insert(0, columns[7].text.strip())
                eqid.insert(0, columns[0].text.strip())
                eqsource.insert(0, 'weathergokr')
                eqrectime.insert(0, datetime.datetime.now().strftime('%H:%M:%S') + ' ' + "수신")
                lastnuridata = (columns[0].text.strip())
                eqlat.pop()
                eqlon.pop()
                eqdepth.pop()
                eqsize.pop()
                eqtime.pop()
                eqsin.pop()
                eqid.pop()
                eqrectime.pop()
                eqsec.pop()
                eqsource.pop()

def handle_eqk(body, info_bytes, phase):
    global eqsec
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

    if eqk_id in eqid: # 지진이 포함된 경우 (업데이트)
        if orig_lat not in eqlat or orig_lon not in eqlon or eqk_mag not in eqsize or eqk_dep not in eqdepth or datetime.datetime.fromtimestamp(eqk_time + 9 * 3600).strftime('%Y/%m/%d %H:%M:%S') not in eqtime or eqk_max not in eqsin: # 변경 내용이 있는 경우에만
            eqlat[eqid.index(eqk_id)] = orig_lat
            eqlon[eqid.index(eqk_id)] = orig_lon
            eqregion[eqid.index(eqk_id)] = geteqregion(phase, url2)
            eqdepth[eqid.index(eqk_id)] = eqk_dep
            eqsize[eqid.index(eqk_id)] = eqk_mag
            eqtime[eqid.index(eqk_id)] = datetime.datetime.fromtimestamp(eqk_time + 9 * 3600).strftime('%Y/%m/%d %H:%M:%S')
            eqsin[eqid.index(eqk_id)] = eqk_max
            eqid[eqid.index(eqk_id)] = eqk_id
            eqrectime[eqid.index(eqk_id)] = datetime.datetime.now().strftime('%H:%M:%S') + " 수신"
            if eqsec[eqid.index(eqk_id)] > 0:
                eqsec[eqid.index(eqk_id)] = int(format(haversine((eqlat, eqlon), curpos, unit = 'km') / 3.75 - datetime.datetime.now().timestamp() + eqk_time, ".0f"))
            else:
                eqsec[eqid.index(eqk_id)] = 0

    else: # 새로운 지진 업데이트
        if phase == 2:
            soundplay('eew')
        else:
            soundplay('earthquakeinfo')
        eqlat.insert(0, orig_lat)
        eqlon.insert(0, orig_lon)
        eqregion.insert(0, geteqregion(phase, url2))
        eqdepth.insert(0, eqk_dep)
        eqsize.insert(0, eqk_mag)
        eqtime.insert(0, datetime.datetime.fromtimestamp(eqk_time + 9 * 3600).strftime('%Y/%m/%d %H:%M:%S'))
        eqsin.insert(0, eqk_max)
        eqid.insert(0, eqk_id)
        eqsource.insert(0, 'PEWS')
        eqrectime.insert(0, datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S') + " 수신")
        if int(format(haversine((eqlat, eqlon), curpos, unit = 'km') / 3.75 - datetime.datetime.now().timestamp() + eqk_time, ".0f")) > 0:
            eqsec[eqid.index(eqk_id)] = int(format(haversine((eqlat, eqlon), curpos, unit = 'km') / 3.75 - datetime.datetime.now().timestamp() + eqk_time, ".0f"))
        else:
            eqsec[eqid.index(eqk_id)] = 0
        if len(eqdepth) == 7:
            eqlat.pop()
            eqlon.pop()
            eqdepth.pop()
            eqsize.pop()
            eqtime.pop()
            eqsin.pop()
            eqid.pop()
            eqrectime.pop()
            eqsec.pop()
            eqsource.pop()

    print("위도:", orig_lat)
    print("경도:", orig_lon)
    print("규모:", eqk_mag)
    print("깊이:", eqk_dep)
    print("시각:", datetime.datetime.fromtimestamp(eqk_time).strftime('%Y-%m-%d %H:%M:%S'))
    print("ID:", eqk_id)
    print("설명:", eqk_str)
    print("최대 진도:", eqk_max)
    print("영향 지역:", ", ".join(eqk_max_area))

def eqsecupdate():
    for i in range (6):
        if eqsec[i] > 0:
            eqsec[i] -= 1
        elif eqsec[i] < 0:
            eqsec[i] = 0    

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

def handlecomm():
    global doneparsing
    global errorhappened
    global rectime
    global lastfilename
    errorhappened = False
    prev_bin_time = ''
    tide = 1000
    next_sync_time = datetime.datetime.min
    print('/bin/'+str(lastfilename)+'.b')
    if os.path.isfile('bin/'+str(lastfilename)+'.b'):
        os.remove('bin/'+str(lastfilename)+'.b')
        print('bin/'+str(lastfilename)+'.b deleted')
    try:
        bin_time = (datetime.datetime.utcnow() - datetime.timedelta(milliseconds=tide)).strftime("%Y%m%d%H%M%S")
        if prev_bin_time == bin_time:
            return 0
        prev_bin_time = bin_time

        print(bin_time)

        url = f"https://www.weather.go.kr/pews/data/{bin_time}"
                
        errorhappened = False
        try:
            response = requests.get(url + ".b", headers={"user-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.2; .NET CLR 1.0.3705;)"}, timeout=1)
        except:
            errorhappened = True
            doneparsing = True
                    
        if errorhappened == False:
            rectime = datetime.datetime.now().strftime('%H:%M:%S') + ' 갱신'
            doneparsing = True
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
                eqexist = False
                if header[1] == '0':
                    phase = 1
                elif header[1] == '1' and header[2] == '0':
                    phase = 2
                elif header[2] == '1':
                    phase = 3
                else:
                    phase = 4

                if phase > 1:
                    eqexist = True
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
                    print(doneparsing)
                    lastfilename = bin_time
    except Exception as e:
        print(e)
        with open("log.txt", "a") as log_file:
            log_file.write(str(datetime.datetime.utcnow()) + "\n")
            log_file.write(str(e) + "\n")
        errorhappened = True
    doneparsing = True

def main():
    kmaeqkparse(True)
    guiupdate()
    doneparsing = True
    event, values = window.read(timeout=10)
    while True:
        eqsecupdate()
        timenow = datetime.datetime.now().strftime("%H:%M:%S")
        window.refresh()
        threading.Thread(target=handlecomm, args=(), daemon=True).start()
        if datetime.datetime.now().strftime("%S") == '00':
            threading.Thread(target=kmaeqkparse, args=(False, ), daemon=True).start()
        guiupdate()
        while doneparsing == False:
            window.refresh()
            window['timern'].update(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            window['rectime'].update(rectime)
        while timenow == datetime.datetime.now().strftime("%H:%M:%S"):
            window.refresh()
            window['timern'].update(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
            window['rectime'].update(rectime)
        if event == sg.WIN_CLOSED:
            break
    return 0

if __name__ == "__main__":
    main()