# -*- coding: utf-8 -*-
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
import pandas as pd

from config.settings import PDF_DIR, LOGO_PATH


class PDFReportBuilder:
    def __init__(self):
        self.today = datetime.now().strftime("%Y-%m-%d")
        self.output_path = f"{PDF_DIR}/AI_Weekly_Report_{self.today}.pdf"
        self.data_path = "../data/daily_ai_news.csv"
        self.logo_path = LOGO_PATH
        self.styles = getSampleStyleSheet()

    def load_data(self):
        """加载本周数据"""
        end_date = datetime.now()
        start_date = end_date - pd.Timedelta(days=7)
        df = pd.read_csv(self.data_path)
        df['date'] = pd.to_datetime(df['date'])
        return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    def create_header(self):
        """创建页眉"""
        elements = []
        if os.path.exists(self.logo_path):
            logo = Image(self.logo_path, width=2*inch, height=0.5*inch)
            elements.append(logo)
        header = Paragraph(f"AI Weekly Report - {self.today}", self.styles['Heading1'])
        elements.extend([header, Spacer(1, 12)])
        return elements

    def build_content(self, data):
        """构建内容"""
        elements = self.create_header()
        for _, row in data.iterrows():
            title = Paragraph(row['title'], self.styles['Heading2'])
            content = Paragraph(row['content'], self.styles['BodyText'])
            link = Paragraph(f"<link href='{row['link']}'>Read More...</link>", self.styles['Italic'])
            elements.extend([title, content, link, Spacer(1, 12)])
        return elements

    def generate_pdf(self):
        """生成PDF报告"""
        data = self.load_data()
        elements = self.build_content(data)

        doc = SimpleDocTemplate(self.output_path, pagesize=letter)
        doc.build(elements)


if __name__ == "__main__":
    builder = PDFReportBuilder()
    builder.generate_pdf()
