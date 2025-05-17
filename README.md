# PDF 병합 프로그램

여러 PDF 파일을 손쉽게 하나로 병합할 수 있는 그래픽 인터페이스(GUI) 프로그램입니다.

## 주요 기능

- 여러 PDF 파일 선택 및 추가
- 파일 순서 변경 (위로/아래로 이동)
- 선택한 파일 제거 및 목록 초기화
- 모든 PDF 파일을 순서대로 하나의 PDF로 병합
- 진행 상황 표시 및 결과 요약 정보 제공

## 설치 및 실행 방법

### 방법 1: 실행 파일(.exe) 다운로드 (가장 쉬운 방법)

- GitHub 리포지토리의 [릴리스 페이지](https://github.com/nebulakes/pdf-merger/releases)에서 `PDFMerger.exe` 파일을 다운로드하세요.
- 다운로드한 파일을 더블클릭하면 즉시 프로그램이 실행됩니다.
- **참고**: `.\dist\PDFMerger.exe` 파일만 다운로드하여 사용하셔도 됩니다. Python이나 다른 라이브러리를 설치할 필요가 없습니다.

### 방법 2: 소스 코드로 실행하기

1. Python 3.x 설치
2. 필요한 라이브러리 설치:
   ```
   pip install PyPDF2
   ```
3. 프로그램 실행:
   ```
   python pdf_merger_gui.py
   ```

## 사용 방법

1. **파일 추가**: "파일 추가" 버튼을 클릭하여 병합할 PDF 파일들을 선택합니다.
2. **순서 변경**: 파일 목록에서 항목을 선택하고 "위로 이동"/"아래로 이동" 버튼으로 순서를 조정합니다.
3. **파일 제거**: "선택 파일 제거" 버튼으로 특정 파일을 제거하거나 "목록 초기화"로 전체 목록을 비웁니다.
4. **PDF 병합**: "PDF 병합하기" 버튼을 클릭하여 병합 과정을 시작합니다.
5. **저장 위치 선택**: 병합된 PDF 파일을 저장할 위치와 이름을 지정합니다.

## 사용된 라이브러리

이 프로그램은 다음 라이브러리에 의존합니다:
- [Python](https://www.python.org/) (PSF 라이선스)
- [PyPDF2](https://pypi.org/project/PyPDF2/) (BSD 라이선스)
- Tkinter (Python 내장 라이브러리)

## 법적 고지

- PDF(Portable Document Format)는 Adobe Inc.의 등록 상표입니다.
- 이 프로그램은 Adobe Inc.와 관련이 없으며, 독립적으로 개발되었습니다.

## 시스템 요구사항

- Windows 7/8/10/11 (실행 파일 사용 시)
- 또는 Python 3.6 이상 및 PyPDF2 라이브러리가 설치된 환경

## 라이선스

이 프로젝트는 MIT 라이선스 하에 공개되어 있습니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 기여 방법

1. 이 저장소를 포크합니다.
2. 새 기능 브랜치를 만듭니다 (`git checkout -b feature/amazing-feature`)
3. 변경 사항을 커밋합니다 (`git commit -m '새로운 기능 추가'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다.