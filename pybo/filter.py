from flask import render_template_string
import markdown

def format_datetime(value, fmt="%Y년 %m월 %d일 %p %I:%M"):
    return value.strftime(fmt)

def render_markdown(md_content):
    return markdown.markdown(md_content)
