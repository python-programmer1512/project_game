import serial

# 'COM3' 부분에 환경에 맞는 포트 입력
ser = serial.Serial('COM3', 115200)

while True:
    if ser.readable():
        input_str = input()  # 최대 32 문자
        size = len(input_str)
        if 0 <= size <= 32:
            # data 전송
            input_str = input_str.encode('utf-8')
            ser.write(input_str)
        else:
            print("32 글자 초과, 재입력 바랍니다.")
