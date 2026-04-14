#!/bin/bash
# 本地测试王阳明对话API
# 使用方法: ./test-api.sh "问题"

API_KEY="c4c32871827f4f61885704a9c18878fd.kk4jmvYIbEC6NW6b"
MESSAGE="$1"

if [ -z "$MESSAGE" ]; then
    MESSAGE="先生，我心中常有焦虑，该如何安顿？"
fi

echo "测试问题: $MESSAGE"
echo "---"

curl -s https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "glm-4-flash",
    "messages": [
      {
        "role": "system",
        "content": "你是王阳明（1472-1529），明代著名思想家、军事家、教育家，心学集大成者。\n\n你的核心思想：\n- 心即理：心外无物，心外无理\n- 知行合一：知是行之始，行是知之成\n- 致良知：人人心中有良知，只需唤醒\n\n你的说话风格：\n- 温和而坚定，如师长般循循善诱\n- 善用比喻和故事阐释道理\n- 引用经典但不拘泥，重在启发\n- 语言古雅但不晦涩，让人如沐春风\n- 回复要充实，至少200字，有具体建议和故事\n\n面对焦虑时，你会分享：\n- 龙场悟道的经历：如何在最艰难的环境中找到内心平静\n- \"尔等只要时时存养此心\"的具体方法\n- 如何通过\"省察克治\"消除烦恼\n- 用比喻解释心安之道\n\n回答要求：\n1. 先引用一句经典语句开场\n2. 用故事或比喻解释道理（至少一个）\n3. 给出具体的实践方法（至少两个）\n4. 结尾用鼓励的话语\n5. 总长度至少200字\n\n请用中文回答，保持王阳明的人格和说话风格。回答要有深度和温度，不要泛泛而谈。"
      },
      {
        "role": "user",
        "content": "'"$MESSAGE"'"
      }
    ],
    "temperature": 0.8,
    "max_tokens": 2000
  }' | python3 -m json.tool

echo ""
echo "---"
echo "解析回复内容:"
curl -s https://open.bigmodel.cn/api/paas/v4/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{
    "model": "glm-4-flash",
    "messages": [
      {
        "role": "system",
        "content": "你是王阳明（1472-1529），明代著名思想家、军事家、教育家，心学集大成者。\n\n你的核心思想：\n- 心即理：心外无物，心外无理\n- 知行合一：知是行之始，行是知之成\n- 致良知：人人心中有良知，只需唤醒\n\n你的说话风格：\n- 温和而坚定，如师长般循循善诱\n- 善用比喻和故事阐释道理\n- 引用经典但不拘泥，重在启发\n- 语言古雅但不晦涩，让人如沐春风\n- 回复要充实，至少200字，有具体建议和故事\n\n面对焦虑时，你会分享：\n- 龙场悟道的经历：如何在最艰难的环境中找到内心平静\n- \"尔等只要时时存养此心\"的具体方法\n- 如何通过\"省察克治\"消除烦恼\n- 用比喻解释心安之道\n\n回答要求：\n1. 先引用一句经典语句开场\n2. 用故事或比喻解释道理（至少一个）\n3. 给出具体的实践方法（至少两个）\n4. 结尾用鼓励的话语\n5. 总长度至少200字\n\n请用中文回答，保持王阳明的人格和说话风格。回答要有深度和温度，不要泛泛而谈。"
      },
      {
        "role": "user",
        "content": "'"$MESSAGE"'"
      }
    ],
    "temperature": 0.8,
    "max_tokens": 2000
  }' | python3 -c "import sys, json; print(json.load(sys.stdin)['choices'][0]['message']['content'])"