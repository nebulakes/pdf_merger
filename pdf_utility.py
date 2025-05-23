import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import os
from PyPDF2 import PdfReader, PdfWriter

class PDFUtilityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 병합 및 분할 프로그램")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 탭 컨트롤 생성
        self.tab_control = ttk.Notebook(root)
        
        # 병합 탭
        self.merge_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.merge_tab, text="PDF 병합")
        
        # 분할 탭
        self.split_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.split_tab, text="PDF 분할")
        
        self.tab_control.pack(expand=1, fill="both")
        
        # 병합 탭 초기화
        self.setup_merge_tab()
        
        # 분할 탭 초기화
        self.setup_split_tab()
        
        # 상태 표시줄
        self.status_var = tk.StringVar()
        self.status_var.set("프로그램이 준비되었습니다.")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_merge_tab(self):
        """병합 탭 UI 구성"""
        # 파일 목록 저장
        self.pdf_files = []
        
        # 메인 프레임
        main_frame = tk.Frame(self.merge_tab, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = tk.Label(main_frame, text="PDF 파일 병합 기능", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        
        # 설명
        description = "여러 PDF 파일을 하나로 병합합니다.\n파일들을 원하는 순서대로 추가한 후 '병합하기' 버튼을 클릭하세요."
        desc_label = tk.Label(main_frame, text=description, justify=tk.LEFT)
        desc_label.pack(pady=5, anchor=tk.W)
        
        # 버튼 프레임
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 파일 추가 버튼
        add_btn = tk.Button(button_frame, text="파일 추가", command=self.add_files, width=15)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # 선택 파일 제거 버튼
        remove_btn = tk.Button(button_frame, text="선택 파일 제거", command=self.remove_selected_files, width=15)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # 목록 초기화 버튼
        clear_btn = tk.Button(button_frame, text="목록 초기화", command=self.clear_files, width=15)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 파일 순서 이동 버튼
        move_frame = tk.Frame(main_frame)
        move_frame.pack(fill=tk.X, pady=5)
        
        move_up_btn = tk.Button(move_frame, text="위로 이동", command=self.move_up, width=15)
        move_up_btn.pack(side=tk.LEFT, padx=5)
        
        move_down_btn = tk.Button(move_frame, text="아래로 이동", command=self.move_down, width=15)
        move_down_btn.pack(side=tk.LEFT, padx=5)
        
        # 파일 목록 프레임
        list_frame = tk.LabelFrame(main_frame, text="병합할 PDF 파일 목록")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 스크롤바
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 파일 목록 리스트박스
        self.file_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
        # 스크롤바 연결
        self.file_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_listbox.yview)
        
        # 병합 버튼
        merge_btn = tk.Button(main_frame, text="PDF 병합하기", command=self.merge_pdfs,
                         bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"), height=2)
        merge_btn.pack(fill=tk.X, pady=10)

    def setup_split_tab(self):
        """분할 탭 UI 구성"""
        # 메인 프레임
        main_frame = tk.Frame(self.split_tab, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = tk.Label(main_frame, text="PDF 파일 분할 기능", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)
        
        # 설명 프레임
        desc_frame = tk.Frame(main_frame)
        desc_frame.pack(fill=tk.X, pady=5)
        
        description = "PDF 파일을 여러 방식으로 분할할 수 있습니다."
        desc_label = tk.Label(desc_frame, text=description, justify=tk.LEFT)
        desc_label.pack(anchor=tk.W)
        
        # 파일 선택 프레임
        file_frame = tk.LabelFrame(main_frame, text="분할할 PDF 파일 선택")
        file_frame.pack(fill=tk.X, pady=10, padx=5)
        
        # 파일 경로 표시 및 선택 버튼
        self.split_file_var = tk.StringVar()
        split_file_entry = tk.Entry(file_frame, textvariable=self.split_file_var, width=50)
        split_file_entry.pack(side=tk.LEFT, padx=5, pady=10, fill=tk.X, expand=True)
        
        select_file_btn = tk.Button(file_frame, text="파일 선택", command=self.select_split_file, width=12)
        select_file_btn.pack(side=tk.RIGHT, padx=5, pady=10)
        
        # 분할 옵션 프레임
        options_frame = tk.LabelFrame(main_frame, text="분할 옵션")
        options_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)
        
        # 분할 방식 선택 라디오 버튼 - 옵션을 2개로 줄임
        self.split_mode = tk.IntVar(value=1)
        
        option1 = tk.Radiobutton(options_frame, text="모든 페이지를 개별 PDF 파일로 분할", 
                               variable=self.split_mode, value=1)
        option1.pack(anchor=tk.W, padx=10, pady=5)
        
        option2 = tk.Radiobutton(options_frame, text="페이지 번호/범위 지정 분할", 
                               variable=self.split_mode, value=2)
        option2.pack(anchor=tk.W, padx=10, pady=5)
        
        # 통합된 페이지 번호/범위 입력 프레임
        self.pages_frame = tk.Frame(options_frame)
        self.pages_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(self.pages_frame, text="분할할 페이지 번호/범위:").pack(side=tk.LEFT)
        
        self.split_pages_var = tk.StringVar()
        self.split_pages_entry = tk.Entry(self.pages_frame, textvariable=self.split_pages_var, width=30)
        self.split_pages_entry.pack(side=tk.LEFT, padx=5)
        
        # 페이지 번호/범위 설명 레이블 
        help_label = tk.Label(options_frame, text="사용 방법: \n• 개별 페이지: 5,10,15 (5, 10, 15페이지까지가 각각 별도 파일) \n• 범위 지정: 1-5,6-10,11-15 (각 범위가 개별 파일로 분할)", 
                            justify=tk.LEFT, font=("Helvetica", 8))
        help_label.pack(anchor=tk.W, padx=20, pady=5)
        
        # 저장 옵션 프레임
        save_frame = tk.Frame(options_frame)
        save_frame.pack(fill=tk.X, padx=10, pady=15)
        
        # 저장 경로 선택
        tk.Label(save_frame, text="저장 위치:").pack(side=tk.LEFT, padx=5)
        
        self.output_dir_var = tk.StringVar()
        output_dir_entry = tk.Entry(save_frame, textvariable=self.output_dir_var, width=30)
        output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        select_dir_btn = tk.Button(save_frame, text="폴더 선택", command=self.select_output_dir, width=10)
        select_dir_btn.pack(side=tk.RIGHT, padx=5)
        
        # PDF 정보 표시 영역
        self.info_frame = tk.LabelFrame(main_frame, text="PDF 정보")
        self.info_frame.pack(fill=tk.X, pady=10, padx=5)
        
        self.pdf_info_label = tk.Label(self.info_frame, text="파일을 선택하면 정보가 표시됩니다.")
        self.pdf_info_label.pack(pady=10)
        
        # 분할 실행 버튼
        split_btn = tk.Button(main_frame, text="PDF 분할하기", command=self.split_pdf,
                         bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"), height=2)
        split_btn.pack(fill=tk.X, pady=10)

    # PDF 병합 관련 메소드
    def add_files(self):
        """파일 추가 대화상자를 열고 선택된 PDF 파일을 목록에 추가"""
        files = filedialog.askopenfilenames(
            title="병합할 PDF 파일 선택",
            filetypes=[("PDF 파일", "*.pdf"), ("모든 파일", "*.*")]
        )
        
        if files:
            for file in files:
                if file.lower().endswith('.pdf') and file not in self.pdf_files:
                    self.pdf_files.append(file)
                    self.file_listbox.insert(tk.END, os.path.basename(file))
            self.status_var.set(f"{len(files)}개 파일이 추가되었습니다.")

    def remove_selected_files(self):
        """선택된 파일을 목록에서 제거"""
        selected_indices = self.file_listbox.curselection()
        
        if not selected_indices:
            messagebox.showinfo("알림", "제거할 파일을 선택해주세요.")
            return
        
        # 역순으로 삭제 (인덱스 변화를 방지)
        for i in sorted(selected_indices, reverse=True):
            del self.pdf_files[i]
            self.file_listbox.delete(i)
        
        self.status_var.set("선택한 파일이 목록에서 제거되었습니다.")

    def clear_files(self):
        """파일 목록 전체 초기화"""
        self.file_listbox.delete(0, tk.END)
        self.pdf_files.clear()
        self.status_var.set("파일 목록이 초기화되었습니다.")

    def move_up(self):
        """선택한 항목을 위로 이동"""
        selected_indices = self.file_listbox.curselection()
        
        if not selected_indices or 0 in selected_indices:
            return
        
        for i in selected_indices:
            # 파일 목록과 리스트박스 항목을 모두 교체
            self.pdf_files[i], self.pdf_files[i-1] = self.pdf_files[i-1], self.pdf_files[i]
            file_text = self.file_listbox.get(i)
            self.file_listbox.delete(i)
            self.file_listbox.insert(i-1, file_text)
            self.file_listbox.selection_set(i-1)
        
        self.status_var.set("선택한 파일을 위로 이동했습니다.")

    def move_down(self):
        """선택한 항목을 아래로 이동"""
        selected_indices = list(self.file_listbox.curselection())
        
        if not selected_indices or self.file_listbox.size()-1 in selected_indices:
            return
        
        # 역순으로 처리 (아래에서부터)
        for i in sorted(selected_indices, reverse=True):
            # 파일 목록과 리스트박스 항목을 모두 교체
            self.pdf_files[i], self.pdf_files[i+1] = self.pdf_files[i+1], self.pdf_files[i]
            file_text = self.file_listbox.get(i)
            self.file_listbox.delete(i)
            self.file_listbox.insert(i+1, file_text)
            self.file_listbox.selection_set(i+1)
        
        self.status_var.set("선택한 파일을 아래로 이동했습니다.")

    def merge_pdfs(self):
        """선택된 PDF 파일들을 병합"""
        if not self.pdf_files:
            messagebox.showwarning("경고", "병합할 PDF 파일을 먼저 추가해주세요.")
            return
        
        # 저장할 파일 경로 선택
        output_file = filedialog.asksaveasfilename(
            title="병합된 PDF 저장",
            defaultextension=".pdf",
            filetypes=[("PDF 파일", "*.pdf"), ("모든 파일", "*.*")]
        )
        
        if not output_file:
            return
        
        try:
            # 진행 상태 창 생성
            progress_win = tk.Toplevel(self.root)
            progress_win.title("병합 진행 중...")
            progress_win.geometry("300x100")
            progress_win.resizable(False, False)
            
            # 가운데 위치
            progress_win.geometry(f"+{self.root.winfo_x() + 150}+{self.root.winfo_y() + 150}")
            
            tk.Label(progress_win, text="PDF 파일 병합 중...").pack(pady=(10, 0))
            
            progress_bar = ttk.Progressbar(progress_win, mode="indeterminate")
            progress_bar.pack(fill=tk.X, padx=20, pady=15)
            progress_bar.start()
            
            # 업데이트 강제
            self.root.update()
            
            # PDF 병합 로직
            pdf_writer = PdfWriter()
            
            # 각 PDF 파일 처리
            total_pages = 0
            for pdf_file in self.pdf_files:
                pdf_reader = PdfReader(pdf_file)
                for page_num in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                    total_pages += 1
            
            # 병합 PDF 저장
            with open(output_file, 'wb') as output:
                pdf_writer.write(output)
            
            progress_win.destroy()
            
            # 성공 메시지
            messagebox.showinfo("성공", 
                               f"PDF 파일 병합이 완료되었습니다!\n\n"
                               f"- 병합된 파일: {os.path.basename(output_file)}\n"
                               f"- 총 {len(self.pdf_files)}개 파일, {total_pages}페이지\n"
                               f"- 저장 위치: {os.path.dirname(output_file)}")
            
            self.status_var.set(f"PDF 병합 완료! 저장 위치: {output_file}")
            
        except Exception as e:
            if 'progress_win' in locals() and progress_win.winfo_exists():
                progress_win.destroy()
            
            messagebox.showerror("오류", f"PDF 병합 중 오류가 발생했습니다.\n\n{str(e)}")
            self.status_var.set("오류 발생! 병합에 실패했습니다.")

    # PDF 분할 관련 메소드
    def select_split_file(self):
        """분할할 PDF 파일 선택"""
        file_path = filedialog.askopenfilename(
            title="분할할 PDF 파일 선택",
            filetypes=[("PDF 파일", "*.pdf"), ("모든 파일", "*.*")]
        )
        
        if file_path:
            if file_path.lower().endswith('.pdf'):
                self.split_file_var.set(file_path)
                self.load_pdf_info(file_path)
            else:
                messagebox.showwarning("경고", "선택한 파일이 PDF 형식이 아닙니다.")

    def select_output_dir(self):
        """분할된 파일을 저장할 디렉토리 선택"""
        dir_path = filedialog.askdirectory(title="저장할 폴더 선택")
        
        if dir_path:
            self.output_dir_var.set(dir_path)

    def load_pdf_info(self, pdf_path):
        """PDF 파일 정보 로드 및 표시"""
        try:
            pdf_reader = PdfReader(pdf_path)
            total_pages = len(pdf_reader.pages)
            
            info_text = f"파일명: {os.path.basename(pdf_path)}\n"
            info_text += f"총 페이지 수: {total_pages}\n"
            
            # 파일 크기 정보 추가
            file_size = os.path.getsize(pdf_path)
            if file_size < 1024*1024:
                file_size_str = f"{file_size/1024:.1f} KB"
            else:
                file_size_str = f"{file_size/(1024*1024):.1f} MB"
            
            info_text += f"파일 크기: {file_size_str}"
            
            self.pdf_info_label.config(text=info_text)
            self.status_var.set("PDF 정보를 로드했습니다.")
            
        except Exception as e:
            self.pdf_info_label.config(text="파일 정보를 읽는 중 오류가 발생했습니다.")
            self.status_var.set("오류 발생! PDF 정보를 읽을 수 없습니다.")
            messagebox.showerror("오류", f"PDF 정보를 읽는 중 오류가 발생했습니다.\n\n{str(e)}")

    def split_pdf(self):
        """선택된 PDF 파일을 분할"""
        pdf_file = self.split_file_var.get()
        output_dir = self.output_dir_var.get()
        
        if not pdf_file:
            messagebox.showwarning("경고", "분할할 PDF 파일을 선택해주세요.")
            return
            
        if not output_dir:
            messagebox.showwarning("경고", "저장할 폴더를 선택해주세요.")
            return
            
        # PDF 파일 로드
        try:
            pdf_reader = PdfReader(pdf_file)
            total_pages = len(pdf_reader.pages)
            
            # 진행 상태 창 생성
            progress_win = tk.Toplevel(self.root)
            progress_win.title("분할 진행 중...")
            progress_win.geometry("300x100")
            progress_win.resizable(False, False)
            
            # 가운데 위치
            progress_win.geometry(f"+{self.root.winfo_x() + 150}+{self.root.winfo_y() + 150}")
            
            status_label = tk.Label(progress_win, text="PDF 파일 분할 중...")
            status_label.pack(pady=(10, 0))
            
            progress_bar = ttk.Progressbar(progress_win, mode="determinate", maximum=100)
            progress_bar.pack(fill=tk.X, padx=20, pady=15)
            
            # 업데이트 강제
            self.root.update()
            
            # 분할 모드에 따른 처리
            split_mode = self.split_mode.get()
            base_filename = os.path.splitext(os.path.basename(pdf_file))[0]
            saved_files = []
            
            # 모든 페이지를 개별 파일로 분할
            if split_mode == 1:
                for page_num in range(total_pages):
                    progress_value = (page_num + 1) / total_pages * 100
                    progress_bar["value"] = progress_value
                    status_label.config(text=f"페이지 {page_num+1}/{total_pages} 처리 중...")
                    progress_win.update()
                    
                    pdf_writer = PdfWriter()
                    pdf_writer.add_page(pdf_reader.pages[page_num])
                    
                    output_path = os.path.join(output_dir, f"{base_filename}_page{page_num+1}.pdf")
                    with open(output_path, "wb") as output_file:
                        pdf_writer.write(output_file)
                    
                    saved_files.append(output_path)
                
                message = f"총 {total_pages}개의 페이지가 개별 파일로 분할되었습니다."
                
            # 페이지 번호/범위 지정 분할 - 통합 모드
            elif split_mode == 2:
                split_input = self.split_pages_var.get().strip()
                
                if not split_input:
                    progress_win.destroy()
                    messagebox.showwarning("경고", "분할할 페이지 번호나 범위를 입력해주세요.")
                    return
                
                try:
                    # 범위 형식인지 확인 (1-5와 같은 형식이 있는지)
                    is_range_format = "-" in split_input
                    
                    # 범위 형식인 경우 (1-5,6-10 등)
                    if is_range_format:
                        page_ranges = []
                        for range_str in split_input.split(","):
                            if "-" in range_str:
                                start, end = map(int, range_str.split("-"))
                                if start <= 0 or end > total_pages or start > end:
                                    raise ValueError(f"유효하지 않은 범위: {range_str}")
                                # 시작 페이지부터 끝 페이지까지 포함 (0-based -> 1-based 조정)
                                page_ranges.append((start-1, end))
                            else:
                                page = int(range_str.strip())
                                if page <= 0 or page > total_pages:
                                    raise ValueError(f"유효하지 않은 페이지 번호: {page}")
                                page_ranges.append((page-1, page))  # 단일 페이지
                        
                        for i, (start_page, end_page) in enumerate(page_ranges):
                            # 진행 상태 표시
                            progress_value = (i + 1) / len(page_ranges) * 100
                            progress_bar["value"] = progress_value
                            status_label.config(text=f"범위 {i+1}/{len(page_ranges)} 처리 중...")
                            progress_win.update()
                            
                            pdf_writer = PdfWriter()
                            
                            # 페이지 추가 - 끝 페이지까지 포함
                            for page_num in range(start_page, end_page):
                                pdf_writer.add_page(pdf_reader.pages[page_num])
                            
                            # 마지막 페이지도 추가 (end_page는 인덱스이므로 포함)
                            pdf_writer.add_page(pdf_reader.pages[end_page-1])
                            
                            output_path = os.path.join(output_dir, f"{base_filename}_range{i+1}.pdf")
                            with open(output_path, "wb") as output_file:
                                pdf_writer.write(output_file)
                            
                            saved_files.append(output_path)
                        
                        message = f"{len(page_ranges)}개의 페이지 범위로 분할되었습니다."
                    
                    # 개별 페이지 번호 형식인 경우 (1,5,10 등)
                    else:
                        # 페이지 번호 파싱 (문자열 -> 정수 리스트)
                        split_pages = [int(p.strip()) for p in split_input.split(",") if p.strip()]
                        # 중복 제거 및 정렬
                        split_pages = sorted(list(set(split_pages)))
                        
                        # 범위 유효성 검사
                        if any(p <= 0 or p > total_pages for p in split_pages):
                            progress_win.destroy()
                            messagebox.showwarning("경고", f"유효하지 않은 페이지 번호가 있습니다. 페이지 번호는 1 ~ {total_pages} 사이여야 합니다.")
                            return
                        
                        # 지정한 페이지를 포함하여 앞부분이 한 파일이 되도록 수정
                        # 1페이지부터 첫 번째 지정 페이지까지
                        start_page = 0  # 0-based 인덱스
                        
                        for i, end_page in enumerate(split_pages):
                            # 진행 상태 표시
                            progress_value = (i + 1) / len(split_pages) * 100
                            progress_bar["value"] = progress_value
                            status_label.config(text=f"파트 {i+1}/{len(split_pages)} 처리 중...")
                            progress_win.update()
                            
                            pdf_writer = PdfWriter()
                            
                            # 지정한 페이지까지 포함하여 추가 (end_page는 1-based, 변환 필요)
                            for page_num in range(start_page, end_page):
                                pdf_writer.add_page(pdf_reader.pages[page_num])
                            
                            output_path = os.path.join(output_dir, f"{base_filename}_part{i+1}.pdf")
                            with open(output_path, "wb") as output_file:
                                pdf_writer.write(output_file)
                            
                            saved_files.append(output_path)
                            
                            # 다음 시작 페이지 설정 (현재 end_page 이후부터)
                            start_page = end_page
                        
                        # 마지막 부분 파일 (마지막 지정 페이지부터 문서 끝까지)
                        if start_page < total_pages:
                            progress_bar["value"] = 100
                            status_label.config(text=f"마지막 파트 처리 중...")
                            progress_win.update()
                            
                            pdf_writer = PdfWriter()
                            
                            for page_num in range(start_page, total_pages):
                                pdf_writer.add_page(pdf_reader.pages[page_num])
                            
                            output_path = os.path.join(output_dir, f"{base_filename}_part{len(split_pages)+1}.pdf")
                            with open(output_path, "wb") as output_file:
                                pdf_writer.write(output_file)
                            
                            saved_files.append(output_path)
                        
                        message = f"PDF가 {len(saved_files)}개의 파일로 분할되었습니다."
                    
                except ValueError as e:
                    progress_win.destroy()
                    messagebox.showerror("오류", f"페이지 번호/범위 형식이 올바르지 않습니다: {str(e)}\n'5,10,15' 또는 '1-5,6-10' 형식으로 입력해주세요.")
                    return
            
            progress_win.destroy()
            
            # 성공 메시지
            messagebox.showinfo("성공", 
                              f"PDF 파일 분할이 완료되었습니다!\n\n"
                              f"- {message}\n"
                              f"- 저장 위치: {output_dir}")
            
            self.status_var.set(f"PDF 분할 완료! {len(saved_files)}개 파일이 생성되었습니다.")
            
        except Exception as e:
            if 'progress_win' in locals() and progress_win.winfo_exists():
                progress_win.destroy()
            
            messagebox.showerror("오류", f"PDF 분할 중 오류가 발생했습니다.\n\n{str(e)}")
            self.status_var.set("오류 발생! 분할에 실패했습니다.")

# 메인 애플리케이션 실행
if __name__ == "__main__":
    try:
        # PyPDF2 라이브러리 확인
        import PyPDF2
    except ImportError:
        print("PyPDF2 라이브러리가 설치되지 않았습니다.")
        print("다음 명령어로 설치해주세요: pip install PyPDF2")
        exit(1)
        
    root = tk.Tk()
    app = PDFUtilityApp(root)
    root.mainloop()
