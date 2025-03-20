import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 한글 폰트를 설정 (나눔고딕 사용)
plt.rcParams['font.family'] = 'NanumGothic'

# 다이어그램 설정
fig, ax = plt.subplots(figsize=(10, 8))

# 중앙 LLM 박스
ax.text(0.5, 0.5, "LLM (대규모 언어 모델)", ha='center', va='center', fontsize=14, bbox=dict(facecolor='lightgray', boxstyle='round,pad=0.5'))

# 복잡성 요소 (상단, 좌, 우, 하단)
elements = [
    ("프롬프트 설계 및 최적화", 0.5, 0.8),
    ("상태 기억 불가 (기록 저장 필요)", 0.9, 0.5),
    ("다양한 모델 선택\n(시나리오별)", 0.5, 0.2),
    ("응답 조정 및 후처리", 0.1, 0.5)
]

# 개발자가 해결해야 할 작업 요소
tasks = [
    ("데이터베이스 통합\n(대화 기록 저장)", 0.7, 0.7),
    ("프롬프트 템플릿 관리", 0.3, 0.7),
]

# 복잡성 요소 추가
for text, x, y in elements:
    ax.text(x, y, text, ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightblue', boxstyle='round,pad=0.3'))

# 개발자 작업 요소 추가
for text, x, y in tasks:
    ax.text(x, y, text, ha='center', va='center', fontsize=12, bbox=dict(facecolor='lightgreen', boxstyle='round,pad=0.3'))

# 화살표 추가 (복잡성 요소 -> LLM)
arrows = [
    (0.5, 0.75, 0.5, 0.55),
    (0.75, 0.5, 0.65, 0.5),
    (0.5, 0.25, 0.5, 0.45),
    (0.2, 0.5, 0.35, 0.5),
    (0.6, 0.6, 0.55, 0.55),
    (0.35, 0.6, 0.45, 0.55)
]

for x_start, y_start, x_end, y_end in arrows:
    ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                arrowprops=dict(facecolor='black', shrink=0.05, width=2))

# 레이아웃 조정
plt.axis('off')  # 축 제거
plt.title("LLM 활용의 복잡성 및 문제점", fontsize=16, pad=20)

plt.show()