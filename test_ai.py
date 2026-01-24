import requests
import json

def test_ernie_api():
    url = "https://aistudio.baidu.com/llm/lmapi/v3/chat/completions"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 831a87555da15eb5702d7fea6ab9555b82b20b24'
    }
    
    payload = {
        "model": "ernie-x1.1-preview",
        "messages": [
            {
                "role": "user",
                "content": "你好，请回复“API连接成功”"
            }
        ],
        "stream": False
    }

    try:
        print(f"Testing connection to: {url}")
        print("Waiting for response...")
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Response Body:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print("\n✅ 测试通过！API Key有效，网络畅通。")
        else:
            print(f"❌ 请求失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 发生异常: {str(e)}")

if __name__ == "__main__":
    test_ernie_api()
