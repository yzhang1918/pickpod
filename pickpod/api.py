# !/usr/bin/env python3.8
# -*- coding: utf-8 -*-

import re

import requests

from pickpod.doc import SummaryDocument, ViewDocument


PROMPT_KEYWORDS_ZH = "Human:你的任务是对下面的文本提取不超过10个关键词，每个关键词都应简明扼要，不能重复，且必须用中文输出，文本如下：\"{}\"\n\nAssistant:"
PROMPT_KEYWORDS_EN = "Human:Your task is to extract no more than 10 keywords from the received text. Each keyword should be concise and non-repetitive. The text is as follows: \"{}\"\n\nAssistant:"
PROMPT_SUMMARY_ZH = "Human:从视频文本中创建不超过30个关键时刻，包括时间，您的答案应简明，并以00:00:00开头，你的回答必须翻译成简体中文。\n\nAssistant:好的，我已经清楚规则了，我会用简体中文根据我所接收到的文本创建包括时间的关键时刻。\n\nHuman:文本：\"大家好,这里是阶梯计划第五期，我们做阶梯计划这个平台主要是希望针对加密生态的关键问题进行真诚的讨论与深入的分析。介绍一下，我是Frank Lee，DeFi和智能合约安全从业者。\"\n\nAssistant:00:00:00 - 介绍节目\n\nHuman:文本:\"{}\"\n\nAssistant:"
PROMPT_SUMMARY_EN = "Human:Create no more than 30 key moments from the video text, including the time, your answer should be concise and start with 00:00:00, your answer must be translated into English.\n\nAssistant:Sure, I konw the rule. I'll create key moments from the recived text including the time in English.\n\nHuman:TEXT: \"Hello everyone, this is phase 5 of the Ladder Project. We created the Ladder Project as a platform for sincere discussion and in-depth analysis of key issues in the crypto ecosystem. By the way, I'm Frank Lee, a DeFi and smart contract security practitioner.\"\n\nAssistant:00:00:00 - Introducing the Program\n\nHuman:TEXT: \"{}\"\n\nAssistant:"
PROMPT_VIEWS_ZH = "Human:用中文回答文中有哪些反常识或者有尖锐态度的新观点？请输出7~8个，并说明和常识不一致的具体原因。\n\nAssistant:好的，我明白要求和输出的格式了，请给我具体的文字。\n\nHuman:文本：\"{}\"\n\nAssistant:"
PROMPT_VIEWS_EN = "Human:What unconventional or sharp attitudes are there in the following transcript? List the five most important ones and explain why they contradict the consensus. The language you respond in must be consistent with the language of the transcript. The text is as follows: \"{}\"\n\nAssistant:"


def t2s(t: str = "") -> int:
    h, m, s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


class ClaudeClient(object):

    def __init__(self, key_claude: str = ""):
        self.url = "https://api.anthropic.com/v1/complete"
        self.header = {
            "accept": "application/json",
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
            "x-api-key": key_claude
        }
        self.body = {"model": "claude-2", "max_tokens_to_sample": 10000}

    def get_keywords_zh(self, doc: str = ""):
        self.body["prompt"] = PROMPT_KEYWORDS_ZH.format(doc)
        claude_response = requests.request("POST", url=self.url, headers=self.header, json=self.body)
        claude_keywords = claude_response.json().get("completion", "")
        print(claude_keywords)
        return [
            re.sub("^\d*\.\s|^\d*\.|^-\s|^-|^\s*|\s$", "", x)
            for x in claude_keywords.split("\n\n")[1].split("\n")
        ]

    def get_keywords_en(self, doc: str = ""):
        self.body["prompt"] = PROMPT_KEYWORDS_EN.format(doc)
        claude_response = requests.request("POST", url=self.url, headers=self.header, json=self.body)
        claude_keywords = claude_response.json().get("completion", "")
        print(claude_keywords)
        return [
            re.sub("^\d*\.\s|^\d*\.|^-\s|^-|^\s*|\s$", "", x)
            for x in claude_keywords.split("\n\n")[1].split("\n")
        ]

    def get_summary_zh(self, doc: str = ""):
        self.body["prompt"] = PROMPT_SUMMARY_ZH.format(doc)
        claude_response = requests.request("POST", url=self.url, headers=self.header, json=self.body)
        claude_summary = claude_response.json().get("completion", "")
        print(claude_summary)
        return [
            SummaryDocument(t2s(re.match("^\s*\d\d:\d\d:\d\d", x).group()), re.sub("^\s*\d\d:\d\d:\d\d\s*-\s*", "", x))
            for x in claude_summary.split("\n\n")
            if re.match("^\s*\d\d:\d\d:\d\d", x)
        ]

    def get_summary_en(self, doc: str = ""):
        self.body["prompt"] = PROMPT_SUMMARY_EN.format(doc)
        claude_response = requests.request("POST", url=self.url, headers=self.header, json=self.body)
        claude_summary = claude_response.json().get("completion", "")
        print(claude_summary)
        return [
            SummaryDocument(t2s(re.match("^\s*\d\d:\d\d:\d\d", x).group()), re.sub("^\s*\d\d:\d\d:\d\d\s*-\s*", "", x))
            for x in claude_summary.split("\n\n")
            if re.match("^\s*\d\d:\d\d:\d\d", x)
        ]

    def get_views_zh(self, doc: str = ""):
        self.body["prompt"] = PROMPT_VIEWS_ZH.format(doc)
        claude_response = requests.request("POST", url=self.url, headers=self.header, json=self.body)
        claude_views = claude_response.json().get("completion", "")
        print(claude_views)
        return [
            ViewDocument(re.sub("^\d*\.\s|^\d*\.|^-\s|^-|^\s*|\s$", "", x))
            for x in claude_views.split("\n")
            if x
        ]

    def get_views_en(self, doc: str = ""):
        self.body["prompt"] = PROMPT_VIEWS_EN.format(doc)
        claude_response = requests.request("POST", url=self.url, headers=self.header, json=self.body)
        claude_views = claude_response.json().get("completion", "")
        print(claude_views)
        return [
            ViewDocument(re.sub("^\d*\.\s|^\d*\.|^-\s|^-|^\s*|\s$", "", x))
            for x in claude_views.split("\n")
            if x
        ]
