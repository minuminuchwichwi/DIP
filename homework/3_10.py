import numpy as np

np.random.seed(10)          #난수의 시드값 생성
a = np.random.randint(0, 50, 500)   #0부터 50사이의 임의의 정수 500개 생성, 50은 포함되지않음.
cnt = np.zeros(50, np.int8)         #중복 횟수를 반환하기위해 원소가 모두 0인 ndarray 행렬 생성
first, second, third = [0, 0], [0, 0], [0, 0]       #중복이 가장 많이 된 수 3개를 반환하기 위한 리스트 생성. [0]은 수, [1]은 중복 횟수
c, d = np.zeros(50, np.int8), np.zeros(50, np.int8) #가장 큰 수와 두번째로 큰 수를 0으로 바꾸기위해 원소를 모두 0인 행렬 2개 생성

#0부터 50사이의 정수 500개를 임의로 생성한 후 정수 00개와 행렬의 크기 출력
print('0~50사이의 임의의 정수 원소 500개\n', a)
print('\n행렬의 크기 : ', a.shape[0])

#행렬 a를 리스트로 바꿔 count함수를 사용하여 중복된 횟수를 cnt에 저장 후 cnt 출력
b = a.tolist()
for i in range(50):
    cnt[i] = b.count(i)

print('\n0~50사이의 중복되는 횟수\n', cnt)

#반복문을 이용해 가장 중복이 많이 된 수를 max함수를 통해 first에 반환.
#i와 first[0]은 가장 많이 나온 수, max(cnt)와 first[1]은 중복된 횟수
for i in range(50):
    if cnt[i] == max(cnt):
        first[0] = i
        first[1] = max(cnt)

#조건문을 이용해 위에서 나온 수를 제외하고 나머지 수를 c에 저장.
#중복이 가장 많이 된 횟수는 0으로 나머지 횟수들은 그대로 c에 저장 후
#위와 같은 방식으로 두번째로 많이 나온 수를 second에 저장
for i in range(50):
    if i != first[0]:
        c[i] = cnt[i]
    if c[i] == max(c):
        second[0] = i
        second[1] = max(c)

#위 조건문과 마찬가지로 첫 번째와 두 번째로 많이 나온 수를 제외한 최댓값을 third에 저장
for i in range(50):
    if i != first[0] and i != second[0]:
        d[i] = cnt[i]
    if d[i] == max(d):
        third[0] = i
        third[1] = max(d)

print('\n가장 많이 나온 원소 3개')
print(first[0], ':', first[1], '번')
print(second[0], ':', second[1], '번')
print(third[0], ':', third[1], '번')