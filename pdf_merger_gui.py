import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from PyPDF2 import PdfReader, PdfWriter

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF 병합 프로그램")
        self.root.geometry("600x450")
        self.root.resizable(True, True)
        
        # 파일 목록 저장
        self.pdf_files = []
        
        # 메인 프레임
        main_frame = tk.Frame(root, padx=10, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = tk.Label(main_frame, text="PDF 파일 병합 프로그램", font=("Helvetica", 16, "bold"))
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
        
        # 상태 표시줄
        self.status_var = tk.StringVar()
        self.status_var.set("프로그램이 준비되었습니다.")
        status_bar = tk.Label(root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

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
    app = PDFMergerApp(root)
    root.mainloop()
