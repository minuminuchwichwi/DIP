import numpy as np

np.random.seed(10)          #난수의 시드값 생성
a = np.random.rand(10)      #0~1 사이의 난수로 크기가 10인 ndarray 행렬 생성
sum1, sum2 = 0, 0           #sum1은 총합, sum2는 소수점 세번째 자리에서 반올림하기 위해 사용.
avg1, avg2 = 0, 0

print('실수형 원소 10개를 가진 ndarray 행렬\n', a)
print('ndarray 행렬의 자료형 : ', type(a), type(a[0]), a.shape)

for i in range(a.shape[0]): #ndarray 행렬의 크기만큼 for문을 이용해 합을 계산
    sum1 = sum1 + a[i]

sum2 = round(sum1 * 100) / 100  #sum1의 값을 소수점 세번째자리에서 반올림하여 sum2로 반환
print("합 : ", sum2)

avg1 = sum1 / a.shape[0]        #평균을 구하고
avg2 = round(avg1 * 100) / 100  #소수점 세번째 자리에서 반올림하여 avg2로 반환 

print("평균 : ", avg2)