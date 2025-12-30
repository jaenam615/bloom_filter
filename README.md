# Bloom Filter (블룸 필터)

파이썬으로 구현한 블룸 필터 (Bloom Filter implementation in Python)

## 개요 (Overview)

블룸 필터는 원소가 집합에 속하는지를 검사하는데 사용되는 확률적 자료구조입니다. 공간 효율적이며, 거짓 양성(false positive)은 발생할 수 있지만 거짓 음성(false negative)은 발생하지 않습니다.

A Bloom filter is a space-efficient probabilistic data structure used to test whether an element is a member of a set. It is highly space-efficient but may yield false positives (though never false negatives).

## 주요 특징 (Features)

- ✅ 공간 효율적인 멤버십 테스트 (Space-efficient membership testing)
- ✅ 거짓 음성 없음 (No false negatives)
- ✅ 설정 가능한 거짓 양성률 (Configurable false positive rate)
- ✅ 다양한 데이터 타입 지원 (Support for various data types)
- ✅ 통계 정보 제공 (Statistics and metrics)
- ✅ 간단한 API (Simple and intuitive API)

## 설치 (Installation)

이 저장소를 클론하세요 (Clone this repository):

```bash
git clone https://github.com/jaenam615/bloom_filter.git
cd bloom_filter
```

## 사용법 (Usage)

### 기본 사용 (Basic Usage)

```python
from bloom_filter import BloomFilter

# 블룸 필터 생성 (Create a Bloom filter)
# 예상 원소 수: 1000개, 거짓 양성률: 1%
bf = BloomFilter(expected_elements=1000, false_positive_rate=0.01)

# 원소 추가 (Add elements)
bf.add("apple")
bf.add("banana")
bf.add("cherry")

# 멤버십 체크 (Check membership)
print(bf.contains("apple"))   # True
print(bf.contains("orange"))  # False

# 'in' 연산자 사용 (Using 'in' operator)
print("banana" in bf)  # True
print("grape" in bf)   # False
```

### 통계 정보 (Statistics)

```python
# 필터 통계 확인 (Get filter statistics)
stats = bf.get_stats()
print(f"Size: {stats['size']} bits")
print(f"Hash functions: {stats['hash_count']}")
print(f"Elements added: {stats['element_count']}")
print(f"Load factor: {stats['load_factor']:.2%}")
print(f"Estimated FPR: {stats['estimated_false_positive_rate']:.2%}")
```

### 실용적인 예제 (Practical Example)

```python
# 사용자명 중복 체크 시스템 (Username availability checker)
user_filter = BloomFilter(expected_elements=100000, false_positive_rate=0.001)

# 기존 사용자 등록 (Register existing users)
existing_users = ["alice", "bob", "charlie"]
for user in existing_users:
    user_filter.add(user)

# 신규 사용자명 체크 (Check new username)
new_username = "david"
if new_username in user_filter:
    print("이름이 사용 중일 수 있음 - DB 확인 필요")
    print("Username might be taken - check database")
else:
    print("확실히 사용 가능!")
    print("Definitely available!")
```

## 예제 실행 (Running Examples)

더 많은 예제를 보려면 example.py를 실행하세요 (Run example.py to see more examples):

```bash
python3 example.py
```

## 테스트 실행 (Running Tests)

단위 테스트를 실행하려면 (Run unit tests):

```bash
python3 -m unittest test_bloom_filter.py -v
```

## 작동 원리 (How It Works)

블룸 필터는 비트 배열과 여러 해시 함수를 사용합니다:

1. **추가 (Add)**: 원소를 k개의 해시 함수로 해싱하여 k개의 비트를 1로 설정
2. **검사 (Check)**: 원소의 모든 해시 위치가 1인지 확인
   - 모두 1이면: 아마도 존재 (false positive 가능)
   - 하나라도 0이면: 확실히 존재하지 않음

A Bloom filter uses a bit array and multiple hash functions:

1. **Add**: Hash element with k hash functions and set k bits to 1
2. **Check**: Verify if all hash positions are 1
   - All 1s: Probably exists (may be false positive)
   - Any 0: Definitely does not exist

## 시간 복잡도 (Time Complexity)

- 추가 (Add): O(k) - k는 해시 함수 개수
- 검사 (Contains): O(k)
- 공간 (Space): O(m) - m은 비트 배열 크기

## 매개변수 선택 (Parameter Selection)

이 구현은 최적의 매개변수를 자동으로 계산합니다:

- **비트 배열 크기**: m = -(n × ln(p)) / (ln(2)²)
- **해시 함수 개수**: k = (m / n) × ln(2)

Where:
- n = 예상 원소 수 (expected elements)
- p = 목표 거짓 양성률 (target false positive rate)
- m = 비트 배열 크기 (bit array size)
- k = 해시 함수 개수 (number of hash functions)

## API 문서 (API Documentation)

### BloomFilter 클래스 (Class)

#### `__init__(expected_elements, false_positive_rate)`

블룸 필터를 생성합니다 (Create a Bloom filter).

- `expected_elements` (int): 예상 원소 수 (default: 1000)
- `false_positive_rate` (float): 목표 거짓 양성률 (default: 0.01)

#### `add(item)`

원소를 필터에 추가합니다 (Add an item to the filter).

#### `contains(item)`

원소가 필터에 있는지 확인합니다 (Check if item might be in the filter).

Returns: True if item might be in set, False if definitely not in set

#### `get_stats()`

필터 통계를 반환합니다 (Return filter statistics).

Returns: Dictionary with size, hash_count, element_count, bits_set, load_factor, estimated_false_positive_rate

#### `clear()`

필터를 초기화합니다 (Clear all elements from the filter).

## 제약사항 (Limitations)

- ❌ 원소 삭제 불가능 (Cannot remove elements)
- ❌ 거짓 양성 발생 가능 (May produce false positives)
- ❌ 정확한 원소 개수 추적 불가 (Cannot track exact element count with duplicates)

## 활용 사례 (Use Cases)

- 🔍 중복 URL 체크 (웹 크롤러)
- 👤 사용자명 중복 검사
- 📧 스팸 필터링
- 💾 캐시 최적화
- 🔐 악성 URL 차단
- 📊 빅데이터 멤버십 테스트

## 라이선스 (License)

MIT License

## 기여 (Contributing)

기여를 환영합니다! Pull request를 보내주세요.

Contributions are welcome! Please feel free to submit a Pull Request.
